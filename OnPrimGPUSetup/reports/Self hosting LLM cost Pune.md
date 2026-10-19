# Coding agents justify buying GPUs; chat does not

At 90 concurrent users and 30 tok/s per user, one standalone self-hosted model costs Stark Digital about **₹16.4–20.3 lakh a month for chat** and **₹33.3–72.9 lakh a month for coding agents**. That figure is all-in: hardware recovered over 3 years at 11% with 20% resale, power, UPS/DG, cooling, staff and space, ex-GST with input tax credit (ITC) claimed. For agents compacting at 128k, GLM-5.3 and DeepSeek V4 Pro cost the same, **₹33.4 and ₹33.3 lakh/month**, each on two 8×MI355X nodes in a new Baner server room. Kimi K2.7 Code costs **₹46.4 lakh** because it needs a third node. At the 1M ceiling the three spread out to **₹34.1, ₹46.4 and ₹72.9 lakh**. For every coding-agent workload, buying beats renting, with a **28–32-month breakeven**. Renting still wins in two cases: deployments that fit on one node, such as chat on H200 (**₹16.4 vs ₹18.8 lakh**, 46-month breakeven), and business-hours-only use. If you buy, Pune or Navi Mumbai colocation is cheaper than an own room in every case, by about 7–9%. Each model should run at its official precision: FP8 for GLM-5.3, FP4+FP8 for DeepSeek, INT4 for Kimi (or an FP8 upcast, which is faster). FP32 cannot be served at all, and BF16 for DeepSeek and Kimi is an upcast that only adds nodes. These cheapest results rest on AMD MI355X, whose purchase price is inferred. Budget on the NVIDIA-only (B200) figures instead: **₹36.3, ₹51.0 and ₹65.5 lakh** for 128k agents. No paid benchmark was run, so throughput is modelled: it is calibrated on 12 published points, and pairs with no data carry ±25%. Chandra OCR 2 also needs a paid commercial licence, which is not costed.

> **Live calculator:** `/home/stark/prateek/prateek-obsidian/reports/Self hosting LLM cost Pune.xlsx` has six sheets: Summary, Calculator, Inputs, Matrix, OCR and Sources. Every costed figure in this note is copied from the cost model's output, [[model_results]]. The formulas are in `cost_model/catalog.py` and the inputs in `cost_model/data/*.yaml`. Money is in INR at **₹95.18/USD**, the open.er-api.com rate on 19 Oct 2026 ([open.er-api.com](https://open.er-api.com/v6/latest/USD)).

## Ninety users cost ₹16 lakh for chat and up to ₹73 lakh for agents

The model sizes each model as its **own standalone deployment**, so the three are not added together and nothing is shared between them. It uses five workloads. **Chat** assumes users generate output about 20% of the time they are present, with a 12k-token context. **Mixed** is 70% chat users and 30% agent users. **agent_128k** is coding agents busy about 55% of session time that auto-summarise at 128k tokens; summaries carry the 1M ceiling. **agent_1m** lets agents run almost to the 1M window before compacting. **stress_1m** puts every user at the context ceiling at once. That is a bound, not a plan.

