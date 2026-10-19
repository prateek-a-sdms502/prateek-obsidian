"""Emit out/model.js: the formula catalog as JavaScript plus all data tables.

The HTML calculator includes this file, so it runs exactly the same formulas as
engine.py and the Excel workbook. Exposes window.CostModel with:
  data, llm(v) -> v (fills every formula), ocr(v) -> v, llmRow(keys, levers), ocrRow(keys, levers), meta
"""
import json
from pathlib import Path

from dsl import to_js, toposort
from formulas import INPUTS, LLM, OCR, OCR_INPUTS
from inputs import Data, val

OUT = Path(__file__).parent / "out"


def js_fn(name, order):
    body = "\n".join(f"  v.{f.name} = {to_js(f.expr)};" for f in order)
    return f"function {name}(v) {{\n{body}\n  return v;\n}}"


def plain(x):
    if isinstance(x, dict):
        if "value" in x:
            return x["value"]
        return {k: plain(v) for k, v in x.items()}
    if isinstance(x, list):
        return [plain(v) for v in x]
    return x


def main():
    d = Data()
    llm_order = toposort(LLM, set(INPUTS))
    ocr_order = toposort(OCR, set(INPUTS) | set(OCR_INPUTS))
    data = {
        "models": plain(d.models), "gpus": plain(d.gpus),
        "eff_default": plain(d.eff_default), "eff_override": plain(d.eff_override),
        "workloads": plain(d.workloads), "globals": {k: val(v) for k, v in d.globals.items()},
        "ocr": plain(d.ocr), "scen": plain(d.scen),
    }
    meta = {
        "inputs": {**INPUTS, **OCR_INPUTS},
        "formulas": {f.name: {"unit": f.unit, "desc": f.desc, "group": f.group, "expr": f.expr}
                     for f in llm_order + ocr_order},
    }
    resolve = r"""
function pick(o, pre) { const r = {}; for (const k in o) if (pre.some(p => k.startsWith(p))) r[k] = o[k]; return r; }
function levers(l) { return { s_bh: l.uptime === 'bh' ? 1 : 0, s_itc: l.itc, s_spare: l.spare, s_years: l.years }; }
function llmRow(k, l) {
  const D = DATA, m = D.models[k.model], p = m.precisions[k.precision], g = D.gpus[k.gpu];
  const e = Object.assign({}, D.eff_default);
  for (const key of [k.model, k.gpu, k.model + '/' + k.gpu, k.model + '/' + k.gpu + '/' + k.precision])
    Object.assign(e, D.eff_override[key] || {});
  const tf = g.tflops, fmt = p.compute_fmt;
  const gf = pick(g, ['g_']);
  gf.g_tflops = (tf[fmt] != null) ? tf[fmt] : tf[g.fp4_fallback || 'fp8'];
  return Object.assign({}, D.globals, levers(l), pick(D.workloads[k.workload], ['w_', 'c_']),
    pick(m, ['m_']), pick(p, ['m_']), gf, e, { s_users: k.users, s_speed: k.speed });
}
function ocrRow(k, l) {
  const o = DATA.ocr, g = o.gpus[k.gpu];
  return Object.assign({}, DATA.globals, levers(l), pick(g, ['q_']), pick(g.precisions[k.precision], ['q_']),
    { q_pages_h: o.tiers[k.tier] });
}
"""
    js = "\n".join([
        "(function () {",
        "'use strict';",
        "function _ceil(x) { return Math.sign(x) * Math.ceil(Math.abs(x)); }",
        "function _floor(x) { return Math.trunc(x); }",
        f"const DATA = {json.dumps(data)};",
        f"const META = {json.dumps(meta)};",
        js_fn("llm", llm_order),
        js_fn("ocr", ocr_order),
        resolve,
        "window.CostModel = { data: DATA, meta: META, llm, ocr, llmRow, ocrRow };",
        "})();",
    ])
    OUT.mkdir(exist_ok=True)
    (OUT / "model.js").write_text(js)
    print(f"wrote {OUT / 'model.js'} ({len(js) // 1024} KB)")


if __name__ == "__main__":
    main()
