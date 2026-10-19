"""The cost model, written once as DSL formulas (see dsl.py).

Each Formula is: name, expression, unit, description. Inputs are the names in
INPUTS (resolved per scenario by inputs.py from the YAML data files).

Units: bytes in GB (1e9), bandwidth TB/s (1e12 B/s), compute TFLOPS (1e12),
params in billions, money in INR unless the name ends in _usd, time in seconds
unless the name says otherwise. Booleans are 0/1.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Formula:
    name: str
    expr: str
    unit: str = ""
    desc: str = ""
    group: str = ""


def F(group):
    def make(name, expr, unit="", desc=""):
        return Formula(name, expr, unit, desc, group)
    return make


# ---------------------------------------------------------------------------
# Inputs: name -> (unit, description). Resolved per scenario row.
# ---------------------------------------------------------------------------
INPUTS = {
    # scenario
    "s_users": ("users", "Peak concurrent users (signed-in, in a session)"),
    "s_speed": ("tok/s", "Target output speed per user while generating"),
    "s_bh_hours": ("h/month", "Operating hours per month in business-hours mode (~10 h x 22 days)"),
    "s_usage_hours": ("h/month", "Hours per month users are actually present"),
    "s_itc": ("0/1", "1 = company claims GST input tax credit"),
    "s_spare": ("0/1", "1 = add one spare replica (N+1)"),
    "s_years": ("years", "TCO horizon"),
    "s_fx": ("INR/USD", "Exchange rate"),
    "s_bh": ("0/1", "1 = business-hours operation (cloud on-demand stopped outside hours)"),
    "s_it_tariff": ("0/1", "1 = registered IT/data-centre unit: HT industrial tariff (+ duty exemption); 0 = HT commercial"),
    # model x precision
    "m_weights_gb": ("GB", "Checkpoint bytes at this precision (weights resident in HBM)"),
    "m_repl_gb": ("GB", "Non-routed-expert weights (attention, dense, shared experts, embeddings) at this precision; replicated on every GPU under DP-attention"),
    "m_active_b": ("B params", "Active parameters per token"),
    "m_layers": ("layers", "Transformer layers"),
    "m_experts": ("experts", "Routed experts per MoE layer"),
    "m_topk": ("experts", "Routed experts active per token"),
    "m_kv_tok_b": ("bytes", "KV cache stored per context token per sequence (all layers, incl. sparse-index keys)"),
    "m_kv_read_tok_b": ("bytes", "KV bytes read per context token per decode step (= stored for dense MLA; indexer keys only for sparse)"),
    "m_kv_read_fixed_b": ("bytes", "KV bytes read per decode step independent of context (sparse top-k entries x latent, all layers)"),
    "m_attn_flop_ctx": ("FLOP", "Attention FLOPs per new token per attended context token (all layers)"),
    "m_attend_cap": ("tokens", "Max context tokens each query attends to (sparse top-k; huge = dense)"),
    "m_idx_flop_ctx": ("FLOP", "Sparse-indexer FLOPs per new token per context token (0 if dense)"),
    "m_native_ctx": ("tokens", "Native max context"),
    "m_mtp_accept": ("tokens", "Effective tokens emitted per decode step at high concurrency incl. accepted drafts (1 = no MTP)"),
    "m_kv_seq_fixed_b": ("bytes", "Fixed KV/state stored per sequence regardless of length (sliding window, recurrent state)"),
    "m_deployable": ("0/1", "0 = not servable on current engines (e.g. FP32)"),
    "m_ops_per_layer": ("ops", "Collective/sync operations per layer per step"),
    # gpu x precision
    "g_hbm_gb": ("GB", "HBM per GPU"),
    "g_bw_tbs": ("TB/s", "HBM bandwidth per GPU"),
    "g_tflops": ("TFLOPS", "Dense tensor TFLOPS per GPU at this precision's compute format"),
    "g_per_node": ("GPUs", "GPUs per node (8 for HGX/MI355X, 72 for NVL72)"),
    "g_node_kw": ("kW", "Max power per node"),
    "g_lat_us": ("us", "Per-collective latency inside a node (NVLink/xGMI)"),
    "g_node_usd": ("USD", "Purchase price per node, incl. 3-yr warranty"),
    "g_rate_od_usd": ("USD/GPU-h", "Global cloud on-demand rate (cheapest production provider), 0 = not offered"),
    "g_rate_res1_usd": ("USD/GPU-h", "Global cloud ~1-year reserved rate, 0 = not offered"),
    "g_rate_res3_usd": ("USD/GPU-h", "Global cloud 3-year reserved rate, 0 = not offered"),
    "g_rate_in_od_inr": ("INR/GPU-h", "Indian cloud on-demand (hourly) rate, ex-GST, 0 = not offered"),
    "g_rate_in_mo_inr": ("INR/GPU-h", "Indian cloud monthly / 1-year commitment rate, ex-GST, 0 = not offered"),
    "g_rate_in_res3_inr": ("INR/GPU-h", "Indian cloud 3-year commitment rate, ex-GST, 0 = not offered"),
    "g_rack_kw": ("kW", "Rack power density this node needs (drives cooling type)"),
    # serving efficiency (calibrated per model x gpu)
    "e_mem_util": ("frac", "Fraction of HBM the engine may use"),
    "e_overhead_gb": ("GB", "Per-GPU runtime overhead: CUDA graphs, activations, comm buffers, prefill workspace"),
    "e_bw_eff": ("frac", "Achieved fraction of peak HBM bandwidth in decode"),
    "e_flop_eff": ("frac", "Achieved fraction of peak FLOPS in decode compute"),
    "e_pf_eff": ("frac", "Achieved fraction of peak FLOPS in prefill"),
    "e_xnode_lat_us": ("us", "Per-collective latency across nodes (IB/RoCE)"),
    "e_frag": ("x", "KV fragmentation / imbalance factor across replicas"),
    "e_max_batch": ("seqs", "Engine max running sequences per replica"),
    "e_dp_attn": ("0/1", "1 = data-parallel attention + expert parallelism (KV sharded across GPUs); 0 = tensor parallel (MLA KV replicated per GPU)"),
    "e_seq_us": ("us", "Calibrated per-sequence overhead per emitted token on an 8-GPU replica (attention kernels, sampling, scheduling)"),
    "e_min_batch": ("seqs", "Sequences a replica must hold at minimum when sizing nodes/replica"),
    # workload
    "w_duty": ("frac", "Fraction of a present user's time spent generating (decode+prefill in flight)"),
    "w_sawtooth": ("0/1", "1 = context follows the compaction saw-tooth between floor and trigger"),
    "w_ctx_mean": ("tokens", "Mean context per active sequence (when not saw-tooth)"),
    "w_ctx_sd": ("tokens", "Std-dev of context per active sequence (when not saw-tooth)"),
    "w_stress": ("0/1", "1 = worst case: every user active at the context ceiling"),
    "w_uncached_per_out": ("tokens", "Uncached input (prefill) tokens per output token"),
    "w_cached_per_out": ("tokens", "Prefix-cache-hit input tokens per output token"),
    "w_presence": ("frac", "Average present users / peak users during usage hours"),
    "w_turn_uncached": ("tokens", "Uncached prompt tokens in a typical turn (for TTFT)"),
    "w_out_share": ("frac", "Share of context growth that is model output"),
    # compaction (auto-summarization)
    "c_ceiling": ("tokens", "Advertised context ceiling (1,000,000)"),
    "c_trigger": ("tokens", "Compaction trigger T requested"),
    "c_floor": ("tokens", "Context right after compaction: system + summary + pinned files"),
    "c_summary_out": ("tokens", "Tokens generated to write a summary"),
    "c_reserve": ("tokens", "Window kept free for the summary prompt + max output"),
    # cloud extras
    "p_storage_tb_inr": ("INR/TB-month", "Persistent storage for weights"),
    "p_cloud_gst": ("frac", "GST on cloud services"),
    "p_warmup_h": ("h/day", "Daily cold-start hours billed for business-hours rental (weights load)"),
    "p_days": ("days/month", "Working days per month"),
    "p_rent_decline": ("frac/yr", "Year-on-year decline in GPU rental rates"),
    "p_staff_inr_24": ("INR/month", "MLOps staff to run inference on rented GPUs, 24x7 on-call"),
    "p_staff_inr_bh": ("INR/month", "MLOps staff to run inference on rented GPUs, business hours"),
    # tax / import
    "t_freight": ("frac", "Freight + insurance as fraction of FOB (gives CIF)"),
    "t_landing": ("frac", "Customs landing charge on CIF"),
    "t_bcd_srv": ("frac", "BCD on servers/GPU boards"),
    "t_bcd_net": ("frac", "BCD on network switches/optics"),
    "t_sws": ("frac", "Social Welfare Surcharge as fraction of BCD"),
    "t_igst": ("frac", "IGST/GST on hardware"),
    "t_clear_inr": ("INR", "Customs broker, port, IMS/BIS and clearance per shipment"),
    "t_fx_spread": ("frac", "Bank FX spread + LC/remittance charges"),
    "t_itc_lag_m": ("months", "Months IGST cash is tied up before ITC is used"),
    "t_tax_rate": ("frac", "Corporate tax rate (for post-tax PV)"),
    "t_dep_wdv": ("frac", "Income-tax WDV depreciation rate on servers"),
    # hardware extras (USD)
    "h_net_xnode_usd": ("USD/node", "Scale-out fabric per node (NICs, leaf share, optics) when a replica spans nodes"),
    "h_net_base_usd": ("USD", "Front-end switching + management network per deployment"),
    "h_storage_usd": ("USD", "Shared NVMe storage for weights + logs per deployment"),
    "h_host_kv_usd_per_tb": ("USD/TB", "Host RAM/NVMe tier for idle-session KV"),
    "h_rack_usd": ("USD/rack", "Rack + PDUs + cabling"),
    # facility, own room in Baner (INR)
    "f_pue_air": ("x", "PUE, small air-cooled room in Pune"),
    "f_pue_liq": ("x", "PUE, liquid-cooled (DLC + dry cooler)"),
    "f_load": ("frac", "Average draw / max node power while serving"),
    "f_idle": ("frac", "Draw / max power when idle (outside business hours, on-prem)"),
    "f_pf": ("x", "Power factor (kW -> kVA)"),
    "f_lt_limit_kva": ("kVA", "Max contract demand on an LT connection"),
    "f_bldg_kva": ("kVA", "Existing building/office load already on the connection"),
    "f_ht_fixed_inr": ("INR", "HT connection fixed costs: RMU, HT metering, CEIG, MSEDCL charges, deposit, civil for substation"),
    "f_xfmr_inr_kva": ("INR/kVA", "Transformer cost per kVA"),
    "f_elec_inr_kw": ("INR/kW", "LT panels, busbar, cabling, earthing per kW of IT"),
    "f_ups_inr_kva": ("INR/kVA", "Online modular UPS per kVA"),
    "f_batt_inr_kwh": ("INR/kWh", "UPS battery per kWh"),
    "f_batt_min": ("min", "UPS runtime minutes (until DG takes load)"),
    "f_batt_life_y": ("years", "Battery replacement cycle"),
    "f_dg_inr_kva": ("INR/kVA", "CPCB-IV+ DG set per kVA incl. install"),
    "f_air_inr_kw": ("INR/kW", "Precision air cooling per kW (racks <= 30 kW)"),
    "f_liq_inr_kw": ("INR/kW", "Rear-door / direct-liquid cooling per kW (racks > 30 kW)"),
    "f_fire_inr": ("INR", "Clean-agent suppression + VESDA + access control + CCTV"),
    "f_sqft_per_rack": ("sq ft", "Room area per rack incl. aisles, UPS, cooling"),
    "f_civil_inr_sqft": ("INR/sq ft", "Civil/fit-out per sq ft (raised floor, insulation, reinforcement)"),
    "f_rent_inr_sqft": ("INR/sq ft-month", "Office lease in Baner"),
    "f_contingency": ("frac", "Contingency on facility capex"),
    "f_energy_ind": ("INR/kWh", "HT industrial energy + wheeling + FAC, per kWh"),
    "f_energy_com": ("INR/kWh", "HT commercial energy + wheeling + FAC, per kWh"),
    "f_duty_ind": ("frac", "Electricity duty + tax on sale, industrial (0 if IT/DC duty exemption)"),
    "f_duty_com": ("frac", "Electricity duty + tax on sale, commercial"),
    "f_demand_inr_kva": ("INR/kVA-month", "Demand / fixed charge"),
    "f_struct_inr_rack": ("INR/rack", "Structural load spreading / plinth per rack (office floors ~3 kN/m2 vs 14-20 kN/m2 under a rack)"),
    "f_outage_h": ("h/month", "Grid outage hours on DG"),
    "f_diesel_inr_l": ("INR/L", "Diesel price"),
    "f_dg_l_kwh": ("L/kWh", "DG fuel consumption"),
    "f_fac_amc": ("frac/yr", "Facility equipment AMC (UPS, DG, cooling) as fraction of its capex"),
    "f_staff_inr_24": ("INR/month", "Loaded staff cost per month, own room 24x7"),
    "f_staff_inr_bh": ("INR/month", "Loaded staff cost per month, own room business hours"),
    "f_bw_inr": ("INR/month", "Internet leased line"),
    "f_insure": ("frac/yr", "Insurance premium on hardware + facility"),
    "f_hw_amc": ("frac/yr", "Hardware AMC after warranty"),
    "f_warranty_y": ("years", "Warranty years included in server price"),
    # colocation
    "o_inr_kw": ("INR/kW-month", "Colo price per contracted kW (space + cooling), ex-power"),
    "o_liq_mult": ("x", "Price multiplier for high-density / liquid-cooled colo racks (> 30 kW)"),
    "o_power_incl": ("0/1", "1 = power included in per-kW price"),
    "o_pue": ("x", "Colo PUE used for power pass-through"),
    "o_energy_inr": ("INR/kWh", "Colo power pass-through tariff"),
    "o_fixed_inr": ("INR/month", "Cross-connects, remote hands, bandwidth"),
    "o_staff_inr_24": ("INR/month", "Loaded staff cost per month with colo, 24x7 (no facility techs)"),
    "o_staff_inr_bh": ("INR/month", "Loaded staff cost per month with colo, business hours"),
    # finance
    "k_rate": ("frac/yr", "Cost of capital"),
    "k_resale": ("frac", "Resale value of hardware at end of horizon (fraction of cost)"),
}


# ---------------------------------------------------------------------------
# LLM sizing + cost formulas
# ---------------------------------------------------------------------------
_c = F("compaction")
_m = F("memory")
_d = F("throughput")
_z = F("sizing")
_r = F("rent")
_b = F("buy")
_o = F("colo")
_x = F("outputs")

_l = F("levers")
LEVERS = [
    _l("s_hours_on", "iff(s_bh == 1, s_bh_hours, 730)", "h/month", "Hours per month powered/rented"),
    _l("staff_room_m", "iff(s_bh == 1, f_staff_inr_bh, f_staff_inr_24)", "INR/month", "Staff, own room"),
    _l("staff_colo_m", "iff(s_bh == 1, o_staff_inr_bh, o_staff_inr_24)", "INR/month", "Staff, colocation"),
    _l("staff_cloud_m", "iff(s_bh == 1, p_staff_inr_bh, p_staff_inr_24)", "INR/month", "Staff, cloud rental"),
    _l("f_energy_inr", "iff(s_it_tariff == 1, f_energy_ind, f_energy_com)", "INR/kWh", "Energy tariff in use"),
    _l("f_duty", "iff(s_it_tariff == 1, f_duty_ind, f_duty_com)", "frac", "Electricity duty in use"),
    _l("gst_svc", "1 + t_igst * (1 - s_itc)", "x", "GST factor on services/equipment (18%, recoverable with ITC)"),
]

LLM = LEVERS + [
    # --- compaction / context ------------------------------------------------
    _c("c_T", "min(c_trigger, m_native_ctx - c_reserve)", "tokens",
       "Effective compaction trigger: requested T, capped so summary prompt + max output fit the native window"),
    _c("ctx_mean", "iff(w_stress == 1, min(c_ceiling, m_native_ctx), iff(w_sawtooth == 1, (c_T + c_floor) / 2, w_ctx_mean))", "tokens",
       "Mean context per active sequence (saw-tooth mean is (T+floor)/2)"),
    _c("ctx_sd", "iff(w_stress == 1, 0, iff(w_sawtooth == 1, (c_T - c_floor) / sqrt(12), w_ctx_sd))", "tokens",
       "Std-dev of context per active sequence (uniform saw-tooth: (T-floor)/sqrt(12))"),
    _c("cmp_out_overhead", "iff(w_sawtooth == 1, c_summary_out / max(1, w_out_share * (c_T - c_floor)), 0)", "frac",
       "Extra output tokens spent writing summaries, per normal output token"),
    _c("cmp_pf_overhead", "iff(w_sawtooth == 1, c_floor / max(1, w_uncached_per_out * w_out_share * (c_T - c_floor)), 0)", "frac",
       "Extra uncached prefill after each compaction (cold re-prefill of the floor), per normal uncached token"),
    _c("uncached_per_out", "w_uncached_per_out * (1 + cmp_pf_overhead) / (1 + cmp_out_overhead)", "tokens",
       "Uncached prefill tokens per emitted token, incl. compaction"),

    # --- concurrency -----------------------------------------------------------
    _z("active_mean", "iff(w_stress == 1, s_users, s_users * w_duty)", "seqs", "Mean sequences in flight at peak"),
    _z("active_p99", "iff(w_stress == 1, s_users, min(s_users, active_mean + 2.33 * sqrt(s_users * w_duty * (1 - w_duty))))", "seqs",
       "99th-percentile sequences in flight (binomial)"),

    # --- memory ----------------------------------------------------------------
    _m("usable_gb", "g_hbm_gb * e_mem_util - e_overhead_gb", "GB/GPU", "HBM usable for weights + KV per GPU"),
    _m("fits_repl", "iff(usable_gb > m_repl_gb, 1, 0)", "0/1", "Replicated weights fit on one GPU"),
    _m("kv_seq_gb", "(ctx_mean * m_kv_tok_b + m_kv_seq_fixed_b) / 1e9", "GB", "KV per sequence at mean context"),
    _m("gpus_rep_min", "iff(e_dp_attn == 1, iff(fits_repl == 1, (m_weights_gb - m_repl_gb + e_min_batch * kv_seq_gb) / max(0.001, usable_gb - m_repl_gb), 1e9), g_per_node * (m_weights_gb / g_per_node + e_min_batch * kv_seq_gb) / usable_gb)", "GPUs",
       "GPUs a replica needs for weights + minimum batch (DP-attention: replicated non-expert weights; TP: KV replicated within a node)"),
    _m("nodes_rep_min", "max(1, ceil(gpus_rep_min / g_per_node))", "nodes", "Fewest nodes one replica's weights fit on"),
    _m("nodes_rep", "nodes_rep_min", "nodes", "Nodes per replica (replaced by the replica-size search below)"),
    _m("gpus_rep", "nodes_rep * g_per_node", "GPUs", "GPUs per replica"),
    _m("kv_shards", "iff(e_dp_attn == 1, gpus_rep, nodes_rep)", "x", "Ways the KV cache is split (DP: every GPU; TP: per node/pipeline stage)"),
    _m("w_per_gpu_gb", "iff(e_dp_attn == 1, m_repl_gb + (m_weights_gb - m_repl_gb) / gpus_rep, m_weights_gb / gpus_rep)", "GB", "Weights resident per GPU"),
    _m("kv_cap_gb", "kv_shards * (usable_gb - w_per_gpu_gb)", "GB", "KV capacity per replica (unique bytes)"),
    _m("kv_need_gb", "e_frag * (active_p99 * (ctx_mean * m_kv_tok_b + m_kv_seq_fixed_b) + 2.33 * ctx_sd * sqrt(active_p99) * m_kv_tok_b) / 1e9", "GB",
       "Total KV needed at the 99th percentile of summed context"),
    _m("rep_mem", "ceil(kv_need_gb / max(0.001, kv_cap_gb))", "replicas", "Replicas needed for KV memory"),

    # --- decode / prefill timing (per replica) ---------------------------------
    _d("lat_us", "iff(nodes_rep > 1, e_xnode_lat_us, g_lat_us)", "us", "Per-collective latency"),
    _d("t_wr", "iff(e_dp_attn == 1, m_repl_gb, m_repl_gb / gpus_rep) * 1e9 / (g_bw_tbs * 1e12 * e_bw_eff)", "s",
       "Read time per step for non-expert weights (attention, dense, shared expert)"),
    _d("t_we", "(m_weights_gb - m_repl_gb) / gpus_rep * 1e9 / (g_bw_tbs * 1e12 * e_bw_eff)", "s",
       "Read time per step if every routed expert is touched"),
    _d("cov_q", "1 - m_topk / m_experts", "x", "Probability one token does not route to a given expert"),
    _d("t_lat", "m_layers * m_ops_per_layer * lat_us * 1e-6", "s", "Collective latency per step"),
    _d("attended", "min(ctx_mean, m_attend_cap)", "tokens", "Context tokens each query attends to"),
    _d("t_kv", "(ctx_mean * m_kv_read_tok_b + m_kv_read_fixed_b) * m_mtp_accept / (kv_shards * g_bw_tbs * 1e12 * e_bw_eff)", "s/seq",
       "KV-read time per sequence per step (DP-attention spreads sequences over GPUs; TP re-reads replicated KV)"),
    _d("flop_tok", "2 * m_active_b * 1e9 + m_attn_flop_ctx * attended + m_idx_flop_ctx * ctx_mean", "FLOP", "FLOPs per processed token at mean context"),
    _d("t_c", "m_mtp_accept * flop_tok / (gpus_rep * g_tflops * 1e12 * e_flop_eff)", "s/seq", "Decode compute per sequence per step"),
    _d("t_pf", "m_mtp_accept * uncached_per_out * flop_tok / (gpus_rep * g_tflops * 1e12 * e_pf_eff)", "s/seq",
       "Chunked prefill time per sequence per step (its share of new prompt tokens)"),
    _d("t_ovh", "m_mtp_accept * e_seq_us * 1e-6 * 8 / gpus_rep", "s/seq", "Calibrated per-sequence overhead per step"),
    _d("t_seq", "t_kv + t_c + t_pf + t_ovh", "s/seq", "Per-sequence time added to each step"),
    _d("lnq", "ln(cov_q)", "x", "ln of the per-token miss probability"),
    _d("t_fix0", "t_wr + t_we + t_lat - m_mtp_accept / s_speed", "s", "f(B) offset: fixed step time minus the time budget per step"),
    _d("b_nt1", "1 - (t_fix0 - t_we * cov_q ** (1 * m_mtp_accept) + 1 * t_seq) / (t_we * (-lnq) * m_mtp_accept * cov_q ** (1 * m_mtp_accept) + t_seq)", "seqs", "Newton step 1: largest batch meeting the speed target (expert coverage 1-q^(B*accept))"),
    _d("b_nt2", "b_nt1 - (t_fix0 - t_we * cov_q ** (b_nt1 * m_mtp_accept) + b_nt1 * t_seq) / (t_we * (-lnq) * m_mtp_accept * cov_q ** (b_nt1 * m_mtp_accept) + t_seq)", "seqs", "Newton step 2: largest batch meeting the speed target (expert coverage 1-q^(B*accept))"),
    _d("b_nt3", "b_nt2 - (t_fix0 - t_we * cov_q ** (b_nt2 * m_mtp_accept) + b_nt2 * t_seq) / (t_we * (-lnq) * m_mtp_accept * cov_q ** (b_nt2 * m_mtp_accept) + t_seq)", "seqs", "Newton step 3: largest batch meeting the speed target (expert coverage 1-q^(B*accept))"),
    _d("b_nt4", "b_nt3 - (t_fix0 - t_we * cov_q ** (b_nt3 * m_mtp_accept) + b_nt3 * t_seq) / (t_we * (-lnq) * m_mtp_accept * cov_q ** (b_nt3 * m_mtp_accept) + t_seq)", "seqs", "Newton step 4: largest batch meeting the speed target (expert coverage 1-q^(B*accept))"),
    _d("b_nt5", "b_nt4 - (t_fix0 - t_we * cov_q ** (b_nt4 * m_mtp_accept) + b_nt4 * t_seq) / (t_we * (-lnq) * m_mtp_accept * cov_q ** (b_nt4 * m_mtp_accept) + t_seq)", "seqs", "Newton step 5: largest batch meeting the speed target (expert coverage 1-q^(B*accept))"),
    _d("b_dec_raw", "b_nt5", "seqs", "Max batch per replica that still meets the speed target (Newton from below: never overshoots)"),
    _d("speed_ok", "iff(b_dec_raw >= 1, 1, 0)", "0/1", "Target speed reachable on this hardware"),
    _d("b_dec", "max(1, min(e_max_batch, floor(b_dec_raw)))", "seqs", "Decode batch per replica at target speed"),
    _d("rep_dec", "ceil(active_p99 / b_dec)", "replicas", "Replicas needed for speed"),

    # --- sizing ----------------------------------------------------------------
    _z("rep_n", "max(rep_mem, rep_dec)", "replicas", "Replicas (N)"),
    _z("rep_total", "rep_n + s_spare", "replicas", "Replicas incl. spare"),
    _z("nodes", "rep_total * nodes_rep", "nodes", "Nodes"),
    _z("gpus", "nodes * g_per_node", "GPUs", "GPUs"),
    _z("bound", "iff(rep_mem > rep_dec, 1, 0)", "0/1", "1 = memory-bound, 0 = speed-bound"),
    _z("b_actual", "active_p99 / rep_n", "seqs", "Sequences per replica at peak"),
    _z("cov_actual", "1 - cov_q ** (max(1, b_actual) * m_mtp_accept)", "frac", "Expert coverage at peak batch"),
    _z("speed_actual", "m_mtp_accept / (t_wr + t_we * cov_actual + t_lat + b_actual * t_seq)", "tok/s", "Per-user speed at peak load"),
    _z("ttft", "w_turn_uncached * flop_tok / (gpus_rep * g_tflops * 1e12 * e_pf_eff) + t_wr + t_we + t_lat", "s",
       "Time to first token for a typical uncached turn on an idle replica"),
    _z("feasible", "iff(m_deployable == 1, speed_ok * fits_repl, 0)", "0/1", "Configuration is deployable and meets the target"),
    _z("host_kv_tb", "iff(w_stress == 1, 0, s_users * (1 - w_duty) * ctx_mean * m_kv_tok_b / 1e12)", "TB",
       "Host RAM/NVMe tier for idle sessions' KV"),

    # --- power -----------------------------------------------------------------
    _z("it_kw_max", "nodes * g_node_kw", "kW", "IT load at max power"),
    _z("f_pue", "iff(g_rack_kw > 30, f_pue_liq, f_pue_air)", "x", "PUE for this cooling type"),
    _z("it_kw_avg", "it_kw_max * f_load", "kW", "IT load while serving"),

    # --- tokens served -----------------------------------------------------------
    _x("out_tok_m", "s_users * w_presence * w_duty * speed_actual * 3600 * min(s_usage_hours, s_hours_on) / (1 + cmp_out_overhead)", "tokens/month",
       "Useful output tokens served per month"),
    _x("in_tok_m", "out_tok_m * (uncached_per_out + w_cached_per_out)", "tokens/month", "Input tokens processed per month"),

    # --- rent ------------------------------------------------------------------
    _r("rent_hours_bh", "s_hours_on + p_warmup_h * p_days", "h/month", "Billed hours for business-hours on-demand"),
    _r("rent_gst", "1 + p_cloud_gst * (1 - s_itc)", "x", "GST factor on cloud (recoverable with ITC)"),
    _r("rent_storage", "p_storage_tb_inr * rep_total * m_weights_gb / 1000 * 1.2", "INR/month", "Weights on persistent storage"),
    _r("na", "1e15", "INR/month", "Marker for a rental option that is not offered"),
    _r("rent_hrs", "iff(s_bh == 1, rent_hours_bh, 730)", "h/month", "Billed hours for hourly on-demand"),
    _r("rent_od", "iff(g_rate_od_usd > 0, (gpus * g_rate_od_usd * s_fx * rent_hrs + rent_storage) * rent_gst, na)", "INR/month",
       "Global cloud, on-demand"),
    _r("rent_res1", "iff(g_rate_res1_usd > 0, (gpus * g_rate_res1_usd * s_fx * 730 + rent_storage) * rent_gst, na)", "INR/month", "Global cloud, ~1-yr reserved (billed 24/7)"),
    _r("rent_res3", "iff(g_rate_res3_usd > 0, (gpus * g_rate_res3_usd * s_fx * 730 + rent_storage) * rent_gst, na)", "INR/month", "Global cloud, 3-yr reserved (billed 24/7)"),
    _r("rent_in_od", "iff(g_rate_in_od_inr > 0, (gpus * g_rate_in_od_inr * rent_hrs + rent_storage) * rent_gst, na)", "INR/month",
       "Indian cloud, on-demand"),
    _r("rent_in_mo", "iff(g_rate_in_mo_inr > 0, (gpus * g_rate_in_mo_inr * 730 + rent_storage) * rent_gst, na)", "INR/month",
       "Indian cloud, monthly / 1-yr commitment (billed 24/7)"),
    _r("rent_in_res3", "iff(g_rate_in_res3_inr > 0, (gpus * g_rate_in_res3_inr * 730 + rent_storage) * rent_gst, na)", "INR/month",
       "Indian cloud, 3-yr commitment (billed 24/7)"),
    _r("rent_best", "iff(s_bh == 1, min(rent_od, rent_in_od), min(rent_od, rent_res1, rent_in_od, rent_in_mo, iff(s_years >= 3, min(rent_res3, rent_in_res3), na)))", "INR/month",
       "Cheapest rental option for this pattern (business hours: hourly only; 24/7: any commitment up to the horizon)"),
    _r("rent_m", "rent_best + staff_cloud_m", "INR/month", "All-in monthly cost, cloud rental (cheapest option + MLOps staff)"),
    _r("rent_decline_avg", "iff(p_rent_decline > 0, (1 - (1 - p_rent_decline) ** s_years) / (p_rent_decline * s_years), 1)", "x",
       "Average rate over the horizon relative to today (declining prices)"),
    _r("rent_tco", "(rent_best * rent_decline_avg + staff_cloud_m) * 12 * s_years", "INR", "Rental cost over the horizon"),

    # --- buy: landed hardware ---------------------------------------------------
    _b("hw_srv_usd", "nodes * g_node_usd + h_host_kv_usd_per_tb * host_kv_tb + h_storage_usd", "USD", "Servers + host KV tier + storage (imported)"),
    _b("hw_net_usd", "h_net_base_usd + iff(nodes_rep > 1, nodes * h_net_xnode_usd, 0)", "USD", "Networking"),
    _b("racks", "ceil(it_kw_max / g_rack_kw)", "racks", "Racks"),
    _b("hw_rack_usd", "racks * h_rack_usd", "USD", "Racks, PDUs, cabling (bought in India)"),
    _b("cif_srv", "hw_srv_usd * s_fx * (1 + t_freight) * (1 + t_landing)", "INR", "Assessable value, servers"),
    _b("cif_net", "hw_net_usd * s_fx * (1 + t_freight) * (1 + t_landing)", "INR", "Assessable value, network"),
    _b("duty_srv", "cif_srv * t_bcd_srv * (1 + t_sws)", "INR", "BCD + SWS, servers"),
    _b("duty_net", "cif_net * t_bcd_net * (1 + t_sws)", "INR", "BCD + SWS, network"),
    _b("igst_hw", "(cif_srv + duty_srv + cif_net + duty_net) * t_igst", "INR", "IGST on import"),
    _b("hw_landed", "(cif_srv + duty_srv + cif_net + duty_net) * (1 + t_fx_spread) + t_clear_inr + igst_hw * (1 - s_itc) + igst_hw * s_itc * k_rate * t_itc_lag_m / 12",
       "INR", "Landed hardware cost (IGST is a cost without ITC; with ITC only its financing cost)"),

    # --- buy: own room in Baner ------------------------------------------------
    _b("kva_it", "it_kw_max * f_pue / f_pf", "kVA", "Contract demand (facility at peak)"),
    _b("needs_ht", "iff(kva_it + f_bldg_kva > f_lt_limit_kva, 1, 0)", "0/1", "Load exceeds LT limit -> HT connection"),
    _b("fac_elec", "needs_ht * (f_ht_fixed_inr + f_xfmr_inr_kva * (kva_it + f_bldg_kva)) + f_elec_inr_kw * it_kw_max", "INR",
       "Electrical: HT connection/transformer if needed + LT distribution"),
    _b("fac_ups", "f_ups_inr_kva * it_kw_max / f_pf + f_batt_inr_kwh * it_kw_max * f_batt_min / 60", "INR", "UPS + batteries (IT load)"),
    _b("fac_dg", "f_dg_inr_kva * kva_it", "INR", "DG set (whole facility load)"),
    _b("fac_cool", "it_kw_max * iff(g_rack_kw > 30, f_liq_inr_kw, f_air_inr_kw)", "INR", "Cooling"),
    _b("room_sqft", "racks * f_sqft_per_rack", "sq ft", "Room area"),
    _b("fac_civil", "room_sqft * f_civil_inr_sqft + f_fire_inr + racks * f_struct_inr_rack", "INR", "Civil, fit-out, fire, security, floor reinforcement"),
    _b("fac_equip", "(fac_ups + fac_dg + fac_cool + hw_rack_usd * s_fx) * (1 + f_contingency)", "INR", "Facility equipment incl. racks (GST credit allowed)"),
    _b("fac_works", "(fac_elec + fac_civil) * (1 + f_contingency)", "INR", "Facility works (GST credit blocked u/s 17(5))"),
    _b("fac_capex", "fac_equip * (1 + t_igst * (1 - s_itc)) + fac_works * (1 + t_igst)", "INR", "Facility capex incl. GST"),
    _b("buy_capex", "hw_landed + fac_capex", "INR", "Total capex, own room"),

    _b("hours_idle", "730 - s_hours_on", "h/month", "Hours idle (on-prem stays powered)"),
    _b("kwh_m", "it_kw_max * f_pue * (f_load * s_hours_on + f_idle * hours_idle)", "kWh/month", "Facility energy"),
    _b("power_m", "kwh_m * f_energy_inr * (1 + f_duty) + kva_it * f_demand_inr_kva", "INR/month", "Electricity bill (incremental)"),
    _b("diesel_m", "f_outage_h * it_kw_avg * f_pue * f_dg_l_kwh * f_diesel_inr_l", "INR/month", "DG diesel"),
    _b("amc_years", "max(0, s_years - f_warranty_y)", "years", "Years of paid hardware AMC within the horizon"),
    _b("hw_amc_m", "hw_landed * f_hw_amc * amc_years / s_years / 12 * gst_svc", "INR/month", "Hardware AMC (averaged)"),
    _b("fac_amc_m", "fac_equip * f_fac_amc / 12 * gst_svc", "INR/month", "Facility AMC"),
    _b("batt_m", "f_batt_inr_kwh * it_kw_max * f_batt_min / 60 / (f_batt_life_y * 12)", "INR/month", "Battery replacement reserve"),
    _b("insure_m", "buy_capex * f_insure / 12 * gst_svc", "INR/month", "Insurance"),
    _b("space_m", "room_sqft * f_rent_inr_sqft * gst_svc", "INR/month", "Space rent"),
    _b("buy_opex", "power_m + diesel_m + hw_amc_m + fac_amc_m + batt_m + insure_m + staff_room_m + space_m + f_bw_inr * gst_svc", "INR/month", "Opex, own room"),

    # --- finance ---------------------------------------------------------------
    _b("k_m", "k_rate / 12", "frac/month", "Monthly cost of capital"),
    _b("k_n", "s_years * 12", "months", "Horizon months"),
    _b("crf", "k_m / (1 - (1 + k_m) ** (-k_n))", "x", "Capital recovery factor"),
    _b("resale_pv", "k_resale * hw_landed / (1 + k_m) ** k_n", "INR", "PV of resale"),
    _b("buy_capex_m", "crf * (buy_capex - resale_pv)", "INR/month", "Capex as a monthly charge (incl. cost of capital)"),
    _b("buy_m", "buy_capex_m + buy_opex", "INR/month", "All-in monthly cost, own room"),
    _b("buy_tco", "buy_m * k_n", "INR", "Cost over horizon, own room"),

    # --- colocation ------------------------------------------------------------
    _o("colo_kw", "it_kw_max", "kW", "Contracted kW"),
    _o("colo_power_m", "(1 - o_power_incl) * it_kw_max * o_pue * (f_load * s_hours_on + f_idle * hours_idle) * o_energy_inr", "INR/month", "Power pass-through"),
    _o("colo_opex", "(colo_kw * o_inr_kw * iff(g_rack_kw > 30, o_liq_mult, 1) + colo_power_m + o_fixed_inr) * gst_svc + hw_amc_m + hw_landed * f_insure / 12 * gst_svc + staff_colo_m", "INR/month", "Opex, colocation (colo fees carry 18% GST)"),
    _o("colo_capex_m", "crf * (hw_landed - resale_pv)", "INR/month", "Hardware capex as monthly charge"),
    _o("colo_m", "colo_capex_m + colo_opex", "INR/month", "All-in monthly cost, colocation"),
    _o("colo_tco", "colo_m * k_n", "INR", "Cost over horizon, colocation"),

    # --- post-tax PV (WDV depreciation shield) ----------------------------------
    _x("k_y", "(1 + k_m) ** 12 - 1", "frac/yr", "Effective annual cost of capital"),
    _x("dep_q", "(1 - t_dep_wdv) / (1 + k_y)", "x", "WDV discount ratio"),
    _x("dep_shield_pv", "t_tax_rate * hw_landed * t_dep_wdv / (1 + k_y) * (1 - dep_q ** s_years) / (1 - dep_q)", "INR",
       "PV of depreciation tax shield on hardware over the horizon"),
    _x("annuity", "(1 - (1 + k_m) ** (-k_n)) / k_m", "x", "PV of 1 INR/month over the horizon"),
    _x("pv_buy", "buy_capex - dep_shield_pv + buy_opex * (1 - t_tax_rate) * annuity - resale_pv * (1 - t_tax_rate)", "INR",
       "Post-tax PV, own room"),
    _x("pv_rent", "(rent_best * rent_decline_avg + staff_cloud_m) * (1 - t_tax_rate) * annuity", "INR", "Post-tax PV, rent"),

    # --- headline outputs -------------------------------------------------------
    _x("best_m", "min(rent_m, buy_m, colo_m)", "INR/month", "Cheapest option per month"),
    _x("breakeven_m", "iff(rent_m > buy_opex, buy_capex / (rent_m - buy_opex), 999)", "months",
       "Months until buying (own room) beats renting at today's rates (999 = never)"),
    _x("per_user_buy", "buy_m / s_users", "INR/user-month", "Own room, per peak user"),
    _x("per_user_rent", "rent_m / s_users", "INR/user-month", "Rent, per peak user"),
    _x("per_mtok_out_buy", "buy_m / max(1, out_tok_m / 1e6)", "INR/M output tok", "Own room, per million output tokens (all cost on output)"),
    _x("per_mtok_out_rent", "rent_m / max(1, out_tok_m / 1e6)", "INR/M output tok", "Rent, per million output tokens"),
    _x("usd_buy_m", "buy_m / s_fx", "USD/month", "Own room, USD"),
    _x("usd_rent_m", "rent_m / s_fx", "USD/month", "Rent, USD"),
    _x("usd_colo_m", "colo_m / s_fx", "USD/month", "Colo, USD"),
]


# ---------------------------------------------------------------------------
# OCR (Chandra OCR 2): sized by pages/hour, not users
# ---------------------------------------------------------------------------
OCR_INPUTS = {
    "q_pages_h": ("pages/h", "Peak pages per hour"),
    "q_pages_s_gpu": ("pages/s", "Measured/estimated pages per second per GPU at this precision"),
    "q_util": ("frac", "Target utilisation at peak"),
    "q_gpus_per_srv": ("GPUs", "GPUs per OCR server"),
    "q_srv_usd": ("USD", "OCR server price (with q_gpus_per_srv GPUs)"),
    "q_srv_kw": ("kW", "OCR server max power"),
    "q_rate_usd": ("USD/GPU-h", "Cloud rate for this GPU"),
    "q_rate_in_inr": ("INR/GPU-h", "Indian cloud rate for this GPU"),
    "q_deployable": ("0/1", "0 = precision not servable"),
}

_q = F("ocr")
OCR = LEVERS + [
    _q("q_gpus_n", "max(1, ceil(q_pages_h / 3600 / (q_pages_s_gpu * q_util)))", "GPUs", "GPUs needed (N)"),
    _q("q_gpus", "q_gpus_n + s_spare", "GPUs", "GPUs incl. spare"),
    _q("q_srv", "ceil(q_gpus / q_gpus_per_srv)", "servers", "Servers"),
    _q("q_kw", "q_srv * q_srv_kw", "kW", "IT load at max power"),
    _q("q_rent_m", "min(q_gpus * q_rate_usd * s_fx, q_gpus * q_rate_in_inr) * iff(s_bh == 1, s_hours_on + p_warmup_h * p_days, 730) * (1 + p_cloud_gst * (1 - s_itc))", "INR/month",
       "Cheapest rental"),
    _q("q_cif", "(q_srv * q_srv_usd + h_rack_usd) * s_fx * (1 + t_freight) * (1 + t_landing)", "INR", "Assessable value"),
    _q("q_landed", "q_cif * (1 + t_bcd_srv * (1 + t_sws)) * (1 + t_fx_spread) + t_clear_inr + q_cif * (1 + t_bcd_srv * (1 + t_sws)) * t_igst * (1 - s_itc)", "INR",
       "Landed hardware"),
    _q("q_kwh_m", "q_kw * f_pue_air * (f_load * s_hours_on + f_idle * (730 - s_hours_on))", "kWh/month", "Energy"),
    _q("q_k_m", "k_rate / 12", "frac/month", "Monthly cost of capital"),
    _q("q_crf", "q_k_m / (1 - (1 + q_k_m) ** (-(s_years * 12)))", "x", "Capital recovery factor"),
    _q("q_colo_m", "q_crf * (q_landed - k_resale * q_landed / (1 + q_k_m) ** (s_years * 12)) + q_kw * o_inr_kw * gst_svc + (1 - o_power_incl) * q_kwh_m / f_pue_air * o_pue * o_energy_inr + q_landed * (f_insure + f_hw_amc * max(0, s_years - f_warranty_y) / s_years) / 12 * gst_svc", "INR/month",
       "Bought, hosted in colo (no extra staff: shares the LLM team)"),
    _q("q_room_m", "q_crf * (q_landed - k_resale * q_landed / (1 + q_k_m) ** (s_years * 12)) + q_kwh_m * f_energy_inr * (1 + f_duty) + q_kw * f_pue_air / f_pf * f_demand_inr_kva + q_landed * (f_insure + f_hw_amc * max(0, s_years - f_warranty_y) / s_years) / 12 * gst_svc", "INR/month",
       "Bought, in an existing room (incremental power + capex; no facility build)"),
    _q("q_pages_m", "q_pages_h * min(s_usage_hours, s_hours_on) * 0.5", "pages/month", "Pages per month (average = half of peak over usage hours)"),
    _q("q_per_1k_rent", "q_rent_m / max(1, q_pages_m / 1000)", "INR/1k pages", "Rent, per 1,000 pages"),
    _q("q_per_1k_room", "q_room_m / max(1, q_pages_m / 1000)", "INR/1k pages", "Bought, per 1,000 pages"),
    _q("q_feasible", "q_deployable", "0/1", "Deployable"),
]


# ---------------------------------------------------------------------------
# Replica-size search. A replica can span more nodes than its weights need:
# spreading weights over more GPUs frees HBM for KV (memory-bound cases) at the
# cost of cross-node latency. The per-replica chain below is cloned for
# candidates nodes_rep_min + 0..REP_CANDIDATES-1, and the candidate needing the
# fewest nodes (incl. spare, infeasible speed penalised) is selected.
# ---------------------------------------------------------------------------
import re as _re

REP_CANDIDATES = 3
_REP_CHAIN = ["nodes_rep", "gpus_rep", "kv_shards", "w_per_gpu_gb", "kv_cap_gb", "rep_mem", "lat_us", "t_wr", "t_we",
              "t_lat", "t_kv", "t_c", "t_pf", "t_ovh", "t_seq", "t_fix0", "b_nt1", "b_nt2", "b_nt3", "b_nt4", "b_nt5",
              "b_dec_raw", "speed_ok", "b_dec", "rep_dec"]


def _rep_search(formulas):
    by = {f.name: f for f in formulas}
    pat = _re.compile(r"\b(" + "|".join(_REP_CHAIN) + r")\b")
    clones, sel = [], []
    for k in range(1, REP_CANDIDATES + 1):
        sub = lambda e, k=k: pat.sub(lambda m: f"{m.group(1)}_c{k}", e)
        for n in _REP_CHAIN:
            f = by[n]
            expr = f"nodes_rep_min + {k - 1}" if n == "nodes_rep" else sub(f.expr)
            clones.append(Formula(f"{n}_c{k}", expr, f.unit, f"{f.desc} [candidate {k}: nodes_rep_min + {k - 1}]", "replica search"))
        clones.append(Formula(f"rep_tot_c{k}", f"(max(rep_mem_c{k}, rep_dec_c{k}) + s_spare) * nodes_rep_c{k} + iff(speed_ok_c{k} == 1, 0, 1000000)",
                              "nodes", f"Total nodes with candidate {k} (infeasible speed penalised)", "replica search"))
    best = "min(" + ", ".join(f"rep_tot_c{k}" for k in range(1, REP_CANDIDATES + 1)) + ")"
    clones.append(Formula("rep_tot_best", best, "nodes", "Fewest total nodes over replica-size candidates", "replica search"))
    pick = str(REP_CANDIDATES)
    for k in range(REP_CANDIDATES - 1, 0, -1):
        pick = f"iff(rep_tot_c{k} == rep_tot_best, {k}, {pick})"
    clones.append(Formula("rep_sel", pick, "candidate", "Chosen replica-size candidate (smallest on ties)", "replica search"))
    for n in _REP_CHAIN:
        f = by[n]
        e = f"{n}_c{REP_CANDIDATES}"
        for k in range(REP_CANDIDATES - 1, 0, -1):
            e = f"iff(rep_sel == {k}, {n}_c{k}, {e})"
        sel.append(Formula(n, e, f.unit, f.desc + " (chosen candidate)", f.group))
    out = [f for f in formulas if f.name not in _REP_CHAIN]
    return out + clones + sel


LLM = _rep_search(LLM)
