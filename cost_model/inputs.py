"""Load the YAML data files and resolve one flat input dict per scenario row.

Data layout (cost_model/data/):
  models.yaml      model -> common fields + precisions -> m_* fields
  gpus.yaml        gpu -> g_* fields + tflops per compute format
  efficiency.yaml  e_* defaults + overrides keyed "model/gpu"
  workloads.yaml   profile -> w_* fields (+ optional c_* overrides)
  globals.yaml     every scalar input: {value, unit?, source, note?}
  ocr.yaml         Chandra OCR 2: per gpu x precision q_* fields
  scenarios.yaml   grid axes and the reference scenarios used for parity checks

Values in YAML may be plain numbers or {value: x, source: ..., note: ...}.
"""
import itertools
from pathlib import Path

import yaml

from formulas import INPUTS, OCR_INPUTS

DATA = Path(__file__).parent / "data"

# Scalar inputs that vary per matrix row; everything else comes from globals.yaml.
ROW_KEYS = ("model", "precision", "gpu", "workload", "users", "speed")


def _load(name):
    with open(DATA / name) as f:
        return yaml.safe_load(f)


def val(x):
    return x["value"] if isinstance(x, dict) and "value" in x else x


def meta(x):
    return x if isinstance(x, dict) else {"value": x}


class Data:
    def __init__(self):
        self.models = _load("models.yaml")["models"]
        self.gpus = _load("gpus.yaml")["gpus"]
        eff = _load("efficiency.yaml")
        self.eff_default = eff["default"]
        self.eff_override = eff.get("overrides", {}) or {}
        self.workloads = _load("workloads.yaml")["workloads"]
        self.globals = _load("globals.yaml")["globals"]
        self.ocr = _load("ocr.yaml")
        self.scen = _load("scenarios.yaml")

    # -- per-dimension resolution -------------------------------------------
    def model_fields(self, model, precision):
        m = self.models[model]
        common = {k: val(v) for k, v in m.items() if k.startswith("m_")}
        p = {k: val(v) for k, v in m["precisions"][precision].items() if k.startswith("m_")}
        out = {**common, **p}
        fmt = m["precisions"][precision]["compute_fmt"]
        return out, fmt

    def gpu_fields(self, gpu, fmt):
        g = self.gpus[gpu]
        out = {k: val(v) for k, v in g.items() if k.startswith("g_")}
        tf = {k: val(v) for k, v in g["tflops"].items()}
        # Hopper has no FP4 tensor cores: FP4 weights run as W4A8 on FP8 cores.
        out["g_tflops"] = tf[fmt] if tf.get(fmt) is not None else tf[g.get("fp4_fallback", "fp8")]
        return out

    def eff_fields(self, model, gpu, precision):
        out = {k: val(v) for k, v in self.eff_default.items()}
        for key in (model, gpu, f"{model}/{gpu}", f"{model}/{gpu}/{precision}"):
            out.update({k: val(v) for k, v in (self.eff_override.get(key) or {}).items()})
        return out

    def workload_fields(self, workload):
        return {k: val(v) for k, v in self.workloads[workload].items() if k[:2] in ("w_", "c_")}

    def global_fields(self):
        return {k: val(v) for k, v in self.globals.items()}

    # -- rows ------------------------------------------------------------------
    def levers(self, uptime="24x7", itc=1, spare=0, years=3):
        return {"s_bh": 1 if uptime == "bh" else 0, "s_itc": itc, "s_spare": spare, "s_years": years}

    def llm_row(self, model, precision, gpu, workload, users, speed, **lever_kw):
        g = self.global_fields()
        mf, fmt = self.model_fields(model, precision)
        row = {**g, **self.levers(**lever_kw), **self.workload_fields(workload), **mf,
               **self.gpu_fields(gpu, fmt), **self.eff_fields(model, gpu, precision),
               "s_users": users, "s_speed": speed}
        missing = [k for k in INPUTS if k not in row]
        if missing:
            raise KeyError(f"{model}/{precision}/{gpu}/{workload}: missing inputs {missing}")
        return row

    def llm_grid(self):
        ax = self.scen["grid"]
        for model, gpu, wl, users, speed in itertools.product(
                ax["models"], ax["gpus"], ax["workloads"], ax["users"], ax["speeds"]):
            for precision in self.models[model]["precisions"]:
                yield {"model": model, "precision": precision, "gpu": gpu, "workload": wl,
                       "users": users, "speed": speed}

    def ocr_row(self, gpu, precision, tier, **lever_kw):
        g = self.global_fields()
        o = self.ocr
        q = {k: val(v) for k, v in o["gpus"][gpu].items() if k.startswith("q_")}
        q.update({k: val(v) for k, v in o["gpus"][gpu]["precisions"][precision].items() if k.startswith("q_")})
        row = {**g, **self.levers(**lever_kw), **q, "q_pages_h": o["tiers"][tier]}
        missing = [k for k in OCR_INPUTS if k not in row]
        if missing:
            raise KeyError(f"ocr {gpu}/{precision}: missing inputs {missing}")
        return row

    def ocr_grid(self):
        for gpu, gd in self.ocr["gpus"].items():
            for precision in gd["precisions"]:
                for tier in self.ocr["tiers"]:
                    yield {"gpu": gpu, "precision": precision, "tier": tier}
