# Model specs for self-hosting cost: Chandra OCR 2, GLM-5.3, DeepSeek V4 Pro, Kimi K2.7 Code

All sources were fetched on **2026-10-19**. Hugging Face (HF) values come from the raw `config.json`, `model.safetensors.index.json` and the HF model API (`/api/models/<repo>?blobs=true`) at the commit SHAs listed. Labels used below:
- **[config]** means read directly from the official file.
- **[derived]** means my arithmetic from config values.
- **[3rd-party]** means a non-official source.

Unit convention: "GB" means 10^9 bytes and "GiB" means 2^30 bytes. Several engine recipes write "GB" when they mean GiB. Those cases are flagged.

**Generic KV formulas used [derived]:**
- MLA (DeepSeek-V3-style):
  - BF16: `(kv_lora_rank + qk_rope_head_dim) × 2 B` per layer per token = (512+64)×2 = **1,152 B**.
  - vLLM FP8 `fp8_ds_mla`: **656 B** = 512 FP8 NoPE values + 16 B of scales (4 × FP32) + 64 BF16 RoPE values = 128 B. Source: [vLLM DeepSeek-V3.2 post](https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2025-09-29-deepseek-v3-2.md).
  - Plain FP8 MLA: 576 B.
- DSA lightning-indexer key (index_head_dim 128):
  - BF16: 256 B per layer per token.
  - vLLM FP8: 132 B (128 FP8 values + one FP32 scale; the layout is described in the same V3.2 post).
- Under tensor parallelism, MLA latent KV is **replicated on every TP rank, not sharded**. "MLA KV is identical across TP ranks" ([vLLM GLM-5.3 Part 1](https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2026-09-08-glm53-part1-hybrid-sparse-offloading.md)). So per-GPU KV capacity = free HBM per GPU ÷ bytes/token. Do not divide by the TP size.

## Chandra OCR 2 (datalab-to/chandra-ocr-2): params, base model, vision, tokens/page, serving, throughput, license

### Takeaway
Chandra OCR 2 is a fine-tune of the **Qwen3.5-4B architecture**. Its config matches Qwen3.5-4B field for field. The checkpoint stores **5,295,564,288** parameters only because `lm_head` is saved as a separate copy even though `tie_word_embeddings=true`. Remove that duplicate and the count is exactly Qwen3.5-4B's **4,659,865,088**. So the official "4B" and the third-party "5B" are both explained.

It is a hybrid model: 8 of its 32 layers are full-attention GQA layers and 24 are Gated-DeltaNet linear-attention layers. KV cache is therefore only **32,768 B/token in BF16**, plus about 49 MiB of fixed recurrent state per sequence. One H100 does about 1.44 pages/s on the hard olmOCR mix (Datalab estimates about 2 pages/s on real-world documents).

The weights license blocks commercial use by any entity with more than $2M in revenue or funding unless it buys a license.

