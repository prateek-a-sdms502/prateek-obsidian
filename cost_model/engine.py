"""Run the cost model over the scenario grid.

  python engine.py                 # full grid -> out/llm_grid.csv, out/ocr_grid.csv
  python engine.py --scenario ID   # print one reference scenario from scenarios.yaml
"""
import argparse
import csv
import itertools
import json
from pathlib import Path

from dsl import compile_py
from formulas import INPUTS, LLM, OCR, OCR_INPUTS
from inputs import ROW_KEYS, Data

OUT = Path(__file__).parent / "out"

_llm_eval, LLM_ORDER = compile_py(LLM, set(INPUTS))
_ocr_eval, OCR_ORDER = compile_py(OCR, set(INPUTS) | set(OCR_INPUTS))


def run_llm(row):
    return _llm_eval(dict(row))


def run_ocr(row):
    return _ocr_eval(dict(row))


def lever_grid(data):
    lv = data.scen["levers"]
    for uptime, itc, spare, years in itertools.product(lv["uptime"], lv["itc"], lv["spare"], lv["years"]):
        yield {"uptime": uptime, "itc": itc, "spare": spare, "years": years}


def full_grid(data):
    llm_cols = list(ROW_KEYS) + ["uptime", "itc", "spare", "years"] + [f.name for f in LLM_ORDER]
    llm_rows = []
    for keys in data.llm_grid():
        for lv in lever_grid(data):
            v = run_llm(data.llm_row(**keys, **lv))
            llm_rows.append({**keys, **lv, **{c: v[c] for c in llm_cols if c in v}})
    ocr_cols = ["gpu", "precision", "tier", "uptime", "itc", "spare", "years"] + [f.name for f in OCR_ORDER]
    ocr_rows = []
    for keys in data.ocr_grid():
        for lv in lever_grid(data):
            v = run_ocr(data.ocr_row(**keys, **lv))
            ocr_rows.append({**keys, **lv, **{c: v[c] for c in ocr_cols if c in v}})
    return llm_cols, llm_rows, ocr_cols, ocr_rows


def reference(data, sid):
    s = data.scen["reference"][sid]
    keys = {k: s[k] for k in ROW_KEYS}
    lv = {k: s[k] for k in ("uptime", "itc", "spare", "years")}
    return run_llm(data.llm_row(**keys, **lv))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario")
    a = ap.parse_args()
    data = Data()
    if a.scenario:
        v = reference(data, a.scenario)
        print(json.dumps({f.name: v[f.name] for f in LLM_ORDER}, indent=1))
        return
    OUT.mkdir(exist_ok=True)
    llm_cols, llm_rows, ocr_cols, ocr_rows = full_grid(data)
    for name, cols, rows in (("llm_grid.csv", llm_cols, llm_rows), ("ocr_grid.csv", ocr_cols, ocr_rows)):
        with open(OUT / name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
    print(f"{len(llm_rows)} LLM rows, {len(ocr_rows)} OCR rows -> {OUT}")


if __name__ == "__main__":
    main()
