# Measured inference performance: GLM-5.x, DeepSeek V4 Pro (V3.2/R1 proxies), Kimi K2.x, Chandra OCR 2 on datacenter GPUs

Research date: 2026-10-19. Data from 2026 unless labelled **[PROXY]** (older data or a predecessor model). Raw numbers are as reported. Unit conventions used throughout:

- **InferenceX "tok/s/GPU"** (SemiAnalysis, also called tok/s/chip) = **total tokens (input + output) per GPU per second**. This is not output tokens. I checked this against the published tables (see the Q1 inferences). For 8k/1k, output tok/s/GPU ≈ tok/s/GPU ÷ 9. For 1k/1k, it is ≈ ÷ 2.
- **InferenceX "tok/s/user"** (interactivity) = 1000 / TPOT(ms). It excludes TTFT. Check: 84.49 tok/s/user × 11.84 ms = 1000.
- "Per node" means 8 GPUs unless stated otherwise.

---

## Q1. Per model and GPU: tok/s/user and tok/s/GPU at concurrency ~50/64/90/128 (1k/1k, 8k/1k, 32k+/1k)

### Takeaway
There is dense, measured 2026 data for **8k/1k on 8-GPU nodes**: GLM-5 on H200, B200 and MI355X; Kimi K2.5/K2.6 on H200, B200 and GB200; DeepSeek V4 Pro on MI355X, GB300 and B300. At concurrency 64, an 8-GPU node delivers roughly 850–1,900 total tok/s/GPU at 17–27 tok/s/user in FP8/INT4. NVFP4 on B200 reaches about 3,700–3,900 tok/s/GPU on 4 GPUs. Rack-scale disaggregation (GB200/GB300 NVL72) reaches 11k–12.6k tok/s/GPU. I found no 32k/1k fixed-shape sweeps for these models. 1k/1k data exists only for GLM-5 (third-party) and DeepSeek R1 (proxy).

### Cited Findings