### Cited Findings
**Parameters and checkpoint** (HF commit `af93b47`, lastModified 2026-06-26)
- HF API: `{"BF16": 5295564288}`, total **5,295,564,288** params. One file, `model.safetensors`, of **10,591,220,088 bytes**. There is no `model.safetensors.index.json` (single-shard). — [HF API](https://huggingface.co/api/models/datalab-to/chandra-ocr-2), [Files](https://huggingface.co/datalab-to/chandra-ocr-2/tree/main)
- Safetensors header breakdown [derived, from the HTTP-range-read header of `model.safetensors`]:

  | Component | Params |
  |---|---|
  | `lm_head` | 635,699,200 |
  | `embed_tokens` | 635,699,200 |
  | LM decoder layers | 3,570,052,096 |
  | vision tower | 333,514,240 |
  | MTP | 120,599,552 |
  | **Sum** | **5,295,564,288** |

  — [HF file](https://huggingface.co/datalab-to/chandra-ocr-2/blob/main/model.safetensors)
- Qwen3.5-4B (and Qwen3.5-4B-Base) has **4,659,865,088** params with an identical text and vision config. The figures check out: 5,295,564,288 − 635,699,200 (duplicate lm_head) = 4,659,865,088. — [Qwen/Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B)
- Official size claim: v0.2.0 "Chandra OCR 2" release notes say "4B parameters (down from 9B), 2x throughput improvement", released 18 Mar (2026). — [GitHub releases](https://github.com/datalab-to/chandra/releases)
- Conflicting claim: a third-party guide calls it "roughly 5B-parameter … fine-tuned from Qwen 3.5". — [st-hakky guide [3rd-party]](https://book.st-hakky.com/en/data-science/chandra-ocr-cli-vllm-hf-vram-guide). The model card itself credits "Qwen 3.5" without naming a size. — [model card](https://huggingface.co/datalab-to/chandra-ocr-2)

**Architecture** [config] — [config.json](https://huggingface.co/datalab-to/chandra-ocr-2/raw/main/config.json)
- `Qwen3_5ForConditionalGeneration`, model_type `qwen3_5`.
- Text model:
  - num_hidden_layers 32; hidden_size 2560; intermediate_size 9216 (dense model).
  - `layer_types`: 3 × `linear_attention` then 1 × `full_attention`, repeated. `full_attention_interval` 4, so there are **8 full-attention layers**.
  - Full attention: num_attention_heads 16, num_key_value_heads 4, head_dim 256, attn_output_gate true, partial_rotary_factor 0.25.
  - Linear attention (Gated DeltaNet): linear_num_key_heads 16, linear_num_value_heads 32, key/value head_dim 128, conv kernel 4, `mamba_ssm_dtype` float32.
  - mtp_num_hidden_layers **1**; vocab_size 248,320.
  - **max_position_embeddings 262,144**; rope theta 1e7 with interleaved mRoPE [11,11,10]; tie_word_embeddings true.
- Vision: depth 24, hidden 1024, 16 heads, patch_size 16, spatial_merge_size 2, out_hidden 2560.

**Serving defaults** (GitHub HEAD `d4f7467`, 2026-06-26)
- Settings file: `IMAGE_DPI` 192; `MIN_PDF_IMAGE_DIM` 1024; `MIN_IMAGE_DIM` 1536; **`MAX_OUTPUT_TOKENS` 12384**. — [settings.py](https://github.com/datalab-to/chandra/blob/master/chandra/settings.py)
- `scale_to_fit` caps an image at 3072×2048 px (6,291,456 px), on a 28-px grid. — [util.py](https://github.com/datalab-to/chandra/blob/master/chandra/model/util.py)
- Official vLLM launcher (`chandra_vllm`, [scripts/vllm.py](https://github.com/datalab-to/chandra/blob/master/chandra/scripts/vllm.py)):
  - Image and engine: docker `vllm/vllm-openai:v0.17.0`, `--dtype bfloat16`, **`--max-model-len 18000`**, `--gpu-memory-utilization .85`, `--enable-prefix-caching`.
  - `--mm-processor-kwargs {"min_pixels":3136,"max_pixels":6291456}`.
  - The H100-80GB baseline is `max-num-batched-tokens 8192` and `max-num-seqs 64`, scaled by VRAM for presets h100, a100-80, a100(-40), l40s, a10, l4, 4090, 3090 and t4.
  - MTP speculative decoding (1 token) is optional and is labelled "disabled by default, unstable with vLLM".
- Model card: "With vLLM (recommended)". — [model card](https://huggingface.co/datalab-to/chandra-ocr-2)

**Throughput**
- Model card: "Benchmarked with vLLM on a single NVIDIA H100 80GB … olmOCR benchmark set. This set is significantly slower than real-world usage — we estimate 2 pages/s in real-world usage." Configuration "vLLM, 96 concurrent sequences": **1.44 pages/s**, avg latency 60 s, P95 156 s, 0% failures. — [model card](https://huggingface.co/datalab-to/chandra-ocr-2)
- Release notes: "2 pages/sec on H100 with 96 concurrent requests". — [GitHub releases](https://github.com/datalab-to/chandra/releases)
- Accuracy: olmOCR 85.8 ± 0.8 on the model card vs "85.9%" in the release notes (minor conflict). Multilingual score is 77.8% on 43 languages. — [model card](https://huggingface.co/datalab-to/chandra-ocr-2)

**License**
- The model card says: "Code is Apache 2.0. Model weights use a modified OpenRAIL-M license: free for research, personal use, and startups under $2M funding/revenue. Cannot be used competitively with our API." — [model card](https://huggingface.co/datalab-to/chandra-ocr-2)
- The GitHub README says: "Commercial self-hosting requires a license"; on-prem licensing is via contact. — [GitHub README](https://github.com/datalab-to/chandra)
- LICENSE Attachment A, "Commercial", forbids use "(a) for any purpose if You (your employer, or the entity you are affiliated with) generated more than two million US Dollars ($2,000,000) in gross revenue in the prior year, except where Your Use is limited to personal use or research purposes; (b) … has raised more than two million US dollars ($2,000,000) in total equity or debt funding …; or (c) … provides … any product or service that competes with any product or service offered by … Licensor". — [LICENSE](https://huggingface.co/datalab-to/chandra-ocr-2/blob/main/LICENSE)

### Inferences
- **Parameter count to use [derived].**
  - Use about **4.66B unique parameters**, which is what is resident when tying is honoured.
  - The **on-disk / worst-case GPU weight footprint is 10.59 GB** (5.30B × 2 B) if the engine loads the untied lm_head copy, or about 9.32 GB if it is tied.
  - Text-decode compute is about 2 × (3.57B layers + 0.64B lm_head) ≈ **8.4 GFLOP per output token**, excluding attention and the vision encoder.
- **KV per token [derived].**
  - Full-attention layers only: 8 layers × 2 (K,V) × 4 KV heads × 256 × 2 B = **32,768 B/token (BF16)**, or **16,384 B/token (FP8)**.
  - Fixed per-sequence linear-attention state:
    - SSM state: 24 layers × 32 value heads × 128 × 128 × 4 B (FP32) = **48 MiB**.
    - Conv state: 24 × 8,192 channels × 3 × 2 B ≈ 1.1 MiB.
    - Total ≈ **49 MiB per sequence**.
  - A full 18,000-token sequence costs ≈ 562 MiB of KV plus 49 MiB of state.
- **Image tokens per page [derived].** Qwen3.5 vision uses patch 16 × merge 2, so one LLM token covers 32×32 px.
  - US-Letter at 192 DPI is 1632×2112 px, about **3,366 image tokens**.
  - A4 at 192 DPI is 1588×2246 px, about 3,500 tokens.
  - The maximum (3072×2048) is **6,144 tokens**.
  - The `max-model-len 18000` budget therefore holds about 6K image tokens plus the 12,384-token max output.
- **4B vs 5B resolved.** "4B" is the architecture/unique count. "5B" (5.3B) is the raw safetensors counter including the duplicated lm_head. I suspect the third-party blog read the HF counter, but that is my guess.
- The launcher's H100 preset sets `max-num-seqs 64`, while the published benchmark used 96 concurrent sequences. The benchmark config is not identical to the default launcher.

### Gaps
- Datalab does not publish typical **output tokens per page**. Only the 12,384 cap is known. The token count is logged per page in `<filename>_metadata.json`, so measure it on your own corpus.
- Datalab does not publish pages/s for **A100, L40S, L4 or other GPUs**. Only H100 is published, plus VRAM-scaled launcher presets.
- The prompt-token length of the `ocr_layout` prompt was not quantified (see `chandra/prompts.py`).
- No official statement names the exact base checkpoint (Qwen3.5-4B vs -4B-Base). The architecture match is exact but the training lineage is not stated.

## GLM-5.3 (zai-org/GLM-5.3 FP8, zai-org/GLM-5.3-BF16): params, bytes, architecture, KV, context, hardware, license

### Takeaway
GLM-5.3 reuses the GLM-5.2 base model and architecture (`GlmMoeDsaForCausalLM`): 78 layers, MLA attention with DSA sparse attention (top-2048), and IndexShare, so only 21 of the 78 layers own a lightning indexer. It has 256 routed experts (top-8) and 1 MTP layer.

- **Size:** about 743–744B total, about 39–40B active (official). The checkpoint stores 753.33B including the MTP layer.
- **Checkpoints:** the default repo is now **native FP8 at 755,617,140,416 B**. BF16 is **1,506,659,919,872 B**.
- **Context:** **1,048,576 tokens, native**, with no RoPE scaling.
- **KV:** about **53.9–54.7 KB/token in vLLM FP8** and about 95 KB/token in BF16.
- **Hardware:** FP8 runs on a single 8×H200/H20 node with context capped at 256K in the recipe. Full 1M needs 8×B200 (vLLM).
- **License:** **no longer MIT**. It is a custom "GLM-5.3 License": MIT-style terms plus a security-review clause for Model-as-a-Service operators with more than $10B in revenue.

### Cited Findings
**Checkpoints and parameters** (HF GLM-5.3 commit `ba32f8c`, lastModified 2026-10-14; GLM-5.3-BF16 commit `abf42e6`, 2026-10-15)
- **FP8 (default repo `zai-org/GLM-5.3`):**
  - Index `total_size` **755,617,140,416**.
  - Sum of 141 safetensors files 755,632,050,320.
  - HF params: F8_E4M3 751,226,191,872, BF16 2,103,729,152, F32 19,456; total **753,329,940,480**.
  - — [index](https://huggingface.co/zai-org/GLM-5.3/blob/main/model.safetensors.index.json), [HF API](https://huggingface.co/api/models/zai-org/GLM-5.3)
- **BF16 (`zai-org/GLM-5.3-BF16`):**
  - Index `total_size` **1,506,659,919,872**.
  - Sum of 282 files 1,506,667,387,408.
  - Params: BF16 753,329,921,024 + F32 19,456.
  - — [index](https://huggingface.co/zai-org/GLM-5.3-BF16/blob/main/model.safetensors.index.json), [HF API](https://huggingface.co/api/models/zai-org/GLM-5.3-BF16)
- **Shared base:** the GLM-5.3 card says "GLM-5.3 uses the same base model as GLM-5.2 — every gain comes from post-training". GLM-5.2 FP8/BF16 have byte-identical sizes (755,617,140,416 / 1,506,659,919,872). — [GLM-5.3 card](https://huggingface.co/zai-org/GLM-5.3), [GLM-5.2-FP8 API](https://huggingface.co/api/models/zai-org/GLM-5.2-FP8)
- **Official counts:**
  - vLLM recipe: `parameter_count: "743B"`, `active_parameters: "39B"`. — [vLLM recipe GLM-5.3.yaml](https://github.com/vllm-project/recipes/blob/main/models/zai-org/GLM-5.3.yaml) (date_updated 2026-10-15)
  - GLM-5 card: "scales from 355B parameters (32B active) to 744B parameters (40B active)". — [GLM-5 card](https://huggingface.co/zai-org/GLM-5)
  - The GLM-5.3 card states no count.
- **Third-party quantizations:**
  - `Inferact/GLM-5.3-NVFP4`: 464,822,832,448 B. — [HF](https://huggingface.co/Inferact/GLM-5.3-NVFP4)
  - `RadixArk/GLM-5.3-NVFP4`: 464,823,042,096 B. — [HF](https://huggingface.co/RadixArk/GLM-5.3-NVFP4)
  - `gpustack/GLM-5.3-W4A8`: 399,716,726,536 B. Its I32 count of 734,439,407,616 = the routed-expert params. — [HF](https://huggingface.co/gpustack/GLM-5.3-W4A8)

**Architecture** [config] — [GLM-5.3-BF16 config.json](https://huggingface.co/zai-org/GLM-5.3-BF16/raw/main/config.json)
- `model_type glm_moe_dsa`; num_hidden_layers **78**; hidden_size 6144.
- MLA attention: num_attention_heads 64; num_key_value_heads 64 (MLA, the latent is shared); q_lora_rank 2048; **kv_lora_rank 512**; **qk_rope_head_dim 64**; qk_nope_head_dim 192; qk_head_dim 256; v_head_dim 256; head_dim 192.
- DSA indexer: index_n_heads 32; **index_head_dim 128**; **index_topk 2048**; index_topk_freq 4; index_skip_topk_offset 3; index_share_for_mtp_iteration true.
- `indexer_types`: **21 "full"** (layers 0,1,2,6,10,…,74) and **57 "shared"** [counted from config].
- MoE:
  - n_routed_experts **256**; num_experts_per_tok **8**; n_shared_experts **1**.
  - moe_intermediate_size **2048**; dense intermediate_size 12288.
  - first_k_dense_replace **3** (mlp_layer_types 3 dense + 75 sparse); scoring sigmoid, noaux_tc; routed_scaling 2.5.
- Other: num_nextn_predict_layers **1**; vocab_size **154,880**; **max_position_embeddings 1,048,576**; `rope_parameters {rope_theta: 8,000,000, rope_type: default}` (**no YaRN/rope scaling**).
- GLM-5.2 card on IndexShare: "reuses the same indexer across every four sparse attention layers, reducing per-token FLOPs by 2.9× at a 1M context length … improve GLM-5.2's MTP layer … increasing the acceptance length by up to 20%". — [GLM-5.2 card](https://huggingface.co/zai-org/GLM-5.2)

**Context**
- GLM-5.2 card: "for the first time, delivers that capability on a **solid 1M-token context**". — [GLM-5.2 card](https://huggingface.co/zai-org/GLM-5.2)
- vLLM recipe: "GLM-5.3 has a **native 1M-token window**. Whether the full window fits is a KV-cache VRAM question". — [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/zai-org/GLM-5.3.yaml)
- The GLM-5.3 card's "context management strategy" appears only in the **HLE-with-tools eval footnote** ("maximum context length of 300,000 tokens, using a context management strategy"). Other evals (NL2Repo, ALE, PostTrainBench, SWE-Marathon, FrontierSWE) ran at 1M context. — [GLM-5.3 card](https://huggingface.co/zai-org/GLM-5.3)
- SGLang cookbook lists context 1,048,576 for FP8, BF16 and NVFP4. — [SGLang GLM-5.3 cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5.3)

**Serving: vLLM recipe** — [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/zai-org/GLM-5.3.yaml)
- Versions: min_vllm_version 0.29.0 (the guide text says "vLLM 0.28.0 or newer", an internal inconsistency).
- Hardware verified: B300, H200, MI325X, MI350X, Ascend 950PR (8×), DGX Station GB300.
- Base flag: `--kv-cache-dtype fp8_e4m3`. The Hopper override is `fp8`; the W4A8 variant uses `fp8_ds_mla` on Hopper.
- Variants (`vram_minimum_gb`):

  | Variant | vram_minimum_gb | Description (recipe wording) |
  |---|---|---|
  | FP8 (default) | **893** | "8xH200/H20 (141GB × 8) single-node" |
  | NVFP4 (Inferact) | **558** | "Blackwell GPUs (B200/B300) only" |
  | W4A8 (gpustack) | **447** | "CUTLASS W4A8 is SM90-only — H100/H200/H20; Blackwell and AMD are unsupported" |
  | BF16 | **1786** | "requires multi-node deployment" |

- H200 override note: "8x H200 (1128 GB) leaves **~23 GiB/GPU for KV** after the 704 GB FP8 weights — vLLM estimates **~450K max tokens**, so the 1M default fails … Cap at 256K" (`--max-model-len 262144`).
- Guide text: "FP8 checkpoint fits on a single 8xH200 / 8xH20 node and — with FP8 KV cache — reaches the full 1M-token context on **8xB200**"; "BF16 … need multi-node".
- Launch flags: TP8, `--speculative-config.method mtp --speculative-config.num_speculative_tokens 5`; parsers `glm47`. DeepGEMM is required for FP8 performance.
- AMD results:
  - On 8×MI325X (vLLM 0.29.0 ROCm, `--max-model-len 524288`, util 0.80): "1,477,168-token KV cache and 2.82x maximum concurrency", MTP mean acceptance length 2.77 at 5 drafted tokens.
  - On 8×MI350X: "2,013,072-token KV cache … 3.84x", acceptance 3.19.
- Speculation options: native MTP (5 tokens; 4 on DGX Station; 1 on Ascend), DFlash2 (`incoai/GLM-5.3-DFlash2`, 7 tokens, not on AMD/NPU), DSpark (`RedHatAI/GLM-5.3-speculator.dspark`, 8 tokens).
- Supported strategies: single-node TP/TEP, multi-node TP/TP+PP/TEP/DEP, PD cluster.

**Serving: SGLang cookbook** — [SGLang GLM-5.3 cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5.3)
- "78 transformer layers, 256 routed experts (8 active per token), a 1M-token context window, and a single MTP … layer".
- Hardware: H200, B200, B300, GB300, MI300X/MI325X/MI355X. "FP8 is the recommended deployment".
- BF16 (~1.5 TB): "does not fit a single 8×H200 / 8×B200 / 4×GB300 node. It fits single-node on 8×B300 (TP8, ~2.1 TB HBM); on the smaller GPUs it needs a multi-node layout (e.g. 2×8×H200 or 2×8×B200 at TP16, 2×4×GB300 at TP8)". On AMD, BF16 fits single-node only on MI325X and MI355X.
- NVFP4 (RadixArk, experimental): "~0.45 TB so a 4-GPU GB300 node can serve it with TP4".
- KV dtype is auto-selected: "fp8_e4m3 on Blackwell … and bf16 on Hopper (H200)". FP8 KV on Hopper is opt-in via `--kv-cache-dtype fp8_e4m3 --dsa-prefill-backend flashmla_sparse_q8 --dsa-decode-backend flashmla_kv`.
- MTP via EAGLE (5 steps / 6 draft tokens for low latency). "MTP / EAGLE speculative decoding is disabled for AMD".
- DP-Attention + DeepEP are used for throughput. The DFlash2 draft "is licensed **CC BY-NC-ND 4.0** for research and evaluation".

**vLLM GLM-5.3 blog** (2026-09-08)
- Hybrid HiSparse "enables running GLM 5.3 at full 1 million context length" on one 8×H200 node by offloading non-top-K KV to CPU.
- Benchmark config: TP8, MTP3, FP8 KV.
- "Since MLA KV is identical across TP ranks, the pinned host pool is allocated per DP replica".
- — [vLLM GLM-5.3 Part 1](https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2026-09-08-glm53-part1-hybrid-sparse-offloading.md)

**License**
- `license: other`, `license_name: glm-5.3`. The LICENSE grants MIT-style rights "to run, deploy, fine-tune …" with this condition: "If the Licensee or any of its affiliates operates a **Model as a Service** business, and the aggregate revenue of the Licensee and its affiliates exceeds **10 billion US dollars** … over any consecutive 12 months, the Licensee must pass **Z.AI's security review** before using the Software or its derivative works for any commercial purpose".
- "Model as a Service" excludes "(a) end-user products with model capabilities solely embedded within specific features or harnesses, or (b) mere relaying of requests to models hosted by others".
- — [GLM-5.3 LICENSE](https://huggingface.co/zai-org/GLM-5.3/blob/main/LICENSE)
- By contrast, GLM-5.2 is "An MIT open-source license". — [GLM-5.2 card](https://huggingface.co/zai-org/GLM-5.2)

### Inferences
- **KV per token [derived].** Formula: 78 layers × MLA + 21 indexer layers (IndexShare) + optional MTP layer.
  - **BF16:** 78×1,152 + 21×256 = 89,856 + 5,376 = **95,232 B/token**. Adding the MTP layer (1,152+256) gives 96,640.
  - **FP8 (vLLM fp8_ds_mla):** 78×656 + 21×132 = 51,168 + 2,772 = **53,940 B/token**. With the MTP layer (656+132) it is **54,728 B/token**.
  - If the indexer were cached on all 78 layers: BF16 109,824 and FP8 61,464 B/token.
  - **Cross-check against the recipe:** 23 GiB ÷ 54,728 B = **451,251 tokens**, which matches the H200 recipe's "~450K max tokens". 23 GiB ÷ 61,464+MTP gives 397K. This supports (a) the indexer cache existing only on the 21 "full" layers, and (b) MLA KV being replicated per TP rank.
  - **At 1M context:** about 52.7 GiB per sequence (FP8), resident on *every* GPU under TP8. That is why 8×H200 (about 23 GiB free per GPU) cannot fit even one 1M sequence without offload, while 8×B200 can.
- **Total vs active [derived].**
  - Routed-expert params: 256 × 3 × 6144 × 2048 = 9,663,676,416 per MoE layer, × 76 (75 main + MTP) = 734,439,407,616. This exactly equals gpustack's I32 count.
  - Non-routed: 753,329,940,480 − 734,439,407,616 = 18,890,532,864.
  - Active ≈ 18.89B + 75 × 8 × 37,748,736 (22.65B) = **41.54B**, including embeddings, lm_head and the MTP non-expert params.
  - Excluding the 0.95B embedding table and the MTP layer, about 40B, which is consistent with the official 39–40B.
  - Total excluding the MTP layer is about 743.4B, consistent with 743/744B.
- **Decode compute and bandwidth [derived, rough].**
  - About 2 × 40B ≈ **80 GFLOP per token**, plus DSA attention over 2,048 selected tokens.
  - At batch 1 a decode step reads about 40 GB of FP8 active weights.
- **Units.** The recipe's "704 GB FP8 weights" is really **703.7 GiB** (= 755.6 GB).

### Gaps
- No Z.ai-published KV-bytes-per-token figure was found. Values above are derived, then cross-checked against the vLLM recipe's 450K-token estimate.
- AMD-reported KV capacities (1,477,168 tokens on MI325X at 0.80 utilization) imply about 70 KB/token per GPU. That does not reconcile with 54.7 KB. The ROCm path may use a different layout (for example, BF16 RoPE or an indexer on all layers). Not resolved.
- No official Z.ai "minimum hardware" statement exists on the model card. The hardware guidance comes from the vLLM and SGLang recipes.

## DeepSeek V4 Pro (deepseek-ai/DeepSeek-V4-Pro preview; DeepSeek-V4-Pro-0813 official): params, bytes, CSA/HCA KV, context, hardware, license

### Takeaway
DeepSeek-V4-Pro is a 1.6T-total / 49B-active MoE with 384 routed experts, top-6, and moe_intermediate 3,072. Its 61 layers use a hybrid attention mix: **30 CSA layers (c4a, compression 4, with a top-1024 indexer)** and **31 HCA layers (c128a, compression 128)**. All layers also have a 128-token sliding window over a single 512-dim shared KV head.

- **Checkpoints:** the preview's FP4+FP8 mixed checkpoint is **864,704,792,696 B**. The official **0813** release, which adds 2 more MTP/DSpark layers, is **892,727,580,904 B**.
- **KV:** about **9,848 B/token in BF16** (vLLM: 9.62 GiB per 1M-token sequence vs 83.9 GiB for V3.2) and about **5.0–5.5 KB/token** with FP8 attention plus an FP4/FP8 indexer cache. That confirms the "about 10% of V3.2" claim.
- **Context:** native 1,048,576 tokens (YaRN ×16 over 65,536).
- **Hardware:** 8×H200 (context capped at 800K), 8×B200/B300, 4×GB300, or 8×MI355X. H100 needs 16 GPUs.
- **License:** MIT.

### Cited Findings
**Checkpoints and parameters** (preview commit `b5968e9`, lastModified 2026-06-22; 0813 commit `72e1d32`, 2026-08-13)
- **Model card:** "DeepSeek-V4-Pro with 1.6T parameters (49B activated) … supporting a context length of one million tokens". Download table: V4-Pro "1.6T | 49B | 1M | FP4 + FP8 Mixed*" ("MoE expert parameters use FP4 precision; most other parameters use FP8"). V4-Pro-Base is "FP8 Mixed". — [V4-Pro card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)
- **Preview (`DeepSeek-V4-Pro`):**
  - Index `total_size` **864,704,792,696**.
  - Sum of 64 files 864,721,029,744.
  - HF params: BF16 2,816,899,328; I64 2,327,040; F32 87,776,414; F8_E4M3 23,169,335,296; I8 (FP4 experts) 1,572,763,336,704; total **1,598,839,674,782**.
  - — [index](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/model.safetensors.index.json), [HF API](https://huggingface.co/api/models/deepseek-ai/DeepSeek-V4-Pro)
- **Official 0813 (`DeepSeek-V4-Pro-0813`):**
  - Index `total_size` **892,727,580,904**.
  - Sum of 66 files 892,744,322,880.
  - Params total **1,650,497,936,906** (I8 1,623,497,637,888).
  - Card: "the official release of DeepSeek-V4-Pro, superseding the preview … built on the DeepSeek-V4-Pro (Preview) model structure, with a DSpark speculative decoding module attached".
  - — [0813 card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813), [HF API](https://huggingface.co/api/models/deepseek-ai/DeepSeek-V4-Pro-0813)
- **Other variants:**

  | Repo | Bytes (sum of files) | Notes |
  |---|---|---|
  | `deepseek-ai/DeepSeek-V4-Pro-Base` (FP8 mixed, base model, not for chat) | **1,606,048,407,872** | 1,600,790,440,862 params |
  | `sgl-project/DeepSeek-V4-Pro-FP8` (instruct preview converted to all-FP8) [3rd-party/engine] | 1,606,501,419,888 | |
  | `nvidia/DeepSeek-V4-Pro-NVFP4` | 913,092,561,960 | |
  | `nvidia/DeepSeek-V4-Pro-0813-NVFP4` | 941,115,855,096 | |
  | `deepseek-ai/DeepSeek-V4-Pro-DSpark` (preview + DSpark) | 892,744,322,880 | |

  — [Base API](https://huggingface.co/api/models/deepseek-ai/DeepSeek-V4-Pro-Base), [sgl FP8](https://huggingface.co/sgl-project/DeepSeek-V4-Pro-FP8), [nvidia NVFP4](https://huggingface.co/nvidia/DeepSeek-V4-Pro-NVFP4), [nvidia 0813 NVFP4](https://huggingface.co/nvidia/DeepSeek-V4-Pro-0813-NVFP4)
- **There is no official BF16 release of V4-Pro.** The repo lists only Base (FP8 mixed) and Instruct (FP4+FP8). The inference README says that to use FP8 experts, "remove `"expert_dtype": "fp4"` … and specify `--expert-dtype fp8` in `convert.py`". — [inference README](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/inference/README.md)

**Architecture** [config] — [V4-Pro config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/raw/main/config.json), [inference/config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/raw/main/inference/config.json)
- `DeepseekV4ForCausalLM`; num_hidden_layers **61**; hidden_size 7168.
- Attention dims: num_attention_heads 128; **num_key_value_heads 1**; **head_dim 512** (of which qk_rope_head_dim **64**, so 448 NoPE); q_lora_rank 1536; o_lora_rank 1024; o_groups 16.
- No `kv_lora_rank`, `qk_nope_head_dim` or `v_head_dim` fields. The single 512-dim shared KV entry replaces the MLA latent.
- Hybrid attention: **sliding_window 128**; **index_n_heads 64; index_head_dim 128; index_topk 1024**; `compress_ratios` has 62 entries = 61 layers + 1 MTP, with values 128, 128, then alternating 4/128, then 0 for the MTP layer. That gives **30 layers with ratio 4 (CSA/c4a) and 31 with ratio 128 (HCA/c128a)**; the MTP layer is sliding-window only [counted]. compress_rope_theta 160,000.
- MoE: n_routed_experts **384**; num_experts_per_tok **6**; n_shared_experts **1**; moe_intermediate_size **3072**; num_hash_layers 3; scoring `sqrtsoftplus`; routed_scaling 2.5. There is no `first_k_dense_replace` field: all 61 layers are MoE, and the first 3 use hash routing.
- mHC hyper-connections: hc_mult 4. num_nextn_predict_layers **1** (preview). vocab_size **129,280**.
- **max_position_embeddings 1,048,576**; `rope_scaling {type: yarn, factor 16, original_max_position_embeddings 65536, beta_fast 32, beta_slow 1}`; rope_theta 10,000.
- Quantization: FP8 e4m3, ue8m0 scales, 128×128 weight blocks; `expert_dtype fp4`. The reference code uses FP4 block size 32 with float8_e8m0 scales. — [inference/model.py](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/inference/model.py)
- **0813 config:** identical, plus `dspark_block_size 5`, `dspark_target_layer_ids [58,59,60]`, `dspark_markov_rank 512`, and `compress_ratios` ending in **0, 0, 0**. Its `inference/config.json` has **`n_mtp_layers: 3`**, while `config.json` still says `num_nextn_predict_layers: 1` (conflict flagged). — [0813 config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813/raw/main/config.json), [0813 inference/config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813/raw/main/inference/config.json)
- **Reference KV layout:**
  - `Attention.kv_cache` per layer = `window_size + max_seq_len // compress_ratio` entries × head_dim 512. Comment: "kv could also use fp8 format, though current implementation uses bf16".
  - `Indexer.kv_cache` = `max_seq_len // 4` × 128 (CSA layers only).
  - Plus per-sequence FP32 compressor state.
  - — [inference/model.py](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/inference/model.py)

**Engine-published KV figures** ([vLLM blog "DeepSeek V4 in vLLM", 2026-04-24](https://vllm.ai/blog/2026-04-24-deepseek-v4); [raw source](https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2026-04-24-deepseek-v4.md))
- Headline: "With `bf16` KV cache, DeepSeek V4 only has **9.62 GiB KV cache per sequence at 1M context**. That is about 8.7x smaller than the **83.9 GiB** estimate for a 61-layer DeepSeek V3.2-style stack. In practice, we use `fp4` for the indexer cache and `fp8` for the attention cache, which further reduces the KV cache size by roughly **2x**".
- Appendix, V3.2: "MLA cache per token per layer: (512 + 64) × 2 = 1152 bytes. Indexer cache per token per layer: 128 × 2 = 256 bytes. Total … 1408 bytes".
- Appendix, V4: "Each shared-KV cached entry stores 512 × 2 = 1024 bytes. Each `c4a` indexer cached entry stores 128 × 2 = 256 bytes. `c4a` layer: (128 + 1,048,576/4) × 1024 + (1,048,576/4) × 256 … about 320.1 MiB. `c128a` layer: (128 + 1,048,576/128) × 1024 ≈ 8.1 MiB. Total across **30 `c4a` layers and 31 `c128a` layers**: about 9.62 GiB".
- Compression mechanics: c4a: "one compressed token is a weighted sum of 8 uncompressed tokens, with a stride of 4"; c128a uses stride 128. The vLLM default top-k is 512 for c4a and 8192 for c128a. The compressor state is "an 8-token (overlapped) partial state for C4, and a 128-token partial state for C128". The logical block is 256 native positions.
- An HTML-commented (not rendered) line in the source gives three per-block page sizes: "1,728 B, 8,640 B, and 37,440 B … multiple of FlashMLA's 576 B alignment".
- Hardware in the blog: the Pro example runs "on 8xB200 or 8xB300" with `--data-parallel-size 8 --enable-expert-parallel --kv-cache-dtype fp8 --block-size 256 --attention_config.use_fp4_indexer_cache=True`. "The current implementation mainly targets NVIDIA GPUs, including both the Hopper and Blackwell architectures".
- Card claim: "In the 1M-token context setting, DeepSeek-V4-Pro requires only **27% of single-token inference FLOPs** and **10% of KV cache** compared with DeepSeek-V3.2". — [V4-Pro card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)

**DeepSeek-V3.2 reference** [config] — [V3.2 config.json](https://huggingface.co/deepseek-ai/DeepSeek-V3.2/raw/main/config.json)
- Config: 61 layers; kv_lora_rank 512; qk_rope 64; qk_nope 128; v_head_dim 128; 128 heads; index_head_dim 128; index_n_heads 64; index_topk 2048; 256 experts, top-8; first_k_dense_replace 3; max_position_embeddings 163,840 (YaRN ×40 over 4,096); 1 MTP layer.
- HF params 685,355,329,792; file sum **689,483,049,129 B**.
- Its index `total_size` says 1,370,793,842,752, about 2× the real file sum (an index anomaly; don't trust it). — [HF API](https://huggingface.co/api/models/deepseek-ai/DeepSeek-V3.2)
- vLLM fp8_ds_mla = 656 B/token/layer. — [vLLM V3.2 post](https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2025-09-29-deepseek-v3-2.md)

**Serving: vLLM recipe** — [vLLM recipe DeepSeek-V4-Pro.yaml](https://github.com/vllm-project/recipes/blob/main/models/deepseek-ai/DeepSeek-V4-Pro.yaml) (date_updated 2026-10-13)
- Recipe metadata:
  - Hardware verified: H200, B200, GB200, B300, GB300, MI355X. **MI300X and MI325X are unsupported.**
  - `parameter_count "1600B"`, `active_parameters "49B"`, `context_length 1048576`, min vLLM 0.20.0 (0.25.0 for 0813/DSpark).
  - Base args: `--trust-remote-code --kv-cache-dtype fp8 --block-size 256`.
  - The default variant is **0813** (`vram_minimum_gb 960`, DSpark spec decoding, 7 tokens probabilistic).
  - The preview "FP8 (Preview)" variant is "Native FP4+FP8 mixed checkpoint (MoE experts FP4, remaining params FP8)", vram_minimum 960. The NVFP4 variant (nvidia) is 960 and Blackwell-only; RedHat NVFP4+FP8 is 1000.
- Hopper override: "H200 (141 GB × 8 = 1128 GB) leaves KV cache tight at 1M context with ~960 GB mixed-precision weights replicated across DP ranks — **cap to 800K**". The H20 note is `--max-model-len 200000 --max-num-seqs 16`.
- Blackwell override: `--attention_config.indexer_kv_dtype=mxfp4` (FP4 indexer cache) and `--moe-backend deep_gemm_mega_moe` for the FP8 checkpoints.
- Recommended deployments: "B300 (8×): single-node DP + EP `--data-parallel-size 8`"; "H200 (8×): DP + EP … capped at 800K"; "MI355X (8×)"; "GB200 NVL4 … ~960 GB … does not fit on one tray; run … across **2 trays (8 GPUs)**".
- PD notes: "1 GB300 NVL4 tray = 4 GPUs (1072 GB/tray fits weights)". "The fused checkpoints are ~893 GB on disk versus ~865 GB for the preview".
- Spec decoding: MTP 2 draft tokens (preview/NVFP4); DSpark 5–7 tokens (0813). The default strategy is `single_node_tep`. CPU and FS KV offload are verified.
- MI355X data point (8× TP8, InferenceX lane): "raised GPU KV-cache capacity from 4,730,981 to **8,524,228 tokens**" with `--max-num-batched-tokens 8192` at util 0.86.

**Serving: SGLang cookbook** — [SGLang DeepSeek-V4 cookbook](https://docs.sglang.io/cookbook/autoregressive/DeepSeek/DeepSeek-V4)
- Verified hardware:
  - "DeepSeek-V4-Pro 1.6T 49B: B200 / B300 (TP=8) · GB300 (TP=4) · **H200 FP4 (TP=8)** · GB200 (2-node, TP=8) · H200 FP8 (2-node, TP=16) · **H100 (2-node, TP=16)**".
  - "DeepSeek-V4-Pro-0813 **1.65T** 49B … 4×GB300 (TP=4) · B200 / B300 / H200 FP4 (TP=8) · GB200 (2-node, TP=8) · H100 (2-node, TP=16) · MI355X".
- **FP4 on Hopper vs Blackwell:**
  - "Original FP4 checkpoints — run the MoE experts with **W4A16** kernels (Marlin or the FlashInfer SM90 CUTLASS runner) … [or] the **W4A8** path — MXFP4 weights with FP8 activations … `--flashinfer-mxfp4-moe-precision fp8` … Both work on H100 and H200; FP4 is the only option for H100 (no FP8 path). It is TP-only; on H200 the Pro variant fits on a single 8-GPU node, while H100 Pro needs 2 nodes (TP=16)".
  - "Converted FP8 checkpoints (H100 and H200 only) … unlock DP-attention + DeepEP".
  - "MegaMoE W4A8 / W4A4 fused kernel (**Blackwell only**; Hopper SM90 uses a separate all-FP8 MegaMoE path)".
- Other SGLang flags:
  - Experimental FP4 indexer `--enable-deepseek-v4-fp4-indexer` (SM100/SM120 and MI355X).
  - `SGLANG_DSV4_COMPRESS_STATE_DTYPE` (fp32 default, bf16 optional) for C4/C128 compressed-state pools.
  - Do not use EAGLE on 0813 (accept length 1.00); use `--speculative-algorithm DSPARK`.
- 0813 SGLang example: `--tp 4 --moe-runner-backend flashinfer_mxfp4 --speculative-algorithm DSPARK … --swa-full-tokens-ratio 0.1` on 4×GB300. — [0813 card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813)

**Context and license**
- Card: "For the Think Max reasoning mode, we recommend setting the context window to at least **384K** tokens". 0813: "recommend a maximum output length of 384K tokens" for high/max effort. — [V4-Pro card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro), [0813 card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813)
- License: "This repository and the model weights are licensed under the MIT License" (both preview and 0813). — [V4-Pro card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro), [LICENSE](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/LICENSE)

### Inferences
- **V4-Pro KV per token by layer type [derived].** Entries per token: c4a = 1/4 entry plus 1/4 indexer entry; c128a = 1/128 entry. Every layer also holds a fixed 128-token SWA window.

  | Precision | c4a (×30) | c128a (×31) | **Per-token total** | Fixed SWA per sequence | @1M (1,048,576 tok) |
  |---|---|---|---|---|---|
  | **BF16** (1,024 B entry, 256 B indexer) | 256 + 64 = 320 B | 8 B | **9,848 B/token** | 61 × 128 × 1,024 = **7.62 MiB** | **9.625 GiB** (matches vLLM's 9.62 GiB) |
  | **FP8 attention + FP8 indexer** (584 B entry, 132 B indexer) | 146 + 33 = 179 B | 4.5625 B | **≈5,511 B/token** | 4.35 MiB | ≈5.39 GiB |
  | **FP8 attention + FP4 indexer** (584 B, 68 B indexer = 64 B MXFP4 + 4 B scales) | | | **≈5,031 B/token** | | ≈4.92 GiB |

  - The FP8 entry of **584 B** = 448 FP8 NoPE + 64 BF16 RoPE (128 B) + 7 ue8m0 scales + 1 pad. This size is my inference.
  - It reproduces all three vLLM page buckets after rounding up to the 576 B alignment: 64 × 584 → **37,440**; 2 × 584 → **1,728**; and the 64 × 132 FP8 indexer → **8,640**.
- **Cross-check of "10% of V3.2" [derived].**
  - V3.2 BF16 = 61 × 1,408 = **85,888 B/token** (83.9 GiB at 1M; vLLM agrees).
  - V3.2 vLLM FP8 = 61 × (656+132) = **48,068 B/token** (46.9 GiB at 1M).
  - V4/V3.2 ratio: **11.5%** (BF16 vs BF16); **10.5%** (V4 FP8+FP4 indexer vs V3.2 FP8); 11.5% (FP8+FP8). This is consistent with the card's "10%".
  - V3.2 MLA-only (no indexer) BF16 is 70,272 B/token.
- **Total and active [derived].**
  - Routed experts per layer: 384 × 3 × 7168 × 3072 = 25,367,150,592. × 62 (61 + MTP) = 1,572,763,336,704, which exactly equals HF's I8 count. So HF counts logical FP4 parameters.
  - Non-routed = 26.08B.
  - Active ≈ 26.08B + 61 × 6 × 66,060,288 (24.18B) = **50.25B** including embeddings and the MTP non-expert part, i.e. about 49B as stated.
  - **0813:** I8 is larger by exactly 2 × 25.37B, i.e. 2 extra MTP/DSpark layers (3 total), which explains "1.65T".
  - **Byte reconciliation:** FP4 1.5728T × 0.5 B = 786.4 GB, + ue8m0 scales (1/32 B per param) 49.1 GB, + FP8 23.2 GB, + BF16 5.6 GB, + F32 0.35 GB ≈ **864.7 GB** = index total_size.
- **Decode cost [derived, rough].**
  - About 2 × 49B ≈ **98 GFLOP/token** of matmul at short context. Attention adds about 1,024 c4a entries plus up to 8K c128a entries per layer.
  - At batch 1, active weights read per step ≈ 24.2B FP4 experts × 0.53 B (≈12.8 GB) + about 25B mostly-FP8 non-expert params (≈28 GB) ≈ **~40 GB**.
- **DP vs TP memory.** With DP+EP (the vLLM default on 8×), the ~26B non-expert params are replicated on each DP rank; that is why the H200 config caps at 800K. The SWA state is tiny (≈4–8 MiB per sequence). The KV of long sequences dominates only at very high concurrency × length.
- **Units.** The recipe's "~960 GB" is a VRAM minimum and not the checkpoint size. Disk is 864.7 GB (805 GiB) for the preview and 892.7 GB for 0813.

### Gaps
- The DeepSeek technical report ([arXiv 2606.19348](https://arxiv.org/abs/2606.19348)) was not retrieved. Its own per-token KV figure, if any, is not captured. The vLLM appendix serves as the engine-published figure.
- vLLM's exact FP8 main-KV entry size (584 B) is inferred from page buckets in an HTML-commented part of the blog source. It is not stated in rendered docs.
- The MI355X TP8 KV capacity (8.52M tokens at util 0.86) does not obviously reconcile with 5.0–5.5 KB/token. The ROCm cache layout is unknown.
- Whether vLLM/SGLang allocate KV for the 3 DSpark layers in 0813 (they are SWA-only, so the amount is small) was not verified.

## Kimi K2.7 Code (moonshotai/Kimi-K2.7-Code): params, bytes, MLA KV, context/YaRN, hardware, license

### Takeaway
Kimi K2.7 Code reuses the Kimi K2.5/K2.6 architecture: a DeepSeek-V3 backbone with MLA and a MoonViT vision encoder. It has 61 layers (1 dense), 384 experts (top-8), 1 shared expert, and **no MTP layer**. Size is about 1T total and 32B active.

- **Checkpoint:** released only as **native INT4 (QAT, compressed-tensors W4A16, group 32) at 595,148,192,736 B**. There is no official BF16 or FP8 release. A third-party NVIDIA NVFP4 version exists.
- **KV:** 70,272 B/token in BF16 and 35,136 B/token with plain FP8.
- **Context:** **262,144 tokens**, already YaRN-extended (factor 64 over 4,096). No officially supported extension beyond that was found.
- **Hardware:** 8×H200 TP8 is the verified minimum on NVIDIA. SGLang also lists 4×GB300 and 4× AMD MI300X/MI325X/MI350X/MI355X at TP4.
- **License:** Modified MIT with a UI attribution clause above 100M MAU or $20M monthly revenue.

### Cited Findings
**Checkpoints and parameters** (HF commit `74797c9`, lastModified 2026-06-15)
- **Model card:** Total Parameters **1T**; Activated **32B**; Layers **61** (Dense 1); Attention Hidden Dimension 7168; MoE Hidden Dimension (per Expert) 2048; Attention Heads 64; Experts **384**; Selected per Token **8**; Shared Experts **1**; Vocabulary **160K**; **Context Length 256K**; Attention Mechanism **MLA**; Vision Encoder MoonViT, **400M**.
- Card: "Kimi-K2.7-Code adopts the same native int4 quantization method as Kimi-K2-Thinking"; "Kimi-K2.7-Code has the same architecture as Kimi-K2.5/Kimi-K2.6".
- — [K2.7 Code card](https://huggingface.co/moonshotai/Kimi-K2.7-Code)
- **INT4 checkpoint:** index `total_size` **595,148,192,736** (identical to Kimi-K2.6's). Sum of 64 files 595,177,988,208. HF params: I32 (packed INT4 experts) 1,014,686,023,680; BF16 12,193,329,648; F32 23,040; total **1,026,879,376,368**. — [index](https://huggingface.co/moonshotai/Kimi-K2.7-Code/blob/main/model.safetensors.index.json), [HF API](https://huggingface.co/api/models/moonshotai/Kimi-K2.7-Code), [K2.6 HF API](https://huggingface.co/api/models/moonshotai/Kimi-K2.6)
- The moonshotai org has no BF16 or FP8 repo for K2.7 Code. Its repos are Kimi-K2.7-Code, Kimi-K3, Kimi-K2.6 and older. — [HF moonshotai org listing](https://huggingface.co/moonshotai)
- Third-party: `nvidia/Kimi-K2.7-Code-NVFP4` is 595,185,395,016 B. — [HF](https://huggingface.co/nvidia/Kimi-K2.7-Code-NVFP4)

**Architecture** [config] — [config.json](https://huggingface.co/moonshotai/Kimi-K2.7-Code/raw/main/config.json)
- `KimiK25ForConditionalGeneration`; `text_config` is `DeepseekV3ForCausalLM` (model_type `kimi_k2`).
- num_hidden_layers **61**; hidden_size 7168; intermediate_size 18432 (dense layer).
- MLA: num_attention_heads 64; num_key_value_heads 64 (MLA); q_lora_rank 1536; **kv_lora_rank 512; qk_rope_head_dim 64; qk_nope_head_dim 128; v_head_dim 128**.
- MoE: n_routed_experts **384**; num_experts_per_tok **8**; n_shared_experts **1**; moe_intermediate_size **2048**; first_k_dense_replace **1**; routed_scaling 2.827.
- **num_nextn_predict_layers 0**; vocab_size **163,840**.
- **max_position_embeddings 262,144**; `rope_scaling {type: yarn, factor 64.0, original_max_position_embeddings 4096, beta_fast 32, beta_slow 1, mscale 1.0}`; rope_theta 50,000.
- No DSA/indexer fields.
- Quantization: compressed-tensors `pack-quantized`, INT4 symmetric, **group_size 32**, applied to `Linear`. The `ignore` list (kept BF16) covers self_attn, shared_experts, dense mlp, lm_head, vision_tower and mm_projector.
- Vision: MoonViT, 27 layers, hidden 1152, patch 14, 2×2 merge.

**Context**
- Card footnote: tested "with thinking mode enabled … and a **262,144-token context length**". — [K2.7 Code card](https://huggingface.co/moonshotai/Kimi-K2.7-Code)
- vLLM recipe: `context_length: 262144`. — [vLLM recipe Kimi-K2.7-Code.yaml](https://github.com/vllm-project/recipes/blob/main/models/moonshotai/Kimi-K2.7-Code.yaml)
- SGLang K2.6 cookbook (same architecture): "Use `--context-length 128000` to conserve memory". — [SGLang Kimi-K2.6 cookbook](https://cookbook.sglang.io/autoregressive/Moonshotai/Kimi-K2.6)

**Serving: vLLM**
- Recipe (date_updated 2026-07-29):
  - Hardware verified: H200, MI300X, MI325X, MI355X. min vLLM **0.19.1**.
  - `vram_minimum_gb 714`, "Native INT4 via compressed-tensors (~595 GB on disk); fits 8×H200".
  - Guide text: "8x H200 GPUs (verified), or equivalent aggregate VRAM (~640 GB)" (inconsistent with 714).
  - Launch: TP8, `--mm-encoder-tp-mode data`, parsers `kimi_k2`. `--language-model-only` skips MoonViT.
  - Spec decoding: **EAGLE3** draft `lightseekorg/kimi-k2.7-coder-eagle3.1-mla`, 3 tokens.
  - `supports_dcp: true`. Strategies include TP, TEP, DEP, multi-node and PD.
  - On MI350X/MI355X the FlyDSL W4A16 MoE path "does not support expert parallelism".
  - — [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/moonshotai/Kimi-K2.7-Code.yaml)
- Moonshot deploy guide: "serve this model on a H200 single node with TP8 via vLLM"; "For stable production use, we recommend vLLM 0.19.1". — [deploy_guidance.md](https://huggingface.co/moonshotai/Kimi-K2.7-Code/blob/main/docs/deploy_guidance.md)

**Serving: SGLang and KTransformers**
- Moonshot deploy guide: "supported in SGLang v0.5.10 and later … TP8 on H200 in a single node". KTransformers+SGLang CPU/GPU hybrid: "Achieves 640.12 tokens/s Prefill and 24.51 tokens/s Decode (48-way concurrency) on 8× NVIDIA L20 + 2× Intel 6454S". `transformers >=4.57.1, <5.0.0`. — [deploy_guidance.md](https://huggingface.co/moonshotai/Kimi-K2.7-Code/blob/main/docs/deploy_guidance.md), [card](https://huggingface.co/moonshotai/Kimi-K2.7-Code)
- SGLang K2.6 cookbook (same architecture): "Requires GPUs with ≥140GB each. The native INT4 checkpoint supports **H200 (8×, TP=8), B300 (8×, TP=8), GB300 (4×, TP=4), MI300X/MI325X (4×, TP=4), and MI350X/MI355X (4×, TP=4)**".
  - AMD TP limit: "TP must be ≤ 4 … AITER MLA kernel requires heads_per_gpu % 16 == 0".
  - FP8 KV on AMD: "the generator adds `--kv-cache-dtype fp8_e4m3` by default".
  - NVFP4 (`nvidia/Kimi-K2.6-NVFP4`) uses `--quantization modelopt_fp4` on Blackwell, under the "NVIDIA Open Model License".
  - EAGLE3 example: 3 steps, 4 draft tokens.
  - — [SGLang Kimi-K2.6 cookbook](https://cookbook.sglang.io/autoregressive/Moonshotai/Kimi-K2.6)

**FP8 KV accuracy and license**
- vLLM FP8 KV post on Kimi-K2.5 with FlashMLA and uncalibrated FP8 KV on H200: "The drop is modest in aggregate AUC but consistently negative across context lengths". — [vLLM FP8 KV-cache post (2026-04-22)](https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2026-04-22-fp8-kvcache.md)
- License: "Modified MIT License … Our only modification part is that, if the Software (or any derivative works thereof) is used for any of your commercial products or services that have more than **100 million monthly active users**, or more than **20 million US dollars** (or equivalent in other currencies) in **monthly revenue**, you shall prominently display "**Kimi K2.7 Code**" on the user interface of such product or service". — [LICENSE](https://huggingface.co/moonshotai/Kimi-K2.7-Code/blob/main/LICENSE)

### Inferences
- **KV per token [derived].**
  - **BF16:** 61 × (512+64) × 2 = **70,272 B/token**, i.e. 17.16 GiB per 262,144-token sequence.
  - **Plain FP8 (e4m3):** 61 × 576 = **35,136 B/token** (8.58 GiB at 262K).
  - If an engine used the 656-B fp8_ds_mla-style layout, it would be 40,016 B/token.
  - Replicated on every TP rank. Example: on 8×H200 the weights take about 74.4 GB/GPU. At 0.9 utilization (126.9 GB) minus about 5 GB of activations, roughly 45–48 GB/GPU is left. That is about 0.65–0.68M BF16 tokens (≈2.5 full 262K sequences) per TP8 replica, or about twice that with FP8 KV. This is a rough estimate.
- **Active and total [derived].**
  - Routed experts: 384 × 3 × 7168 × 2048 × 60 MoE layers = 1,014,686,023,680, which exactly equals HF's I32 count. So HF reports logical INT4 parameters.
  - Active ≈ 12.19B non-expert (BF16, includes about 0.4B vision and 1.17B embeddings) + 60 × 8 × 44,040,192 (21.14B) = **33.3B**. Excluding vision and the embedding table, about 31.7B, consistent with "32B activated".
  - **Byte reconciliation:** 1.0147T × 0.5 B (INT4) = 507.3 GB, + BF16 group scales (1/32 × 2 B) 63.4 GB, + 12.19B × 2 B = 24.4 GB ≈ **595.1 GB** = index total_size.
- **Decode cost [derived, rough].** About 2 × 32B ≈ **64 GFLOP/token**. At batch 1, about 31 GB of weights are read per step: 21.1B INT4 experts at 0.5625 B/param (≈11.9 GB) plus about 10B active BF16 params (≈20 GB).
- **Context.** 262,144 is the trained and served limit, and the YaRN factor 64 is already baked in to reach it. Going beyond 262,144 would mean un-sanctioned extra RoPE scaling (my inference).
- **Speculative decoding.** It needs an external EAGLE3 draft (lightseekorg), because the checkpoint has no MTP head.

### Gaps
- No Moonshot statement on YaRN extension beyond 262,144 was found, and none on official BF16 or FP8 weights.
- No Moonshot-published KV-bytes-per-token figure was found. The values above are derived from config.
- The exact vLLM FP8 KV byte layout for non-sparse FlashMLA on Kimi (576 vs 656 B/layer) was not confirmed from vLLM source.
- The license or provenance terms of the lightseekorg EAGLE3 draft were not checked.

## Which precisions are runnable today, minimum official hardware, and cross-model notes

### Takeaway
All four models run in vLLM and SGLang today on 8× 141 GB-class GPUs or better, except Chandra, which needs one GPU.

- FP4 behaves differently on Hopper and Blackwell. DeepSeek's native FP4 experts run on **Hopper via W4A16/W4A8 kernels** (SGLang) and in vLLM's H200-verified recipe.
- NVFP4 re-quants of GLM, DeepSeek and Kimi are **Blackwell-only**. GLM's community W4A8 is **Hopper-only**.
- FP8 KV cache is the default in the vLLM recipes for GLM-5.3 and DeepSeek V4, and opt-in for Kimi.
- For memory planning, MLA/shared-KV caches are replicated per TP rank.

### Cited Findings
- **GLM-5.3:**
  - FP8 runs on 8×H200/H20 (vLLM caps context at 262,144), 8×MI300X/MI325X/MI350X/MI355X and 8×B200/B300. The full 1M context needs 8×B200 in vLLM.
  - BF16 needs 8×B300, 8×MI325X/MI355X, or 16×H200/B200 across 2 nodes.
  - NVFP4 (Inferact/RadixArk) is Blackwell-only; it runs on 4×GB300 TP4 (SGLang) or 1×GB300 DGX Station with CPU offload (vLLM).
  - W4A8 (gpustack) is SM90-only.
  - — [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/zai-org/GLM-5.3.yaml), [SGLang cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5.3)
- **DeepSeek V4 Pro:**
  - The FP4+FP8 checkpoint runs on 8×H200 (vLLM DP8+EP, 800K cap; SGLang TP8 W4A16/W4A8), 8×B200/B300, 4×GB300, 2×GB200 trays (8 GPUs) and 8×MI355X.
  - H100 needs 16 GPUs (TP16, 2 nodes).
  - The converted all-FP8 checkpoint needs 16×H200 (TP16).
  - NVFP4 is Blackwell-only. MI300X/MI325X are unsupported in vLLM.
  - — [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/deepseek-ai/DeepSeek-V4-Pro.yaml), [SGLang cookbook](https://docs.sglang.io/cookbook/autoregressive/DeepSeek/DeepSeek-V4)
- **Kimi K2.7 Code:**
  - INT4 runs on 8×H200 TP8 (vLLM, SGLang), 8×B300 TP8, 4×GB300 TP4, and 4×MI300X/MI325X/MI350X/MI355X TP4 (AMD must use TP≤4 in SGLang).
  - NVFP4 (nvidia) runs on Blackwell.
  - KTransformers can do CPU+GPU hybrid on 8×L20.
  - — [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/moonshotai/Kimi-K2.7-Code.yaml), [SGLang K2.6 cookbook](https://cookbook.sglang.io/autoregressive/Moonshotai/Kimi-K2.6), [deploy guide](https://huggingface.co/moonshotai/Kimi-K2.7-Code/blob/main/docs/deploy_guidance.md)
- **Chandra OCR 2:** BF16 runs on 1 GPU. The official launcher has presets from T4-16GB to H100-80GB and pins vLLM docker v0.17.0. — [scripts/vllm.py](https://github.com/datalab-to/chandra/blob/master/chandra/scripts/vllm.py)
- **Speculative decoding summary:**

  | Model | Method | Draft tokens | Source |
  |---|---|---|---|
  | GLM-5.3 | Native MTP (vLLM) | 5 | [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/zai-org/GLM-5.3.yaml) |
  | GLM-5.3 | EAGLE-MTP (SGLang) | 6 (5 steps) | [SGLang cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5.3) |
  | GLM-5.3 | DFlash2 | 7 | [SGLang cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5.3) |
  | GLM-5.3 | DSpark | 8 | [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/zai-org/GLM-5.3.yaml) |
  | DeepSeek V4 Pro (preview) | MTP | 2 | [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/deepseek-ai/DeepSeek-V4-Pro.yaml) |
  | DeepSeek V4 Pro-0813 | DSpark | 5–7 | [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/deepseek-ai/DeepSeek-V4-Pro.yaml) |
  | Kimi K2.7 Code | EAGLE3 (external) | 3 | [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/moonshotai/Kimi-K2.7-Code.yaml) |
  | Chandra OCR 2 | MTP | 1 ("unstable") | [scripts/vllm.py](https://github.com/datalab-to/chandra/blob/master/chandra/scripts/vllm.py) |

- **Engine versions referenced:** vLLM recipes HEAD `2338e9e` (2026-10-18). — [vllm-project/recipes](https://github.com/vllm-project/recipes)

### Inferences
- **Per-GPU KV rule.** For KV capacity per GPU, use (HBM × utilization − weights/GPU − activations) ÷ per-token bytes, without dividing by TP. This holds for all three big models, because their attention caches are latent/shared-head and replicated per rank.
- **Commercial-license ranking for a Pune self-hoster** (my read of the license texts):
  - **DeepSeek (MIT)** is the most permissive.
  - **Kimi** adds only attribution above 100M MAU / $20M monthly revenue.
  - **GLM-5.3** adds a security review only for Model-as-a-Service businesses above $10B revenue.
  - **Chandra** requires a paid license for any company above $2M revenue or funding, or for any company competing with Datalab.
  - The GLM-5.3 DFlash2 draft is non-commercial (CC BY-NC-ND).

### Gaps
- No vendor-official per-token KV figure exists for GLM-5.3 or Kimi. Only DeepSeek V4/V3.2 have an engine-published one (vLLM).
- Measured tokens/s per GPU for GLM-5.3, V4 Pro or K2.7 Code on H200/B200 were not collected here. InferenceX dashboards are referenced in the recipes but were not pulled.

## Consolidated spec table (one row per model × precision)

### Takeaway
Use the rows below for weights + KV sizing.

- KV columns are bytes per token for the main model. For DeepSeek V4 they are asymptotic per-token values, plus the fixed SWA state per sequence noted in brackets.
- Under TP, KV is replicated per GPU.
- "Official" in `min_official_gpus` means the model vendor's card or the vLLM/SGLang recipe.
- Rows marked 3rd-party are not vendor releases.

### Cited Findings

| model × precision | total_params | active_params | checkpoint_bytes | layers | kv_bytes_per_token_bf16 | kv_bytes_per_token_fp8 | native_context | mtp_layers | min_official_gpus | source |
|---|---|---|---|---|---|---|---|---|---|---|
| Chandra OCR 2 · BF16 | 5,295,564,288 stored (4,659,865,088 unique; official "4B") | dense (≈4.66B; ≈4.2B text decode) | 10,591,220,088 (single file, no index) | 32 (8 full-attn GQA + 24 Gated-DeltaNet) | 32,768 (+≈49 MiB fixed state/seq) | 16,384 | 262,144 (served at 18,000) | 1 | 1 GPU (H100-80GB baseline; launcher presets to 16 GB) | [HF API](https://huggingface.co/api/models/datalab-to/chandra-ocr-2), [config](https://huggingface.co/datalab-to/chandra-ocr-2/raw/main/config.json), [card](https://huggingface.co/datalab-to/chandra-ocr-2), [launcher](https://github.com/datalab-to/chandra/blob/master/chandra/scripts/vllm.py) |
| GLM-5.3 · FP8 (zai-org/GLM-5.3, default) | 753,329,940,480 stored (official 743B / 744B) | 39B (vLLM) / 40B (GLM-5 card); derived ≈41.5B incl. embed+MTP | 755,617,140,416 | 78 (3 dense + 75 MoE) | 95,232 (MLA 89,856 + 21 indexer × 256) | 53,940 (vLLM fp8_ds_mla; 54,728 incl. MTP layer) | 1,048,576 (native, no RoPE scaling) | 1 | 8×H200/H20 (ctx capped at 262,144); 8×MI300X+; 8×B200 for full 1M | [index](https://huggingface.co/zai-org/GLM-5.3/blob/main/model.safetensors.index.json), [config](https://huggingface.co/zai-org/GLM-5.3-BF16/raw/main/config.json), [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/zai-org/GLM-5.3.yaml) |
| GLM-5.3 · BF16 (zai-org/GLM-5.3-BF16) | 753,329,940,480 | same | 1,506,659,919,872 | 78 | 95,232 | 53,940 | 1,048,576 | 1 | 8×B300 or 8×MI325X/MI355X single node; else 16×H200/B200 (2 nodes) | [index](https://huggingface.co/zai-org/GLM-5.3-BF16/blob/main/model.safetensors.index.json), [SGLang cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5.3) |
| GLM-5.3 · NVFP4 (Inferact, 3rd-party) | same model | same | 464,822,832,448 (sum of files) | 78 | 95,232 | 53,940 | 1,048,576 | 1 | Blackwell only; 4×GB300 TP4 (SGLang RadixArk build); vram_min 558 GB (vLLM) | [HF](https://huggingface.co/Inferact/GLM-5.3-NVFP4), [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/zai-org/GLM-5.3.yaml) |
| GLM-5.3 · W4A8 (gpustack, 3rd-party) | same model | same | 399,716,726,536 (sum of files) | 78 | 95,232 | 53,940 | 1,048,576 | 1 | Hopper only (H100/H200/H20); vram_min 447 GB | [HF](https://huggingface.co/gpustack/GLM-5.3-W4A8), [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/zai-org/GLM-5.3.yaml) |
| DeepSeek V4 Pro (preview) · FP4+FP8 mixed | 1,598,839,674,782 (1.6T) | 49B (derived ≈50.3B incl. embed+MTP) | 864,704,792,696 | 61 (30 CSA c4a + 31 HCA c128a; all MoE) | 9,848 (+7.62 MiB SWA/seq) | ≈5,511 (FP8 indexer) / ≈5,031 (FP4 indexer) (+4.35 MiB SWA/seq) | 1,048,576 (YaRN ×16 over 65,536) | 1 | 8×H200 (ctx capped at 800K) / 8×B200 / 4×GB300 / 8×MI355X; H100: 16 | [index](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/model.safetensors.index.json), [config](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/raw/main/config.json), [vLLM blog](https://vllm.ai/blog/2026-04-24-deepseek-v4), [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/deepseek-ai/DeepSeek-V4-Pro.yaml), [SGLang](https://docs.sglang.io/cookbook/autoregressive/DeepSeek/DeepSeek-V4) |
| DeepSeek V4 Pro-0813 (official) · FP4+FP8 mixed | 1,650,497,936,906 (1.65T incl. DSpark layers) | 49B | 892,727,580,904 | 61 (+3 MTP/DSpark) | 9,848 | ≈5,031–5,511 | 1,048,576 | 3 (inference config `n_mtp_layers 3`; config.json says 1 — conflict) | 8×H200 / 8×B200 / 4×GB300 (TP4) / MI355X; H100: 16; vram_min 960 GB | [index](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813/blob/main/model.safetensors.index.json), [card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813), [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/deepseek-ai/DeepSeek-V4-Pro.yaml) |
| DeepSeek V4 Pro · FP8 (sgl-project converted, 3rd-party/engine) | ≈1.6T | 49B | 1,606,501,419,888 (sum of files) | 61 | 9,848 | ≈5,031–5,511 | 1,048,576 | 1 | 16×H200 (2 nodes, TP16) | [HF](https://huggingface.co/sgl-project/DeepSeek-V4-Pro-FP8), [SGLang](https://docs.sglang.io/cookbook/autoregressive/DeepSeek/DeepSeek-V4) |
| DeepSeek V4 Pro-Base · FP8 mixed (base model, not for chat) | 1,600,790,440,862 | 49B | 1,606,048,407,872 (sum of files) | 61 | 9,848 | ≈5,031–5,511 | 1,048,576 | 1 | not given (pre-training use only) | [HF API](https://huggingface.co/api/models/deepseek-ai/DeepSeek-V4-Pro-Base), [card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro) |
| DeepSeek V4 Pro · NVFP4 (nvidia, 3rd-party) | ≈1.6T | 49B | 913,092,561,960 (0813-NVFP4: 941,115,855,096) | 61 | 9,848 | ≈5,031–5,511 | 1,048,576 | 1 (0813: 3) | Blackwell only; 8×B200 (TP8) | [HF](https://huggingface.co/nvidia/DeepSeek-V4-Pro-NVFP4), [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/deepseek-ai/DeepSeek-V4-Pro.yaml) |
| DeepSeek V3.2 · FP8 (reference only) | 685,355,329,792 | 37B (not re-verified here) | 689,483,049,129 (sum of files; index total_size 1,370,793,842,752 is wrong) | 61 | 85,888 (MLA 70,272 + indexer 15,616) | 48,068 (vLLM 656 + 132 B/layer) | 163,840 | 1 | 8×H200 / 8×B200 / 16×H100 (vLLM V3.2 post) | [config](https://huggingface.co/deepseek-ai/DeepSeek-V3.2/raw/main/config.json), [vLLM V3.2 post](https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2025-09-29-deepseek-v3-2.md), [vLLM V4 blog](https://vllm.ai/blog/2026-04-24-deepseek-v4) |
| Kimi K2.7 Code · INT4 QAT (W4A16, g32), the only official precision | 1,026,879,376,368 (1T; incl. ≈0.4B MoonViT) | 32B (derived ≈33.3B incl. vision+embed) | 595,148,192,736 | 61 (1 dense + 60 MoE) | 70,272 | 35,136 (plain FP8; 40,016 if 656-B layout) | 262,144 (YaRN ×64 over 4,096) | 0 (EAGLE3 external draft) | 8×H200 TP8 (vLLM/SGLang); 4×GB300 TP4; 4×MI300X–MI355X TP4 (SGLang); vram_min 714 GB | [index](https://huggingface.co/moonshotai/Kimi-K2.7-Code/blob/main/model.safetensors.index.json), [config](https://huggingface.co/moonshotai/Kimi-K2.7-Code/raw/main/config.json), [card](https://huggingface.co/moonshotai/Kimi-K2.7-Code), [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/moonshotai/Kimi-K2.7-Code.yaml), [SGLang](https://cookbook.sglang.io/autoregressive/Moonshotai/Kimi-K2.6) |
| Kimi K2.7 Code · NVFP4 (nvidia, 3rd-party) | 1T | 32B | 595,185,395,016 (sum of files) | 61 | 70,272 | 35,136 | 262,144 | 0 | Blackwell only (B300 TP8 / GB300 TP4 per the K2.6 cookbook) | [HF](https://huggingface.co/nvidia/Kimi-K2.7-Code-NVFP4), [SGLang](https://cookbook.sglang.io/autoregressive/Moonshotai/Kimi-K2.6) |

All values are as of 2026-10-19.

### Inferences
- **KV values are derived.**
  - Cross-checks: DeepSeek V4/V3.2 BF16 values match vLLM's published 9.62 GiB / 83.9 GiB at 1M. GLM-5.3 FP8 matches the recipe's ~450K tokens in 23 GiB.
  - Kimi and Chandra values follow from the standard MLA/GQA formulas with no engine cross-check.
- **Quick weights-per-GPU numbers** at an even split (index bytes ÷ GPUs):

  | Model | Split | GB per GPU |
  |---|---|---|
  | GLM-5.3 FP8 | ÷8 | ≈94.5 |
  | DeepSeek V4 Pro preview | ÷8 | ≈108 |
  | DeepSeek V4 Pro-0813 | ÷8 | ≈111.6 |
  | Kimi K2.7 Code | ÷8 | ≈74.4 |

  DP-attention deployments replicate the non-expert params on top of this split: about 2.1B for GLM, about 26B for V4, and about 12B for Kimi.

### Gaps
- `active_params` for the third-party quantized rows is assumed equal to the base model.
- The DeepSeek V3.2 active-param figure (37B) is from prior knowledge and was not re-fetched in this session.
- No minimum GPU count is given for V4-Pro-Base.
