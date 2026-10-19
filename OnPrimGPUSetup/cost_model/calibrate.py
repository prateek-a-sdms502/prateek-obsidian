"""Calibrate the decode model against published benchmark points.

e_bw_eff is fixed per GPU family (data/calibration.yaml); e_seq_us is least-squares
fitted per model x GPU over all its points, holding everything else at the engine's
formulas under each benchmark's own parallelism (TP size, TP vs DP attention, MTP).

  python calibrate.py           # print fits and residuals
  python calibrate.py --write   # also write data/efficiency.yaml overrides
"""
import sys

import yaml

from engine import run_llm
from inputs import DATA, Data


def bench_row(d, model, gpu, pt, e_bw, e_seq):
    row = d.llm_row(model, pt["precision"], gpu, "bench_8k1k", pt["conc"], 30)
    row.update({"g_per_node": pt["tp_gpus"], "e_dp_attn": pt["dp_attn"], "m_mtp_accept": pt["accept"],
                "e_bw_eff": e_bw, "e_seq_us": e_seq, "s_spare": 0, "e_max_batch": 4096})
    if "ctx" in pt:
        row["w_ctx_mean"] = pt["ctx"]
    if "uncached" in pt:
        row["w_uncached_per_out"] = pt["uncached"]
    return row


def c1(v):
    """The benchmark ran one replica on exactly tp_gpus GPUs: use replica-size candidate 1."""
    return {**v, **{k[:-3]: x for k, x in v.items() if k.endswith("_c1")}}


def predict(d, model, gpu, pt, e_bw, e_seq):
    v = c1(run_llm(bench_row(d, model, gpu, pt, e_bw, e_seq)))
    b = pt["conc"]
    cov = 1 - v["cov_q"] ** (b * v["m_mtp_accept"])
    stp = v["t_wr"] + v["t_we"] * cov + v["t_lat"] + b * v["t_seq"]
    return v["m_mtp_accept"] / stp, v


def fit_set(d, key, pts, e_bw):
    model, gpu = key.split("/")
    num = den = 0.0
    for pt in pts:
        _, v0 = predict(d, model, gpu, pt, e_bw, 0.0)
        b, A = pt["conc"], pt["accept"]
        cov = 1 - v0["cov_q"] ** (b * A)
        base = v0["t_wr"] + v0["t_we"] * cov + v0["t_lat"] + b * v0["t_seq"]
        cy = b * A * 8e-6 / v0["gpus_rep"]          # d(step)/d(e_seq)
        res = A / pt["tok_s_user"] - base
        num += res * cy
        den += cy * cy
    e_seq = max(0.0, num / den)
    errs = [100 * (predict(d, model, gpu, pt, e_bw, e_seq)[0] / pt["tok_s_user"] - 1) for pt in pts]
    return round(e_seq, 1), errs


def main():
    d = Data()
    cal = yaml.safe_load(open(DATA / "calibration.yaml"))
    bw = cal["gpu_bw_eff"]
    fits = {}
    print(f"{'model/gpu':20s} {'e_bw':>5s} {'e_seq_us':>9s}  residuals (pred/meas - 1)")
    for key, pts in cal["sets"].items():
        gpu = key.split("/")[1]
        e_seq, errs = fit_set(d, key, pts, bw[gpu])
        fits[key] = {"e_bw_eff": bw[gpu], "e_seq_us": e_seq, "errs": errs, "n": len(pts)}
        print(f"{key:20s} {bw[gpu]:5.2f} {e_seq:9.1f}  " + "  ".join(f"{e:+5.1f}%" for e in errs))
    allerr = [abs(e) for f in fits.values() for e in f["errs"]]
    print(f"\nmean |residual| {sum(allerr) / len(allerr):.1f}%, max {max(allerr):.1f}% over {len(allerr)} points")
    if "--write" in sys.argv:
        eff = yaml.safe_load(open(DATA / "efficiency.yaml"))
        ov = {g: {"e_bw_eff": {"value": v, "source": "GPU-family bandwidth efficiency (calibration.yaml)"}} for g, v in bw.items()}
        for key, f in fits.items():
            ov[key] = {"e_seq_us": {"value": f["e_seq_us"], "source": f"Least-squares fit to {f['n']} published points (calibrate.py); residuals " + ", ".join(f"{e:+.0f}%" for e in f["errs"])}}
        for key, src in cal["inherit"].items():
            ov[key] = {"e_seq_us": {"value": fits[src]["e_seq_us"], "source": f"No published data: inherited from {src}"}}
        eff["overrides"] = ov
        with open(DATA / "efficiency.yaml", "w") as fh:
            fh.write("# Serving-efficiency coefficients. Overrides are written by calibrate.py --write.\n")
            yaml.safe_dump(eff, fh, sort_keys=False, width=200, allow_unicode=True)
        print("wrote overrides to data/efficiency.yaml")


if __name__ == "__main__":
    main()