**GLM-5 (744B total / ~40B active), 8k/1k, SGLang v0.5.12, single node, aggregated, InferenceX (published 2026-05-26, data as of 2026-05-25)** — [InferenceX GLM-5 B200 vs H200](https://inferencex.semianalysis.com/blog/b200-glm5-nvfp4-vs-h200-fp8-3-6x-perf-per-dollar)
- MTP config: EAGLE, `--speculative-num-steps 3 --speculative-eagle-topk 1 --speculative-num-draft-tokens 4`, `SGLANG_ENABLE_SPEC_V2=1`. Checkpoints: `zai-org/GLM-5-FP8` and `nvidia/GLM-5-NVFP4`. Parallelism is TP only; EP and DP-attention are not reported.
- H200 FP8 + MTP, TP=8 (8 GPUs). Format is tok/s/GPU at tok/s/user (TPOT): conc 4: 347.9 @ 84.49 (11.84 ms); conc 8: 489.7 @ 59.82; conc 16: 675.9 @ 39.64; conc 32: 851.9 @ 24.90 (40.16 ms); **conc 64: 847.2 @ 20.80 (48.08 ms)**.
- B200 FP8 + MTP, TP=8 (8 GPUs): conc 4: 417.0 @ 100.85; conc 8: 650.1 @ 77.82; conc 16: 952.7 @ 56.93; conc 32: 1,296.8 @ 38.16; **conc 64: 1,619.3 @ 23.56 (42.45 ms); conc 128: 1,929.5 @ 13.78 (72.59 ms)**; conc 256: 1,947.3 @ 11.88.
- B200 NVFP4 + MTP, TP=4 (4 GPUs): conc 4: 1,038.7 @ 121.22; conc 8: 1,523.5 @ 94.53; conc 16: 2,228.1 @ 66.27; conc 32: 3,037.3 @ 43.99; **conc 64: 3,739.7 @ 26.78 (37.33 ms); conc 128: 4,115.5 @ 17.63 (56.73 ms)**; conc 256: 4,090.7 @ 17.37. With TP=8, conc 4 gives 579.2 @ 140.08.
- TCO basis: H200 $1.41/GPU/hr and B200 $1.95/GPU/hr. Specs: H200 4.8 TB/s and 141 GB; B200 8.0 TB/s and 180 GB.

**GLM-5 FP8, 8k/1k, SGLang v0.5.12, MI355X vs B200 (published 2026-05-25, run 2026-05-20)** — [InferenceX MI355X GLM-5](https://inferencex.semianalysis.com/blog/mi355x-glm5-fp8-sglang-40-cheaper-than-b200)
- MI355X FP8 + MTP, TP=4 (4 GPUs), container `lmsysorg/sglang-rocm:v0.5.12-rocm720-mi35x-20260517`: conc 4: 625.5 @ 76.80; conc 8: 911.7 @ 54.59; conc 16: 1,208.1 @ 35.82; conc 32: 1,707.4 @ 24.83; **conc 64: 1,895.0 @ 18.19 (54.99 ms); conc 128: 1,911.7 @ 18.05 (55.40 ms)**.
- MI355X FP8 + MTP, TP=8: conc 4: 373.4 @ 90.43; conc 8: 534.2 @ 65.05.
- B200 FP8 **no MTP**, TP=8: conc 4: 231.3 @ 54.25; conc 16: 613.2 @ 36.65; conc 32: 933.7 @ 27.47; **conc 64: 1,291.8 @ 18.42; conc 128: 1,669.1 @ 11.87**; conc 256: 1,746.1 @ 10.72.
- MI355X FP8 **no MTP**, TP=4: conc 4: 358.8 @ 42.03; conc 16: 870.8 @ 25.86; conc 32: 1,274.0 @ 18.57; **conc 64: 1,660.1 @ 11.83; conc 128: 2,071.4 @ 7.33**; conc 256: 2,189.4 @ 6.69.
- MI355X TCO basis: $1.48/GPU/hr. No disaggregated or wide-EP GLM-5 recipe exists for MI355X.

**GLM-5-FP8, 1k/1k random, 8× B200 and 8× H200, SGLang image `lmsysorg/sglang:glm5-blackwell`, third-party (2026-02-13)** — [BenHamm gist](https://gist.github.com/BenHamm/dcd09f595fef141567a39582f502cef4)
- Conc 100 (1,000 prompts), B200 + EAGLE: 1,370 output tok/s per node (171.3 per GPU), 2,747 total tok/s, TPOT mean 34.46 ms, median ITL 15.36 ms, **TTFT mean 18,239 ms**, accept length 3.52.
- Conc 100, B200 without EAGLE: 1,233 output tok/s per node (154.2 per GPU), TPOT 77.09 ms, TTFT mean 693 ms.
- Conc 100, H200 + EAGLE (cookbook recipe): 1,215 output tok/s per node (151.9 per GPU), TPOT 38.7 ms, TTFT mean 8,690 ms.
- Conc 1: B200 without EAGLE gives 48 tok/s (TPOT 20.22 ms, TTFT 260 ms). B200 + EAGLE gives 112 tok/s (TPOT 7.69 ms). H200 + EAGLE gives 118 tok/s (TPOT 7.54 ms, TTFT 291 ms).

**GLM-5.1-FP8, 8k/2k, 512 prompts, conc 32, 1× HGX B200 (8 GPUs), TP=8 (date not stated; 2026 page)** — [Lambda GLM-5.1](https://lambda.ai/inference-models/zai-org/glm-5.1)
- SGLang v0.5.10 with EAGLE (3 steps, topk 1, 4 draft tokens): 1,345.44 output tok/s, 42.04 tok/s/user, 6,727.19 total tok/s, TTFT mean 1,072.61 ms (P99 14,237.85 ms), TPOT 22.83 ms.
- vLLM v0.19.0 with MTP (3 speculative tokens): 1,265.45 output tok/s, 39.55 tok/s/user, 6,327.24 total tok/s, TTFT mean 1,316.86 ms, TPOT 24.34 ms.

**GLM-5.3 (744B), B200 FP4 (InferenceX compare page; engine, MTP and date not shown; scenario labelled "8K/1K (deprecated)", default selection "agentic-traces · fp4")** — [InferenceX GLM-5.3 B200 vs H200](https://inferencex.semianalysis.com/compare/glm-5-3-b200-vs-h200)
- 138 tok/s/user: 10,091 tok/s/chip, $0.05/M, conc ~34. 192 tok/s/user: 6,951 tok/s/chip, conc ~8. 247 tok/s/user: 4,541 tok/s/chip, $0.11/M, conc ~5. H200 is unmeasured.
- An older GLM-5/5.1 compare snapshot (about 4 months old at search time) gave 82 tok/s/user: B200 275 tok/s/chip ($1.75/M) vs H200 132 ($2.54/M) — [InferenceX GLM-5.1 B200 vs H200](https://inferencex.semianalysis.com/compare/glm-5-1-b200-vs-h200) (search snippet only).

**Kimi K2.5/K2.6 (1T / 32B active), 8k/1k, vLLM v0.21.0, single 8-GPU node, InferenceX (published 2026-05-26, measured 2026-05-19; no speculative decoding reported)** — [InferenceX Kimi B200 vs H200](https://inferencex.semianalysis.com/blog/b200-nvfp4-vs-h200-int4-kimi-k2-vllm-perf-per-dollar)
- H200 INT4, TP=8: conc 4: 384.4 @ 91.18; conc 8: 590.2 @ 70.28; conc 16: 797.9 @ 46.64; conc 32: 990.9 @ 28.86; **conc 64: 1,174.5 @ 16.67 (59.98 ms)**.
- B200 INT4, TP=8: conc 4: 446.7 @ 104.36; conc 16: 969.4 @ 59.21; conc 32: 1,351.4 @ 40.48; **conc 64: 1,790.7 @ 26.01 (38.45 ms)**.
- B200 NVFP4, TP=4: conc 4: 532.0 @ 125.51 (TP=8 gives 947.4 @ 111.08); conc 8: 1,537.2 @ 90.66; conc 16: 2,318.7 @ 67.40; conc 32: 3,202.7 @ 46.83; **conc 64: 3,879.3 @ 32.19 (31.07 ms)**.
- The article says the K2.5 and K2.6 architectures are identical. It does not say which checkpoint was used for each run.

**Kimi K2.5 NVFP4, 8k/1k, no speculative decoding (published 2026-04-23)** — [InferenceX GB200 Kimi K2.5](https://inferencex.semianalysis.com/blog/gb200-nvl72-kimi-k2-5-vllm-wide-ep-3x-vs-b200)
- B200 vLLM (run 2026-03-27), 16-GPU pool with prefill and decode both at TP4/EP4: conc 4: 878 @ 101.8; conc 16: 2,286 @ 66.3; conc 32: 3,108 @ 45.0; **conc 64: 4,021 @ 29.3 (34.1 ms)**.
- GB200 NVL72 Dynamo vLLM 0.18.0, disaggregated with NIXL (run 2026-04-07), prefill on 4 GPUs at TP4/EP4: conc 32: 1,230 @ 96.9; **conc 128: 2,173 @ 77.9** (decode TP4/EP4); conc 512: 6,885 @ 48.8 (TP16/EP16); conc 1,024: 7,565 @ 46.2; conc 2,048: **12,587 @ 23.2** (TP8/EP8); conc 4,096: 12,576 @ 36.3 (TP16/EP16).

**Kimi K2.6, 8k/2k, 512 prompts, conc 32, 1× HGX B200, vLLM cu130-nightly, INT4 (QAT) + BF16, FP8 KV, TP=8, EAGLE-3 with 3 tokens (`lightseekorg/kimi-k2.6-eagle3`), prefix caching off** — [Lambda Kimi K2.6](https://lambda.ai/inference-models/moonshotai/kimi-k2.6)
- 1,408 output tok/s per node, 44 tok/s/user, 7,046 total tok/s, TTFT mean 2,264.48 ms (P99 32,176.03 ms), TPOT mean 21.14 ms.

**DeepSeek V4 Pro (1.6T / 49B active), MI355X, SGLang `amd/deepseek_v4` branch, 8k/1k, TP=8, single node (published 2026-05-26; MTP not mentioned)** — [InferenceX MI355X DSv4-Pro](https://inferencex.semianalysis.com/blog/mi355x-deepseek-v4-pro-sglang-110x-in-26-days)
- 2026-05-21 run (FP4, SGLang v0.5.12, Triton attention, FlyDSL MoE): conc 1: 59.2 @ 57.06; conc 8: 348.2 @ 41.78; conc 16: 561.3 @ 33.37; conc 32: 811.7 @ 23.99; **conc 64: 959.6 @ 16.79 (59.56 ms); conc 128: 1,556.0 @ 13.76 (72.69 ms)**; conc 256 (DP attention): 2,256.1 @ 9.37; conc 512: 1,814.4 @ 5.59.
- Day 0 (2026-04-25, FP8, non-native checkpoint): conc 64 gave 67.4 @ 0.93. The article reports a 110.5x gain over 26 days.
- The article says the B200 SGLang curve sits about **5x above** MI355X in the 15–30 tok/s/user band, with a further ~1.5x estimated for PD-disaggregated B200. It gives no absolute B200 values.

**DeepSeek V4 Pro, HGX B200, vLLM `latest-cu129`, FP4 experts + FP8, FP8 KV, DP=8 + EP, MTP 2 tokens (~33% acceptance), 8k/2k, conc 32, 512 prompts** — [Lambda DSv4 Pro](https://lambda.ai/inference-models/deepseek-ai/deepseek-v4-pro)
- 911.92 output tok/s per node, 28.50 tok/s/user, 4,561.38 total tok/s, TTFT mean 1,186.15 ms (P99 7,121 ms), TPOT mean 33.36 ms, ITL mean 55.79 ms.

**DeepSeek V4 Pro, GB300 and B300 (Blackwell Ultra), SGLang (PyTorch blog, 2026-06-23; data from the InferenceX dashboard)** — [PyTorch/SGLang GB300 blog](https://pytorch.org/blog/serving-deepseek-v4-on-gb300-with-sglang-5x-higher-throughput-at-the-same-interactivity-since-day-0/)
- GB300 disaggregated (dynamo-sglang, FP4, 8k/1k): the June 2026 MTP curve gives **~11,200 tok/s/GPU at ~50 tok/s/user**. The Day-0 (April 2026) no-MTP curve gave ~2,200. Relative to Day 0, the June curves give 2.1x at 40 tok/s/user (no MTP) and 2.6x at 80 tok/s/user (MTP).
- Blackwell Ultra aggregated 8k/1k: 2.91x at 30 tok/s/user (no MTP) and 2.85x at 90 tok/s/user (MTP) vs Day 0. No-MTP peak throughput is >6x Day 0. The blog gives no absolute values.
- Example recipe: `disagg-gb300-10p1d-dep4-dep32-18-c2500.yaml` (10 prefill workers at DEP4 and 1 decode worker at DEP32).

**DeepSeek V4 Pro, Day 0 to Day 43 (published 2026-06-09)** — [InferenceX DSv4 Day 0–43](https://inferencex.semianalysis.com/blog/deepseekv4-16t-day-0-to-day-43-performance)
- GB300 NVL72: **$0.156 per million output tokens at 50 tok/s/user, MTP on, 8k/1k**.
- B200 vLLM: about 300,000 tok/s/MW at 50 tok/s/user on Day 0, rising to nearly 500,000 by June 5. The B200 all-in power assumption is ~2.17 kW/GPU.
- B300 SGLang (DeepGEMM MegaMoE): 3x improvement in under a week by switching EP8 to EP4. GB300 SGLang May 20 run: decode EP=16 with 4–12 prefill workers per decode worker, concurrency up to 21,504.
- B200 and B300 perform similarly. TRT-LLM is better at lower interactivity on B200.
- An AMD article (2026-06-10) says MI355X with ATOM matches or beats B200 and B300 running Dynamo vLLM on per-GPU throughput across most of the interactivity range. This comes from an unmerged InferenceX PR — [AMD article](https://www.amd.com/en/developer/resources/technical-articles/2026/amd-instinct-mi355x-gpu-sets-a-new-bar-for-deepseek-inference.html). The fetch timed out, so this is from a search snippet only.

**[PROXY] DeepSeek R1-0528 (671B / 37B active), FP4, 1k/1k, Dynamo TRT-LLM, MTP on, disaggregated, multi-node (published 2026-05-23, measured 2026-05-22)** — [InferenceX GB200 vs B200 R1](https://inferencex.semianalysis.com/blog/gb200-nvl72-vs-b200-disagg-deepseek-r1-fp4-dynamo-trt)
- B200 (prefill 4 GPUs TP4, decode 40 GPUs EP8): conc 45: 369.9 @ 191.18; **conc 90: 577.3 @ 150.56 (6.64 ms)**; conc 180: 897.9 @ 126.42; conc 875: 2,832.9 @ 101.79; conc 1,214 (decode 16 GPUs): 7,111.4 @ 74.04; conc 4,968: 9,660.7 @ 56.35; conc 10,860: 12,515.7 @ 21.34.
- GB200 NVL72: conc 48: 363.3 @ 207.30; conc 180 (decode EP32): 1,149.1 @ 164.37; conc 2,253: 7,698.0 @ 90.99; conc 4,301: 12,659.7 @ 43.29; conc 16,130: 14,659.4 @ 17.82.
- Iso-interactivity, GB200 vs B200: 25 tok/s/user: 14,125 vs 12,292 (1.15x). 45: 12,508 vs 10,853. 90: 7,796 vs 4,512 (1.73x). 125: 4,130 vs 941 (4.39x).

**[PROXY] DeepSeek R1, 8k/1k, InferenceX live ranking at 50 tok/s/user (newest result 2026-10-13)** — [InferenceX ranking R1](https://inferencex.semianalysis.com/rankings/fastest-gpu-for-deepseek-r1)
- B200 FP4 SGLang: 4,610 tok/s/GPU ($0.10/M). GB200 NVL72 FP8 Dynamo SGLang: 2,697 ($0.19). GB300 NVL72 FP8 Dynamo SGLang: 2,438 ($0.26). B300 FP8 SGLang: 1,779 ($0.35). MI355X FP8 SGLang: 1,608 ($0.26). H100, H200, MI300X and MI325X are not ranked.

**[PROXY] DeepSeek R1-0528, 8k/1k, H100 vs MI300X (InferenceX compare; page says fp8 in the intro but FP4 in the config; engine and date not shown)** — [InferenceX H100 vs MI300X](https://inferencex.semianalysis.com/compare/deepseek-r1-h100-vs-mi300x)
- 28 tok/s/user: H100 850.1 tok/s/chip (conc ~154, $0.382/M) vs MI300X 656.4 (conc ~22, $0.402/M).
- 36 tok/s/user: H100 850.1 vs MI300X 532.4 ($0.496/M).
- 44 tok/s/user: H100 760.9 (conc ~136) vs MI300X 363.7 (conc ~8).
- TCO table ($/chip/hr): H100 1.17, H200 1.22, B200 1.73, B300 2.26, GB200 1.86, GB300 2.31, MI300X 0.95, MI325X 1.1, MI355X 1.5, RTX6000PRO 0.68 (SemiAnalysis July 2026 survey).

**[PROXY] DeepSeek V3/R1 on 96× H100 (12 nodes), SGLang PD disaggregation + large EP (2025-05-05)** — [LMSYS large-scale EP](https://lmsys.org/blog/2025-05-05-large-scale-ep/)
- 52.3k input tok/s and 22.3k output tok/s per node for 2,000-token inputs.
- Decode: 9 nodes at EP72, 22,282 tok/s per node at batch 256 (5.2x over TP16).
- Prefill: 4 nodes at EP32, 57,674 / 54,543 / 50,302 tok/s per node for 1K / 2K / 4K prompts.
- TTFT 2–5 s, ITL ~100 ms. Cost estimate $0.20 per 1M output tokens.

**[PROXY] DeepSeek R1 on GB200 NVL72, SGLang (2025)** — about 26k input and 13k output tok/s per GPU (prefill and decode respectively) with FP8 attention, NVFP4 MoE and PD-disaggregated EP — [LMSYS Oct 2025](https://www.lmsys.org/blog/2025-10-14-sa-inference-max). 7,583 decode tok/s/GPU at 2k input, 2.7x H100 — [LMSYS Jun 2025](https://www.lmsys.org/blog/2025-06-16-gb200-part-1). Both are from search excerpts only.

**[PROXY] DeepSeek V3.2 on GB300, vLLM v0.14.1 (2026-02-13)** — NVFP4 TP2 prefill-only at ISL 2k gives 7,360 tokens/GPU/s. Mixed ISL 2k / OSL 1k gives 2,816 TGS. R1 NVFP4 EP2 gives 22,476 TGS prefill-only and 3,072 mixed. GB300 shows 8x H200 per-GPU prefill — [vLLM V3.2 GB300 blog](https://vllm.ai/blog/2026-02-13-gb300-deepseek).

**[PROXY] DeepSeek V3.2 on Hopper, SGLang cookbook, 2 nodes, 1k/1k:** 4,948 tok/s raw and 6,842 tok/s with DP2 + MTP — [SGLang V3.2 cookbook](https://docs.sglang.io/cookbook/autoregressive/DeepSeek/DeepSeek-V3_2) (search snippet only).

**Kimi K2.6 on MI350X, SGLang cookbook:** latency run at conc 16 gives 258.18 output tok/s — [SGLang Kimi-K2.6 cookbook](https://docs.sglang.io/cookbook/autoregressive/Moonshotai/Kimi-K2.6) (search snippet only).

### Inferences
- **The InferenceX tok/s/GPU metric counts input + output tokens.** Check with GLM-5 B200 FP8 MTP at conc 64. If the metric were output-only, 1,619.3 tok/s/GPU × 8 GPUs ÷ 64 users = 202 tok/s/user, which is impossible next to the reported 23.56. As total tokens, 1,619.3 ÷ 9 × 8 ÷ 64 = 22.5 tok/s/user. That is just under 1/TPOT, and the gap is explained by TTFT. Kimi B200 NVFP4 at conc 64 gives the same result: 3,879 ÷ 9 × 4 ÷ 64 = 26.9, vs 32.19 for 1/TPOT. **For a cost model, output tok/s/GPU ≈ InferenceX value ÷ 9 at 8k/1k and ÷ 2 at 1k/1k.**
  - GLM-5 H200 FP8 MTP, conc 64: ≈ 94 output tok/s/GPU.
  - GLM-5 B200 NVFP4, conc 64: ≈ 416.
  - Kimi H200 INT4, conc 64: ≈ 130.
  - DSv4 Pro MI355X FP4, conc 128: ≈ 173.
  - DSv4 Pro GB300 disaggregated with MTP at 50 tok/s/user: ≈ 1,244.
- Converting the DSv4 Pro B200 vLLM tok/s/MW figures with the article's 2.17 kW/GPU gives ≈ 650 tok/s/GPU at 50 tok/s/user on Day 0 and ≈ 1,085 tok/s/GPU on June 5 (8k/1k, total tokens).
- The Lambda conc-32 8k/2k runs agree with InferenceX on output per GPU. GLM-5.1 SGLang gives 168 output tok/s/GPU. InferenceX GLM-5 B200 FP8 at conc 32 gives 1,296.8 ÷ 9 ≈ 144.
- H100 (8× 80 GB = 640 GB) cannot hold GLM-5-FP8 (~744 GB of weights) or the DSv4 Pro checkpoint (~960 GB, per the vLLM recipe) on one node. That explains why no single-node H100 data exists for these models. They need 16× H100 or lower precision.
- **HBM-bandwidth efficiency (rough derivations, not published):**
  - GLM-5 FP8 single stream on B200 TP8 without EAGLE (TPOT 20.22 ms, ~40B active ≈ 40 GB per token ÷ 8 GPUs ≈ 5 GB/GPU) gives ≈ 250 GB/s per GPU, about 3% of 8 TB/s.
  - DSv4 Pro single stream on B200 TP8 (199 tok/s, TPOT ≈ 5 ms) gives ≈ 9% under an assumed ~0.6 bytes/param for mixed FP4/FP8 at 49B active. It is unclear whether speculation was on.
  - Batch-1 decode on 8-GPU TP is therefore dominated by communication and launch overhead, not by HBM bandwidth. A pure bandwidth model will badly overestimate single-user speed.
  - The only published bandwidth figure is kernel-level: the DSv4 Flash Compressor reaches "up to 80% of peak memory bandwidth on H200" — [LMSYS DSv4 Day 0](https://www.lmsys.org/blog/2026-04-25-deepseek-v4/).

### Gaps
- No fixed-shape 32k/1k sweeps were found for GLM-5.x, Kimi K2.x or DSv4 Pro. The AgentX agentic traces (ISL p50 88k) are the only long-input throughput data.
- No 1k/1k InferenceX data was found for GLM-5, Kimi or DSv4. InferenceX appears to have deprecated 1k/1k for these models.
- No GLM-5.x, Kimi K2.x or DSv4 Pro data was found for H100, MI300X or MI325X.
- MI325X appears only in a 2025 InferenceMAX summary snippet: H200 SGLang has "~40% lower latency than MI325X" for DeepSeek FP8 — [SemiAnalysis InferenceMAX](https://newsletter.semianalysis.com/p/inferencemax-open-source-inference).
- No absolute B200 or B300 SGLang tok/s values for DSv4 Pro at 8k/1k were in text form; they appear only as chart images.
- The data has no explicit concurrency-90 points except DeepSeek R1 B200 disaggregated (conc 90).
- Kimi K2 Thinking: no 2026 per-GPU measurements found. NVIDIA's "10x on GB200 NVL72 vs H200" claim (Dec 2025) is known only from secondary coverage — [Wallstreetcn](https://wallstreetcn.com/articles/3760723). A Simplismart blog is titled "Deploying Kimi K2 Thinking at 173 Tokens per Second" — [Simplismart](https://simplismart.ai/blog/deploying-kimi-k2-thinking). I did not read its body.

---

## Q2. What InferenceX / InferenceMAX publishes at ~15–20, ~30 and ~50 tok/s/user

### Takeaway
At about 50 tok/s/user on 8k/1k, Kimi K2.6 FP4 ranges from 2,831 (MI355X) to 5,601 (GB300 NVL72) total tok/s/GPU. DeepSeek V4 Pro reaches ~11,200 on GB300 disaggregated with MTP. GLM-5 NVFP4 on B200 interpolates to ≈ 2,800 at 50 tok/s/user. At 15–20 tok/s/user, single-node FP8/INT4 nodes sit at ~850–1,900 tok/s/GPU, and NVFP4 B200 sits at ~4,100. InferenceX's agentic (AgentX) lane reports much larger "total token" figures because cached input tokens count, for example DSv4 Pro B300 at 71,955 tok/s/GPU at 50 tok/s/user.

### Cited Findings
- **GLM-5 iso-interactivity cost ($/M total tokens), 8k/1k** — [InferenceX GLM-5](https://inferencex.semianalysis.com/blog/b200-glm5-nvfp4-vs-h200-fp8-3-6x-perf-per-dollar)

  | tok/s/user | H200 FP8 MTP | B200 FP8 MTP | B200 NVFP4 MTP |
  |---|---|---|---|
  | 25 | $0.46 | $0.34 | $0.14 |
  | 30 | $0.50 | $0.37 | $0.15 |
  | 50 | $0.69 | $0.51 | $0.19 |
  | 80 | $1.06 | $0.87 | $0.29 |

  B200 NVFP4 peaks above 4,000 tok/s/GPU at 18 tok/s/user. Decomposed lifts: B200 FP8 vs H200 FP8 is 1.36x at 50 tok/s/user and 1.22x at 80. NVFP4 vs FP8 on B200 is 2.98x at 80 tok/s/user.
- **GLM-5 MI355X vs B200, MTP, $/M** — 18 tok/s/user: B200 $0.30 vs MI355X $0.22 (1.41x). 24: $0.34 vs $0.24. 35: $0.40 vs $0.34. 55: $0.55 vs $0.45. 90: $1.08 vs $1.10. Without MTP: 15 tok/s/user gives $0.37 vs $0.28, and 30 gives $0.66 vs $0.58 — [InferenceX MI355X GLM-5](https://inferencex.semianalysis.com/blog/mi355x-glm5-fp8-sglang-40-cheaper-than-b200)
- **Kimi K2.5/K2.6 iso-interactivity $/M, 8k/1k, vLLM v0.21.0** — 32 tok/s/user: H200 INT4 $0.413, B200 INT4 $0.343, B200 NVFP4 $0.140. 50: $0.511 / $0.477 / $0.177. 90: $0.996 / $0.927 / $0.347. B200 INT4 at 26 tok/s/user gives 1,791 tok/s/GPU, vs an interpolated 1,055 for H200 INT4 — [InferenceX Kimi](https://inferencex.semianalysis.com/blog/b200-nvfp4-vs-h200-int4-kimi-k2-vllm-perf-per-dollar)
- **Kimi K2.6 ranking at 50 tok/s/user, 8k/1k, FP4 (newest result 2026-08-07)** — GB300 NVL72 Dynamo vLLM 5,601 tok/s/GPU ($0.11/M). GB200 NVL72 Dynamo vLLM 4,594 ($0.11). B300 vLLM 3,504 ($0.18). B200 Dynamo vLLM 3,449 ($0.14). MI355X vLLM 2,831 ($0.15) — [InferenceX Kimi ranking](https://inferencex.semianalysis.com/rankings/fastest-gpu-for-kimi-k26)
- **Kimi K2.5/K2.6/K2.7-Code, B200 vs B300, 8k/1k FP4 (interpolated; engines include B300 vLLM, B200 Dynamo TRT-LLM and Dynamo vLLM)** — 50 tok/s/user: B200 8,178.4 tok/s/chip (conc ~323, $0.059/M) vs B300 3,504.2 (conc ~32, $0.179/M). 91: 1,745.8 vs 1,962.6. 132: 961.9 vs 856.6 — [InferenceX Kimi B200 vs B300](https://inferencex.semianalysis.com/compare/kimi-k26-b200-vs-b300). This conflicts with the ranking page's B200 figure of 3,449 at 50 tok/s/user. The likely cause is a different engine or recipe selection (multi-node Dynamo TRT-LLM vs Dynamo vLLM) or a different date. The page also notes that disaggregated configs "report per decode or prefill chip rather than per total chip".
- **Kimi K2.6, B200 vs MI355X, 8k/1k FP4** — 38 tok/s/user: B200 12,043 tok/s/chip (conc ~736, $0.04/M) vs MI355X 4,004 (conc ~102, $0.10/M). 67: 3,662 vs 2,493. 95: 1,643 vs 1,739. Footnote: ATOM on MI355X "has not yet served production tokens" — [InferenceX Kimi B200 vs MI355X](https://inferencex.semianalysis.com/compare/kimi-k26-b200-vs-mi355x)
- **DeepSeek V4 Pro MI355X iso-interactivity (tok/s/GPU, 05-21 run)** — 10 tok/s/user: 2,162. 15: 1,272. 17: 951. 20: 876. 25: 788. 30: 653. 40: 393. 50: 140 — [InferenceX MI355X DSv4](https://inferencex.semianalysis.com/blog/mi355x-deepseek-v4-pro-sglang-110x-in-26-days)
- **DeepSeek V4 Pro GB300 disaggregated with MTP:** ~11,200 tok/s/GPU at ~50 tok/s/user — [PyTorch blog](https://pytorch.org/blog/serving-deepseek-v4-on-gb300-with-sglang-5x-higher-throughput-at-the-same-interactivity-since-day-0/)
- **DeepSeek V4 Pro AgentX (agentic coding) ranking at 50 tok/s/user (newest result 2026-10-15)** — B300 vLLM FP4 71,955 tok/s/GPU ($0.009/M). B200 vLLM FP4 65,134 ($0.007/M). MI355X MoRI SGLang FP4 37,438 ($0.011/M) — [InferenceX DSv4 ranking](https://inferencex.semianalysis.com/rankings/fastest-gpu-for-deepseek-v4)
- **InferenceX overview, $/M total tokens, mostly AgentX agentic (run dates 2026):**
  - DSv4 Pro 0813: B200 vLLM FP4 $0.007 (09-19); B300 $0.009 (09-28); MI355X MoRI SGLang FP4 8P+8D disaggregated $0.011 (10-04).
  - GLM-5.2/5.3: MI355X SGLang FP4 with MTP $0.023 (10-06); B300 Dynamo SGLang FP4 with MTP, multi-node, $0.018 (10-14).
  - No GLM-5.x B200, GB200 or GB300 result exists at that point.
  - Source: [InferenceX overview](https://inferencex.semianalysis.com/overview)
- **GLM-5.3, AgentX:** at 150 tok/s/user p90 interactivity, NVIDIA has "up to 5x better cost efficiency than AMD SGLang" — [AgentX v3 article](https://inferencex.semianalysis.com/blog/agentx-inferencexv3-does-cuda-moat) (2026-08-24)
- **[PROXY] DeepSeek R1 at 50 tok/s/user (8k/1k):** B200 FP4 SGLang 4,610, GB200 FP8 2,697, GB300 FP8 2,438, B300 FP8 1,779, MI355X FP8 1,608 — [InferenceX R1 ranking](https://inferencex.semianalysis.com/rankings/fastest-gpu-for-deepseek-r1)
- **[PROXY] DeepSeek R1 1k/1k disaggregated with MTP** — 25 tok/s/user: GB200 14,125 vs B200 12,292. 45: 12,508 vs 10,853 — [InferenceX GB200 vs B200](https://inferencex.semianalysis.com/blog/gb200-nvl72-vs-b200-disagg-deepseek-r1-fp4-dynamo-trt)

### Inferences
- Interpolating the GLM-5 B200 NVFP4 TP4 table gives ≈ 2,820 tok/s/GPU total (≈ 313 output) at ~50 tok/s/user, and ≈ 3,600 tok/s/GPU at ~30 tok/s/user. The interpolation runs between conc 16 (66 tok/s/user) and conc 32 (44), and between conc 32 and conc 64 (27). The published $0.19/M at 50 tok/s/user implies 1.95e6 / (3600 × 0.19) ≈ 2,850 tok/s/GPU, which agrees.
- At ~50 tok/s/user, GLM-5 H200 FP8 MTP interpolates to ≈ 580 tok/s/GPU (≈ 64 output) and GLM-5 B200 FP8 MTP to ≈ 1,080 (≈ 120 output).
- **AgentX "tok/s/GPU" is dominated by cached prefix tokens.** With ISL p50 of 88k and OSL p50 of 413 (see Q6), only about 0.5% of counted tokens are output. The B300 DSv4 Pro figure of 71,955 tok/s/GPU therefore implies only a few hundred output tok/s/GPU. Use AgentX $/M figures only with the same input/cached/output mix.
- InferenceX values move a lot over weeks: DSv4 Pro moved 5x on GB300 and 110x on MI355X between April and June. The B200 Kimi figure at 50 tok/s/user disagrees by 2.4x between two pages. Pin a date and engine when calibrating.

### Gaps
- The rankings page for GLM-5 returned 404. No cross-GPU GLM-5.x table at 50 tok/s/user was retrieved beyond the overview's $/M.
- The DSv4 model page and the compare pages show many values only in charts. Per-date snapshots were not accessible through the date selector.
- Kimi K2.7-Code is bundled with K2.5/K2.6 ("same architecture") in InferenceX. No separate K2.7-Code measurements were found.

---

## Q3. Long-context behaviour (prefill at 32k/128k/256k/1M; decode degradation; DSA, CSA/HCA)

### Takeaway
DeepSeek V4's CSA/HCA keeps decode almost flat out to ~1M context: under 10% drop from 4K to 900K. Its KV is ~9.6 KB/token in bf16, about 8.7x smaller than a V3.2-style stack. V3.2-style DSA, also used by GLM-5, adds prefill overhead: a DSA layer takes 2.7x the kernel time of MLA, and R1 prefill is ~3x V3.2 at short context. DSA's decode advantage starts at about 10–20k tokens. I found no absolute prefill tok/s at 128k, 256k or 1M for any target model.

### Cited Findings
- **DeepSeek V4 single-batch decode is nearly flat with context.** B200 Pro at TP=8 goes from 199 to 180 tok/s, and H200 Flash at TP=4 from 266 to 240 tok/s, "essentially flat from 4K to 900K" context. The drop is under 10%. Setup: OSL 4096 on a 30K prefix, decode throughput = 1000/TPOT — [LMSYS DSv4 Day 0](https://www.lmsys.org/blog/2026-04-25-deepseek-v4/) (2026-04-25)
- **Compute and KV at 1M context:** V4 Pro needs 27% of V3.2's single-token inference FLOPs and 10% of its KV cache — [arXiv 2606.19348](https://arxiv.org/abs/2606.19348). V4 Flash needs 10% of the FLOPs and 7% of the KV — [search summary of the V4 paper](https://arxiv.org/pdf/2606.19348).
- **KV size:** "9.62 GiB KV cache per sequence at 1M context" with bf16, vs 83.9 GiB for a V3.2-style 61-layer stack (~8.7x). The FP4 indexer cache plus FP8 attention cache gives about a further 2x reduction — [vLLM DSv4 blog](https://vllm.ai/blog/2026-04-24-deepseek-v4)
- **Attention parameters:** 61 layers, 30 `c4a` and 31 `c128a`. Sliding window of 128 tokens. Top-k is 512 for c4a and 8,192 for c128a (V3.2 uses 2,048). At 1M context, c4a holds ~250k compressed tokens and c128a at most 8k — [vLLM DSv4 blog](https://vllm.ai/blog/2026-04-24-deepseek-v4). HCA compresses m′ = 128 tokens per entry and CSA m = 4 with a lightning indexer. KV is reduced ~50x at 1M context vs the baseline — [InferenceX DSv4 Day 0–43](https://inferencex.semianalysis.com/blog/deepseekv4-16t-day-0-to-day-43-performance)
- **H200 context limit:** context is capped at `--max-model-len 800000` because replicated dense parameters reduce KV headroom — [vLLM recipes DSv4 Pro](https://recipes.vllm.ai/deepseek-ai/DeepSeek-V4-Pro)
- **[PROXY] V3.2 DSA vs MLA on GB300, vLLM v0.14.1:**
  - A DSA layer step takes 2.7x the kernel time of an MLA layer.
  - R1 prefill is ~3x V3.2 prefill at ISL 2k.
  - "DSA overtakes MLA between 10k and 20k tokens" in decode TPOT. MLA's TPOT slope vs context is about 6x steeper.
  - MTP-1 acceptance is >80%, but MTP is beneficial only when context is not long and concurrency is ≤256.
  - Source: [vLLM V3.2 GB300](https://vllm.ai/blog/2026-02-13-gb300-deepseek)
- **[PROXY]** An SGLang issue reports that V3.2 prefill throughput in PD-disaggregation mode is ~1/3 of V3.1 — [SGLang issue #14498](https://github.com/sgl-project/sglang/issues/14498) (search snippet; ~317 days old).
- **DeepSeek V4.1 Flash (proxy successor, vLLM, 2026-10-07):**
  - Long-context prefill is 1.43x faster at 512K and 2x faster at 1M after optimizations.
  - Sparse MQA logits are 14–23x faster per layer at 512K on GB300, giving a 3–6% end-to-end decode gain on 4× GB300.
  - Global KV is ~890 bytes/token (FP4).
  - Active parameters are 16B in decode and 8B in prefill.
  - Source: [vLLM V4.1 Flash blog](https://vllm.ai/blog/2026-10-07-deepseek-v41-flash)
- **HiSparse (CPU-offloaded C4 KV) for DSv4:** improves long-context capacity and throughput "by up to 3x". The chart is for DSv4 Flash on 2× B200 at 200K input / 20K output — [LMSYS DSv4 Day 0](https://www.lmsys.org/blog/2026-04-25-deepseek-v4/)
- **ATOM prefill context parallelism (AgentX):** 35–43% lower mean TTFT and up to ~49% throughput gain at 64k input — [AgentX v3](https://inferencex.semianalysis.com/blog/agentx-inferencexv3-does-cuda-moat)
- **LMCache:** reloading a 32k-token prefix takes about 0.32 s vs about 2.5 s to recompute — [AgentX v3](https://inferencex.semianalysis.com/blog/agentx-inferencexv3-does-cuda-moat)
- **Modeled, not measured:** RoofLang reports V4 Flash peak decode throughput at 9.6x and 16.7x GLM-5.3 at 64K and 1M context on 64× GB300, and V4 Pro at 5.3x GLM-5.3 at 1M — [RoofLang arXiv 2609.12551](https://arxiv.org/pdf/2609.12551) (search snippet).
- **GLM-5 DSA:** the indexer is skipped in favour of full attention for sequences shorter than K, and the indexer can make sparse attention slower at short context — [Baseten GLM-5](https://www.baseten.co/blog/how-we-built-the-fastest-glm-5-api/). Claims that "128K at roughly half the GPU cost" and "1.5–2x lower attention cost" are not sourced to the paper — [Neurohive](https://neurohive.io/en/news/glm-5-top-1-open-weight-model-for-code-and-text-generation-competing-with-claude-and-gpt-on-agentic-tasks/) (secondary).

### Inferences
- The vLLM figure of 9.62 GiB per 1M-token sequence works out to ≈ 9.9 KB/token in bf16, or ≈ 5 KB/token with FP8/FP4 caches. A V3.2-style stack works out to ≈ 86 KB/token. For a bandwidth model, DSv4's per-token KV read at decode is dominated by top-k selection plus SWA, not by full context length. That is consistent with the flat 4K→900K decode curve.
- The LMCache data point (32k recompute ≈ 2.5 s) implies ≈ 13k prefill tok/s for that model and setup. The model and GPU for this point were not in the excerpt, so treat it as an order-of-magnitude figure only.
- For GLM-5 and V3.2-style DSA, expect higher prefill cost per token than MLA models at short to medium context, and a decode advantage only beyond ~10–20k tokens.

### Gaps
- No absolute prefill tok/s at 32k, 128k, 256k or 1M was found for GLM-5.x, Kimi K2.x or DSv4 Pro on any target GPU. The V4 tech report's text was not accessible beyond the abstract.
- No decode-vs-context curves were found for Kimi K2.x (MLA, 256K context) or GLM-5.x.
- No long-context data was found for H100, MI300X or MI325X.

---

## Q4. MTP / EAGLE speculative-decoding acceptance and speedup

### Takeaway
- GLM-5 EAGLE/MTP with 3 steps reaches an acceptance length of ~3.5. That roughly doubles single-stream speed (48 → 112 tok/s on B200), but gives only +11–25% throughput at conc 64–100, and MTP can lose at high batch.
- Kimi K2.6 EAGLE3 with 3 draft tokens accepts ~2.5–3.2 tokens, about 2x at batch 1.
- DeepSeek V4 Pro MTP measured ~2.5 accept length in SGLang. Acceptance on random-token benchmarks is much lower (e.g., ~33% for MTP-2). The 0813 release ships DSpark with 5–7 draft tokens.

### Cited Findings
- **GLM-5-FP8 (SGLang, EAGLE 3 steps / topk 1 / 4 draft tokens, 1k/1k random):**
  - Accept length 3.48 on H200 and 3.52 on B200.
  - B200 conc 1: 48 → 112 tok/s (TPOT 20.22 → 7.69 ms).
  - B200 conc 100: output 1,233 → 1,370 tok/s (+11%) and TPOT 77.09 → 34.46 ms, but TTFT mean rose from 693 ms to 18,239 ms.
  - Source: [BenHamm gist](https://gist.github.com/BenHamm/dcd09f595fef141567a39582f502cef4) (2026-02-13)
- **GLM-5 FP8, 8k/1k, InferenceX, MTP vs no MTP:**
  - B200 TP8 conc 4: 417.0 vs 231.3 tok/s/GPU (1.80x), and 100.85 vs 54.25 tok/s/user.
  - B200 TP8 conc 64: 1,619.3 vs 1,291.8 (1.25x).
  - B200 TP8 conc 256: 1,947.3 vs 1,746.1 (1.12x).
  - MI355X TP4 conc 64: 1,895.0 vs 1,660.1 (1.14x).
  - **MI355X TP4 conc 128: 1,911.7 vs 2,071.4 (0.92x, MTP loses).**
  - Source: [InferenceX MI355X GLM-5](https://inferencex.semianalysis.com/blog/mi355x-glm5-fp8-sglang-40-cheaper-than-b200)
  - Acceptance rate is not reported there.
- **DeepSeek V4:**
  - SGLang EAGLE (3 steps / topk 1 / 4 draft tokens) gives an accept length of ~2.5 on both Pro and Flash.
  - Another OSS engine with MTP-3 on B200 Pro gave an accept of ~1.19, with per-position accepted tokens of 2,226 / 354 / 55.
  - MTP-1 on H200 Flash gave ~1.92.
  - Source: [LMSYS DSv4 Day 0](https://www.lmsys.org/blog/2026-04-25-deepseek-v4/)
  - An FP8-einsum scaling fix on Blackwell raised the acceptance rate from 0.57 to 0.70 in one run — [PyTorch blog](https://pytorch.org/blog/serving-deepseek-v4-on-gb300-with-sglang-5x-higher-throughput-at-the-same-interactivity-since-day-0/)
  - MI355X MTP worked on all frameworks by week 4 with "multiple-fold" iso-interactivity gains that shrink at high batch. Huawei reports time per decode step, and users multiply by their own acceptance length — [InferenceX DSv4 Day 0–43](https://inferencex.semianalysis.com/blog/deepseekv4-16t-day-0-to-day-43-performance)
  - Lambda: MTP with 2 tokens gave "about 33% acceptance on this workload" (random 8k/2k) — [Lambda DSv4 Pro](https://lambda.ai/inference-models/deepseek-ai/deepseek-v4-pro)
  - The vLLM MI355X agentic lane uses `"synthetic_acceptance_length": 2.49` with 3 tokens. This is a benchmark-comparability device, not a measurement. The 0813 checkpoint auto-enables DSpark with `num_speculative_tokens: 7` and needs vLLM 0.25.0 — [vLLM recipes](https://recipes.vllm.ai/deepseek-ai/DeepSeek-V4-Pro)
  - A secondary source reports DSpark on V4 Pro at accept ~5 and 383.7 tok/s on B300 TP8 at batch size 1 — [Spheron DSpark](https://www.spheron.network/blog/dspark-explained-deepseek-s-new-speculative-decoding-in-vllm/) (unverified, secondary).
  - Tree-structured speculative decoding on V4 Flash gives up to ~18.5% decode throughput — [arXiv 2609.24698](https://arxiv.org/pdf/2609.24698) (search snippet).
- **Kimi K2.6:**
  - NVIDIA EAGLE3 head at draft length 3: 2.62 accepted tokens/step on MT-Bench and 2.67 on the SPEED-Bench qualitative subset — [nvidia/Kimi-K2.6-Eagle3](https://huggingface.co/nvidia/Kimi-K2.6-Eagle3)
  - LightSeek EAGLE3-MLA on vLLM 0.20.0, 8× B200, 3 tokens: MT-Bench 2.62, CEval 2.49, GSM8K 2.99, HumanEval 3.24 — [lightseekorg/kimi-k2.6-eagle3-mla](https://huggingface.co/lightseekorg/kimi-k2.6-eagle3-mla)
  - EAGLE3.1-MLA (for NVFP4): coding 3.03 → 3.01, math 3.30 → 3.40 — [lightseekorg/kimi-k2.6-eagle3.1-mla](https://huggingface.co/lightseekorg/kimi-k2.6-eagle3.1-mla)
  - Batch-1 speedups: DSpark 2.17x at 3 tokens and 2.55x at 7 tokens, vs 2.01x for EAGLE3-MLA — [Novita](https://novita.ai/blog/kimi-k2-dspark-speculative-decoding-throughput/)
  - Lambda claims a 60–90% gain in generation throughput with EAGLE-3 at 3 tokens (vendor claim) — [Lambda Kimi K2.6](https://lambda.ai/inference-models/moonshotai/kimi-k2.6)
- **[PROXY] DeepSeek V3.2 MTP-1 on GB300:** acceptance >80%. It wins only at concurrency ≤256 and short context — [vLLM V3.2 GB300](https://vllm.ai/blog/2026-02-13-gb300-deepseek)
- **[PROXY] DeepSeek V3 decode with simulated MTP on H100:** 17,373 tok/s per node at 4K input, batch 128. TBO raised the MTP case from 12,929 to 17,552 tok/s — [LMSYS large-scale EP](https://lmsys.org/blog/2025-05-05-large-scale-ep/)

### Inferences
- For a cost model, a reasonable range is an MTP throughput multiplier of ~1.8–2.3x at batch 1–4, ~1.1–1.25x at conc 64–256, and ≤1.0x at very high batch. This holds for GLM-5 on MI355X and V3.2 on GB300.
- Interactivity (tok/s/user) gains from MTP are larger and more persistent than the gains in throughput per GPU.
- Random-token benchmarks (Lambda, the gist) can understate (33%) or oddly overstate acceptance compared with real coding traffic. Code workloads (HumanEval 3.24 for Kimi) tend to accept more than chat.

### Gaps
- No measured DSv4 Pro accept length on real coding traces in 2026 was found, and no measured DSpark acceptance from a primary source.
- No GLM-5.x MTP acceptance on InferenceX recipes was found.
- No MTP data was found for H100, MI300X or MI325X.

---

## Q5. Chunked prefill and PD disaggregation impact on decode throughput

### Takeaway
PD disaggregation combined with wide EP is the largest single lever at scale:
- Up to 5x output throughput vs TP on H100 (2025 proxy).
- 3.1x on GB200 NVL72 vs single-node B200 for Kimi K2.5.
- 1.15x at low interactivity and 4.39x at 125 tok/s/user for R1 on GB200 vs B200.
- ~5x lift on GB300 for DSv4 Pro between Day 0 and June 2026, largely from disaggregated topology tuning.

Disaggregation mainly protects TPOT. In aggregated mode, 8k prefill chunks inflate TPOT, and 1P1D at 2–8K ISL becomes prefill-bound. I found no clean chunked-prefill size sweeps.

### Cited Findings
- **[PROXY] SGLang 96× H100, PD + EP:** output throughput up to 5x vs vanilla TP16 on the same resources. Decode on EP72 gives 22,282 tok/s per node at 2K inputs, batch 256 (5.2x vs TP16). TBO gives +27–35% on prefill and +25.5% on decode at 256 tokens/device. EPLB gives 1.49x on prefill and 2.54x on decode. TTFT 2–5 s, ITL ~100 ms — [LMSYS large-scale EP](https://lmsys.org/blog/2025-05-05-large-scale-ep/)
- **[PROXY] Rationale (LMSYS, Oct 2025):** running prefill and decode in one engine causes prefill batches to interrupt decode streams — [LMSYS SA InferenceMAX](https://www.lmsys.org/blog/2025-10-14-sa-inference-max) (search excerpt).
- **Kimi K2.5:** GB200 NVL72 Dynamo vLLM disaggregated peaks at 12,587 tok/s/GPU vs 4,021 for the best B200 recipe (3.13x) — [InferenceX GB200 Kimi](https://inferencex.semianalysis.com/blog/gb200-nvl72-kimi-k2-5-vllm-wide-ep-3x-vs-b200)
- **[PROXY] DeepSeek R1 1k/1k:** GB200 NVL72 vs B200, both disaggregated with MTP: 1.15x at 25 tok/s/user, 1.73x at 90, 4.39x at 125, 0.82x at 275. Decode becomes network-bound at about 75–175 tok/s/user — [InferenceX GB200 vs B200](https://inferencex.semianalysis.com/blog/gb200-nvl72-vs-b200-disagg-deepseek-r1-fp4-dynamo-trt)
- **DeepSeek V4 Pro:**
  - GB200 NVL72 Dynamo vLLM (disaggregated prefill, NIXL) was up to 5x better than B200 at lower interactivity on Day 0 — [InferenceX DSv4 Day 0–43](https://inferencex.semianalysis.com/blog/deepseekv4-16t-day-0-to-day-43-performance)
  - GB300 gains came from tuning the prefill-to-decode ratio, wide-EP plans and SWA KV budgeting. The June 2 gain was attributed to "decode topology rather than kernels or precision". The Dynamo DP-rank alignment fix reduced imbalance — [PyTorch blog](https://pytorch.org/blog/serving-deepseek-v4-on-gb300-with-sglang-5x-higher-throughput-at-the-same-interactivity-since-day-0/)
  - A further ~1.5x is estimated for PD-disaggregated B200 over aggregated; no MI355X disaggregated recipe had shipped by May 2026 — [InferenceX MI355X DSv4](https://inferencex.semianalysis.com/blog/mi355x-deepseek-v4-pro-sglang-110x-in-26-days)
- **[PROXY] V3.2 on GB300, vLLM:** at batch 256, 1P1D TPOT is <60 ms vs >80 ms integrated. At ISL 2K–8K, 1P1D becomes prefill-bound, and 3P1D improves total throughput. Disaggregated per-GPU throughput is "not always highest", but goodput and SLO attainment are better — [vLLM V3.2 GB300](https://vllm.ai/blog/2026-02-13-gb300-deepseek)
- **AgentX engine fixes (2026):**
  - ATOM chunked pipeline-parallel prefill on GLM-5.2 at high load: output throughput doubled, and median TTFT fell from 28.6 s to 8.7 s.
  - SGLang decode-interval change: output throughput +141% and p99 ITL −97.3%, but median TTFT rose from 36.5 s to 59 s.
  - TRT-LLM NIXL KV transfer p99: 26.74 s → 125 ms at conc 5.
  - Dynamo agentic router preset on 8× H200: +8.26% completed-output throughput and −43.1% p95 TTFT.
  - Source: [AgentX v3](https://inferencex.semianalysis.com/blog/agentx-inferencexv3-does-cuda-moat)
- **AMD MoRI SGLang:** 2,436 tok/s/GPU on 24 GPUs for DeepSeek disaggregated inference on MI355X — [LMSYS MoRI](https://www.lmsys.org/blog/2026-05-28-mori/) (search snippet only).
- **vLLM DSv4 Pro GB200 recipe:** prefill uses `--max-num-batched-tokens 8192 --max-num-seqs 64`, and decode uses `--max-num-seqs 8 --max-num-batched-tokens 8240` with DSpark — [vLLM recipes](https://recipes.vllm.ai/deepseek-ai/DeepSeek-V4-Pro)

### Inferences
- On a single 8-GPU node with 8k/1k aggregated serving, TPOT at conc 64–128 (42–73 ms on B200 GLM-5) is inflated by co-scheduled 8k prefills. Disaggregation, or a separate prefill pool, should lower TPOT at the same concurrency. Expect ~1.5x per GPU on B200 for DSv4 according to SemiAnalysis's estimate, and more at high interactivity on NVL72.
- At small scale (one or two 8-GPU nodes), the gain from disaggregation is modest and depends on the ratio. 1P1D can be prefill-starved when inputs are long.

### Gaps
- No controlled chunked-prefill size sweep (e.g., 2k vs 8k vs 16k chunk) measuring decode TPOT for these models was found.
- No disaggregation results for H100, H200, MI300X or MI325X were found with the 2026 models.

---

## Q6. Prefix-cache hit rates in multi-turn coding-agent workloads; KV offload results

### Takeaway
Claude-Code-style agentic traces are ~99% cacheable in theory, with a median input of 142k tokens (88.8k in the 256k variant) and a median output of only ~376–444 tokens. Realized hit rates depend on how much KV fits:
- B300 with 3 TB DRAM: 91% HBM + 1.4% DRAM.
- B200: 73% HBM + ~20% DRAM.

CPU/DRAM offload adds +81.7% throughput for DSv4 compared with recomputing. The rule of thumb is DRAM ≈ 1.5–3x HBM KV capacity.

### Cited Findings
- **AgentX corpus:** 393 published sessions (from 8,271 sessions and 3.41M requests). 135,282 requests. Median input 142,016 tokens (full) and 88,768 (256k variant). Median output 444 (full) and 376 (256k). Corpus cache-hit rate 99%. Servers without a standard DRAM configuration are capped at 3 TB. Concurrency = number of live agent clients — [AgentX methodology](https://inferencex.semianalysis.com/agentx/methodology)
- **DSv4 Pro 0813 request distribution:** ISL p50 88k, p90 272k, p95 404k, p99 675k. OSL p50 413, p90 2.2k, p99 8.6k. Production p90 TTFT is typically 200–5,000 ms — [AgentX v3](https://inferencex.semianalysis.com/blog/agentx-inferencexv3-does-cuda-moat)
- **DSv4 Pro hit rates:** B300 vLLM DEP8 with 3 TB DRAM at 384 concurrent traces: 91% HBM + 1.36% DRAM, working set ~43M tokens. B200 vLLM at conc 196: 73% HBM + nearly 20% offload, working set ~22M tokens. DRAM offload works best when DRAM is ~1.5–3x the HBM KV capacity — [InferenceX AgentX DSv4](https://inferencex.semianalysis.com/blog/deepseek-v4-pro-agentx-b200-vs-b300-kv-working-set) (2026-08-25, run 2026-08-21)
- **vLLM upstream:**
  - Prefix-cache hit rate >95% with 14 concurrent requests and contexts up to 1M.
  - SimpleCPU hybrid offload on DSv4 gives +81.7% output throughput and −46.6% mean E2E latency vs recomputing.
  - MooncakeStore serves as a distributed KV pool.
  - Source: [InferenceX vLLM optimizations](https://inferencex.semianalysis.com/agentx/optimizations/vllm)
  - The vLLM DSv4 GB200 recipe uses an embedded Mooncake store at "140 GB per local rank" — [vLLM recipes](https://recipes.vllm.ai/deepseek-ai/DeepSeek-V4-Pro)
- **Other engines (AgentX):**
  - ATOM DSv4 checkpoint retention at conc 48: prefix hit rate 5.6% → 96.45%. Unconditional checkpoint publishing costs 17.5% throughput on zero-hit traffic.
  - SGLang context-length-as-runtime-scalar: +26.75% output throughput and −36.25% mean TTFT at conc 384.
  - LMCache: reloading a 32k prefix takes ~0.32 s vs ~2.5 s to recompute. LMCache cut DSv4 storage per token by almost 20x.
  - [Different model] MiniMax M3 on GB200 at conc 32: 28.8% realized cache hit vs 96.0% theoretical.
  - AMD KV offload gap: `hipMemcpyBatchAsync` was missing until ROCm 7.14.
  - Source: [AgentX v3](https://inferencex.semianalysis.com/blog/agentx-inferencexv3-does-cuda-moat)
- **vLLM DSv4.1 Flash:** SWA KV costs more than 10x the storage of global KV when prefix-cached. SWA bounded replay gives ~30% lower TTFT — [vLLM V4.1 Flash](https://vllm.ai/blog/2026-10-07-deepseek-v41-flash)
- **[PROXY] SGLang HiCache (2025-09-10):** up to 6x throughput and up to 80% lower TTFT. Ant Group (DeepSeek-R1 PD serving) saw TTFT 84% lower on cache hits. Novita (Qwen3-Coder-480B coding agent, 3FS): hit rate 40% → 80%, session TTFT −56%, throughput ~2x — [LMSYS HiCache](https://lmsys.org/blog/2025-09-10-sglang-hicache) (search excerpts).
- **Netpreme X-Mem (vendor, 2026-06-27):** hit ratio >95% in subsequent rounds, with a mean of ~98% on Claude Code SWE-bench traces — [LMSYS Netpreme](https://www.lmsys.org/blog/2026-06-27-netpreme-xmem) (search excerpt).
- **Methodology note:** InferenceX disables prefix caching on random fixed-sequence datasets, so 8k/1k numbers are a zero-hit baseline — [InferenceX prefix caching glossary](https://inferencex.semianalysis.com/glossary/prefix-caching) (search summary). The Lambda runs also used `--no-enable-prefix-caching` — [Lambda Kimi K2.6](https://lambda.ai/inference-models/moonshotai/kimi-k2.6)

### Inferences
- For coding-agent cost modelling, use a cached-input share of ~90–95% when HBM plus DRAM can hold the working set (B300-class with TB-scale DRAM). Use ~70–75% from HBM alone on a 180 GB-class GPU at high concurrency. Uncached prefill per turn is then the incremental ~5–10% of ISL, which at an 88k median is still ~4–9k tokens per request.
- Fixed 8k/1k InferenceX throughput (zero cache hits) understates effective prefill capacity for agentic workloads. It is a conservative bound.

### Gaps
- No published per-turn hit-rate distributions for GLM-5.x or Kimi K2.x agentic runs were found.
- No published Mooncake throughput numbers (as a standalone product) for these models were found.
- No LMCache or HiCache results specific to H200 or MI300-series with 2026 models were found.

---

## Q7. Chandra OCR 2 (and Chandra 1): pages/sec, tokens/page, Datalab vLLM claims

### Takeaway
Datalab's only measured throughput is on **1× H100 80GB with vLLM at 96 concurrent requests: 1.44 pages/s** on the hard olmOCR-bench mix (avg latency 60 s, P95 156 s). Datalab estimates ~2 pages/s for real-world documents, and its blog headline is "2 pages/sec". Chandra 1 (9B) claimed up to 4 pages/s on H100 with quantized variants. I found no published Chandra numbers for L40S, RTX PRO 6000 Blackwell or L4, and no published average output tokens per page.

### Cited Findings
- **Chandra OCR 2:** 1.44 pages/s on vLLM with 96 concurrent sequences, avg latency 60 s, P95 156 s, 0% failures, single H100 80GB, olmOCR benchmark mix. "We estimate 2 pages/s in real-world usage." 5B params in BF16 (HF card). Code is Apache 2.0, and weights use a modified OpenRAIL-M licence. olmOCR-bench overall score is 85.8 ± 0.8, vs 83.1 for Chandra 1 and 86.7 for the Datalab API — [HF chandra-ocr-2](https://huggingface.co/datalab-to/chandra-ocr-2)
- **Datalab blog (2026-03-18):** "2 pages/second on an H100 with 96 concurrent requests". The model is 4B parameters, "down from 9B" in Chandra 1. An MTP head "can be used to further improve latency". Quantized versions exist for on-prem use. Datalab "ran 300M pages last week" — [Datalab Chandra 2 blog](https://www.datalab.to/blog/chandra-2). This conflicts on size: 4B (blog) vs 5B (HF card).
- **GitHub README:** sample config `MAX_OUTPUT_TOKENS=12384`. `--batch-size` defaults to 28 for vLLM. `chandra_vllm` launches a Docker container with "optimized inference settings" that are not listed. The managed batch service has processed "200M+ pages per week". Chandra 2 was released in 3/2026 and Chandra 1 in 10/2025 — [GitHub datalab-to/chandra](https://github.com/datalab-to/chandra)
- **[PROXY] Chandra 1 (2025-10-30):** "up to 4 pages/second on an H100, or 345,000 pages per day, with minimal accuracy degradation" (quantized). Quantized 8B and 2B on-prem versions exist — [Datalab Introducing Chandra](https://www.datalab.to/blog/introducing-chandra)
- **A secondary source** lists Chandra 2's maximum output at 8,192 tokens — [search summary citing emelia.io](https://emelia.io/hub/chandra-ocr-tables-handwriting) (secondary; conflicts with the 12,384 in the README sample config).
- **[PROXY] olmOCR (7B VLM, FP8):** "less than $200 USD per million pages". Tested on RTX 4090, L40S, A100 and H100, with a 12 GB GPU minimum. Example launch is `vllm serve allenai/olmOCR-2-7B-1025-FP8 --max-model-len 16384`. No per-GPU pages/s are published — [GitHub allenai/olmocr](https://github.com/allenai/olmocr)
- **L40S, RTX PRO 6000 and L4:** no Chandra benchmarks found. A vendor page ranks RTX 6000 PRO first for OCR throughput, but only for PaddleOCR, Surya and a generic 3B VLM — [GIGAGPU OCR benchmarks](https://gigagpu.com/ocr-speed-benchmarks/) (not Chandra).

### Inferences
- 1.44–2 pages/s on H100 = **5,200–7,200 pages/hour per H100**, or about 124k–173k pages/day. Little's law gives the same: 96 concurrent requests ÷ 60 s average latency ≈ 1.6 pages/s.
- Scaling to other GPUs by memory bandwidth, the bottleneck for a 4–5B decode-heavy VLM at moderate batch, would put L40S at ≈ 0.26x H100, L4 at ≈ 0.09x and RTX PRO 6000 Blackwell at ≈ 0.54x. These ratios use datasheet bandwidths (H100 SXM ~3.35 TB/s, L40S ~864 GB/s, L4 ~300 GB/s, RTX PRO 6000 ~1.8 TB/s) that I recalled rather than fetched in this session, so treat them as an unverified estimate. That would be roughly 0.4–0.5 pages/s on L40S, ~0.15 on L4 and ~0.8–1.1 on RTX PRO 6000. Vision-encoder prefill is compute-bound and may shift these ratios.

### Gaps
- No published average output tokens per page for Chandra 1/2 or olmOCR was found.
- No vLLM version or launch flags were published for the 1.44 pages/s benchmark.
- No measured Chandra throughput was found on L40S, RTX PRO 6000 Blackwell or L4.
- No details on quantized-variant throughput for Chandra 2 were found.

---

## Q8. Reference API prices (official and OpenRouter) as a sanity line

### Takeaway
Official prices (USD per 1M tokens, retrieved 2026-10-19):
- **DeepSeek V4-Pro-0813:** $0.66 / $0.022 / $1.98 (input miss / cache hit / output) off-peak, double at peak.
- **Z.ai GLM-5.1/5.2/5.3:** $1.40 / $0.26 / $4.40. GLM-5 is $1.00 / $0.20 / $3.20.
- **Moonshot Kimi K2.6** (first-party endpoint on OpenRouter): $0.95 / $0.16 / $4.00.

The cheapest third-party OpenRouter providers run ~30–55% below first-party list prices on output.

### Cited Findings
- **DeepSeek official:**
  - `deepseek-v4-pro` (DeepSeek-V4-Pro-0813): cache hit $0.022 off-peak / $0.044 peak; cache miss $0.66 / $1.32; output $1.98 / $3.96. 1M context, concurrency limit 500.
  - `deepseek-flash` (V4.1-Flash-1017): $0.003 / $0.006; $0.15 / $0.30; $0.60 / $1.20.
  - Off-peak rates are half of peak. Peak hours are 01:00–04:00 and 06:00–10:00 UTC, Mon–Fri.
  - Source: [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing)
- **Z.ai official** (input / cached input / output; cached storage "Limited-time Free"):
  - GLM-5.3, GLM-5.2 and GLM-5.1: $1.4 / $0.26 / $4.4.
  - GLM-5: $1 / $0.2 / $3.2.
  - GLM-5.3-Flash: $0.15 / $0.03 / $0.50.
  - GLM-5.3-FlashX: $0.37 / $0.075 / $1.25.
  - Source: [Z.ai pricing](https://docs.z.ai/guides/overview/pricing)
- **Moonshot first-party, from OpenRouter endpoint listings** (in / out / cache read; retrieved 2026-10-19 from `openrouter.ai/api/v1/models/{id}/endpoints`):
  - Kimi K2.6, "Moonshot AI" endpoint, INT4: $0.95 / $4.00 / $0.16.
  - Kimi K2.7-Code, "Moonshot AI": $0.95 / $4.00 / $0.19. A second Moonshot endpoint is listed at $1.9 / $8.0 / $0.38, possibly a high-speed tier, but it is unlabelled.
  - Source: [OpenRouter API endpoints](https://openrouter.ai/api/v1/models/moonshotai/kimi-k2.6/endpoints)
- **OpenRouter, selected providers** (in / out / cache read per 1M; retrieved 2026-10-19):
  - DeepSeek V4 Pro 0813: DeepSeek $0.66 / $1.98 / $0.022. Novita FP8 $0.99 / $2.97 / $0.033. CoreWeave FP8 $1.31 / $3.96 / $0.044. Many others at $1.32 / $3.96. Wafer MXFP4 $0.25 / $5.00 / $0.249 — [OpenRouter DSv4 Pro 0813 endpoints](https://openrouter.ai/api/v1/models/deepseek/deepseek-v4-pro-0813/endpoints)
  - DeepSeek V4 Pro (preview): GMICloud FP8 $0.957 / $1.914 / $0.0798. DeepInfra FP8 $1.3 / $2.6 / $0.1 — [OpenRouter DSv4 Pro endpoints](https://openrouter.ai/api/v1/models/deepseek/deepseek-v4-pro/endpoints)
  - Kimi K2.6: Chutes INT4 $0.45 / $1.95 / $0.045. CoreWeave FP4 $0.65 / $3.41 / $0.15. DeepInfra FP4 $0.75 / $3.5 / $0.15 — [OpenRouter K2.6 endpoints](https://openrouter.ai/api/v1/models/moonshotai/kimi-k2.6/endpoints)
  - Kimi K2.5: AtlasCloud INT4 $0.49 / $2.5 / $0.2. Novita $0.57 / $2.85 / $0.095 — [OpenRouter K2.5 endpoints](https://openrouter.ai/api/v1/models/moonshotai/kimi-k2.5/endpoints). Kimi K2 Thinking model-level price: $0.6 / $2.5 / $0.15 — [OpenRouter models API](https://openrouter.ai/api/v1/models)
  - GLM-5.1: Chutes FP8 $0.98 / $3.08 / $0.098. Z.AI FP8 $1.4 / $4.4 / $0.26 — [OpenRouter GLM-5.1 endpoints](https://openrouter.ai/api/v1/models/z-ai/glm-5.1/endpoints)
  - GLM-5.2: DeepInfra FP4 $0.45 / $1.44 / $0.084. CoreWeave FP4 $0.62 / $2.42 / $0.14 — [OpenRouter GLM-5.2 endpoints](https://openrouter.ai/api/v1/models/z-ai/glm-5.2/endpoints)
  - [PROXY] DeepSeek V3.2: GMICloud FP8 $0.2088 / $0.3096 / $0.0216. DeepInfra FP4 $0.26 / $0.38 / $0.13 — [OpenRouter V3.2 endpoints](https://openrouter.ai/api/v1/models/deepseek/deepseek-v3.2/endpoints)
- **Provider speed (Artificial Analysis, Kimi K2.6 Reasoning, 10k-input workload):** Nebius 258.9 output tok/s (TTFT 18.74 s). Azure 254.3. CoreWeave 176.5 (TTFT 26.24 s, $0.65 / $3.41). Parasail 124.4. DeepInfra FP4 88.2. The detailed table lists Kimi first-party at 47 t/s. The page marks the model "deprecated", and its cache data is updated Sep 26, 2026 — [AA Kimi K2.6 providers](https://artificialanalysis.ai/models/kimi-k2-6/providers)
- **GLM-5 on Baseten:** "186+ tokens per second" (Artificial Analysis measurement), using NVFP4 on Blackwell with MTP (2026-03-06) — [Baseten GLM-5](https://www.baseten.co/blog/how-we-built-the-fastest-glm-5-api/)
- **[PROXY]** The 2025 SGLang H100 PD+EP deployment estimated $0.20 per 1M output tokens for DeepSeek V3 — [LMSYS large-scale EP](https://lmsys.org/blog/2025-05-05-large-scale-ep/)

### Inferences
- InferenceX's modeled serving costs at 50 tok/s/user, 8k/1k, are in "$/M total tokens" (GLM-5 NVFP4 B200 $0.19; Kimi NVFP4 B200 $0.177; DSv4 GB300 $0.156 per M *output*). Converted to per-output-token terms (×9 for 8k/1k total-token figures), they sit at or below the cheapest OpenRouter providers' blended prices. Self-hosting only wins at high utilization.
- OpenRouter's model-level price for `z-ai/glm-5.3` ($0.079 in / $1.4 out) is inconsistent with Z.ai's $1.4 / $4.4. It probably reflects a promotional or cheapest-provider floor. Use per-endpoint prices.

### Gaps
- Moonshot's own platform pricing page was not retrieved directly; the kimi.com page returned only a K3 launch title. First-party prices come from the OpenRouter endpoint listing.
- Artificial Analysis provider pages for DSv4 Pro and GLM-5.x were not retrieved.

---

## Q9. Consolidated data table (all extracted data points)

### Takeaway
Rows below are raw values. "tok/s/GPU" is **InferenceX total (input + output) tokens** unless marked (out) for output-only. "tok/s/user" for InferenceX is 1000/TPOT. "n/r" = not reported. Agg = aggregated; disagg = PD-disaggregated.

### Cited Findings

| Model | GPU | #GPUs | Precision | Engine | In/Out | Conc | tok/s/user | tok/s/GPU | TTFT | MTP | Source | Date |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GLM-5 | H200 | 8 (TP8) | FP8 | SGLang v0.5.12 | 8k/1k | 32 | 24.90 | 851.9 | n/r | EAGLE 3/1/4 | [IX](https://inferencex.semianalysis.com/blog/b200-glm5-nvfp4-vs-h200-fp8-3-6x-perf-per-dollar) | 2026-05-25 |
| GLM-5 | H200 | 8 (TP8) | FP8 | SGLang v0.5.12 | 8k/1k | 64 | 20.80 | 847.2 | n/r | EAGLE 3/1/4 | [IX](https://inferencex.semianalysis.com/blog/b200-glm5-nvfp4-vs-h200-fp8-3-6x-perf-per-dollar) | 2026-05-25 |
| GLM-5 | B200 | 8 (TP8) | FP8 | SGLang v0.5.12 | 8k/1k | 64 | 23.56 | 1,619.3 | n/r | EAGLE 3/1/4 | [IX](https://inferencex.semianalysis.com/blog/b200-glm5-nvfp4-vs-h200-fp8-3-6x-perf-per-dollar) | 2026-05-25 |
| GLM-5 | B200 | 8 (TP8) | FP8 | SGLang v0.5.12 | 8k/1k | 128 | 13.78 | 1,929.5 | n/r | EAGLE 3/1/4 | [IX](https://inferencex.semianalysis.com/blog/b200-glm5-nvfp4-vs-h200-fp8-3-6x-perf-per-dollar) | 2026-05-25 |
| GLM-5 | B200 | 8 (TP8) | FP8 | SGLang v0.5.12 | 8k/1k | 64 | 18.42 | 1,291.8 | n/r | off | [IX MI355X](https://inferencex.semianalysis.com/blog/mi355x-glm5-fp8-sglang-40-cheaper-than-b200) | 2026-05-20 |
| GLM-5 | B200 | 8 (TP8) | FP8 | SGLang v0.5.12 | 8k/1k | 128 | 11.87 | 1,669.1 | n/r | off | [IX MI355X](https://inferencex.semianalysis.com/blog/mi355x-glm5-fp8-sglang-40-cheaper-than-b200) | 2026-05-20 |
| GLM-5 | B200 | 4 (TP4) | NVFP4 | SGLang v0.5.12 | 8k/1k | 16 | 66.27 | 2,228.1 | n/r | EAGLE 3/1/4 | [IX](https://inferencex.semianalysis.com/blog/b200-glm5-nvfp4-vs-h200-fp8-3-6x-perf-per-dollar) | 2026-05-25 |
| GLM-5 | B200 | 4 (TP4) | NVFP4 | SGLang v0.5.12 | 8k/1k | 32 | 43.99 | 3,037.3 | n/r | EAGLE 3/1/4 | [IX](https://inferencex.semianalysis.com/blog/b200-glm5-nvfp4-vs-h200-fp8-3-6x-perf-per-dollar) | 2026-05-25 |
| GLM-5 | B200 | 4 (TP4) | NVFP4 | SGLang v0.5.12 | 8k/1k | 64 | 26.78 | 3,739.7 | n/r | EAGLE 3/1/4 | [IX](https://inferencex.semianalysis.com/blog/b200-glm5-nvfp4-vs-h200-fp8-3-6x-perf-per-dollar) | 2026-05-25 |
| GLM-5 | B200 | 4 (TP4) | NVFP4 | SGLang v0.5.12 | 8k/1k | 128 | 17.63 | 4,115.5 | n/r | EAGLE 3/1/4 | [IX](https://inferencex.semianalysis.com/blog/b200-glm5-nvfp4-vs-h200-fp8-3-6x-perf-per-dollar) | 2026-05-25 |
| GLM-5 | MI355X | 4 (TP4) | FP8 | SGLang v0.5.12 ROCm | 8k/1k | 64 | 18.19 | 1,895.0 | n/r | EAGLE (MTP) | [IX MI355X](https://inferencex.semianalysis.com/blog/mi355x-glm5-fp8-sglang-40-cheaper-than-b200) | 2026-05-20 |
| GLM-5 | MI355X | 4 (TP4) | FP8 | SGLang v0.5.12 ROCm | 8k/1k | 128 | 18.05 | 1,911.7 | n/r | EAGLE (MTP) | [IX MI355X](https://inferencex.semianalysis.com/blog/mi355x-glm5-fp8-sglang-40-cheaper-than-b200) | 2026-05-20 |
| GLM-5 | MI355X | 4 (TP4) | FP8 | SGLang v0.5.12 ROCm | 8k/1k | 64 | 11.83 | 1,660.1 | n/r | off | [IX MI355X](https://inferencex.semianalysis.com/blog/mi355x-glm5-fp8-sglang-40-cheaper-than-b200) | 2026-05-20 |
| GLM-5 | MI355X | 4 (TP4) | FP8 | SGLang v0.5.12 ROCm | 8k/1k | 128 | 7.33 | 2,071.4 | n/r | off | [IX MI355X](https://inferencex.semianalysis.com/blog/mi355x-glm5-fp8-sglang-40-cheaper-than-b200) | 2026-05-20 |
| GLM-5 | B200 | 8 (TP8) | FP8 | SGLang glm5-blackwell | 1k/1k | 100 | ~29 (1/TPOT 34.46 ms) | 171.3 (out) / 343 total | 18,239 ms mean | EAGLE 3/1/4, AL 3.52 | [gist](https://gist.github.com/BenHamm/dcd09f595fef141567a39582f502cef4) | 2026-02-13 |
| GLM-5 | B200 | 8 (TP8) | FP8 | SGLang glm5-blackwell | 1k/1k | 100 | ~13 (TPOT 77.09 ms) | 154.2 (out) | 693 ms mean | off | [gist](https://gist.github.com/BenHamm/dcd09f595fef141567a39582f502cef4) | 2026-02-13 |
| GLM-5 | H200 | 8 | FP8 | SGLang (cookbook) | 1k/1k | 100 | ~26 (TPOT 38.7 ms) | 151.9 (out) | 8,690 ms mean | EAGLE, AL 3.48 (conc 1) | [gist](https://gist.github.com/BenHamm/dcd09f595fef141567a39582f502cef4) | 2026-02-13 |
| GLM-5 | B200 | 8 (TP8) | FP8 | SGLang glm5-blackwell | 1k/1k | 1 | 48 / 112 (EAGLE) | n/a | 260 / 391 ms | off / EAGLE | [gist](https://gist.github.com/BenHamm/dcd09f595fef141567a39582f502cef4) | 2026-02-13 |
| GLM-5.1 | B200 | 8 (TP8) | FP8 | SGLang v0.5.10 | 8k/2k | 32 | 42.04 | 168 (out) / 841 total | 1,072.61 ms mean | EAGLE 3/1/4 | [Lambda](https://lambda.ai/inference-models/zai-org/glm-5.1) | 2026 (n/s) |
| GLM-5.1 | B200 | 8 (TP8) | FP8 | vLLM v0.19.0 | 8k/2k | 32 | 39.55 | 158 (out) / 791 total | 1,316.86 ms mean | MTP 3 | [Lambda](https://lambda.ai/inference-models/zai-org/glm-5.1) | 2026 (n/s) |
| GLM-5.3 | B200 | n/r | FP4 | n/r | "8K/1K (deprecated)"/agentic default | ~34 | 138 | 10,091 | n/r | n/r | [IX compare](https://inferencex.semianalysis.com/compare/glm-5-3-b200-vs-h200) | 2026 (n/s) |
| Kimi K2.5/2.6 | H200 | 8 (TP8) | INT4 | vLLM v0.21.0 | 8k/1k | 32 | 28.86 | 990.9 | n/r | off | [IX](https://inferencex.semianalysis.com/blog/b200-nvfp4-vs-h200-int4-kimi-k2-vllm-perf-per-dollar) | 2026-05-19 |
| Kimi K2.5/2.6 | H200 | 8 (TP8) | INT4 | vLLM v0.21.0 | 8k/1k | 64 | 16.67 | 1,174.5 | n/r | off | [IX](https://inferencex.semianalysis.com/blog/b200-nvfp4-vs-h200-int4-kimi-k2-vllm-perf-per-dollar) | 2026-05-19 |
| Kimi K2.5/2.6 | B200 | 8 (TP8) | INT4 | vLLM v0.21.0 | 8k/1k | 64 | 26.01 | 1,790.7 | n/r | off | [IX](https://inferencex.semianalysis.com/blog/b200-nvfp4-vs-h200-int4-kimi-k2-vllm-perf-per-dollar) | 2026-05-19 |
| Kimi K2.5/2.6 | B200 | 4 (TP4) | NVFP4 | vLLM v0.21.0 | 8k/1k | 32 | 46.83 | 3,202.7 | n/r | off | [IX](https://inferencex.semianalysis.com/blog/b200-nvfp4-vs-h200-int4-kimi-k2-vllm-perf-per-dollar) | 2026-05-19 |
| Kimi K2.5/2.6 | B200 | 4 (TP4) | NVFP4 | vLLM v0.21.0 | 8k/1k | 64 | 32.19 | 3,879.3 | n/r | off | [IX](https://inferencex.semianalysis.com/blog/b200-nvfp4-vs-h200-int4-kimi-k2-vllm-perf-per-dollar) | 2026-05-19 |
| Kimi K2.5 | B200 | 16 pool (TP4/EP4) | NVFP4 | vLLM | 8k/1k | 64 | 29.3 | 4,021 | n/r | off | [IX GB200 Kimi](https://inferencex.semianalysis.com/blog/gb200-nvl72-kimi-k2-5-vllm-wide-ep-3x-vs-b200) | 2026-03-27 |
| Kimi K2.5 | GB200 NVL72 | 4P + 4D (TP4/EP4) | NVFP4 | Dynamo vLLM 0.18.0 disagg | 8k/1k | 128 | 77.9 | 2,173 | n/r | off | [IX GB200 Kimi](https://inferencex.semianalysis.com/blog/gb200-nvl72-kimi-k2-5-vllm-wide-ep-3x-vs-b200) | 2026-04-07 |
| Kimi K2.5 | GB200 NVL72 | 4P + 16D (TP16/EP16) | NVFP4 | Dynamo vLLM 0.18.0 disagg | 8k/1k | 512 | 48.8 | 6,885 | n/r | off | [IX GB200 Kimi](https://inferencex.semianalysis.com/blog/gb200-nvl72-kimi-k2-5-vllm-wide-ep-3x-vs-b200) | 2026-04-07 |
| Kimi K2.5 | GB200 NVL72 | 4P + 8D (TP8/EP8) | NVFP4 | Dynamo vLLM 0.18.0 disagg | 8k/1k | 2,048 | 23.2 | 12,587 | n/r | off | [IX GB200 Kimi](https://inferencex.semianalysis.com/blog/gb200-nvl72-kimi-k2-5-vllm-wide-ep-3x-vs-b200) | 2026-04-07 |
| Kimi K2.6 | GB300 NVL72 | n/r | FP4 | Dynamo vLLM | 8k/1k | n/r | 50 | 5,601 | n/r | n/r | [IX ranking](https://inferencex.semianalysis.com/rankings/fastest-gpu-for-kimi-k26) | ≤2026-08-07 |
| Kimi K2.6 | GB200 NVL72 | n/r | FP4 | Dynamo vLLM | 8k/1k | n/r | 50 | 4,594 | n/r | n/r | [IX ranking](https://inferencex.semianalysis.com/rankings/fastest-gpu-for-kimi-k26) | ≤2026-08-07 |
| Kimi K2.6 | B300 | n/r | FP4 | vLLM | 8k/1k | ~32 | 50 | 3,504 | n/r | n/r | [IX ranking](https://inferencex.semianalysis.com/rankings/fastest-gpu-for-kimi-k26) | ≤2026-08-07 |
| Kimi K2.6 | B200 | n/r | FP4 | Dynamo vLLM | 8k/1k | n/r | 50 | 3,449 | n/r | n/r | [IX ranking](https://inferencex.semianalysis.com/rankings/fastest-gpu-for-kimi-k26) | ≤2026-08-07 |
| Kimi K2.6 | B200 | multi-node | FP4 | Dynamo (TRT-LLM/vLLM) | 8k/1k | ~323 | 50 | 8,178.4 | n/r | n/r | [IX B200 vs B300](https://inferencex.semianalysis.com/compare/kimi-k26-b200-vs-b300) | 2026 (n/s) |
| Kimi K2.6 | MI355X | n/r | FP4 | vLLM | 8k/1k | n/r | 50 | 2,831 | n/r | n/r | [IX ranking](https://inferencex.semianalysis.com/rankings/fastest-gpu-for-kimi-k26) | ≤2026-08-07 |
| Kimi K2.6 | MI355X | n/r | FP4 | n/r (ATOM noted) | 8k/1k | ~102 | 38 | 4,004 | n/r | n/r | [IX B200 vs MI355X](https://inferencex.semianalysis.com/compare/kimi-k26-b200-vs-mi355x) | 2026 (n/s) |
| Kimi K2.6 | B200 | 8 (TP8) | INT4 + BF16 | vLLM cu130-nightly | 8k/2k | 32 | 44 | 176 (out) / 881 total | 2,264.48 ms mean | EAGLE-3, 3 tok | [Lambda](https://lambda.ai/inference-models/moonshotai/kimi-k2.6) | 2026 (n/s) |
| DSv4 Pro | MI355X | 8 (TP8) | FP4 | SGLang v0.5.12 (amd branch) | 8k/1k | 64 | 16.79 | 959.6 | n/r | n/r | [IX MI355X DSv4](https://inferencex.semianalysis.com/blog/mi355x-deepseek-v4-pro-sglang-110x-in-26-days) | 2026-05-21 |
| DSv4 Pro | MI355X | 8 (TP8) | FP4 | SGLang v0.5.12 (amd branch) | 8k/1k | 128 | 13.76 | 1,556.0 | n/r | n/r | [IX MI355X DSv4](https://inferencex.semianalysis.com/blog/mi355x-deepseek-v4-pro-sglang-110x-in-26-days) | 2026-05-21 |
| DSv4 Pro | MI355X | 8 (TP8 + DP attn) | FP4 | SGLang v0.5.12 (amd branch) | 8k/1k | 256 | 9.37 | 2,256.1 | n/r | n/r | [IX MI355X DSv4](https://inferencex.semianalysis.com/blog/mi355x-deepseek-v4-pro-sglang-110x-in-26-days) | 2026-05-21 |
| DSv4 Pro | MI355X | 8 (TP8) | FP8 | SGLang v0.5.10rc0 | 8k/1k | 64 | 0.93 | 67.4 | n/r | n/r | [IX MI355X DSv4](https://inferencex.semianalysis.com/blog/mi355x-deepseek-v4-pro-sglang-110x-in-26-days) | 2026-04-25 (Day 0) |
| DSv4 Pro | GB300 NVL72 | multi-node disagg (e.g., 10P DEP4 + 1D DEP32) | FP4 | Dynamo SGLang | 8k/1k | n/r | ~50 | ~11,200 | n/r | on | [PyTorch](https://pytorch.org/blog/serving-deepseek-v4-on-gb300-with-sglang-5x-higher-throughput-at-the-same-interactivity-since-day-0/) | 2026-06 |
| DSv4 Pro | GB300 NVL72 | multi-node disagg | FP4 | Dynamo SGLang | 8k/1k | n/r | ~50 | ~2,200 | n/r | off | [PyTorch](https://pytorch.org/blog/serving-deepseek-v4-on-gb300-with-sglang-5x-higher-throughput-at-the-same-interactivity-since-day-0/) | 2026-04 (Day 0) |
| DSv4 Pro | GB300 NVL72 | disagg | FP4 | SGLang | 8k/1k | n/r | 50 | $0.156/M output | n/r | on | [IX Day 0–43](https://inferencex.semianalysis.com/blog/deepseekv4-16t-day-0-to-day-43-performance) | ≤2026-06-09 |
| DSv4 Pro | B200 | 8 | FP4 | vLLM | 8k/1k | n/r | 50 | ~500k tok/s/MW (≈1,085/GPU derived) | n/r | n/r | [IX Day 0–43](https://inferencex.semianalysis.com/blog/deepseekv4-16t-day-0-to-day-43-performance) | 2026-06-05 |
| DSv4 Pro | B200 | 8 (DP8 + EP) | FP4 + FP8 | vLLM latest-cu129 | 8k/2k | 32 | 28.50 | 114 (out) / 570 total | 1,186.15 ms mean | MTP 2 (~33% acc.) | [Lambda](https://lambda.ai/inference-models/deepseek-ai/deepseek-v4-pro) | 2026 (n/s) |
| DSv4 Pro | B200 | 8 (TP8) | FP4/FP8 | SGLang | 30k prefix, OSL 4k | 1 | 199 → 180 (4K → 900K ctx) | n/a | n/r | n/r | [LMSYS](https://www.lmsys.org/blog/2026-04-25-deepseek-v4/) | 2026-04-25 |
| DSv4 Pro 0813 | B300 | 8 (DEP8) | FP4 | vLLM (3 TB DRAM offload) | AgentX (ISL p50 88k) | n/r | 50 | 71,955 (incl. cached) | n/r | n/r | [IX ranking](https://inferencex.semianalysis.com/rankings/fastest-gpu-for-deepseek-v4) | ≤2026-10-15 |
| DSv4 Pro 0813 | B200 | n/r | FP4 | vLLM | AgentX | n/r | 50 | 65,134 (incl. cached) | n/r | n/r | [IX ranking](https://inferencex.semianalysis.com/rankings/fastest-gpu-for-deepseek-v4) | ≤2026-10-15 |
| DSv4 Pro 0813 | MI355X | 8P + 8D | FP4 | MoRI SGLang | AgentX | n/r | 50 | 37,438 (incl. cached) | n/r | n/r | [IX ranking](https://inferencex.semianalysis.com/rankings/fastest-gpu-for-deepseek-v4) | ≤2026-10-15 |
| [PROXY] DS R1-0528 | B200 | 4P + 40D (EP8) | FP4 | Dynamo TRT-LLM disagg | 1k/1k | 90 | 150.56 | 577.3 | n/r | on | [IX GB200 vs B200](https://inferencex.semianalysis.com/blog/gb200-nvl72-vs-b200-disagg-deepseek-r1-fp4-dynamo-trt) | 2026-05-22 |
| [PROXY] DS R1-0528 | B200 | 12P + 32D (EP8) | FP4 | Dynamo TRT-LLM disagg | 1k/1k | 4,968 | 56.35 | 9,660.7 | n/r | on | [IX GB200 vs B200](https://inferencex.semianalysis.com/blog/gb200-nvl72-vs-b200-disagg-deepseek-r1-fp4-dynamo-trt) | 2026-05-22 |
| [PROXY] DS R1-0528 | GB200 NVL72 | 4P + 32D (EP32) | FP4 | Dynamo TRT-LLM disagg | 1k/1k | 180 | 164.37 | 1,149.1 | n/r | on | [IX GB200 vs B200](https://inferencex.semianalysis.com/blog/gb200-nvl72-vs-b200-disagg-deepseek-r1-fp4-dynamo-trt) | 2026-05-22 |
| [PROXY] DS R1-0528 | GB200 NVL72 | 8P + 16D (EP16) | FP4 | Dynamo TRT-LLM disagg | 1k/1k | 4,301 | 43.29 | 12,659.7 | n/r | on | [IX GB200 vs B200](https://inferencex.semianalysis.com/blog/gb200-nvl72-vs-b200-disagg-deepseek-r1-fp4-dynamo-trt) | 2026-05-22 |
| [PROXY] DS R1 | B200 | n/r | FP4 | SGLang | 8k/1k | n/r | 50 | 4,610 | n/r | n/r | [IX R1 ranking](https://inferencex.semianalysis.com/rankings/fastest-gpu-for-deepseek-r1) | ≤2026-10-13 |
| [PROXY] DS R1 | GB200 NVL72 | n/r | FP8 | Dynamo SGLang | 8k/1k | n/r | 50 | 2,697 | n/r | n/r | [IX R1 ranking](https://inferencex.semianalysis.com/rankings/fastest-gpu-for-deepseek-r1) | ≤2026-10-13 |
| [PROXY] DS R1 | GB300 NVL72 | n/r | FP8 | Dynamo SGLang | 8k/1k | n/r | 50 | 2,438 | n/r | n/r | [IX R1 ranking](https://inferencex.semianalysis.com/rankings/fastest-gpu-for-deepseek-r1) | ≤2026-10-13 |
| [PROXY] DS R1 | B300 | n/r | FP8 | SGLang | 8k/1k | n/r | 50 | 1,779 | n/r | n/r | [IX R1 ranking](https://inferencex.semianalysis.com/rankings/fastest-gpu-for-deepseek-r1) | ≤2026-10-13 |
| [PROXY] DS R1 | MI355X | n/r | FP8 | SGLang | 8k/1k | n/r | 50 | 1,608 | n/r | n/r | [IX R1 ranking](https://inferencex.semianalysis.com/rankings/fastest-gpu-for-deepseek-r1) | ≤2026-10-13 |
| [PROXY] DS R1-0528 | H100 | n/r | FP8 (page inconsistent) | n/r | 8k/1k | ~154 | 36 | 850.1 | n/r | n/r | [IX H100 vs MI300X](https://inferencex.semianalysis.com/compare/deepseek-r1-h100-vs-mi300x) | 2026 (n/s) |
| [PROXY] DS R1-0528 | MI300X | n/r | FP8 (page inconsistent) | n/r | 8k/1k | ~15 | 36 | 532.4 | n/r | n/r | [IX H100 vs MI300X](https://inferencex.semianalysis.com/compare/deepseek-r1-h100-vs-mi300x) | 2026 (n/s) |
| [PROXY] DS V3 | H100 | 96 (12 nodes; decode 72) | FP8 | SGLang PD + EP | 2k in | batch 256/GPU | ~10 (ITL ~100 ms) | ~2,785 (out, decode; 22,282/node) | 2–5 s | off | [LMSYS](https://lmsys.org/blog/2025-05-05-large-scale-ep/) | 2025-05-05 |
| [PROXY] DS V3.2 | GB300 | 2 (TP2) | NVFP4 | vLLM v0.14.1 | 2k/1k | n/r | n/r | 2,816 TGS (prefill-only 7,360 at 2k) | n/r | off | [vLLM](https://vllm.ai/blog/2026-02-13-gb300-deepseek) | 2026-02-13 |
| Chandra OCR 2 | H100 80GB | 1 | BF16 | vLLM | olmOCR mix | 96 | n/a | 1.44 pages/s (~2 real-world) | 60 s avg latency (P95 156 s) | n/r (MTP head available) | [HF card](https://huggingface.co/datalab-to/chandra-ocr-2) | 2026-03 |
| [PROXY] Chandra 1 (quantized) | H100 | 1 | quantized | vLLM | n/r | n/r | n/a | up to 4 pages/s | n/r | n/r | [Datalab](https://www.datalab.to/blog/introducing-chandra) | 2025-10-30 |

### Inferences
- To convert any InferenceX 8k/1k "tok/s/GPU" row to output tok/s/GPU, divide by ~9. For 1k/1k rows, divide by ~2. Lambda and gist rows already give output per node, divided by 8 here.
- For cost modelling of an 8-GPU node at ~20–30 tok/s/user, these output rates per GPU are realistic:
  - GLM-5 FP8 on H200: ~95.
  - GLM-5 FP8 on B200: ~145–180.
  - GLM-5 NVFP4 on B200: ~400–420 (~340 at 44 tok/s/user).
  - Kimi INT4 on H200: ~110–130.
  - Kimi NVFP4 on B200: ~355–430.
  - DSv4 Pro FP4 on MI355X: ~90–110 (May 2026; it later improved via ATOM and MoRI).

### Gaps
- Rows marked n/r lack TTFT, concurrency or engine version because the source shows only charts or summary cards.
- No rows exist for H100, H200, MI300X or MI325X with GLM-5.x, Kimi K2.x or DSv4 Pro except GLM-5 and Kimi on H200.
- No rows exist for L40S, RTX PRO 6000 or L4 OCR.
