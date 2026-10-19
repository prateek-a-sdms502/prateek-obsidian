"""Three-way parity: Python engine vs Excel (recalculated) vs JavaScript.

  python parity.py                 # reference scenarios, all three targets
  python parity.py --xlsx FILE     # also compare every Matrix row of a recalculated full workbook

Excel values come from a LibreOffice recalc (xlsx skill's recalc.py) when soffice
is installed, otherwise from the `formulas` package.
"""
import argparse
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from openpyxl import load_workbook

from build_xlsx import Builder
from engine import LLM_ORDER, OCR_ORDER, run_llm, run_ocr
from inputs import ROW_KEYS, Data

HERE = Path(__file__).parent
RECALC = Path("/home/stark/.claude/skills/synced/6742b748-c592-40d7-a7ad-a40971b83c00_f4a7c2c4-918e-4781-9bce-debf2b7c7a47/xlsx/scripts/recalc.py")
RTOL = 1e-9


def close(a, b):
    if a is None or b is None:
        return False
    a, b = float(a), float(b)
    return math.isclose(a, b, rel_tol=RTOL, abs_tol=1e-9)


def matrix_values(wb):
    ws = wb["Matrix"]
    hdr = [c.value for c in ws[2]]
    for row in ws.iter_rows(min_row=4, values_only=True):
        if row[0] is None:
            continue
        yield dict(zip(hdr, row))


def recalc(path):
    """Return (rows of the Matrix sheet as dicts, engine name)."""
    lo = shutil.which("soffice") or shutil.which("libreoffice")
    if lo:
        # snap LibreOffice can only see non-hidden paths under $HOME, so convert inside cost_model/out/
        work = HERE / "out" / "lo_parity"
        work.mkdir(parents=True, exist_ok=True)
        src = work / "in.xlsx"
        shutil.copy(path, src)
        subprocess.run([lo, "--headless", "--calc", "--convert-to", "xlsx", "--outdir", str(work / "done"), str(src)],
                       capture_output=True, text=True, timeout=1800)
        res = work / "done" / "in.xlsx"
        if not res.exists():
            raise SystemExit("LibreOffice did not produce a recalculated file")
        return list(matrix_values(load_workbook(res, data_only=True))), "LibreOffice"
    import re
    import formulas
    from openpyxl.utils import column_index_from_string
    sol = formulas.ExcelModel().loads(str(path)).finish().calculate()
    vals = {}
    for k, v in sol.items():
        m = re.match(r"'\[[^\]]+\]([^']+)'!([A-Z]+)(\d+)$", k)
        if m and m.group(1).upper() == "MATRIX":
            vals[(int(m.group(3)), column_index_from_string(m.group(2)))] = v.value[0][0] if hasattr(v, "value") else v
    ws = load_workbook(path)["Matrix"]
    hdr = [c.value for c in ws[2]]
    rows = []
    for r in range(4, ws.max_row + 1):
        if ws.cell(row=r, column=1).value is None:
            continue
        row = {}
        for ci, h in enumerate(hdr, 1):
            cell = ws.cell(row=r, column=ci).value
            row[h] = vals.get((r, ci), cell) if isinstance(cell, str) and cell.startswith("=") else cell
        rows.append(row)
    return rows, "formulas"


def check_excel(path, data, lv_for):
    xrows, how = recalc(path)
    bad, n = [], 0
    for xrow in xrows:
        keys = {k: xrow[k] for k in ROW_KEYS}
        v = run_llm(data.llm_row(**keys, **lv_for(keys)))
        n += 1
        for f in LLM_ORDER:
            if not close(v[f.name], xrow.get(f.name)):
                bad.append((keys, f.name, v[f.name], xrow.get(f.name)))
    return how, n, bad


def check_js(data, cases):
    subprocess.run([sys.executable, str(HERE / "build_js.py")], check=True, capture_output=True)
    script = f"""
global.window = {{}};
require({json.dumps(str(HERE / 'out' / 'model.js'))});
const M = window.CostModel, cases = {json.dumps(cases)};
const out = cases.map(c => c.kind === 'llm' ? M.llm(M.llmRow(c.keys, c.levers)) : M.ocr(M.ocrRow(c.keys, c.levers)));
console.log(JSON.stringify(out));
"""
    res = subprocess.run(["node", "-e", script], capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx")
    a = ap.parse_args()
    data = Data()
    ref = data.scen["reference"]
    base_lv = {"uptime": "24x7", "itc": 1, "spare": 0, "years": 3}
    ok = True

    # 1) JS vs Python on reference scenarios (each with its own levers) + every OCR row
    cases = []
    for sid, s in ref.items():
        cases.append({"kind": "llm", "id": sid, "keys": {k: s[k] for k in ROW_KEYS},
                      "levers": {k: s[k] for k in ("uptime", "itc", "spare", "years")}})
    for k in data.ocr_grid():
        cases.append({"kind": "ocr", "id": "ocr:" + "/".join(map(str, k.values())), "keys": k, "levers": base_lv})
    js = check_js(data, cases)
    nbad = 0
    for c, jv in zip(cases, js):
        if c["kind"] == "llm":
            pv, order = run_llm(data.llm_row(**c["keys"], **c["levers"])), LLM_ORDER
        else:
            pv, order = run_ocr(data.ocr_row(**c["keys"], **c["levers"])), OCR_ORDER
        for f in order:
            if not close(pv[f.name], jv.get(f.name)):
                nbad += 1
                if nbad <= 20:
                    print(f"JS MISMATCH {c['id']} {f.name}: py={pv[f.name]} js={jv.get(f.name)}")
    print(f"JS vs Python: {len(cases)} cases, {nbad} mismatches")
    ok &= nbad == 0

    # 2) Excel vs Python on a reference-rows workbook (levers fixed at base in the workbook)
    tmp = Path(tempfile.mkdtemp()) / "parity.xlsx"
    Builder(data, "reference").build(tmp)
    how, n, bad = check_excel(tmp, data, lambda keys: base_lv)
    for b in bad[:20]:
        print("XL MISMATCH", *b)
    print(f"Excel ({how}) vs Python: {n} rows x {len(LLM_ORDER)} formulas, {len(bad)} mismatches")
    ok &= not bad

    # 3) optional: full workbook
    if a.xlsx:
        how, n, bad = check_excel(Path(a.xlsx), data, lambda keys: base_lv)
        for b in bad[:20]:
            print("FULL XL MISMATCH", *b)
        print(f"Full workbook ({how}): {n} rows, {len(bad)} mismatches")
        ok &= not bad
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