The base levers are fixed: running 24/7, GST input credit claimed, no spare node, a 3-year horizon, and the HT commercial power tariff, because Stark Digital is not a registered IT/ITeS unit. The rental column is the cheapest cloud option plus one MLOps engineer. The duty cycles and context lengths are modelling assumptions, flagged as such in `workloads.yaml`. The agent profile is anchored on published coding-agent traces: a median of 88–142k input tokens and only about 376–444 output tokens per request, with about 99% of input cacheable ([InferenceX AgentX methodology](https://inferencex.semianalysis.com/agentx/methodology)).

Each deployment is one or more copies of the model (replicas), and each replica spans one or more 8-GPU nodes. The model does not simply put a replica on the fewest nodes its weights fit on. It also tries spreading one replica over one or two more nodes, which leaves more memory for the KV cache but adds about 120 µs of cross-node latency to every collective, and it keeps whichever layout needs the fewest nodes in total. This fixed oversized results in an earlier version, where weights nearly filled a node and left little room for cache. GLM-5.3 FP8 on 8×H200 for 90 coding-agent users had needed 10 nodes and ₹134.9 lakh/month to rent; it now needs 3 nodes, with one replica across all three, at ₹42.7 lakh. The DeepSeek and Kimi BF16 results shrank for the same reason.

**Cheapest option per model and workload, 90 users at 30 tok/s per user (₹ lakh/month)**

| Model | Workload | Own room (Baner) | GPU / precision / nodes | Colo | Rent (incl. staff) | Rent GPU | Buy breakeven vs rent (months) | Own-room range (throughput uncertainty) |
|---|---|---|---|---|---|---|---|---|
| GLM-5.3 | chat | 18.8 | h200 / fp8 / 1 | 17.2 (h200) | 16.4 | h200 fp8 | 46 | 18.8-30.3 (+/-15%; nodes 1-2) |
| GLM-5.3 | mixed | 20.4 | mi355x / fp8 / 1 | 18.7 (mi355x) | 19.6 | mi355x fp8 | 37 | 20.4-20.4 (+/-10%; nodes 1-1) |
| GLM-5.3 | agent_128k | 33.4 | mi355x / fp8 / 2 | 30.9 (mi355x) | 36.0 | mi355x fp8 | 31 | 33.4-33.4 (+/-10%; nodes 2-2) |
| GLM-5.3 | agent_1m | 34.1 | mi355x / fp8 / 2 | 31.6 (mi355x) | 36.0 | mi355x fp8 | 32 | 34.1-34.1 (+/-10%; nodes 2-2) |
| GLM-5.3 | stress_1m | 63.6 | mi355x / fp8 / 4 | 59.5 (mi355x) | 68.8 | mi355x fp8 | 32 | 63.6-72.7 (+/-10%; nodes 4-5) |
| DeepSeek V4 Pro | chat | 20.3 | mi355x / native / 1 | 18.6 (mi355x) | 19.6 | mi355x native | 37 | 20.3-33.3 (+/-25%; nodes 1-2) |
| DeepSeek V4 Pro | mixed | 33.3 | mi355x / native / 2 | 30.8 (mi355x) | 36.0 | mi355x native | 31 | 20.3-33.3 (+/-25%; nodes 1-2) |
| DeepSeek V4 Pro | agent_128k | 33.3 | mi355x / native / 2 | 30.8 (mi355x) | 36.0 | mi355x native | 31 | 33.3-46.3 (+/-25%; nodes 2-3) |
| DeepSeek V4 Pro | agent_1m | 46.4 | mi355x / native / 3 | 43.0 (mi355x) | 52.5 | mi355x native | 29 | 33.4-59.4 (+/-25%; nodes 2-4) |
| DeepSeek V4 Pro | stress_1m | 59.3 | mi355x / native / 4 | 55.1 (mi355x) | 68.9 | mi355x native | 29 | 46.3-72.7 (+/-25%; nodes 3-5) |
| Kimi K2.7 Code | chat | 18.8 | h200 / native / 1 | 17.2 (h200) | 16.4 | h200 native | 46 | 18.8-30.3 (+/-15%; nodes 1-2) |
| Kimi K2.7 Code | mixed | 33.4 | mi355x / native / 2 | 30.8 (mi355x) | 36.0 | mi355x native | 31 | 33.4-46.4 (+/-25%; nodes 2-3) |
| Kimi K2.7 Code | agent_128k | 46.4 | mi355x / fp8 / 3 | 43.0 (mi355x) | 52.5 | mi355x fp8 | 29 | 46.4-72.8 (+/-25%; nodes 3-5) |
| Kimi K2.7 Code | agent_1m | 72.9 | mi355x / fp8 / 5 | 67.4 (mi355x) | 85.3 | mi355x fp8 | 28 | 59.4-98.8 (+/-25%; nodes 4-7) |
| Kimi K2.7 Code | stress_1m | 178.5 | mi355x / fp8 / 13 | 164.6 (mi355x) | 216.7 | mi355x fp8 | 27 | 138.1-243.9 (+/-25%; nodes 10-18) |

The table makes three points. First, **colocation is cheaper than an own room in every row**. It skips the server-room build and gets power at a pass-through rate near ₹10/kWh. It is the cheapest option overall except for H200 chat. Second, **buying beats renting once a workload fills two or more nodes**. Third, **on single-node deployments, renting edges out an own room**: ₹16.4 vs ₹18.8 lakh for chat on H200, and ₹19.6 vs ₹20.4 lakh for GLM-5.3 mixed. Their breakeven of 37–46 months falls beyond a 3-year horizon. Per seat, a 128k agent deployment of GLM-5.3 or DeepSeek works out to roughly ₹37k per user per month (₹33.4 lakh ÷ 90). In dollars that is about **$35k a month** for the whole deployment.

How fast each user wants tokens moves the bill more than how many users there are. The table below repeats the own-room cost (nodes in brackets) at the model's three sizing points. At 50 users and 20 tok/s, **almost everything fits on one node for about ₹20 lakh**. Raising per-user speed from 30 to 50 tok/s roughly doubles agent costs, because each node has to run smaller batches to hold the higher speed.

| Model | Workload | 50 users, 20 tok/s | 90 users, 30 tok/s | 90 users, 50 tok/s |
|---|---|---|---|---|
| GLM-5.3 | chat | 18.8 (1 h200) | 18.8 (1 h200) | 33.3 (2 mi355x) |
| GLM-5.3 | mixed | 20.4 (1) | 20.4 (1) | 33.4 (2) |
| GLM-5.3 | agent_128k | 20.4 (1) | 33.4 (2) | 59.4 (4) |
| GLM-5.3 | agent_1m | 33.7 (2) | 34.1 (2) | 60.1 (4) |
| DeepSeek V4 Pro | chat | 20.3 (1) | 20.3 (1) | 33.3 (2) |
| DeepSeek V4 Pro | mixed | 20.3 (1) | 33.3 (2) | 46.3 (3) |
| DeepSeek V4 Pro | agent_128k | 20.3 (1) | 33.3 (2) | 72.8 (5) |
| DeepSeek V4 Pro | agent_1m | 20.4 (1) | 46.4 (3) | 72.8 (5) |
| Kimi K2.7 Code | chat | 18.8 (1 h200) | 18.8 (1 h200) | 20.4 (1 mi355x) |
| Kimi K2.7 Code | mixed | 20.4 (1) | 33.4 (2) | 46.4 (3) |
| Kimi K2.7 Code | agent_128k | 20.4 (1) | 46.4 (3) | 98.8 (7) |
| Kimi K2.7 Code | agent_1m | 33.4 (2) | 72.9 (5) | 125.3 (9) |

Unless marked h200, every entry above is on MI355X. The stress_1m case reaches **₹401.3 lakh/month (30 nodes) for Kimi at 90 users and 50 tok/s**. It shows what happens if nobody compacts, not a configuration anyone should build.

## Auto-summarisation makes a 1M ceiling affordable

Every agent workload uses the same compaction design. The effective trigger is **T = min(requested trigger, native window − 40,000-token reserve)**. The reserve leaves room for the summary prompt and the maximum output. Context grows in a saw-tooth from a floor (system prompt plus summary plus pinned files: 16k at a 128k trigger, 32k at 1M) up to T, then drops back to the floor. The average context per active sequence is therefore (T + floor) / 2. The design starts the summary in the background at about **0.7T**, so it is ready when context hits T and the swap doesn't make the user wait. The model counts the cost of writing summaries (4,000–8,000 output tokens per compaction) and of re-prefilling the floor afterwards. It does not count any delay, because background compaction removes it.

Kimi is where the formula bites. Its native window is **262,144 tokens**, already stretched with YaRN ×64, and there is no supported extension beyond it ([Kimi K2.7 Code config](https://huggingface.co/moonshotai/Kimi-K2.7-Code/raw/main/config.json)). So a request for a 1M trigger becomes **T = 222,144** in practice. Kimi reaches a "1M ceiling" only by chaining summaries across many ~222k windows. GLM-5.3 has a **native 1,048,576-token window with no RoPE scaling** ([vLLM GLM-5.3 recipe](https://github.com/vllm-project/recipes/blob/main/models/zai-org/GLM-5.3.yaml)). DeepSeek V4 Pro reaches 1,048,576 via YaRN ×16 ([DeepSeek-V4-Pro config](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/raw/main/config.json)). Both therefore compact at 960,000.

| Model | Workload | Effective trigger T | Mean ctx | Extra output for summaries | Own room ₹ lakh/mo | Nodes |
|---|---|---|---|---|---|---|
| GLM-5.3 | agent_128k | 128,000 | 72,000 | 30% | 33.4 (mi355x fp8) | 2 |
| GLM-5.3 | agent_1m | 960,000 | 496,000 | 7% | 34.1 (mi355x fp8) | 2 |
| GLM-5.3 | stress_1m | 960,000 | 1,000,000 | 0% | 63.6 (mi355x fp8) | 4 |
| DeepSeek V4 Pro | agent_128k | 128,000 | 72,000 | 30% | 33.3 (mi355x native) | 2 |
| DeepSeek V4 Pro | agent_1m | 960,000 | 496,000 | 7% | 46.4 (mi355x native) | 3 |
| DeepSeek V4 Pro | stress_1m | 960,000 | 1,000,000 | 0% | 59.3 (mi355x native) | 4 |
| Kimi K2.7 Code | agent_128k | 128,000 | 72,000 | 30% | 46.4 (mi355x fp8) | 3 |
| Kimi K2.7 Code | agent_1m | 222,144 | 127,072 | 35% | 72.9 (mi355x fp8) | 5 |
| Kimi K2.7 Code | stress_1m | 222,144 | 262,144 | 0% | 178.5 (mi355x fp8) | 13 |

The trigger involves a trade-off. Summaries are not free: at a 128k trigger they add **30% more output tokens**, against 7% at 960k. For Kimi, whose saw-tooth is short, they add 35%. On the other hand, a lower trigger cuts the average context almost sevenfold (72,000 vs 496,000 tokens), so each node can batch more users.

What the trade-off is worth depends on the attention design. For GLM-5.3, raising the trigger from 128k to 1M costs only **₹0.7 lakh/month** (33.4 → 34.1, still two nodes). Its DSA sparse attention picks the top 2,048 tokens and its FP8 latent cache is about 54.7 KB/token ([vLLM GLM-5.3 recipe](https://github.com/vllm-project/recipes/blob/main/models/zai-org/GLM-5.3.yaml)). For DeepSeek V4 Pro on MI355X the move adds a node (₹33.3 → ₹46.4 lakh). On B200 the same move costs only ₹0.1 lakh (₹51.0 → ₹51.1, see the NVIDIA-only table). That fits its decode speed, which stays nearly flat out to 900K context, falling less than 10% ([LMSYS DeepSeek V4 Day 0](https://www.lmsys.org/blog/2026-04-25-deepseek-v4/)). For Kimi the cost goes from three nodes to five (₹46.4 → ₹72.9 lakh). Its dense MLA attention reads the whole cache on every step and has no sparse indexer ([Kimi config](https://huggingface.co/moonshotai/Kimi-K2.7-Code/raw/main/config.json)). The practical choice is to make **128k the default trigger**. A per-session opt-in to near-1M is cheap on GLM-5.3 and worth costing case by case on the other two.

Z.ai's own card supports this. Its long-horizon coding evals ran at 1M context, while one tool-use eval capped context at 300,000 with "a context management strategy" ([GLM-5.3 card](https://huggingface.co/zai-org/GLM-5.3)). Summarisation is a legitimate operating mode, not a hack.

## Native precision is the only sensible precision

Each model ships in one or two official precisions, and moving away from them only costs money. **GLM-5.3** ships natively in FP8 (755,617,140,416 bytes), with an official BF16 repository at 1,506,659,919,872 bytes ([GLM-5.3-BF16 index](https://huggingface.co/zai-org/GLM-5.3-BF16/blob/main/model.safetensors.index.json)). SGLang states that "FP8 is the recommended deployment" ([SGLang GLM-5.3 cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5.3)). **DeepSeek V4 Pro** ships as FP4 experts plus FP8 for everything else, and the official 0813 release is 892,727,580,904 bytes ([DeepSeek-V4-Pro-0813](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813)). There is **no official BF16 release**; only Base (FP8 mixed) and Instruct (FP4+FP8) exist ([DeepSeek inference README](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/inference/README.md)). **Kimi K2.7 Code** ships only as **INT4 quantisation-aware-trained weights at 595,148,192,736 bytes**, with no BF16 or FP8 release ([Kimi K2.7 Code card](https://huggingface.co/moonshotai/Kimi-K2.7-Code)).

For DeepSeek and Kimi, BF16 (and FP8 for Kimi) is therefore an **upcast**: it pads trained low-bit weights into a wider format with no gain in quality. FP32 is not deployable for any of the three, because vLLM and SGLang have no FP32 kernels for FlashMLA, DSA, DeepGEMM or fused MoE. The model costs FP32 only to show the memory bill.

**Precision comparison: agent_128k, 90 users, 30 tok/s, cheapest GPU per precision**

| Model | Precision | Weights GB | Feasible | GPU | Nodes | Own room ₹ lakh/mo | Rent ₹ lakh/mo | KV per user at mean ctx (GB) |
|---|---|---|---|---|---|---|---|---|
| GLM-5.3 | fp8 | 756 | yes | mi355x | 2 | 33.4 | 36.0 | 3.9 |
| GLM-5.3 | bf16 | 1,507 | yes | mi355x | 3 | 46.5 | 52.5 | 7.0 |
| GLM-5.3 | fp32 | 3,013 | NO (memory/cost only) | mi355x | 24 | 348.9 | 397.3 | 13.9 |
| DeepSeek V4 Pro | native | 893 | yes | mi355x | 2 | 33.3 | 36.0 | 0.4 |
| DeepSeek V4 Pro | fp8 | 1,606 | yes | mi355x | 3 | 46.3 | 52.5 | 0.4 |
| DeepSeek V4 Pro | bf16 | 3,301 | yes | mi355x | 5 | 78.2 | 85.3 | 0.7 |
| DeepSeek V4 Pro | fp32 | 6,602 | NO (memory/cost only) | mi355x | 40 | 575.8 | 659.9 | 1.4 |
| Kimi K2.7 Code | native | 595 | yes | mi355x | 5 | 72.8 | 85.3 | 2.5 |
| Kimi K2.7 Code | fp8 | 1,026 | yes | mi355x | 3 | 46.4 | 52.5 | 2.5 |
| Kimi K2.7 Code | bf16 | 2,053 | yes | mi355x | 12 | 178.2 | 200.2 | 5.1 |
| Kimi K2.7 Code | fp32 | 4,106 | NO (memory/cost only) | mi355x | 183 | 2,606.7 | 3,010.0 | 10.1 |

Two results stand out. The first is that **Kimi's FP8 upcast is cheaper to serve than its native INT4** (three nodes against five). The model runs native INT4 through W4A16 kernels, which do the maths in BF16, so INT4 gets half the compute rate of FP8. On MI355X it is worse still: vLLM's W4A16 MoE path there "does not support expert parallelism" ([vLLM Kimi K2.7 Code recipe](https://github.com/vllm-project/recipes/blob/main/models/moonshotai/Kimi-K2.7-Code.yaml)). FP8 Kimi is a speed choice, not a quality one, and its accuracy should be checked against the INT4 original before it goes into production.

The second is that **Kimi in BF16 needs 12 MI355X nodes** (₹178.2 lakh/month to own, ₹200.2 lakh to rent), four times as many as its FP8 upcast. That is more than a Baner office's LT connection can supply: an HT connection becomes necessary at the 11th MI355X node (see the power section below).

DeepSeek's tiny cache, 0.4 GB per user at 72k tokens, comes from its compressed CSA/HCA attention: 9.62 GiB per 1M-token sequence in BF16, against 83.9 GiB for a V3.2-style stack ([vLLM DeepSeek V4 blog](https://vllm.ai/blog/2026-04-24-deepseek-v4)). That is why DeepSeek fits 50 users on one node in every workload except the stress case. The deployments use an FP8 KV cache, which costs a little accuracy. On Kimi-K2.5, vLLM found the drop "modest in aggregate AUC but consistently negative across context lengths" ([vLLM FP8 KV-cache post](https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2026-04-22-fp8-kvcache.md)).

## Buying wins only while the GPUs stay busy

The reference configuration below shows where the money goes. It is GLM-5.3 FP8 on two 8×B200 nodes in the Baner room, coding agents at a 128k trigger, 90 users at 30 tok/s, run 24/7. **Capital recovery is two-thirds of the monthly bill.** Of ₹36,25,492.90 all-in, ₹24,28,969.03 is the capex charge, against ₹5,25,698.03 for electricity and ₹5,50,000 for staff.

| Item | ₹ | In lakh/crore |
|---|---|---|
| Landed hardware (servers, network, storage; IGST credited) | 80,620,625.54 | ₹8.06 crore |
| Facility build (electrical, UPS, DG, cooling, civil, fire, racks) | 5,181,384.01 | ₹51.8 lakh |
| Total capex | 85,802,009.55 | ₹8.58 crore (≈ $0.90M) |
| Capex as monthly charge | 2,428,969.03 | ₹24.3 lakh |
| Electricity / month | 525,698.03 | ₹5.26 lakh |
| DG diesel / month | 13,806.52 | |
| Staff / month | 550,000.00 | ₹5.5 lakh |
| Space rent / month | 10,200.00 | |
| Insurance / month | 53,626.26 | |
| Hardware AMC (avg) / month | 0.00 | inside 3-yr warranty |
| Opex / month | 1,196,523.87 | ₹12.0 lakh |
| All-in / month | 3,625,492.90 | ₹36.3 lakh |
| IT load kW (max) | 28.60 | |
| Contract demand kVA | 49.61 | well under the 187 kVA LT limit |
| Per-user tok/s at peak | 32.75 | |
| Output tokens / month | 593,598,255.07 | |
| ₹ per 1M output tokens (own room) | 6,107.65 | |
| Compaction extra output fraction | 0.30 | |

Each lever then moves the same configuration as follows.

| Lever change | Own room ₹ lakh/mo | Colo | Rent (today) | Rent (avg over horizon) | Nodes |
|---|---|---|---|---|---|
| Base (24/7, ITC, N, 3 yr, commercial tariff) | 36.3 | 33.2 | 47.4 | 47.4 | 2 |
| Business hours only | 32.4 | 31.3 | 26.9 | 26.9 | 2 |
| No GST input credit | 40.7 | 38.5 | 55.3 | 55.3 | 2 |
| N+1 spare node | 51.1 | 46.6 | 69.5 | 69.5 | 3 |
| 5-year horizon | 31.3 | 28.8 | 47.4 | 47.4 | 2 |
| Registered IT/ITeS unit (industrial tariff, duty-exempt) | 34.0 | 33.2 | 47.4 | 47.4 | 2 |
| Rental prices fall 25%/yr | 36.3 | 33.2 | 47.4 | 37.3 | 2 |
| Resale 0% (instead of 20%) | 40.1 | 37.0 | 47.4 | 47.4 | 2 |
| TP attention instead of DP-attention | 54.4 | 49.9 | 69.4 | 69.4 | 3 |

**24/7 vs business hours.** This is the only lever that makes renting cheapest: ₹26.9 lakh to rent against ₹32.4 lakh to own. The saving holds only on hourly on-demand capacity that is destroyed or stopped overnight. Monthly bare metal, reserved terms and DigitalOcean's powered-off-but-billed droplets save nothing ([DigitalOcean GPU pricing](https://www.digitalocean.com/pricing/gpu-droplets)). E2E bills hourly with no minimum ([E2E pricing](https://www.e2enetworks.com/pricing.md)). Yotta's B200 bare metal starts at a monthly term ([Yotta bare metal](https://shakticloud.ai/bare-metal-service/)).

**N vs N+1.** A spare node adds 41% to an own room (₹36.3 → ₹51.1 lakh). With only two nodes, one failed GPU tray takes out half the capacity. A cheaper hedge is a 4-hour onsite SLA plus emergency cloud burst. Paying for a third node all year is the expensive one.

**3 vs 5 years.** Five years lowers the own-room cost to ₹31.3 lakh, even after hardware AMC at 10% a year in years 4–5. It also assumes the GPUs stay useful for that long. The resale assumption already hedges: 20% at the end of the horizon, against reported H100 residuals of **40–75% at 36 months and 25–35% at 60+ months** ([Mercatus H100 resale](https://www.mercatus-ai.com/blog/h100-resale-value)).

**Rental price trend.** Buying is a bet that rental prices won't collapse. If rents fell 25% a year, average rent over the horizon would be ₹37.3 lakh, close to the ₹36.3 lakh own-room cost. The 2026 market points the other way. GPU rental is up about 18% year on year ([GetDeploying index](https://getdeploying.com/gpu-price-index)), and Nebius raised on-demand prices 17–21% on 1 Oct 2026 ([UsagePricing](https://usagepricing.com/blueprint/activity/nebius-ai-2026-09-24-gpu-price-increase)). The model therefore assumes no decline.

**Engine configuration.** Serving with tensor-parallel attention instead of DP-attention plus expert parallelism raises the cost by about half, from 2 to 3 nodes and ₹36.3 to ₹54.4 lakh. DP-attention is the recipe default for these MoE models ([SGLang GLM-5.3 cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5.3); [vLLM DeepSeek-V4-Pro recipe](https://github.com/vllm-project/recipes/blob/main/models/deepseek-ai/DeepSeek-V4-Pro.yaml)). Staff who know it are worth more than any hardware discount.

**The API as a sanity line.** The comparison below is my own arithmetic, using the model's agent mix of about 230 cached and 20 uncached input tokens per output token. At Z.ai's list prices of $1.40 input, $0.26 cached and $4.40 output per 1M tokens ([Z.ai pricing](https://docs.z.ai/guides/overview/pricing)), a million GLM-5.3 output tokens costs about $92, or roughly **₹8,776**. The own room delivers them at **₹6,107.65**, about 30% less. DeepSeek's own API, at $0.66 / $0.022 / $1.98 off-peak and double at peak ([DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing)), comes to roughly ₹1,926–3,853 per million output tokens. That is 1.6–3.2 times cheaper than even the reference own room. So the case for self-hosting is **keeping code and data on Stark's own hardware, plus a predictable fixed bill**. It is not the cheapest price per token.

## Pune power, tax and space shape the facility bill

**Electricity tariff.** Stark Digital pays the commercial tariff because it is not registered, and this is the biggest controllable item in running costs. Under MERC's post-remand order for FY2026-27, **HT-II commercial is ₹650/kVA/month plus ₹13.72 + ₹0.81 = ₹14.53/kVAh**. HT-I(A) industrial is **₹650 plus ₹8.44 + ₹0.81 = ₹9.25/kVAh**, and data centres are classed as industrial ([MERC Case 75 of 2025](https://www.mahadiscom.in/wp-content/uploads/2026/07/Tariff-Order_Case-No.-75-of-2025-dated-25th-March-2026.pdf)). On top of that, commercial consumers pay **21% electricity duty** ([MSEDCL Circular 273](https://www.mahadiscom.in/consumer/wp-content/uploads/2018/02/Comm_Cir_273.pdf)). New IT/ITeS units in designated IT parks are exempt for 10 years in Zone I, and data-centre units for 20 years ([TeamLease on the 22 Jun 2026 notification](https://teamleaseregtech.com/updates/article/57168/govt-of-maharashtra-issued-a-notification-regarding-electricity-duty-e/)).

**Registration.** Registering as an IT/ITeS unit brings the industrial tariff and the duty exemption, and saves **₹2.3 lakh/month** on the reference room (₹36.3 → ₹34.0 lakh). It has no effect on colocation or cloud. The policy requires IT/ITeS turnover above 75% of total turnover ([Taxguru on the IT/ITeS Policy 2023](https://taxguru.in/corporate-law/maharashtra-information-technology-enabled-services-policy-2023.html)). MSEDCL applies the industrial tariff only after a field inspection and a registration in the unit's own name ([MSEDCL Circular 212](https://www.mahadiscom.in/consumer/wp-content/uploads/2018/02/Comm_Cir_212.pdf)).

| FY2026-27 tariff | Demand ₹/kVA/month | Energy + wheeling ₹/kVAh | Electricity duty | All-in ₹/kWh (flat 24×7 load, notes' estimate) |
|---|---|---|---|---|
| HT-II commercial (Stark today) | 650 | 14.53 | 21% | 18.9–19.7 |
| HT-I(A) industrial (registered IT/ITeS or DC unit) | 650 | 9.25 | 0% if exempt, else 7.5% | 10.3–11.9 |
| LT-II(C) commercial >50 kW | 550 | 16.42 | 21% | 20.8–21.7 |

**LT or HT connection.** The **LT limit in Municipal Corporation areas is about 150 kW / 187 kVA** ([MERC SoP explanatory memorandum](https://merc.gov.in/wp-content/uploads/2022/07/Explanatory-Memorandum_SoP_2017.pdf)). The reference room needs only 49.61 kVA, so it stays on LT. The model's ratios give about 24.8 kVA per air-cooled B200 node (PUE 1.7) and about 18.5 kVA per liquid-cooled MI355X node (PUE 1.25). On my arithmetic, **HT becomes necessary at the 8th air-cooled B200 node or the 11th MI355X node**. That covers Kimi's 13-node stress case, the 15-node NVIDIA-only Kimi stress case and any NVL72 rack. An HT connection adds about ₹17.4 lakh fixed (service connection, metering, RMU, cabling, CEIG) plus a transformer at about ₹1,400/kVA. MSEDCL also takes a refundable security deposit of about two months' bills.

**Backup power.** Outages are a real factor in Baner, where residents reported **2–3 hours a day in summer 2025** ([Pune Pulse](https://www.mypunepulse.com/?p=90027)). Diesel was ₹98.63/L on 7 Sep 2026 ([energy.thecore.in](https://energy.thecore.in/fuel/petrol-price/pune)), so DG power costs about ₹24–28/kWh in fuel alone. The model sizes Li-ion UPS for 10 minutes, a CPCB IV+ DG set and about 15 outage hours a month.

**Cooling and space.** MI355X systems are 1,400 W-per-GPU, direct-liquid-cooled 4U boxes that **need facility water and a CDU** ([Pantheon MI355X](https://pantheon.run/hardware/amd-instinct-mi355x-supermicro)). None of Pune's 22 colocation facilities advertises liquid cooling ([Baxtel Pune](https://baxtel.com/data-center/pune)). Navi Mumbai does: Sify claims 130+ kW per rack ([Sify Mumbai](https://www.sifytechnologies.com/data-center/mumbai-data-center/)). So the MI355X colo figures assume Navi Mumbai, priced at 1.55× the Pune rate of ₹7,688/kW-month ([JM Financial](https://jmflresearch.com/JMnew/JMCRM/analystreports/pdf/Data-Centre-101_27Mar25.pdf)). Floor loading is the hidden limit for an own room. Office slabs are designed for **2.5–3.5 kN/m²** ([Infralens IS 875](https://infralens.in/handbook/live-loads)), while a loaded rack puts about 14–20 kN/m² on its footprint. The model includes a structural audit and a steel plinth for every rack.

**Import duty and GST.** Tax is mostly a cash-flow item when ITC is claimed. **GPU servers, GPU boards and storage carry 0% basic customs duty** under ITA-1, with only 18% IGST ([EximPe HS 8471 49 00](https://eximpe.com/hsncode-finder/84714900)). The dutiable items are facility gear. Ethernet switches were cut to 10% in Budget 2025 ([TRU letter 2025-26](https://www.indiabudget.gov.in/budget2025-26/doc/cen/dojstru1.pdf)). UPS is 20% unless the ITA exemption is accepted, and CESTAT has settled that in importers' favour ([Taxguru](https://taxguru.in/custom-duty/revenue-withdraws-ups-customs-exemption-appeals-issue-settled-cestat-mumbai.html)).

| Item (HS) | BCD | Stays in cost with ITC | Stays in cost without ITC |
|---|---|---|---|
| GPU servers, boards, storage, DIMMs (8471 / 8473 30) | 0% | 0% | 18.00% |
| Ethernet / IB switches (8517 62 90) | 10% + 1% SWS | 11.00% | 30.98% |
| Optics and routers (classification disputed) | 10–20% | 11–22% | 30.98–43.96% |
| UPS (8504 40) | 20%, or 0% with ITA claim | 22.00% or 0% | 43.96% or 18.00% |
| Li-ion batteries, precision AC (8507 60 / 8415) | 20% | 22.00% | 43.96% |
| DG set >75 kVA (8502 12/13) | 7.5% | 8.25% | 27.74% |
| Racks as furniture (9403) | 20% + 5% AIDC | 25.00% | 47.50% |
| Civil works, embedded wiring, building HVAC (works contract) | n/a, 18% GST | 18% (blocked) | 18% |

**What happens without ITC.** Losing input credit costs the reference room **₹4.4 lakh/month** (₹36.3 → ₹40.7 lakh) and the rental option **₹7.9 lakh** (₹47.4 → ₹55.3 lakh). Rent takes the bigger hit because GST applies to every rupee of it, while electricity carries no GST. With ITC, cloud GST is also neutral, whether it is charged forward by an Indian entity or self-assessed under reverse charge on foreign billing ([AWS India tax help](https://aws.amazon.com/tax-help/india/)). Civil works and building services stay blocked under Section 17(5). The Finance Act 2025 retrospectively narrowed the "plant or machinery" escape route opened by *Safari Retreats* ([BDO](https://bdo.in/en-gb/insights/alerts-updates/indirect-tax-alert-effective-dates-for-implementation-of-the-provisions-of-the-finance-act-2025)). Buy server-room equipment on separate supply invoices. Servers still depreciate at **40% WDV** under the Income-tax Act 2025 ([Taxguru](https://taxguru.in/?p=1036553)).

**Paperwork and lead time.** Importing servers under HS 8471 needs a DGFT import authorisation, and the current authorisations expire on **31 Dec 2026** ([Taxguru on IMS](https://taxguru.in/dgft/import-authorisation-mandated-restricted-hardware-remains-ims-2026.html)). Indian enterprise lead times run 3–9 months ([Cyfuture](https://cyfuture.ai/blog/nvidia-b300-gpu-price-in-india)), and server DRAM roughly doubled in Q1 2026 ([ServnetUK](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026)). A purchase decision now means a delivery in 2027 under an import regime that hasn't been published yet.

**Staff.** The model staffs the own room 24/7 with one MLOps engineer (₹28 LPA), one sysadmin (₹9 LPA) and four shift operators (₹4.5 LPA), loaded by 1.2×, for ₹5.5 lakh/month. Business hours cost ₹3.7 lakh, colocation ₹4.25 lakh (the operator runs the facility) and cloud ₹3.2 lakh (one MLOps engineer with on-call). The bands come from Pune salary surveys ([OwnYourCareer MLOps](https://www.ownyourcareer.in/careers/mlops-engineer/salaries); [Payscale Linux SA Pune](https://www.payscale.com/research/IN/Job=Linux_System_Administrator/Salary/68d9e97c/Pune)). Subsidised IndiaAI compute is not an option: eligibility covers academia, DPIIT startups and MSMEs, and government entities ([IndiaAI compute portal](https://compute.indiaai.gov.in/)), which a general IT services company does not appear to meet.

## MI355X tops the tables, but plan on B200 numbers

AMD's MI355X has 288 GB of HBM per GPU and wins most rows above, but both of its prices are weak. The **purchase price is inferred at $330,000 per 8-GPU node**. The only listing found is an EU Supermicro price of **€261,442.82 ex-VAT**, whose configuration could not be checked because the page returned HTTP 403 ([smicro.eu](https://smicro.eu/supermicro-as-4126gs-nmr-lcc-g1-2)). The **rental price is TensorWave's "from" contract rate of $2.95/GPU-hour**, taken from an aggregator because TensorWave's own page returned 404 ([GetDeploying MI355X](https://getdeploying.com/gpus/amd-mi355x)). No Indian provider rents MI355X.

The software is also young. DeepSeek V4 Pro on MI355X went from **0.93 tok/s/user on day 0 to 16.79 tok/s/user 26 days later**, and at that point B200 still sat about 5× higher in the 15–30 tok/s/user band ([InferenceX MI355X DSv4](https://inferencex.semianalysis.com/blog/mi355x-deepseek-v4-pro-sglang-110x-in-26-days)). On October's agentic benchmark MI355X managed **37,438 tok/s/GPU against 65,134 for B200** ([InferenceX DSv4 ranking](https://inferencex.semianalysis.com/rankings/fastest-gpu-for-deepseek-v4)). The model's DeepSeek-on-MI355X and Kimi-on-MI355X pairs inherit their calibration from B200, so **those results are probably optimistic**. AMD's ATOM engine "has not yet served production tokens" for Kimi ([InferenceX Kimi B200 vs MI355X](https://inferencex.semianalysis.com/compare/kimi-k26-b200-vs-mi355x)), and Kimi on AMD is limited to TP ≤ 4 in SGLang ([SGLang Kimi-K2.6 cookbook](https://cookbook.sglang.io/autoregressive/Moonshotai/Kimi-K2.6)). GLM-5.3 on MI355X is the exception: it is a measured pair, with residuals of −1% and 0%. For budgeting, use the NVIDIA-only table and treat MI355X as upside to confirm with a quote and a benchmark.

**NVIDIA-only cheapest option, 90 users at 30 tok/s (MI355X excluded, ₹ lakh/month)**

| Model | Workload | Own room | GPU / precision / nodes | Colo | Rent (incl. staff) | Rent GPU |
|---|---|---|---|---|---|---|
| GLM-5.3 | chat | 18.8 | h200 / fp8 / 1 | 17.2 (h200) | 16.4 | h200 fp8 |
| GLM-5.3 | mixed | 32.5 | h200 / fp8 / 2 | 30.1 (h200) | 29.5 | h200 fp8 |
| GLM-5.3 | agent_128k | 36.3 | b200 / fp8 / 2 | 33.2 (b200) | 42.7 | h200 fp8 |
| GLM-5.3 | agent_1m | 55.1 | b200 / fp8 / 3 | 50.5 (b200) | 55.8 | h200 fp8 |
| GLM-5.3 | stress_1m | 101.6 | b300 / fp8 / 5 | 94.4 (b300) | 161.1 | h200 fp8 |
| DeepSeek V4 Pro | chat | 21.8 | b200 / native / 1 | 19.8 (b200) | 25.3 | b200 native |
| DeepSeek V4 Pro | mixed | 36.2 | b200 / native / 2 | 33.1 (b200) | 42.7 | h200 native |
| DeepSeek V4 Pro | agent_128k | 51.0 | b200 / native / 3 | 46.5 (b200) | 69.5 | b200 native |
| DeepSeek V4 Pro | agent_1m | 51.1 | b200 / native / 3 | 46.6 (b200) | 69.5 | b200 native |
| DeepSeek V4 Pro | stress_1m | 80.3 | b200 / native / 5 | 73.2 (b200) | 113.7 | b200 native |
| Kimi K2.7 Code | chat | 18.8 | h200 / native / 1 | 17.2 (h200) | 16.4 | h200 native |
| Kimi K2.7 Code | mixed | 36.2 | b200 / native / 2 | 33.2 (b200) | 47.4 | b200 native |
| Kimi K2.7 Code | agent_128k | 65.5 | b200 / fp8 / 4 | 59.9 (b200) | 91.6 | b200 fp8 |
| Kimi K2.7 Code | agent_1m | 94.8 | b200 / fp8 / 6 | 86.6 (b200) | 135.8 | b200 fp8 |
| Kimi K2.7 Code | stress_1m | 227.7 | b200 / fp8 / 15 | 206.6 (b200) | 334.7 | b200 fp8 |

On NVIDIA hardware, **renting costs roughly 1–43% more than owning** for agents (₹42.7 vs ₹36.3 lakh for GLM-5.3 at 128k, but only ₹55.8 vs ₹55.1 lakh at 1M, both rented on H200). For the mixed workload on two H200 nodes, renting is actually cheapest (₹29.5 lakh rent vs ₹32.5 own room and ₹30.1 colo), so renting can win at two nodes as well as one. For NVIDIA, India's cheapest rents are Yotta's B200 at ₹473/GPU-hour on a monthly term and ₹378 on 3 years ([Yotta bare metal](https://shakticloud.ai/bare-metal-service/)), against E2E's ₹759 on demand ([E2E pricing](https://www.e2enetworks.com/pricing.md)). Note one change in ranking: for DeepSeek V4 Pro, a 1M ceiling costs almost nothing extra on B200 (₹51.0 → ₹51.1 lakh), while on MI355X it adds a node. Long-context DeepSeek is a B200 job.

**Throughput uncertainty.** None of these throughput figures was benchmarked by Stark. The model fits a per-sequence overhead to **12 published InferenceX and Lambda points**, with a **mean absolute residual of 2.9% and a maximum of 17.2%** (GLM-5.3 on H200). Six model/GPU pairs are measured: GLM-5.3 on B200, MI355X and H200; Kimi on H200 and B200; DeepSeek on B200. Every other pair borrows from its nearest measured neighbour and carries **±25%**, which is where the range column in the first table comes from. The bands are widest where nodes are many. Kimi agent_1m spans **₹59.4–98.8 lakh (4–7 nodes)** and DeepSeek agent_1m spans **₹33.4–59.4 lakh (2–4 nodes)**. Published numbers also move quickly, with DeepSeek on GB300 improving about 5× between April and June 2026 ([PyTorch / SGLang GB300](https://pytorch.org/blog/serving-deepseek-v4-on-gb300-with-sglang-5x-higher-throughput-at-the-same-interactivity-since-day-0/)). A one-week rented benchmark of the shortlisted model/GPU pair on Stark's own agent traces is the cheapest way to narrow the band.

## Chandra OCR 2 is cheap to run but needs a licence

Chandra OCR 2 is a 4B-class model (5,295,564,288 stored parameters, including a duplicated output head) that runs on a single GPU. Datalab's only measured figure is **1.44 pages/s on one H100 with 96 concurrent requests** on the hard olmOCR mix, and it estimates about 2 pages/s on real-world documents ([Chandra OCR 2 card](https://huggingface.co/datalab-to/chandra-ocr-2)). Speeds on L40S and other GPUs are scaled from that H100 point by memory bandwidth, not measured. **Renting wins at every volume tier**, and the gap closes only at 50,000 pages an hour.

| Tier (pages/h peak) | GPU / precision | GPUs | Rent ₹/mo | Bought (existing room) ₹/mo | ₹ per 1k pages, rent / bought |
|---|---|---|---|---|---|
| light (1,000) | l40s / fp8 | 1 | 74,460 | 227,277 | 676.9 / 2,066.2 |
| medium (10,000) | h100 / fp8 | 2 | 310,980 | 496,518 | 282.7 / 451.4 |
| heavy (50,000) | h100 / fp8 | 9 | 1,399,410 | 1,451,327 | 254.4 / 263.9 |

The licence matters more than the GPU bill. The code is Apache 2.0, but the weights use a modified OpenRAIL-M licence. It forbids commercial use by any entity that "generated more than two million US Dollars ($2,000,000) in gross revenue in the prior year" or raised more than $2M in funding, and any use that competes with Datalab ([Chandra LICENSE](https://huggingface.co/datalab-to/chandra-ocr-2/blob/main/LICENSE)). The README says "commercial self-hosting requires a license" ([Datalab GitHub](https://github.com/datalab-to/chandra)). $2M is about ₹19 crore at ₹95.18/USD. If Stark Digital is above that, it needs a paid Datalab licence on top of the costs above, and that fee is unpublished. By contrast, the three coding models' licences are permissive for a company of Stark's size. DeepSeek is MIT. Kimi requires UI attribution only above 100M monthly active users or $20M monthly revenue ([Kimi LICENSE](https://huggingface.co/moonshotai/Kimi-K2.7-Code/blob/main/LICENSE)). GLM-5.3 adds a security review only for Model-as-a-Service operators with more than $10B in revenue ([GLM-5.3 LICENSE](https://huggingface.co/zai-org/GLM-5.3/blob/main/LICENSE)).

## Four quotes would turn these estimates into a budget

Most of the remaining uncertainty sits in a few prices that nobody publishes. These requests replace the weakest inputs in the model.

| Who to ask | What to ask for | Model input it replaces |
|---|---|---|
| OEMs and distributors: Dell India, HPE India, Supermicro India (via Rashi), Netweb (Tyrone), Ingram Micro India, Redington | INR-landed quotes for 8×B200, 8×H200 and 8×MI355X (DLC) with 3- and 5-year onsite support (4-hour/NBD, India parts depot), a minimal-RAM option, and delivery slots in writing | Node prices of $323,685 (H200 store price), ~$390k (B200) and $330,000 (MI355X, inferred). This also resolves the MI355X caveat |
| Customs broker (CHA) | BCD by HS line for switches, optics and routers; whether the UPS ITA exemption is accepted at Nhava Sheva / Mumbai Air Cargo; rack classification (9403 vs 7308); the IMS authorisation for 2027 shipments; BIS R-numbers | Non-recoverable duty (currently 0–25% by item) and lead time |
| Chartered accountant | ITC on the server-room build (plant and machinery vs works contract under s.17(5)); 40% vs 15% depreciation for network gear and UPS; Income-tax Act 2025 references; whether Stark can qualify as a registered IT/ITeS unit (>75% IT/ITeS turnover) | The ITC lever (₹4.4 lakh/month) and the IT/ITeS lever (₹2.3 lakh/month) |
| MSEDCL and the Baner landlord | Sanctioned load and spare capacity in the building, LT vs HT (187 kVA), the industrial-tariff route after DoI registration, the FY27 peak-hour (ToD) surcharge footnote and current FAC | The ₹15.32/kVAh commercial energy rate plus 21% duty, and the HT threshold |
| Colocation and cloud: Sify, Yotta and RackBank (Navi Mumbai); STT GDC and Nxtra (Pune); E2E, Yotta and TensorWave | Per-kW quotes for 30–60 kW liquid-cooled racks and the power pass-through rate; 8×B200/H200 monthly and 3-year INR rates; MI355X contract terms; a one-week benchmark slot | The colo multiplier (1.55×), the rent row and the ±25% throughput band |
| Datalab | Chandra OCR 2 on-prem commercial licence fee | The uncosted OCR licence |

## Conclusion

The decision splits by workload, not by model. Chat, anything that fits on one node, and anything that runs only in office hours should be rented. Indian clouds bill B200 and H200 by the hour, and a single rented H200 node at ₹16.4 lakh beats owning one. Always-on coding agents are the only case where owning pays back inside three years. Colocation beats a Baner server room on every row, so an own room makes sense only if keeping data on Stark's own premises is a hard requirement. For an agent fleet, compaction at 128k, DP-attention serving and native precision each matter more than the choice of GPU vendor. The TP-attention mistake alone adds about half to the bill, and a full 1M window can add two nodes for Kimi.

Two results go against intuition. First, self-hosting GLM-5.3 beats Z.ai's list API by about 30% per output token, but the same reference room costs 1.6–3.2 times DeepSeek's own API price per output token. The business case for self-hosting therefore rests on keeping code on Stark's own hardware and on a fixed monthly bill, not on token price. Second, the cheapest hardware on paper, MI355X, has the least reliable prices and benchmarks in the data. The sensible order is: get INR quotes for B200 and MI355X, rent each for a week to benchmark Stark's own agent traces, and only then commit capex. That fits naturally around the import authorisation that expires on 31 Dec 2026.
