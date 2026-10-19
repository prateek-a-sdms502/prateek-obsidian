# Hardware price list: GPU servers and datacenter hardware for an on-prem LLM inference cluster (Pune, India), as of 2026-10-19

Conventions used throughout these notes:
- Prices are **USD, ex-tax (ex-VAT/GST), ex-shipping** unless stated. EUR/GBP listings are left in their own currency and marked ex-VAT where the source says so.
- **INR "(calc)"** = USD x ₹95/USD, ex-GST, not landed. The ₹95 figure is my assumption, based on observed rates of ₹94.84 on 2026-09-08 and ₹95.95 on 2026-09-16 ([dollarrupee.in](https://dollarrupee.in/); [longforecast](https://longforecast.com/usd-to-inr-forecast-2017-2018-2019-2020-2021-indian-rupee)). I found no confirmed October 2026 rate. INR figures quoted directly from Indian sources are labelled "(found)".
- Memory figures marked [2025] are older and have been flagged. 2026 server pricing moved sharply because of the DRAM/HBM shortage (see the Market dynamics section).
- NVIDIA and AMD publish no list prices for datacenter GPUs or servers. Every price here is an OEM web-store price, a reseller listing, a purchase-order observation or an analyst estimate, and is labelled as such.

---

## 1. 8-GPU servers: HGX H200, HGX B200, HGX B300, AMD MI355X, MI325X (prices and specs)

### Takeaway
At US list or reseller prices in 2026, a complete 8-GPU server costs roughly **$310–420k for HGX H200**, **$340–515k for HGX B200** (typically about $385–450k) and **$375–700k for HGX B300** (typically about $500–570k at OEM web stores). **AMD MI325X/MI350X** 8-GPU servers start at about **$256–315k**. No verified US-dollar purchase price exists for an **MI355X** server: one EU listing is about €261k ex-VAT, otherwise quotes are on request. For a single node to hold a 1.6T-parameter MoE at FP8 (about 1.6 TB of weights), the node needs at least about 2.1 TB of HBM, which means B300 (2.1–2.3 TB) or MI355X (2.3 TB). H200 (1.13 TB) and B200 (1.44 TB) cannot do it.

### Cited Findings

**HGX H200 (141 GB HBM3e, 4.8 TB/s per GPU)**
- H200 SXM specs: 141 GB HBM3e, 4.8 TB/s, FP8 Tensor 3,958 TFLOPS *with sparsity* (about 1,979 dense), FP16 1,979 TFLOPS sparse, up to 700 W configurable TDP, NVLink 900 GB/s. H200 NVL (PCIe): 141 GB, 4.8 TB/s, FP8 3,341 TFLOPS sparse, up to 600 W, dual-slot, air-cooled — [NVIDIA H200 page](https://www.nvidia.com/en-us/data-center/h200/)
- Supermicro web store: **SYS-821GE-TNHR, 8U, 8x HGX H200 141GB, starting $323,684.64** (fetched 2026-10-19) — [Supermicro eStore GPU systems p2](https://store.supermicro.com/us_en/systems/gpu.html?p=2)
- Supermicro web store: **AS-5126GS-TNRT, 5U, 5x H200 NVL PCIe, starting $250,961.41** (fetched 2026-10-19) — [Supermicro eStore GPU systems](https://store.supermicro.com/us_en/systems/gpu.html)
- **Lenovo ThinkSystem SR780a V3 (8x H200, Neptune liquid cooling): $311,579.80** in Lenovo's own structured price data. Newegg lists $320,169.50 (out of stock) and a configurable SKU elsewhere is $401,500 — [Lenovo SR780a V3](https://www.lenovo.com/us/en/p/servers-storage/servers/racks/lenovo-thinksystem-sr780a-v3/7dj51000na); [Newegg](https://www.newegg.com/lenovo-thinksystem-sr780a-v3-7dj51000na-rack/p/N82E16859100348); [orangehardwares](https://www.orangehardwares.com/products/7dapcto1ww-lenovo-thinksystem-sr780a-v3-sr680a-v3)
- Dell XE9680 with 8x H200 141GB, 2 TB RAM, 2x Xeon 8462Y+: **$240,000**, 0 in stock, **30-day warranty only**. This is probably refurbished or broker stock, not a new Dell price — [Cloud Ninjas](https://cloudninjas.com/products/dell-poweredge-xe9680-gpu-h200-server)
- Analyst/aggregator range for a complete 8-GPU HGX H200: **$320–420k, about $370k typical** (2026) — [Mercatus H200 server price](https://www.mercatus-ai.com/blog/h200-server-price)
- Outlier: BIZON X9000 G3 (HGX H200/H100) "starting at $172,643". This is far below every other quote and is probably an H100 or partial configuration — [BIZON X9000](https://bizon-tech.com/bizon-x9000.html)

**HGX B200 (180 GB usable HBM3e per GPU, 8 TB/s)**
- NVIDIA HGX B200 (8 GPUs): FP4 144 PF sparse / **72 PF dense**, FP8 72 PF sparse (**36 PF dense, i.e. 4.5 PF per GPU**), FP16/BF16 18 PF dense, **1.4 TB total HBM** (about 180 GB per GPU), NVLink 5 at 1.8 TB/s GPU-to-GPU, **0.8 TB/s networking** (8x400G) — [NVIDIA HGX](https://www.nvidia.com/en-us/data-center/hgx/)
- Mercatus (2026-07-16): B200 at 1,000 W per GPU, 8 TB/s. GPUs alone draw 8 kW; it advises budgeting 12 kW or more of colo capacity. It lists 192 GB per GPU, which is the raw stack size; NVIDIA's HGX page implies 180 GB usable. Integrated 8-GPU price **$400–500k, about $450k typical**. **DGX B200 about $515k**. B200 SXM card $30–40k list (8+ volume) and $45–50k street. Its cost breakdown: GPUs $300–380k, CPU/RAM/chassis $30–35k, NVSwitch about $18k, networking+storage $25–35k, integration/support $15–25k — [Mercatus B200 server price](https://www.mercatus-ai.com/blog/b200-server-price)
- DGX B200: **14.3 kW max system power, 10U** (17.5 x 19.0 x 35.3 in) — [flopper.io DGX B200](https://flopper.io/system/nvidia-dgx-b200); [openzeka DGX B200](https://openzeka.com/en/dgx-b200/)
- **Supermicro SYS-A22GA-NBRT-G1 (10U, 2x Xeon 6960P, 2.3 TB DDR5, 8x B200): $384,228** at Newegg (out of stock) — [Newegg](https://www.newegg.com/supermicro-gold-series-sys-a22ga-nbrt-g1-rack/p/N82E16859152392). The same G1 configuration with 2 TB RAM and 8x ConnectX-7 is **€397,336 ex-VAT** at Ahead-IT (no local stock) — [Ahead-IT](https://www.ahead-it.eu/en/shop/hardware/supermicro/supermicro-sys-a22ga-nbrt-g1-gold-x14-gpu10u-hgx-2x6960p-2tb-dimm-8xb200-8xcx7-1)
- **Exxact TensorEX 10U HGX B200**: Xeon variant from **$384,076**, EPYC variant from **$389,713.50**, Xeon 6900 "Essential" configuration **$403,298.50** — [Exxact TS4-124903244](https://www.exxactcorp.com/Exxact-TS4-124903244-E124903244); [Exxact TS4-154079096](https://www.exxactcorp.com/Exxact-TS4-154079096-E154079096); [Exxact configurator](https://configurator.exxactcorp.com/configure/TS4-169219634)
- A GPU price tracker shows 8x B200 Supermicro systems "last listed" at about $384–394k on Newegg (2026-09-21) — [gpuperhour](https://gpuperhour.com/blog/nvidia-gpu-prices)
- Lower quotes: Aivres HGX B200 platform from about $340k; TurboMax Supermicro SYS-A22GA-NBRT $341,000, though its spec sheet's CPUs don't match. Outlier: Vipera lists SYS-A22GA-NBRT-1 at $795,000 — [Mercatus](https://www.mercatus-ai.com/blog/b200-server-price); [TurboMax](https://turbomaxgpu.com/product/supermicro-hgx-b200-gpu-server-supermicro-sys-a22ga-nbrt-ai-enterprise/); [Viperatech](https://viperatech.com/product/supermicro-gpu-superserver-sys-a22ga-nbrt-1)

**HGX B300 / Blackwell Ultra (up to 288 GB HBM3e per GPU, about 270 GB as shipped by Dell, 8 TB/s)**
- NVIDIA HGX B300 (8 GPUs): FP4 144 PF sparse / **108 PF dense (13.5 PF per GPU)**, FP8 72 PF sparse / **36 PF dense (4.5 PF per GPU)**, **2.1 TB total HBM**, NVLink 5 at 1.8 TB/s, **1.6 TB/s networking** (8x800G ConnectX-8). FP64 is cut to 10 TFLOPS, versus 296 on B200 — [NVIDIA HGX](https://www.nvidia.com/en-us/data-center/hgx/)
- Per-GPU HBM is quoted at 270 GB (Dell XE9785), 279 GB usable and 288 GB maximum. One reference architecture gives 2.3 TB total. Per-GPU power is 1,100 W in Dell's air-cooled XE9785 listing; other sources give 1,200–1,400 W, and 1,400 W applies to GB300 / liquid-cooled parts — [GPU Smith HGX B300](https://gpusmith.com/articles/en/nvidia-hgx-b300-price-specs); [Dell XE9785](https://www.dell.com/en-us/shop/ipovw/poweredge-xe9785); [SemiAnalysis InferenceX B300](https://inferencex.semianalysis.com/chips/b300)
- **Supermicro web store (fetched 2026-10-19): SYS-822GS-NB3RT (8U, Intel) from $545,173.05; AS-8126GS-NB3RT (8U, AMD EPYC) from $570,220.95.** The -01-G2 Gold-series variants are listed without a price — [Supermicro eStore GPU systems](https://store.supermicro.com/us_en/systems/gpu.html)
- **Thinkmate A+ Server 8126GS-NB3RT: from $699,977** (fetched 2026-10-19) — [Thinkmate Supermicro AMD](https://www.thinkmate.com/systems/supermicro/superserver/amd?b=)
- **BIZON X9000 G5 (8U, air-cooled, 8x HGX B300): from $496,639.** Supports up to 3 TB DDR5 (EPYC) or 4 TB (Xeon), 8x Gen5 NVMe bays, 8x 800G ConnectX-8 OSFP, 12x 3,000 W Titanium PSUs (6+6). **Lead time 9–10 weeks, ships Dec 18–28 2026**, 9 units shown in stock. Its stated draw of "2,700–2,900 W at 100% load" is implausible when 8x 1,100 W GPUs alone draw 8.8 kW, so treat it as an error. Its 84.5 kg shipping weight also looks low next to Dell's 163.65 kg — [BIZON X9000 G5](https://bizon-tech.com/bizon-x9000-g5.html)
- Supermicro SYS-822GS-NB3RT via TurboMax: **$420,000**. Configuration: 2x Xeon 6767P, **3 TB DDR5**, **8x ConnectX-8 800G**, six 6,600 W Titanium PSUs, air-cooled 8U. Petronella lists a bare HGX B300 baseboard "from $485,000" with no CPU, RAM or chassis — [GPU Smith HGX B300](https://gpusmith.com/articles/en/nvidia-hgx-b300-price-specs)
- **Dell PowerEdge XE9785** (8x HGX B300 NVL8 270 GB 1,100 W SXM6, *or* 8x AMD MI355X 288 GB 1,400 W OAM). Weight fully populated **163.65 kg (360.79 lb)**, 24 DDR5-6400 DIMM slots, air-cooled with 15 hot-swap GPU fans. A liquid-cooled XE9785L was announced. Lead time via Uvation about 4 weeks, quoted as a floor. No public Dell price — [GPU Smith](https://gpusmith.com/articles/en/nvidia-hgx-b300-price-specs); [Dell XE9785](https://www.dell.com/en-us/shop/ipovw/poweredge-xe9785); [Uvation](https://marketplace.uvation.com/dell-poweredge-xe9785-8x-nvidia-hgx-b300-270gb-gpu-server/)
- Servermall (EU) lists an XE9785 16NVMe at €736,091 / €890,670 ex-VAT. The page layout is jumbled, so it is unclear whether those figures are the B300 or MI355X configuration — [Servermall XE9785](https://servermall.com/catalog/servers/dell-poweredge-xe9785-16nvme/)
- **Gigabyte G894-SD3/AD3/ZD3-AAX7 (8U HGX B300): $375,000** (special order, esaitech). Servermall EU lists G894 configurations at about €1.1–1.4M ex-VAT, which looks like a fully loaded or outlier configuration — [esaitech Gigabyte G894](https://esaitech.com/products/gigabyte-g894-sd3-aax7-intel-xeon-8u-rackmount-gpu-server); [Servermall B300](https://servermall.com/sets/servers-with-b300/)
- **ASUS XA NB3I-E12 (9U HGX B300): Viperatech $440,000 list / $395,000 sale, with a separate $348,000 figure.** NTS lists a related configuration at $480,965. One sample configuration: 2x Xeon 6760P, 2.048 TB DDR5, 3.84 TB + 61.44 TB SSD, 8x CX-8, 10x 3,200 W PSU — [Viperatech ASUS](https://viperatech.com/product/asus-xa-nb3i-e12-gpu-server); [rackmountnts](https://www.rackmountnts.com/asus-xa-nb3i-e12); [Microless config](https://global.microless.com/product/xa-nb3i-e12-8-gpu-server-2x-intel-xeon-6760p-64-cores-2-048tb-ddr5-ram-3-84tb-ssd-61-44tb-ssd-nvidia-hgx-b300-288gb-baseboard-with-8-cx8-infiniband-10x-3200w-psu/)
- **HPE ProLiant Compute XD685**: B300 HGX option, **5U direct liquid cooled or 6U air-cooled**, up to 3.0 TB RAM. "Submit your request for a custom quote"; no published list price — [HPE XD685](https://buy.hpe.com/us/en/compute/rack-servers/proliant-compute-xd600-servers/proliant-compute-xd600-server/hpe-proliant-compute-xd685/p/1014862906); [server-configurator XD685](https://server-configurator.com/configure/hpe/xd685)
- **NVIDIA DGX B300**: about **$400k US** (PCMag citing the FT, July 2026); EU resellers **€535k–714k**. EU configuration: 2x Xeon 6776P, 2 TB RAM, 30 TB NVMe, 8x 400G IB + 4x 400G Ethernet, about **14 kW** system power — [GPU Smith](https://gpusmith.com/articles/en/nvidia-hgx-b300-price-specs). Another source gives DGX B300 at **14.5 kW** — [flopper.io DGX B200 vs B300](https://flopper.io/compare-systems/nvidia-dgx-b200-vs-nvidia-dgx-b300)
- Analyst guides put a complete 8-GPU HGX B300 at **$550–750k (Sept 2026)**. A March 2026 guide said $250–400k, which is stale given the memory-driven increases — [search summary of gpusmith/qdna/haink guides](https://qdna.fr/en/architecture/materiel/b300-sxm); [haink.org](https://haink.org/knowledge/technology/ai-infrastructure-cost-guide)
- B300 single GPU is about **$53,000**, based on "July 2026 industry reporting" — [Cyfuture India B300 price](https://cyfuture.ai/blog/nvidia-b300-gpu-price-in-india)

**AMD Instinct MI355X (288 GB HBM3e, 8 TB/s, 1,400 W)**
- MI355X: 288 GB HBM3e, 8 TB/s, **FP8 5,033 TFLOPS dense** (10,066 sparse), **FP4/FP6 10,066 TFLOPS dense** (20,133 sparse), FP16 about 2,517 dense, **TBP 1,400 W**, 8-way OAM UBB — [Glenn Klockwood MI355X](https://glennklockwood.com/garden/processors/MI355X); [SemiAnalysis InferenceX MI355X](https://inferencex.semianalysis.com/chips/mi355x). AMD states the liquid-cooled option "enables MI355X GPUs to consume up to 1400W" — [AMD MI355X platform brochure](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/product-briefs/amd-instinct-miI355x-platform-brochure.pdf)
- MI355X systems: Supermicro **AS-4126GS-NMR-LCC (4U, direct liquid cooled, needs facility water and a CDU)**; Gigabyte G893-ZX1-AAX4 (8U); MiTAC 4U liquid-cooled; Dell XE9785 — [Supermicro datasheet](https://www.supermicro.com/en/products/system/datasheet/as-4126gs-nmr-lcc); [Thinkmate Gigabyte G893](https://www.thinkmate.com/system/gigabyte-g893-zx1-aax4?b=); [MiTAC](https://www.mitaccomputing.com/products/detail/g4826z5u2bc-355x-575)
- **Price: smicro.eu lists the AS-4126GS-NMR-LCC-G1 at €261,442.82 ex-VAT** ("only valid for available quantity"). The page returned HTTP 403 when I fetched it, so I could not confirm the GPU/CPU configuration — [smicro.eu](https://smicro.eu/supermicro-as-4126gs-nmr-lcc-g1-2). Pantheon gives pricing on request with a **4–8 week lead time** — [Pantheon](https://pantheon.run/hardware/amd-instinct-mi355x-supermicro)
- MI355X per-GPU price estimate: **about $30,000 ($25,500–34,500)**. This is an unsourced aggregator estimate — [GPU Advisor](https://gpuadvisor.com/gpu/mi355x)
- Cloud reference: Oracle BM.GPU.MI355X.8 costs $68.80/hr per node ($8.60/GPU-hr) — [getdeploying MI355X](https://getdeploying.com/gpus/amd-mi355x)

**AMD Instinct MI325X (256 GB HBM3e, 6 TB/s, 1,000 W)**
- MI325X: 256 GB HBM3E, 6 TB/s, FP8 about 2.6 PF (2,615 dense TFLOPS), BF16 1,307 dense, **no FP4**, 1,000 W TDP — [SemiAnalysis InferenceX MI325X](https://inferencex.semianalysis.com/chips/mi325x); [Glenn Klockwood MI325X](https://glennklockwood.com/garden/processors/MI325X); [Gigazine](https://gigazine.net/gsc_news/en/20241011-amd-instinct-mi325x-mi355X)
- **Supermicro AS-8126GS-TNMR (8U, 8x MI325X *or* MI350X OAM): from $256,301.19** at the Supermicro store (2026-10-19). Thinkmate lists it at $314,626 now (an earlier snippet showed $304,946). Newegg's AS-8126GS-TNMR-G1 is $261,601 — [Supermicro eStore](https://store.supermicro.com/us_en/systems/gpu.html); [Thinkmate](https://www.thinkmate.com/systems/supermicro/superserver/amd?b=); [Newegg search](https://www.newegg.com/p/pl?d=amd+instinct+mi325x)
- Servermall EU: AS-8126GS-TNMR with 8x MI325X at €382,604 or €593,037 ex-VAT; the listing does not say which is current — [Servermall MI325X](https://servermall.com/sets/servers-with-amd-mi325x/)
- For reference, the older MI300X (192 GB): Supermicro AS-8125GS-TNMR2 from $284,970.87 at the store, $360,808 at Thinkmate — [Supermicro eStore p2](https://store.supermicro.com/us_en/systems/gpu.html?p=2); [Thinkmate](https://www.thinkmate.com/systems/supermicro/superserver/amd?b=)

### Inferences
- **Memory-per-node fit for the target models.** These are weights only and exclude KV cache.
  - FP8 sizes: 1.6T params ≈ 1.6 TB; 0.75T ≈ 0.75 TB. At FP4 the sizes halve.
  - **H200 node (1.13 TB HBM)**: fits 0.75T at FP8 with limited KV headroom. A 1.6T model needs 2 nodes at FP8, or FP4 on Blackwell (H200 has no FP4).
  - **B200 node (1.44 TB)**: fits 0.75T comfortably. 1.6T fits only at FP4 (about 0.8 TB).
  - **B300 node (2.1–2.3 TB)** and **MI355X node (2.3 TB)**: fit 1.6T at FP8 on a single node, with about 0.5–0.7 TB left for KV cache.
  - This is my arithmetic from the HBM figures above.
- **Price per TB of HBM.**
  - H200: about $290–370k per TB.
  - B200: about $270–310k per TB.
  - B300: about $240–270k per TB at store prices ($545–570k for 2.1–2.3 TB).
  - MI325X: about $125–155k per TB ($256–315k for 2.05 TB).
  - MI355X: likely the lowest $/TB if the roughly €261k EU listing holds, but I could not verify that.
- **Typical US-store prices to use for budgeting (ex-tax, ex-shipping):**
  - H200: about $325k
  - B200: about $390k
  - B300: about $545–570k
  - MI325X/MI350X: about $260–310k
  - MI355X: about $280–400k (inferred)
- **Power planning.** Budget about 10 kW per H200 node and about 14–14.5 kW per B200/B300/MI355X node. MI355X: 8 x 1.4 kW = 11.2 kW for GPUs alone, so about 14–15 kW per system (inferred). Air-cooled B300 at about 14 kW in 8U implies at most 2 nodes per 30 kW rack. Most Indian colo racks (8–12 kW) cannot host even one node without special high-density provisioning.

### Gaps
- No public Dell (XE9680/XE9780/XE9785), HPE (XD685) or Lenovo B200/B300 list prices; all three require quotes.
- No verified USD purchase price for a complete MI355X 8-GPU server. The smicro.eu configuration could not be verified (403).
- No official NVIDIA weight figure for DGX/HGX B200/B300. The DGX B200 weight of 170.45 kg comes from a reseller listing that also gives a contradictory power figure — [anafrashop](https://anafrashop.com/nvidia-dgx-b200-8x-180gb-full-bussiness-std-dgxb-g1440-p2ini48-5)
- No sourced max system power for HGX H200. The DGX H200 is commonly cited at about 10.2 kW, but I did not fetch an NVIDIA source.
- Liquid-cooled B300 variants (Supermicro DLC, Dell XE9785L, HPE XD685 DLC) have no public prices.

---

## 2. Rack-scale: GB200 NVL72 and GB300 NVL72

### Takeaway
A GB300 NVL72 rack transacts at **just under $5.0M EXW without a CDU** (August 2026 purchase orders). Published estimates run from $3.7M to $6.5M. A GB200 NVL72 rack is about **$3M**. A GB300 rack draws **132 kW nominal and about 155 kW peak**, is **100% liquid-cooled** with a 200–250 kW in-rack CDU, and weighs about **1.36 t** (nearly 4,000 lb crated). That load is beyond most Indian enterprise or colo rooms without purpose-built DLC facility water.

### Cited Findings
- **GB300 NVL72**:
  - Price: from August 2026 purchase orders, "just under $5.0M" without an in-rack CDU, **plus about $32K for a 250 kW CDU**; about $69K per GPU slot. EXW, so delivery is the buyer's responsibility.
  - Contents: 72 B300 GPUs, 36 Grace CPUs, 18 compute trays and 9 NVLink switch trays; 288 GB HBM3e per GPU, about 21 TB per rack.
  - Power and weight: 132–140 kW per rack; nearly 4,000 lb crated.
  - Other figures: 3-year warranty plus extensions; deployed cost about $5.7M excluding core switching and storage; network attach "several hundred thousand dollars"; GB300 module about $40–50K per GPU.
  - Source: [Data Gravity, 2026-08-31](https://www.datagravity.dev/p/how-much-does-an-nvidia-nvl72-cost)
- GB300 NVL72 estimates:
  - Tom's Hardware (March 2026): **$6.0–6.5M**
  - Loop Capital: **$3.7–4.0M** hardware only
  - Wolfe Research (2026-01-30): about **$4.3M**
  - Sources: [Data Gravity](https://www.datagravity.dev/p/how-much-does-an-nvidia-nvl72-cost); [Spheron GB300 vs GB200](https://www.spheron.network/blog/gb300-nvl72-vs-gb200-nvl72-pricing-availability-2026/); [Wing VC](https://www.wing.vc/content/how-much-does-an-nvidia-nvl72-cost)
- **GB200 NVL72**: about **$3M** (Barron's / Tae Kim); Tom's Hardware **$2.8–3.4M**; Wolfe (January 2026) about $3M. **[2025] SemiAnalysis (2025-08-20): $3.1M for the rack alone, $3.9M all-in with networking and storage** — [Data Gravity](https://www.datagravity.dev/p/how-much-does-an-nvidia-nvl72-cost); [Wing VC](https://www.wing.vc/content/how-much-does-an-nvidia-nvl72-cost)
- GB300 premium over GB200 is about 10–30% per analyst estimates — [Spheron](https://www.spheron.network/blog/gb300-nvl72-vs-gb200-nvl72-pricing-availability-2026/)
- **GB300 NVL72 power** (HPE): **TDP 132 kW nominal, EDPp (peak) about 155 kW; provision busways for 192 kW**; 8 power shelves at up to 33 kW each on a DC busbar — [HPE collateral a50009244enw](https://www.hpe.com/us/en/collaterals/collateral.a50009244enw.html)
- **Gigabyte GB300 NVL72**:
  - Power: 6x 1U 33 kW power shelves; rack power up to **140 kW**.
  - CDU options: **in-rack liquid-to-liquid CDU, 200 kW** capacity (4 °C approach), 1+1 redundant pumps and PSUs; or an **in-row CDU at 1,350 kW**.
  - Facility water must meet ASHRAE water-quality guidance.
  - Source: [Gigabyte GB300 NVL72](https://www.gigabyte.com/Enterprise/GIGAPOD-Pod-Scale/AI-DLC-POD_NVIDIA-GB300-NVL72)
- Weight is about **1.36 t (3,000 lb)** on a standard 42U-rack footprint, which requires a floor-loading check. This is a secondary source — [Introl GB300](https://introl.com/blog/why-nvidia-gb300-nvl72-blackwell-ultra-matters); [Sunbird DCIM](https://www.sunbirddcim.com/blog/how-much-power-does-nvidia-gb300-nvl72-need)
- GB300 in-rack thermal hardware is about **$49,860 per rack**, about 20% more than GB200's roughly $42K (Morgan Stanley via Tom's Hardware/Guru3D) — [Guru3D](https://www.guru3d.com/story/3f5782f43f98056f6165e6938b8fa0f8e06adaeb); [Data Gravity](https://www.datagravity.dev/p/how-much-does-an-nvidia-nvl72-cost)
- Running costs: $240–410K per year in electricity ($0.05–0.15/kWh). Wholesale colo is about $196/kW-month ([2025] Encor, H2 2025) — [Data Gravity](https://www.datagravity.dev/p/how-much-does-an-nvidia-nvl72-cost)
- India, in rupees: Cyfuture estimates GB300 NVL72 at ₹25.2–33.6 crore, but it uses a stale ₹84/USD rate on a $3–4M estimate — [Cyfuture](https://cyfuture.ai/blog/nvidia-b300-gpu-price-in-india)

### Inferences
- At ₹95/USD, a roughly $5.0M GB300 NVL72 is about **₹47.5 crore ex-GST and ex-freight**, plus about $32k (≈₹30 lakh) for the CDU.
- On a per-GPU basis (about $69k), NVL72 costs more than HGX B300 (about $68–71k per GPU at $545–570k per server). Its benefit is a 72-GPU NVLink domain, which matters for very large MoE expert parallelism. For 1–4 nodes serving 0.75–1.6T models, NVL72 is likely oversized and carries heavy facility requirements (130–155 kW, DLC, facility water).

### Gaps
- No primary NVIDIA datasheet value for GB200 NVL72 rack power (commonly about 120 kW) or weight was retrieved.
- No India-landed purchase quote for GB200/GB300 NVL72 was found.

---

## 3. OCR-class GPUs: L40S, RTX PRO 6000 Blackwell Server Edition, L4, H100 NVL / H200 NVL

### Takeaway
For a 4B OCR model, a few PCIe cards are enough. The **RTX PRO 6000 Blackwell Server Edition (96 GB GDDR7, 600 W)** costs about **$16–20k per card** through the channel, with eBay averages around $23k after a 2026 run-up. Supermicro sells a **4x RTX PRO 6000 4U server from $127,673**. The **L40S** is about **$7.5–10k**, the **L4** about **$2.5–2.8k** and the **H100 NVL** about **$29–35k**.

### Cited Findings
- **RTX PRO 6000 Blackwell Server Edition** (96 GB GDDR7 ECC, PCIe 5.0 x16, passive, dual-slot FHFL, 600 W)
  - CDW kit SKU: $16,115 (page printed 2026-10-15). A second CDW listing: $33,327 against a $57,002 "list".
  - ServerBasket: $18,439; Hyperscalers RRP: $20,224; Central Computer kit: $15,499.99 (page about 251 days old, roughly February 2026); Newegg third-party seller: $35,900.
  - Sources: [CDW kit](https://www.cdw.com/product/nvidia-rtx-pro-6000-blackwell-server-edition-graphics-card-rtx-pro-60/8426124); [CDW](https://www.cdw.com/product/nvidia-server-edition-graphics-card-rtx-pro-6000-blackwell-96-gb/8474881); [ServerBasket](https://www.serverbasket.net/p/nvidia-rtx-pro-6000-blackwell-server-edition-gpu/); [Hyperscalers](https://www.hyperscalers.com/NVIDIA-RTX-PRO-6000-Blackwell-Server-Edition); [Central Computer](https://www.centralcomputer.com/all-products/ai-components/ai-gpus/rtx-pro-6000-blackwell.html); [Newegg](https://www.newegg.com/nvidia-900-2g153-0000-000-rtx-pro-6000-96gb-graphics-card/p/N82E16814132104)
- GPU Poet (eBay-based): **October 2026 lowest average $23,332, up 30.8% from the prior three months**; estimated MSRP $13,825 based on CDW list — [GPU Poet Oct 2026](https://gpupoet.com/gpu/learn/price/october-2026/nvidia-rtx-pro-6000-blackwell-server)
- Card about $16,000 on NVIDIA's marketplace versus **[2025] launch MSRP $8,565 (March 2025)**. Single source — [Thunder Compute RTX PRO 6000 pricing](https://www.thundercompute.com/blog/nvidia-rtx-pro-6000-pricing)
- **Supermicro web store (2026-10-19)**:
  - **SYS-422GA-NRT-01-G2, 4U, 4x RTX PRO 6000 BSE: $127,673**
  - **AS-5126GS-TNRT-01-G2, 5U, 2x RTX PRO 6000: $104,669.55**
  - **SYS-212GB-FNR-01-G2, 2U, 2x RTX PRO 6000: $66,680.45**
  - Barebone 8-double-wide-GPU chassis: SYS-422GL-NR $61,303; SYS-522GA-NRT $61,224; SYS-422GA-NRT $25,850
  - Source: [Supermicro eStore](https://store.supermicro.com/us_en/systems/gpu.html)
- **8x RTX PRO 6000 servers**: ServerMall EU **€168,524 (Gigabyte) to about €241,000**, with the ASUS ESC8000A-E13X at €171,631 ex-VAT (+€36,043 VAT; shipping to EU/UK/US included). ctoservers UK lists **£147,780** and an enterprise configuration at **£186,780** — [ServerMall RTX PRO 6000](https://servermall.com/sets/servers-with-rtx-pro-6000/); [ctoservers](https://www.ctoservers.com/rtx-pro-6000-blackwell-222-c.asp)
- **L40S 48 GB**: market about **$9.0k** against an MSRP of about $8.0k; another guide gives **$7,500–10,000** per GPU. **8x L40S server (dual 96-core EPYC 9004): £79,850** at ctoservers, undated — [gpucost.org L40S](https://gpucost.org/gpu/l40s); [Spheron L40S](https://www.spheron.network/blog/nvidia-l40s-for-ai-inference/); [ctoservers](https://www.ctoservers.com/rtx-pro-6000-blackwell-222-c.asp)
- **L4 24 GB** (72 W): MSRP about $2.5k, market about **$2.8k**. Single aggregator source — [gpucost.org GPU prices](https://gpucost.org/gpu-prices)
- **H100 NVL 94 GB**: about **$29,000** (single GPU) per one source; market about **$35k** per a price table. H100 SXM card is about $27–40k — [IntuitionLabs](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide); [gpucost.org](https://gpucost.org/gpu-prices)
- **H200 NVL 141 GB PCIe** (600 W): reseller about **$32,366**; eBay listing $47,500 — [Mercatus H200 price](https://www.mercatus-ai.com/blog/h200-price)
- India, in rupees: an entry 1-GPU server (e.g. L40S) is about **₹5–25 lakh** and a 2–4 GPU server about **₹25 lakh–1 crore** (indicative, July 2026) — [Proactive Data Systems](https://proactive.co.in/blog-details/what-a-gpu-server-really-costs)

### Inferences
- For a 4B OCR model (about 8 GB at BF16), one L40S or RTX PRO 6000 per replica is ample. A 2-GPU 2U RTX PRO 6000 server ($66.7k at Supermicro, ≈₹63 lakh calc) or a 4-GPU 4U ($127.7k, ≈₹1.21 crore calc) covers HA plus throughput.
- An 8x L40S server at about £80k is probably the cheapest dense option. Its date is unknown, and in 2026 the L40S is being displaced by the RTX PRO 6000.
- Card-only builds land at roughly: 4x RTX PRO 6000 at about $64–80k for cards plus about $25–60k for the chassis, CPU and RAM. The 2026 DRAM costs in section 5 inflate the RAM share.

### Gaps
- No 2026-dated US price for a 4x or 8x L40S server from a major OEM.
- No Indian distributor INR card prices for the L40S, RTX PRO 6000 or L4.
- No L40S power figure from a fetched source; NVIDIA's spec is commonly 350 W, but this is unverified here.

---

## 4. Networking for multi-node (InfiniBand NDR/XDR, RoCE/Spectrum-X, front-end Ethernet)

### Takeaway
Switches cost about **$31–53k for a QM9700 (64x400G NDR)**, **$55–89k for an SN5600 (64x800GbE)** and **about $130k for a Quantum-X800 Q3400 (144x800G XDR)**. Per-port switch cost is roughly $500–1,000. NICs: ConnectX-7 400G about $1.6–1.8k list, ConnectX-8 about $1.8–2.8k, BlueField-3 B3220 about $4.5–6k new. 800G twin-port optics range widely, from about $360 to $1,100 for NVIDIA-branded parts at grey-market resellers, and compatible SR8 modules are about $550. HGX B200/B300 servers usually ship with their 8 compute NICs included, so the incremental cost per node is mainly switch share, optics and cables. I estimate that at about $25–55k per node for a 2–8 node cluster (inference).

### Cited Findings
- **NVIDIA Quantum-2 QM9700** (64 NDR 400G ports over 32 OSFP, managed). Prices:
  - Getitnew: **$30,923** new
  - Colfax: $34,555
  - SHI: $38,008 (MSRP $44,462)
  - FS.com: $38,400
  - Naddod: **$53,448** with 5-year service
  - Europe: €25–30k, new or refurbished
  - Sources: [Getitnew](https://getitnew.com/mqm9700-ns2r-nvidia-qm9700-quantum-2-based-ndr-infiniband-switch-64-port-ndr-c2p-airflow-managed-new/); [Colfax](https://colfaxdirect.com/store/pc/viewPrd.asp?idproduct=4163); [SHI](https://www.shi.com/product/44450991/NVIDIA-Quantum-2-QM9700); [FS.com](https://www.fs.com/products/194710.html); [Naddod](https://www.naddod.com/products/nvidia-networking/102408); [server-parts.eu](https://www.server-parts.eu/post/nvidia-qm9700-qm9790-quantum-x800-infiniband-switches)
- **NVIDIA Quantum-X800 Q3400-RA** (144 XDR 800G ports over 72 OSFP): Naddod **$129,999**; server-parts.eu €60–80k. These two sources conflict — [Naddod Q3400](https://www.naddod.com/products/nvidia-networking/102612); [server-parts.eu](https://www.server-parts.eu/post/nvidia-qm9700-qm9790-quantum-x800-infiniband-switches)
- **NVIDIA Spectrum-4 SN5600** (64x 800GbE OSFP, 2U, Spectrum-X RoCE). Prices:
  - Naddod: **$55,250**
  - Hardware Nation: $67,213
  - Capital City: $73,409
  - Server Supply: $76,500
  - Avendor: $71,246 sale / $87,125 regular
  - LTT: **$89,445**
  - GPU Smith street range: **$65–87k**; used units near $18,750
  - Sources: [Naddod SN5600](https://www.naddod.com/products/nvidia-networking/102424); [Hardware Nation](https://hardwarenation.com/product/nvidia-spectrum-sn5600-ethernet-switch-920-9n42f-00ri-7c0/); [Server Supply](https://www.serversupply.com/NETWORKING/SWITCH/64%20PORT/NVIDIA/920-9N42F-00RI-7C0_383148.htm); [LTT](https://www.lttpartners.com/products/nvidia-spectrum-sn5600-ethernet-switch); [GPU Smith SN5600](https://gpusmith.com/hardware/networking/nvidia-spectrum-x-sn5600)
- GPU Smith notes that for a rail-optimised build, 800G optics/DACs plus SuperNICs "typically cost more in aggregate than the switches" (single source) — [GPU Smith SN5600](https://gpusmith.com/hardware/networking/nvidia-spectrum-x-sn5600)
- **ConnectX-7 400G**: Gatewell single-port OSFP $1,750 list; Naddod $1,599; street $1,800–3,700 — [Gatewell](https://gatewellusa.com/ai-compute/interconnect); [GPU Smith CX-7](https://gpusmith.com/hardware/networking/nvidia-connectx-7)
- **ConnectX-8 SuperNIC 800G**: Gatewell C8180 $2,300 list; Naddod C8180/C8240 $1,779; FiberMall estimates $2,500–2,800+ (mid-2026) — [Gatewell](https://gatewellusa.com/ai-compute/interconnect); [Naddod CX-8](https://www.naddod.com/collections/nvidia-networking/connectx-8); [FiberMall](https://www.fibermall.com/blog/connectx-7-vs-connectx-8.htm)
- **BlueField-3 B3220** (dual 200G DPU): Naddod $5,499 (crypto off) / $5,959 (crypto on); FiberMall $4,490; eBay new $3,476–4,400 and used about $2,500 — [Naddod BF-3](https://www.naddod.com/collections/nvidia-networking/nvidia-bluefield-3-dpus-and-supernics); [FiberMall B3220](https://www.fibermall.com/sale-462652-nvidia-b3220.htm)
- **800G OSFP twin-port 2xSR4 MMA4Z00-NS** (850 nm, 50 m):
  - NetworkTigers: $612 / $1,102 (newer revision)
  - CDW Canada: $4,209.99, likely CAD
  - Flat-top MMA4Z00-NS-FLT: $362 at NetworkTigers; Channel Online $2,987 (MSRP $2,624)
  - Finned MMA4Z00-NS-T: Saitech $1,384 (regular $1,825), 1–3 week lead
  - Compatible OSFP-800G-SR8D: **$550** at FiberMall
  - Sources: [NetworkTigers](https://www.networktigers.com/a/s/products/mma4z00-ns-nvidia-osfp); [CDW.ca](https://cdw.ca/product/nvidia-osfp-transceiver-module-800-gigabit-ethernet/7811847); [Channel Online](https://global.channelonline.com/acme/ccs/Products/overview/M024204504); [Saitech](https://esaitech.com/products/nvidia-mma4z00-ns-t-800gbps-transceiver-media-converter); [FiberMall SN5600 page](https://www.fibermall.com/sale-462660-nvidia-sn5600.htm)
- **Front-end 100GbE (32-port)**: NVIDIA SN2700 at Connection $14,631–17,912 (out of stock), EU €20,422 ex-VAT; refurbished Arista 7060CX2-32S **$2,999** (xByte) — [Connection SN2700](https://www.connection.com/product/nvidia-sn2700-32-port-40gbe-switch-w-cumulus-linux-p2c-airflow/msn2700-bs2fc/32025747); [xByte](https://www.xbyte.com/products/cat-22734-ra)
- **Front-end 25GbE (48x25G + 8x100G)**: Arista 7050SX3-48YC8 **$7,499**; 7280SR3-48YC8 $15,899 (xByte, refurbished/resale); EdgeCore AS7326-56X used $2,900 — [xByte](https://www.xbyte.com/products/cat-28483); [eBay EdgeCore](https://www.ebay.com/itm/257086401081)
- HGX B300 servers usually include 8x ConnectX-8 800G (Supermicro SYS-822GS-NB3RT, BIZON X9000 G5, ASUS XA NB3I-E12). HGX B200 servers usually include 8x ConnectX-7 400G (Supermicro A22GA-NBRT-G1) — [GPU Smith](https://gpusmith.com/articles/en/nvidia-hgx-b300-price-specs); [BIZON](https://bizon-tech.com/bizon-x9000-g5.html); [Ahead-IT](https://www.ahead-it.eu/en/shop/hardware/supermicro/supermicro-sys-a22ga-nbrt-g1-gold-x14-gpu10u-hgx-2x6960p-2tb-dimm-8xb200-8xcx7-1)
- India, in rupees: cluster networking is about **₹5–15 lakh per rack**, indicative — [Proactive](https://proactive.co.in/blog-details/what-a-gpu-server-really-costs)

### Inferences
- **Per-port switch cost**:
  - QM9700: about $480–835 per 400G port ($31–53k / 64)
  - SN5600: about $860–1,400 per 800G port
  - Q3400: about $900 per 800G port (at $130k / 144)
- **Per-node back-end fabric, 4-node B300 cluster on one SN5600 or Q3400** (my arithmetic, not a sourced quote):
  - Switch share: about $14–33k per node
  - Optics: 8 links x 2 ends x about $550–1,100, so about $9–18k per node
  - Cables: MPO fibre, not priced
  - NICs: included in the server
  - **Total: about $25–50k per node.** At 8 nodes the switch share halves.
- **Front-end per node**: 2x 100G/25G ports plus optional BF-3 DPUs (about $4.5–6k each) plus a share of a $3–17k ToR switch, so about **$5–15k per node**.
- **For a 2-node configuration** (e.g. 2x H200 or 2x B200 for a 1.6T model at FP8), a single QM9700 or SN5600 is enough. Very small clusters can also be built with direct-attach cabling, but that limits growth.
- InfiniBand (QM9700/Q3400) versus RoCE (SN5600): switch prices are comparable at this scale. RoCE/Spectrum-X lets the same Ethernet skill set run the front end. That is an operational inference, not a sourced claim.

### Gaps
- No sourced price for the 400G single-port OSFP NIC-side transceiver (MMA4Z00-NS400), OSFP DAC/ACC cables or MPO fibre trunks.
- No NVIDIA list prices. Most listings are grey-market or reseller; airflow direction, warranty and condition vary.
- No Indian distributor INR prices for NVIDIA networking.

---

## 5. Storage and host memory (NVMe for weights, DDR5 for KV-cache offload)

### Takeaway
DDR5 RDIMM is now a **major cost line in 2026**. Prices per 64 GB RDIMM:
- **$873** in Q1 2026 (Citi)
- **$1,586** forecast for Q4 2026 (Citi)
- **about $1,970–2,064** spot/street in September 2026

That is about **$14k–33k per TB**, so 2 TB of host RAM costs about $28–66k and **4 TB about $56–132k per server**. Enterprise NVMe is far cheaper per TB: typical U.2 drives are **$80–150/TB** (Q1 2026 benchmark) and a 15.36 TB QLC drive is about $1,800, so several TB of model weights per server costs only a few thousand dollars.

### Cited Findings
- **64 GB DDR5 RDIMM**: Citi (May 2026 note) **$873 in Q1 2026, rising to about $1,586 by Q4 2026 (+82%)**. Server DRAM contract prices rose **+93–98% QoQ in Q1 2026** and **+53–63% in Q2 2026**, with **+13–18% forecast for Q3 2026** (TrendForce via aggregators) — [ServnetUK DDR5 tracker, 2026-07-09](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026)
- A spot-style board showed **RDIMM-64G at $1,970 on 2026-09-09**. DatacenterDisk (updated 2026-09-17) lists the cheapest in-stock 64 GB RDIMM at **$32.25/GB (about $2,064 per module)**, with others at about $2,245–2,976 — [DatacenterDisk 64GB RDIMM](https://datacenterdisk.com/server-ram/ddr5/64gb); [memoryindex](https://memoryindex.io/dram-prices)
- Another tracker reports the 64 GB RDIMM contract price went from **$450 in Q4 2025 [2025] to more than $900 in Q1 2026**, and was expected to exceed $1,000 in Q2 — [tech-insider DRAM crisis](https://tech-insider.org/dram-ram-price-crisis-2026/); [capitalandcompute](https://capitalandcompute.net/memory-prices/)
- TrendForce's 4Q26 forecast reportedly has conventional DRAM contract prices **+10–15% QoQ**. This comes from a secondary citation; I did not verify it on trendforce.com — [ITLDC late-2026 update](https://itldc.com/en/blog/server-ram-ssd-market-update-2026)
- Newegg 128 GB (2x64 GB) ECC RDIMM kits are listed at **$2,729–6,419** — [Newegg](https://www.newegg.com/p/pl?d=128+gb%2C+ddr5%2C+rdimm%2C+ecc)
- Supermicro's B300 SYS-822GS-NB3RT configuration ships with **3 TB DDR5**. B200 G1 configurations ship with **2–2.3 TB**. BIZON B300 supports up to 3 TB (EPYC, 24 slots) or 4 TB (Xeon, 32 slots). Dell XE9785 has 24 DDR5-6400 slots — [GPU Smith](https://gpusmith.com/articles/en/nvidia-hgx-b300-price-specs); [BIZON](https://bizon-tech.com/bizon-x9000-g5.html)
- **Enterprise NVMe**: DatacenterDisk Q1 2026 puts typical U.2 at **$80–150/TB**, with a 15.36 TB Solidigm D5-P5316 at about **$1,800 ($117.19/TB)**. Another 2026 guide gives 15.36 TB enterprise NVMe at **$1,800–8,500+** per drive, and an August 2026 analysis gives new U.2 at **$300–1,172/TB**. Which figure belongs to which of the PCSP/Aloinfo guide pages comes from a search summary and was not verified page by page — [DatacenterDisk SSD/HDD report](https://datacenterdisk.com/reports/ssd-hdd-price-divergence-2026); [PCSP enterprise SSD 2026](https://pcserverandparts.com/news/enterprise-ssd-prices-2026-server-storage-buying-guide/); [Aloinfo SSD guide](https://www.aloinfousa.com/pages/enterprise-ssd-price-guide-2026)
- An Alibaba-hosted guide reports lead times for high-density RDIMMs extended to **6–8 weeks**. This is an unverified marketplace page — [Alibaba server memory guide](https://electronics.alibaba.com/product/server-memory-price)
- The DGX B300 EU configuration includes **30 TB NVMe**; the ASUS B300 sample configuration has 3.84 TB + 61.44 TB SSD — [GPU Smith](https://gpusmith.com/articles/en/nvidia-hgx-b300-price-specs); [Microless](https://global.microless.com/product/xa-nb3i-e12-8-gpu-server-2x-intel-xeon-6760p-64-cores-2-048tb-ddr5-ram-3-84tb-ssd-61-44tb-ssd-nvidia-hgx-b300-288gb-baseboard-with-8-cx8-infiniband-10x-3200w-psu/)

### Inferences
- **Cost of DDR5 per TB (16x 64 GB):**
  - **About $14.0k** at the Q1-2026 contract price
  - **About $25.4k** at the Q4-2026 Citi forecast
  - **About $31.5–33.0k** at September 2026 spot/street
  - In rupees: about ₹13–31 lakh per TB (calc).
  - Moving a server from 2 TB to 4 TB of RAM for KV-cache offload therefore adds roughly **$50–66k per server** at current street prices. That is about 10% of a B300 server, so the cost-benefit of CPU-RAM KV offload versus NVMe-tier offload (e.g. LMCache/NVMe) should be modelled explicitly.
- **NVMe for weights.** 4x 15.36 TB (about 61 TB) per server is about $7–12k at $117–200/TB. That holds weights for many 0.8–1.6 TB checkpoints plus an NVMe KV-cache tier. Shared storage (e.g. a parallel file system) is a separate decision.
- Because 2026 server quotes bundle 2–3 TB of DDR5, part of the 2025→2026 server price increase is memory. Requesting quotes with minimal RAM (e.g. 1–1.5 TB) and populating later is a possible lever, though DRAM prices were still rising in Q4 2026.

### Gaps
- No verified TrendForce server-RDIMM contract price for Q4 2026.
- No 2026 dated price for 30.72 TB or 61.44 TB enterprise NVMe drives, and no 96/128 GB RDIMM server-module contract prices.
- No INR distributor price for DDR5 RDIMM or enterprise NVMe in India.

---

## 6. Racks, power distribution and cooling (racks, 3-phase PDUs, RDHx, in-row, CDUs)

### Takeaway
Racks and PDUs are minor costs: about **$1.6–3.6k per 42U/48U enclosure** and **$1.6–4.3k per 3-phase 32A/63A PDU**, with 2–4 PDUs needed per high-density rack. Cooling is the large facility item:
- CDU hardware: **$150–400/kW** (installed $230–630/kW), or about **$12–35k per 100–500 kW CDU**
- Rear-door heat exchanger systems: **$1,800–3,200/kW**, including distribution
- Direct-to-chip systems: **$3,500–5,000/kW** at 16-rack scale

Indian per-rack estimates are **₹10–20 lakh for cooling** and **₹8–15 lakh for power/UPS**.

### Cited Findings
- **Racks**:
  - APC NetShelter SX Gen 2: **42U about $3,041**; **48U (800 mm wide) about $3,643**
  - APC NetShelter SV 42U: $1,601–2,000
  - Enclosed 42U budget racks: Tripp Lite about $1,650, StarTech about $1,906
  - Open-frame 42U: $201–426
  - Sources: [IP Security Depot APC](https://www.ipsecuritydepot.com/apc-schneider-electric/?page=7); [DatacenterDisk 42U racks](https://datacenterdisk.com/rack/42u)
- **3-phase PDUs**:
  - APC NetShelter Rack PDU Advanced, 32A-class 3-phase switched/metered: **about $4,299**
  - APC 63A-class (400 V, 42 outlets): **$3,142 (metered) to $4,110 (switched/metered)**
  - Eaton 3-phase managed 24A/32A (42/48 outlets): **$2,237–2,349**
  - Panduit 32A 48U: **$1,643**; Panduit 60A IP44: **$2,392**
  - All are undated reseller prices.
  - Sources: [Hummingbird Networks racks](https://www.hummingbirdnetworks.com/racks-infrastructure/?page=15); [Hummingbird APC](https://www.hummingbirdnetworks.com/apc-racks-accessories/?page=2); [IP Security Depot Panduit](https://www.ipsecuritydepot.com/brands/panduit/?page=348)
- **CDUs**:
  - Hardware: **$150–400 per kW**; installed with piping and commissioning: **$230–630 per kW** — [DatacenterScope liquid cooling cost](https://datacenterscope.com/cooling/liquid-cooling-cost/)
  - **$75–150k per 500 kW** — [Introl liquid vs air](https://introl.com/blog/liquid-vs-air-cooling-ai-data-centers)
  - **$12–35k per CDU for 100–500 kW IT load** (vendor-adjacent) — [Alibaba liquid cooling guide](https://electronics.alibaba.com/product/liquid-cooling-system-price)
  - These ranges come from vendor-adjacent pages and don't fully reconcile.
- GB300 NVL72 in-rack **250 kW CDU: about +$32K** on the rack PO (Aug 2026) — [Data Gravity](https://www.datagravity.dev/p/how-much-does-an-nvidia-nvl72-cost)
- **RDHx and DLC, system level**: advanced RDHx air cooling **$1,800–3,200 per kW** including distribution infrastructure; direct-to-chip **$3,500–5,000 per kW** at 16-rack scale; DLC premium of **$2,500–4,500 per kW** over air — [Adam Silva Consulting cooling economics 2026](https://www.adamsilvaconsulting.com/insights/data-center-cooling-economics-2026); [Energy Solutions](https://energy-solutions.co/articles/sub/data-center-cooling-liquid-immersion-vs-air)
- Liquid-cooling retrofit is about **$2M/MW**, versus more than **$11M/MW** for new greenfield liquid-cooled capacity (STL Partners) — [DatacenterScope retrofit](https://datacenterscope.com/ai-infrastructure/data-center-retrofit-cost/)
- India per rack (indicative, July 2026): **cooling ₹10–20 lakh, power/UPS ₹8–15 lakh, cluster networking ₹5–15 lakh** — [Proactive Data Systems](https://proactive.co.in/blog-details/what-a-gpu-server-really-costs)
- Gigabyte GB300 in-rack CDU is 200 kW (1+1 pumps/PSUs) and its in-row CDU is 1,350 kW; facility water must meet ASHRAE guidance — [Gigabyte GB300 NVL72](https://www.gigabyte.com/Enterprise/GIGAPOD-Pod-Scale/AI-DLC-POD_NVIDIA-GB300-NVL72)
- MI355X 1,400 W systems (Supermicro AS-4126GS-NMR-LCC) **require facility water and a CDU** — [Pantheon](https://pantheon.run/hardware/amd-instinct-mi355x-supermicro)

### Inferences
- **2–4 air-cooled HGX nodes (about 14 kW each, 28–56 kW total)**:
  - Racks: 2x 48U at about $3.6k each
  - PDUs: 4–8x 3-phase 32A/63A at about $3–4.3k each
  - Hardware subtotal: **about $20–40k** (≈₹19–38 lakh calc)
  - Cooling: if the room cannot reject about 30 kW per rack, RDHx at $1,800–3,200/kW gives **about $50–180k** for 28–56 kW (≈₹0.5–1.7 crore).
- **Liquid-cooled options (MI355X 4U DLC, B300 DLC, NVL72)**: add a CDU at about $12–35k (or $150–400/kW) plus facility-water plumbing. Installed DLC at $3.5–5k/kW gives about $100–280k for 28–56 kW.
- 3-phase 32A at 400 V gives about 22 kW per PDU and 63A about 43 kW (P ≈ √3 x 400 V x I; my arithmetic, before derating). So each 14 kW server needs its own 32A 3-phase feed, with A+B redundancy.

### Gaps
- No sourced price for **in-row coolers** (e.g. Vertiv Liebert CRV / APC InRow) or standalone RDHx units.
- No 2026 Vertiv list prices.
- No Indian INR quotes for racks, PDUs or CDUs from Indian suppliers.

---

## 7. Support: 3-year / 5-year OEM warranty, AMC in years 4–5, spare parts

### Takeaway
OEM GPU servers ship with **3-year warranties** as standard (e.g. GB300 NVL72: 3 years plus extensions). There is no public pricing for Dell ProSupport, HPE or Lenovo on XE9680/XE9780/XD685-class AI servers. Industry TCO models budget vendor support at **8–12% of hardware value per year** (some use 5%) and spares at about **4% of capex per year**.

### Cited Findings
- GB300 NVL72 comes with a **3-year warranty plus extensions** — [Data Gravity](https://www.datagravity.dev/p/how-much-does-an-nvidia-nvl72-cost)
- Vendor support agreements "typically run **8–12% of hardware value annually**". The same TCO model's cost table uses **5% per year** for maintenance, which is internally inconsistent — [Introl 5-year GPU TCO](https://introl.com/blog/gpu-infrastructure-tco-model-5-year-enterprise-ai-deployment)
- Spares modelled at a flat **4% of system capex per year**. Operators report higher failure rates for datacenter GPUs due to thermal stress and HBM — [CloudRift true cost of GPU ownership](https://www.cloudrift.ai/blog/the-true-cost-of-gpu-ownership)
- Dell 3-year to 5-year ProSupport Plus upgrades on *general-purpose* PowerEdge servers:
  - R640: about €3,341 incl. VAT
  - R440: NZ$1,934
  - R650xs: NZ$5,700
  - These are not GPU-server prices and only illustrate the order of magnitude for mainstream servers.
  - ProSupport Plus covers 24x7 priority access, accidental damage, drive retention, NBD onsite after remote diagnosis, and proactive monitoring.
  - Sources: [e-nitiative R640](https://responsive5.e-nitiative.eu/product/details/dell/servers/per6403935v/3314X097?flang=en); [Comsys NZ](https://www.comsys.co.nz/product/dell-3y-prospt-to-5y-prospt-pl-4731733)
- Third-party maintenance (TPM) for GPU servers exists, e.g. Park Place Technologies, but no pricing is public — [Park Place GPU support](https://www.parkplacetechnologies.com/third-party-maintenance/gpu-support/)
- Broker and refurbished channels may carry only **30-day warranties**, e.g. the Cloud Ninjas XE9680 H200 at $240k — [Cloud Ninjas](https://cloudninjas.com/products/dell-poweredge-xe9680-gpu-h200-server)
- Naddod prices the QM9700 with 5-year service at $53,448, versus about $31–38k for the bare switch elsewhere. That gap (about $15–22k, or 40–70%) is the implied premium for 5-year network support — [Naddod QM9700](https://www.naddod.com/products/nvidia-networking/102408)

### Inferences
- **Budgeting rule (inference from the above):**
  - Years 1–3: covered by the OEM warranty, typically included. Upgrading to 4-hour mission-critical response usually costs extra.
  - Years 4–5 AMC: **8–12% of the original hardware cost per year**.
  - For a $550k B300 server, that is about **$44–66k per year** (≈₹42–63 lakh/yr calc).
- **Spare-parts strategy:**
  - Keep on-site cold spares for parts with high failure rates and long lead times: PSUs, fans, NVMe drives, DIMMs, OSFP optics and one spare NIC.
  - GPU baseboards and HGX trays are OEM-RMA items. With only 2–4 nodes, one failed GPU tray can take out 25–50% of capacity, so negotiate a 4-hour or NBD onsite SLA with an in-India parts depot.
  - Spares at about 4% of capex per year (CloudRift) is a reasonable allowance.

### Gaps
- No public Dell/HPE/Lenovo/Supermicro price for 3-year or 5-year support on 8-GPU AI servers; this requires OEM quotes.
- No Indian AMC benchmark (e.g. % of hardware value charged by Netweb, Dell India or HPE India).

---

## 8. Market dynamics: lead times and allocation, resale value, price trend

### Takeaway
Lead times for owned hardware in late 2026 vary by channel:
- US/EU stock-or-build resellers: **about 4–14 weeks for standard B200/B300 SKUs** (custom builds over 20 weeks)
- MI355X: **4–8 to 12 weeks**
- Indian enterprise buyers: **3–9 months** quoted

Prices **rose in 2026**. The main driver is DRAM/HBM: server DRAM roughly doubled in Q1 2026 and kept rising. Morgan Stanley is cited for a 30–50% rise in GPU-server prices versus early 2025, and B300 server estimates moved from $250–400k (March) to $550–750k (September). H200s resell at about 70–90% of MSRP on asking prices but lower on executed sales. H100s resell at about 40–85% depending on age.

### Cited Findings
- **Lead times**:
  - BIZON HGX B300: **9–10 weeks** (ships Dec 18–28 2026) — [BIZON](https://bizon-tech.com/bizon-x9000-g5.html)
  - Dell XE9785 via Uvation: **about 4 weeks**, as a floor — [GPU Smith](https://gpusmith.com/articles/en/nvidia-hgx-b300-price-specs)
  - Vipera HGX B200: **8–14 weeks for "golden SKUs"**, with custom BOMs over 20 weeks; other pages show 8–20 weeks, custom over 26 weeks; "supply remains strained" — [Viperatech](https://viperatech.com/product/supermicro-10u-b200-gold-series-gpu-server-sys-a21ge-nbrt-g1)
  - Supermicro MI355X 4U: **4–8 weeks** — [Pantheon](https://pantheon.run/hardware/amd-instinct-mi355x-supermicro)
  - Lead-time tracker (July 2026): MI355X/MI325X systems at **about 4–12 weeks**. It notes no OEM publishes a lead time, and that the "allocation layer" decides whether an OEM can accept a build slot — [AI Data Center Guide lead times](https://aidatacenterguide.com/lead-times)
- **India**: enterprise lead times of **3–9 months**; B300 allocation goes primarily to hyperscalers and major clouds, and buyers often pay premiums through partners (vendor blog, Aug 2026) — [Cyfuture](https://cyfuture.ai/blog/nvidia-b300-gpu-price-in-india). One anecdote: an Indian startup was offered a 6–8 week lead time plus deposit for long-term B300 rental — [ZenoCloud](https://zenocloud.io/blog/b200-availability-price-india/)
- B200 is "allocated and waitlisted", with most production absorbed by hyperscalers and mainstream availability expected from 2027 — [Mercatus](https://www.mercatus-ai.com/blog/b200-server-price)
- AMD holds an estimated **about 11% of TSMC CoWoS capacity in 2026, versus about 60% for NVIDIA**, so MI355X supply is constrained by supply, not just price/performance (analysis) — [ValueAdd VC](https://valueaddvc.com/blog/ai-chip-supply-ranked-2026-nvidia-amd-broadcom-tsmc-and-whos-actually-unconstrained)
- **Price trend**:
  - Server DRAM contract: **+93–98% QoQ (Q1 2026), +53–63% (Q2), +13–18% forecast (Q3)** — [ServnetUK](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026)
  - Morgan Stanley is cited for a **30–50% rise in GPU-server prices versus early-2025 levels**, with H1 2026 as the "acute phase" — [Hostkey](https://hostkey.com/blog/152-server-price-increases-in-2026-forecasts-causes-and-recommendations/)
  - Reports relayed from Tom's Hardware say NVIDIA Grace Blackwell / Vera Rubin system prices will rise **more than 15% (up to about 17%) for shipments from early 2027** on memory costs — [Shattered.io](https://shattered.io/nvidia-ai-server-price-hike-memory-shortage-2026/)
  - RTX PRO 6000 Server Edition eBay average **+30.8% in three months** to October 2026 — [GPU Poet](https://gpupoet.com/gpu/learn/price/october-2026/nvidia-rtx-pro-6000-blackwell-server)
  - HGX B300 complete-system estimates went from $250–400k (March 2026 guide) to $550–750k (September 2026) — [GPU Smith](https://gpusmith.com/articles/en/nvidia-hgx-b300-price-specs); [haink.org](https://haink.org/knowledge/technology/ai-infrastructure-cost-guide)
  - DRAM shortage relief is not expected before H1 2027 or later (secondary sources) — [Hostkey](https://hostkey.com/blog/152-server-price-increases-in-2026-forecasts-causes-and-recommendations/)
- **Resale and used value**:
  - H100: used about **60–70% of new** ($15–28k used vs $25–40k new) — [Compute Exchange H100 2026](https://compute.exchange/blogs/h100-gpu-price-2026)
  - H100 residuals (Mercatus): **75–85% at 18–30 months**, **40–75% at 36 months**, **25–35% at 60+ months** of a $30k reference — [Mercatus H100 resale](https://www.mercatus-ai.com/blog/h100-resale-value)
  - Other H100 used ranges: $12–18k and $12–22k — [Spheron depreciation](https://www.spheron.network/blog/gpu-depreciation-in-2026-how-fast-h100s-and-h200s-lose-value/); [ServerBuyBack](https://serverbuyback.com/guides/used-h100-vs-a100-vs-h200-resale-value-2026/)
  - H200: **$30–35k per unit in Q3 2026 vs MSRP near $38k (about 80–90%)** — [Compute Exchange used H200](https://compute.exchange/hardware-market/used-gpus/used-h200)
  - H200 asking vs executed: a UK study notes **posted-ask median $38,248 vs executed median $27,155** (trailing 90 days), so executed is about 71% of ask — [ServnetUK residual value study](https://www.servnetuk.com/research/gpu-residual-value-study-2026)

### Inferences
- **Year-on-year trend.** Late-2026 complete-server prices are roughly **20–50% above late-2025 prices** for the same GPU class. Most of the increase comes from DRAM (2–3 TB per server) and HBM, with GPUs themselves also firm. This combines the Morgan Stanley figure, the B300 estimate shift and the DRAM data; it is not a single sourced YoY number.
- **Residual value for the business case.** Plan at about **50–65% residual after 2–3 years** and **25–35% after 5 years** for Hopper/Blackwell-class GPUs. Executed prices run about 70% of asking prices, so use executed prices.
- **For a Pune buyer.** Plan a 3–6 month procurement window: about 4–14 weeks of OEM build/allocation, plus import, customs and installation. Secure slot and delivery dates in writing, since quoted dates "are forecasts, not commitments".

### Gaps
- No India-specific, OEM-confirmed lead time for B200, B300 or MI355X in 2026.
- No resale data yet for B200/B300, which are too new.
- No primary Tom's Hardware, DigiTimes or SemiAnalysis article was fetched for the 2026 server price-hike claims; they are relayed by secondary sites.

---

## 9. Indian channel: distributors, OEMs/assemblers and landed INR

### Takeaway
I found **no published per-unit INR quote** from Ingram Micro India, Redington, Rashi or iValue for 2026 GPU servers. The usable INR anchors are:
- About **₹2.5–4 crore+** for an 8x H100/H200 server (Proactive, July 2026)
- About **₹5.3–5.5 crore landed** for a DGX B300 (Cyfuture, August 2026, at a stale ₹84/USD)
- Order-level figures: Netweb's **₹1,734 crore (ex-GST) order for HGX B200 8-GPU nodes** under IndiaAI, and Rashi's **₹1,510 crore Yotta project for about 512 NVIDIA GPU servers** (about ₹2.95 crore per server, my calculation; GPU generation and year unconfirmed)

Import duty treatment is contested: **0% BCD under the WTO ITA for HS 8471** versus "7.5–10%". IGST is 18% on top, plus 3–5% freight and insurance.

### Cited Findings
- **Netweb Technologies (Tyrone)**:
  - Purchase order of about **₹1,734 crore ex-GST** for servers on NVIDIA Blackwell; "each node will feature NVIDIA's latest-generation **8x GPU HGX-B200**"; completion by H1 FY27 (i.e. by about September 2026) — [Business Today](https://www.businesstoday.in/amp/markets/stocks/story/netweb-tech-share-jumps-10-on-rs-1734-crore-ai-order-win-stock-up-60-in-6-months-492269-2025-09-03); [Entrepreneur India](https://india.entrepreneur.com/news-and-trends/netweb-technologies-secures-inr-1734-cr-order-to/496720)
  - A separate **~₹450 crore** order for Tyrone AI GPU systems — [Reuters via TradingView](https://vn.tradingview.com/news/reuters.com,2025:newsml_L6N3V909A:0-india-s-netweb-technologies-hits-record-high-on-bagging-4-5-billion-rupee-order)
  - Netweb launched the "Make in India" **Tyrone Camarero GB200** system (February 2026), with some units already supplied to Indian AI organisations — [ANI](https://aninews.in/news/business/netweb-launches-make-in-india-ai-supercomputing-systems-powered-by-nvidia-sovereign-ai-development20260218122018/); [Business Standard](https://www.business-standard.com/markets/capital-market-news/netweb-scales-make-in-india-computing-with-launch-of-its-tyrone-ai-products-powered-by-nvidia-126021800199_1.html)
  - Strategic order book at FY26 end: **INR 16,252 mn** — [Netweb 4QFY26 research update](https://www.netwebindia.com/investors/research-report/Netweb_4QFY26_Update.pdf)
- **Rashi Peripherals**: **₹1,510 crore** AI data centre project with Yotta (Hiranandani) for **about 512 NVIDIA GPU servers**, with ASUS as partner. FY26 revenue about ₹15,827 crore; Q1 FY27 revenue ₹51,019 mn (+61.9% YoY) — [Entrepreneur India](https://india.entrepreneur.com/news-and-trends/rashi-peripherals-posts-inr-11000-crore-revenue-eyes/481769); [CRN Asia](https://www.crnasia.com/india/news/2026/rashi-peripherals-q1-earnings-expanding-into-higher-value-technology-segments-to-enhance-growth-quality-says-ceo)
- **Ingram Micro India**: distribution agreement with NVIDIA for India and SAARC, giving channel partners access to NVIDIA cloud/datacenter GPUs (article undated) — [CRN India](https://www.crn.in/?p=44935)
- **Redington and iValue**: no results on NVIDIA AI-server distribution or pricing (searched).
- **INR price anchors**:
  - 8-GPU H100/H200 server: **₹2.5–4 crore and up**; single H100 ₹25–30 lakh (Proactive, a Dell Platinum partner; updated 2026-07-16) — [Proactive](https://proactive.co.in/blog-details/what-a-gpu-server-really-costs)
  - Cyfuture (2026-08-07): DGX B300 $400–500k = ₹3.36–4.2 crore at ₹84/USD; **landed about ₹5.3–5.5 crore** before infrastructure; HGX B300 baseboard ₹2.52–2.94 crore — [Cyfuture](https://cyfuture.ai/blog/nvidia-b300-gpu-price-in-india)
  - CloudPe/Neysa: single H200 landed ₹40–50 lakh; 8-GPU server landed "approaching ₹1 crore". This is inconsistent with all USD evidence (about $300k+ is ₹2.85 crore+); treat as unreliable — [CloudPe H200](https://www.cloudpe.com/blog/h200-gpu-pricing/); [Neysa](https://neysa.ai/blog/h200-price-in-india/)
  - An IndiaMART listing shows Lenovo SR780a V3 "at ₹3,00,000". That is clearly not an 8-GPU configuration; ignore — [IndiaMART](https://www.indiamart.com/proddetail/lenovo-thinksystem-sr780a-v3-2854144617573.html)
- **Import duty and taxes**:
  - HS 8471 servers: **0% basic customs duty** under the WTO ITA; **18% IGST** on CIF plus duty. One source flags a 2023 move of some 8471 items to "restricted" import, requiring DGFT import authorisation, and BIS certification requirements — [Carraglobe AI server import duties 2026](https://carraglobe.com/?p=7415); [Carraglobe HS 8471](https://carraglobe.com/?p=7430)
  - Contradicted by Cyfuture: **BCD 7.5–10%**, IGST 18%, freight and insurance 3–5%, total uplift "25–30%" in one place and "28–30%" in another; it also flags a 5% INR depreciation risk between PO and delivery — [Cyfuture](https://cyfuture.ai/blog/nvidia-b300-gpu-price-in-india)
- **IndiaAI subsidised compute** benchmark: about **₹67–92/GPU-hour**, within a ₹10,300 crore programme — [Spheron GPU cloud India](https://www.spheron.network/blog/gpu-cloud-india-2026/); [ecorpit](https://ecorpit.com/india-gpu-cloud-rental-pricing-h100-b200-2026/)

### Inferences
- **Landed INR formula for a Pune company (inference):**
  - Landed ≈ USD x FX x (1 + freight/insurance 3–5%) x (1 + BCD 0–10% incl. SWS) x (1 + IGST 18%)
  - IGST is normally claimable as input tax credit by a GST-registered business. If so, the **effective** landed uplift is about **3–15%** over ex-works, against a cash-flow uplift of about **22–36%**. Confirm BCD and the DGFT/BIS position with a customs broker before quoting.
- **Example: Supermicro SYS-822GS-NB3RT B300 at $545k:**
  - At ₹95/USD: ≈ ₹5.18 crore ex-works
  - Landed with 4% freight and 0% BCD: ≈ ₹5.39 crore before GST; ≈ ₹6.36 crore with 18% IGST (cash outlay)
  - With 7.5% BCD: ≈ ₹5.79 crore before IGST
- **Example: HGX B200 at $390k:** ≈ ₹3.70 crore ex-works and ≈ ₹3.85–4.15 crore landed pre-GST.
- **Example: HGX H200 at $325k:** ≈ ₹3.09 crore ex-works. This fits within Proactive's ₹2.5–4 crore band.
- **Channel route.** Dell, HPE and Lenovo sell through Indian partners such as Proactive, a Dell Platinum partner. Supermicro and ASUS go through Rashi, Ingram and others. Netweb's Tyrone line is an Indian-assembled HGX B200/GB200 option, which may simplify import, support and "Make in India" procurement preferences. Ask Netweb, Dell India, HPE India and Supermicro India for INR-landed quotes with 3- and 5-year onsite support.

### Gaps
- No published INR price lists from Ingram Micro India, Redington, Rashi Peripherals, iValue or Netweb for B200, B300, MI355X or RTX PRO 6000 servers.
- The Netweb ₹1,734 crore order's node count is not disclosed, so a per-node INR price can't be derived. The Rashi/Yotta per-server figure (about ₹2.95 crore) is from an older order (likely 2024, H100-era) whose GPU generation was not confirmed.
- The BCD rate for GPU servers (HS 8471 at 0% versus 7.5–10%) and whether DGFT import authorisation applies remain unconfirmed against CBIC notifications.

---

## 10. Consolidated price table

### Takeaway
All figures are USD ex-tax and ex-shipping unless stated. "Typical" means the most representative 2026 OEM-store or channel figure. INR is "(found)" when an Indian source quoted it, otherwise "(calc)" at ₹95/USD, ex-GST, not landed. Rows with no source date are marked "undated"; rows with older data are marked [2025].

### Cited Findings

| item | spec summary | price_low_usd | price_typ_usd | price_high_usd | INR if found | power_kW | cooling | source | date |
|---|---|---|---|---|---|---|---|---|---|
| HGX H200 8-GPU server | 8x141 GB HBM3e (1.13 TB), 4.8 TB/s/GPU, FP8 ~1.98 PF dense/GPU, 700 W/GPU; 8U (SMC SYS-821GE-TNHR) | 300,000 (Lenovo SR780a V3 311,580) | 323,685 (SMC store) – 370,000 | 420,000 | ₹2.5–4 cr+ (found, 8x H100/H200, Proactive); ≈₹3.07 cr (calc) | ~10 (unverified); GPUs 5.6 | Air (SMC); liquid (Lenovo Neptune) | [SMC eStore](https://store.supermicro.com/us_en/systems/gpu.html?p=2); [Lenovo](https://www.lenovo.com/us/en/p/servers-storage/servers/racks/lenovo-thinksystem-sr780a-v3/7dj51000na); [Mercatus](https://www.mercatus-ai.com/blog/h200-server-price); [Proactive](https://proactive.co.in/blog-details/what-a-gpu-server-really-costs) | 2026-10-19 / 2026-07 |
| HGX B200 8-GPU server | 8x180 GB (1.44 TB), 8 TB/s, FP8 4.5 PF / FP4 9 PF dense per GPU, 1,000 W/GPU; 8–10U; typ. 2x Xeon 6960P, 2–2.3 TB DDR5, 8x CX-7 | 340,000 | 384,000–403,000 (Exxact/SMC) ; ~450,000 analyst | 515,000 (DGX B200) | ≈₹3.65–4.28 cr (calc); Netweb ₹1,734 cr order of B200 nodes (found, count n/d) | 14.3 (DGX B200) | Air (10U); DLC variants exist | [Exxact](https://www.exxactcorp.com/Exxact-TS4-124903244-E124903244); [Newegg SMC](https://www.newegg.com/supermicro-gold-series-sys-a22ga-nbrt-g1-rack/p/N82E16859152392); [Mercatus](https://www.mercatus-ai.com/blog/b200-server-price); [flopper](https://flopper.io/system/nvidia-dgx-b200) | 2026-07 to 2026-10 |
| HGX B300 8-GPU server | 8x270–288 GB (2.1–2.3 TB), 8 TB/s, FP8 4.5 PF / FP4 13.5 PF dense per GPU, 1,100 W (air) to 1,400 W; 8U (SMC/Gigabyte), 9U ASUS; typ. 2x Xeon 6767P, 3 TB DDR5, 8x CX-8 800G | 375,000 (Gigabyte G894) | 496,639 (BIZON) – 545,173 / 570,221 (SMC store) | 699,977 (Thinkmate); outliers 795,000 | ≈₹5.18–5.42 cr (calc); DGX B300 landed ₹5.3–5.5 cr (found, at ₹84) | ~14–14.5 (DGX B300) | Air (SMC, Dell XE9785, BIZON); DLC (XE9785L, HPE XD685 5U) | [SMC eStore](https://store.supermicro.com/us_en/systems/gpu.html); [BIZON](https://bizon-tech.com/bizon-x9000-g5.html); [Thinkmate](https://www.thinkmate.com/systems/supermicro/superserver/amd?b=); [esaitech](https://esaitech.com/products/gigabyte-g894-sd3-aax7-intel-xeon-8u-rackmount-gpu-server); [GPU Smith](https://gpusmith.com/articles/en/nvidia-hgx-b300-price-specs); [Cyfuture](https://cyfuture.ai/blog/nvidia-b300-gpu-price-in-india) | 2026-07 to 2026-10 |
| ASUS XA NB3I-E12 (B300) | 9U, 8x B300, sample 2x Xeon 6760P, 2 TB DDR5, 65 TB SSD, 8x CX-8 | 348,000 | 395,000 (sale) | 480,965 (NTS) | ≈₹3.75 cr (calc) | ~14 (inferred) | Air | [Viperatech](https://viperatech.com/product/asus-xa-nb3i-e12-gpu-server); [NTS](https://www.rackmountnts.com/asus-xa-nb3i-e12) | 2026 (undated) |
| NVIDIA DGX B300 | 8x B300, 2x Xeon 6776P, 2 TB RAM, 30 TB NVMe, 8x400G IB + 4x400G Eth | ~400,000 (US, FT) | €535,000 (EU) | €714,000 (EU) | ₹3.36–4.2 cr ex-works / ₹5.3–5.5 cr landed (found, ₹84) | ~14–14.5 | Air | [GPU Smith](https://gpusmith.com/articles/en/nvidia-hgx-b300-price-specs); [Cyfuture](https://cyfuture.ai/blog/nvidia-b300-gpu-price-in-india) | 2026-07/08 |
| Dell XE9785 / XE9780 | 8x B300 270 GB 1,100 W or 8x MI355X 288 GB 1,400 W; 163.65 kg; 24 DIMM | n/a | quote only | €736k–891k ex-VAT (Servermall, config unclear) | – | ~14 (inferred) | Air (XE9785), DLC (XE9785L) | [Dell](https://www.dell.com/en-us/shop/ipovw/poweredge-xe9785); [Servermall](https://servermall.com/catalog/servers/dell-poweredge-xe9785-16nvme/) | 2026 |
| HPE ProLiant XD685 | 8x B300 (or H200), 5U DLC / 6U air, ≤3 TB RAM | n/a | quote only | n/a | – | ~14 (inferred) | DLC or air | [HPE](https://buy.hpe.com/us/en/compute/rack-servers/proliant-compute-xd600-servers/proliant-compute-xd600-server/hpe-proliant-compute-xd685/p/1014862906) | 2026-10 |
| AMD MI355X 8-GPU server | 8x288 GB (2.3 TB), 8 TB/s, FP8 5.03 PF / FP4 10.07 PF dense per GPU, 1,400 W/GPU; SMC 4U DLC, Gigabyte 8U | ~280,000 (inferred) | €261,443 ex-VAT (smicro.eu, config unverified) | ~400,000 (inferred) | ≈₹2.7–3.8 cr (calc, inferred) | ~14–15 (inferred; GPUs 11.2) | DLC (4U, needs CDU + facility water); air 8U variants | [smicro.eu](https://smicro.eu/supermicro-as-4126gs-nmr-lcc-g1-2); [Pantheon](https://pantheon.run/hardware/amd-instinct-mi355x-supermicro); [Klockwood](https://glennklockwood.com/garden/processors/MI355X) | 2026 |
| AMD MI325X / MI350X 8-GPU server | SMC AS-8126GS-TNMR 8U; MI325X 8x256 GB, 6 TB/s, FP8 2.6 PF dense, no FP4, 1,000 W/GPU | 256,301 (SMC store) | 261,601 (Newegg) | 314,626 (Thinkmate) | ≈₹2.43–2.99 cr (calc) | ~11–12 (inferred; GPUs 8.0) | Air | [SMC eStore](https://store.supermicro.com/us_en/systems/gpu.html); [Thinkmate](https://www.thinkmate.com/systems/supermicro/superserver/amd?b=); [SemiAnalysis](https://inferencex.semianalysis.com/chips/mi325x) | 2026-10-19 |
| AMD MI300X 8-GPU server (ref.) | SMC AS-8125GS-TNMR2 8U, 8x192 GB | 284,971 | – | 360,808 | ≈₹2.71–3.43 cr (calc) | n/s | Air | [SMC eStore p2](https://store.supermicro.com/us_en/systems/gpu.html?p=2); [Thinkmate](https://www.thinkmate.com/systems/supermicro/superserver/amd?b=) | 2026-10-19 |
| GB200 NVL72 rack | 72x B200 + 36 Grace, NVLink-72, liquid-cooled | 2,800,000 | 3,000,000–3,100,000 | 3,900,000 (all-in, SemiAnalysis [2025]) | ≈₹28.5 cr (calc) | ~120 (unverified) | 100% liquid (DLC + CDU) | [Data Gravity](https://www.datagravity.dev/p/how-much-does-an-nvidia-nvl72-cost); [Wing VC](https://www.wing.vc/content/how-much-does-an-nvidia-nvl72-cost) | 2025-08 / 2026-01 |
| GB300 NVL72 rack | 72x B300 288 GB (~21 TB HBM), 36 Grace; ~1.36 t; EXW | 3,700,000 (Loop) | ~5,000,000 (POs, ex-CDU) | 6,500,000 (Tom's HW) | ≈₹47.5 cr (calc); ₹25.2–33.6 cr (found, stale ₹84 & $3–4M) | 132 nominal / ~155 peak (provision 192) | 100% liquid; 200–250 kW in-rack CDU (+~$32k) | [Data Gravity](https://www.datagravity.dev/p/how-much-does-an-nvidia-nvl72-cost); [HPE](https://www.hpe.com/us/en/collaterals/collateral.a50009244enw.html); [Gigabyte](https://www.gigabyte.com/Enterprise/GIGAPOD-Pod-Scale/AI-DLC-POD_NVIDIA-GB300-NVL72) | 2026-08 |
| RTX PRO 6000 Blackwell Server Ed. (card) | 96 GB GDDR7 ECC, PCIe 5 x16, passive, 600 W | 15,500 | 16,115–20,224 | 23,332 (eBay avg); 35,900 outlier | ≈₹15.3–19.2 lakh (calc) | 0.6 | Passive (server airflow) | [CDW](https://www.cdw.com/product/nvidia-rtx-pro-6000-blackwell-server-edition-graphics-card-rtx-pro-60/8426124); [Hyperscalers](https://www.hyperscalers.com/NVIDIA-RTX-PRO-6000-Blackwell-Server-Edition); [GPU Poet](https://gpupoet.com/gpu/learn/price/october-2026/nvidia-rtx-pro-6000-blackwell-server) | 2026-10 |
| 2x RTX PRO 6000 server | SMC SYS-212GB-FNR-01-G2, 2U | 66,680 | 66,680 | 104,670 (5U AS-5126GS-TNRT-01-G2) | ≈₹63 lakh–₹99 lakh (calc) | ~2–2.5 (inferred) | Air | [SMC eStore](https://store.supermicro.com/us_en/systems/gpu.html) | 2026-10-19 |
| 4x RTX PRO 6000 server | SMC SYS-422GA-NRT-01-G2, 4U | – | 127,673 | – | ≈₹1.21 cr (calc); 2–4 GPU server ₹25 lakh–1 cr (found) | ~3.5–4 (inferred) | Air | [SMC eStore](https://store.supermicro.com/us_en/systems/gpu.html); [Proactive](https://proactive.co.in/blog-details/what-a-gpu-server-really-costs) | 2026-10-19 |
| 8x RTX PRO 6000 server | ASUS ESC8000A-E13X / Gigabyte etc. | €168,524 ex-VAT | €171,631 ex-VAT; £147,780 | €241,000 ex-VAT; £186,780 | – | ~6–7 (inferred) | Air | [ServerMall](https://servermall.com/sets/servers-with-rtx-pro-6000/); [ctoservers](https://www.ctoservers.com/rtx-pro-6000-blackwell-222-c.asp) | 2026 |
| NVIDIA L40S (card) | 48 GB GDDR6, PCIe | 7,500 | 9,000 | 10,000 | ≈₹7.1–9.5 lakh (calc); 1-GPU server ₹5–25 lakh (found) | ~0.35 (unverified) | Passive | [gpucost.org](https://gpucost.org/gpu/l40s); [Spheron](https://www.spheron.network/blog/nvidia-l40s-for-ai-inference/) | 2026 |
| 8x L40S server | dual 96-core EPYC 9004 | – | £79,850 | – | – | ~3.5–4.5 (inferred) | Air | [ctoservers](https://www.ctoservers.com/rtx-pro-6000-blackwell-222-c.asp) | undated |
| NVIDIA L4 (card) | 24 GB GDDR6, 300 GB/s, 72 W, low-profile | 2,500 | 2,800 | – | ≈₹2.4–2.7 lakh (calc) | 0.072 | Passive | [gpucost.org](https://gpucost.org/gpu-prices) | 2026 |
| H100 NVL (card) | 94 GB HBM3, PCIe | 29,000 | – | 35,000 | ≈₹27.6–33.3 lakh (calc); H100 ₹25–30 lakh (found) | ~0.4 (unverified) | Passive | [IntuitionLabs](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide); [gpucost.org](https://gpucost.org/gpu-prices); [Proactive](https://proactive.co.in/blog-details/what-a-gpu-server-really-costs) | 2026 |
| H200 NVL (card) / 5x H200 NVL server | 141 GB, 4.8 TB/s, 600 W; SMC AS-5126GS-TNRT 5U | 32,366 (card) | 250,961 (5-GPU server) | 47,500 (card, eBay) | ≈₹30.7 lakh card / ₹2.38 cr server (calc) | 0.6/card | Air | [Mercatus](https://www.mercatus-ai.com/blog/h200-price); [SMC eStore](https://store.supermicro.com/us_en/systems/gpu.html) | 2026 |
| Quantum-2 QM9700 IB switch | 64x NDR 400G (32 OSFP), 1U, managed | 30,923 | 38,000 | 53,448 (w/ 5-yr svc) | ≈₹29–51 lakh (calc) | n/s | Air | [Getitnew](https://getitnew.com/mqm9700-ns2r-nvidia-qm9700-quantum-2-based-ndr-infiniband-switch-64-port-ndr-c2p-airflow-managed-new/); [FS.com](https://www.fs.com/products/194710.html); [Naddod](https://www.naddod.com/products/nvidia-networking/102408) | 2026 (reseller) |
| Quantum-X800 Q3400-RA IB switch | 144x XDR 800G (72 OSFP) | €60,000 | – | 129,999 | ≈₹1.23 cr (calc, high) | n/s | Air/liquid variants | [Naddod](https://www.naddod.com/products/nvidia-networking/102612); [server-parts.eu](https://www.server-parts.eu/post/nvidia-qm9700-qm9790-quantum-x800-infiniband-switches) | 2026 (reseller) |
| Spectrum-4 SN5600 (RoCE/Spectrum-X) | 64x 800GbE OSFP, 2U | 55,250 | 65,000–76,500 | 89,445 | ≈₹52–85 lakh (calc) | n/s | Air | [Naddod](https://www.naddod.com/products/nvidia-networking/102424); [GPU Smith](https://gpusmith.com/hardware/networking/nvidia-spectrum-x-sn5600); [LTT](https://www.lttpartners.com/products/nvidia-spectrum-sn5600-ethernet-switch) | 2026 (reseller) |
| ConnectX-7 NIC | 400G NDR/400GbE, OSFP/QSFP112 | 1,599 | 1,750 | 3,700 | ≈₹1.5–3.5 lakh (calc) | ~0.025 (n/s) | Passive | [Gatewell](https://gatewellusa.com/ai-compute/interconnect); [GPU Smith](https://gpusmith.com/hardware/networking/nvidia-connectx-7) | 2026 |
| ConnectX-8 SuperNIC | 800G XDR / 2x400GbE | 1,779 | 2,300 | 2,800 | ≈₹1.7–2.7 lakh (calc) | n/s | Passive | [Naddod](https://www.naddod.com/collections/nvidia-networking/connectx-8); [Gatewell](https://gatewellusa.com/ai-compute/interconnect); [FiberMall](https://www.fibermall.com/blog/connectx-7-vs-connectx-8.htm) | mid/late 2026 |
| BlueField-3 B3220 DPU | 2x 200G QSFP112 | 2,500 (used) | 4,490 | 5,959 (crypto) | ≈₹4.3–5.7 lakh (calc) | n/s | Passive | [FiberMall](https://www.fibermall.com/sale-462652-nvidia-b3220.htm); [Naddod](https://www.naddod.com/collections/nvidia-networking/nvidia-bluefield-3-dpus-and-supernics) | 2026 |
| 800G OSFP twin-port SR8 optic | MMA4Z00-NS 2x400G SR4, 850 nm, 50 m (compatible SR8 = $550) | 362 | 550–1,102 | 2,624 (MSRP, FLT) | ≈₹52k–1.05 lakh (calc, typ) | ~0.017 | – | [NetworkTigers](https://www.networktigers.com/a/s/products/mma4z00-ns-nvidia-osfp); [FiberMall](https://www.fibermall.com/sale-462660-nvidia-sn5600.htm); [Channel Online](https://global.channelonline.com/acme/ccs/Products/overview/M024204504) | 2026 |
| Front-end 100GbE switch (32-port) | NVIDIA SN2700 / Arista 7060CX2-32S | 2,999 (refurb) | 14,631 | 17,912 (new, OOS) | ≈₹2.8–17 lakh (calc) | n/s | Air | [xByte](https://www.xbyte.com/products/cat-22734-ra); [Connection](https://www.connection.com/product/nvidia-sn2700-32-port-40gbe-switch-w-cumulus-linux-p2c-airflow/msn2700-bs2fc/32025747) | undated |
| Front-end 25GbE switch (48x25G+8x100G) | Arista 7050SX3 / 7280SR3, EdgeCore AS7326 | 2,900 (used) | 7,499 (refurb) | 15,899 | ≈₹2.8–15 lakh (calc) | n/s | Air | [xByte](https://www.xbyte.com/products/cat-28483); [eBay](https://www.ebay.com/itm/257086401081) | undated |
| Per-node back-end fabric (inference) | 8x 400/800G rail: switch share + 16 optics + cables (NICs incl. in server) | 25,000 | 35,000 | 55,000 | ≈₹24–52 lakh (calc) | – | – | Inference from rows above | 2026-10 |
| DDR5 RDIMM 64 GB | server RDIMM; per TB = 16 modules | 873 (Q1-26 contract) | 1,586 (Q4-26 fcst) | 2,064 (Sep-26 street) | per TB ≈₹13–31 lakh (calc) | – | – | [ServnetUK](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026); [DatacenterDisk](https://datacenterdisk.com/server-ram/ddr5/64gb) | 2026-05 to 2026-09 |
| DDR5 RDIMM per TB | 1 TB host RAM | 13,968 | 25,376 | 33,024 | ≈₹13.3–31.4 lakh (calc) | – | – | derived from row above | 2026 |
| Enterprise NVMe per TB | U.2/E3.S, e.g. Solidigm D5-P5316 15.36 TB ≈ $1,800 | 80 | 117–150 | 300–1,172 (premium/TLC) | ≈₹7.6k–14k per TB typ (calc) | ~0.025/drive (n/s) | – | [DatacenterDisk](https://datacenterdisk.com/reports/ssd-hdd-price-divergence-2026); [PCSP](https://pcserverandparts.com/news/enterprise-ssd-prices-2026-server-storage-buying-guide/) | 2026-Q1 to Q3 |
| 42U / 48U rack enclosure | APC NetShelter SX Gen2 (48U 800 mm) | 1,650 (budget 42U) | 3,041 (42U) | 3,643 (48U) | ≈₹1.6–3.5 lakh (calc) | – | – | [IP Security Depot](https://www.ipsecuritydepot.com/apc-schneider-electric/?page=7); [DatacenterDisk](https://datacenterdisk.com/rack/42u) | undated |
| 3-phase PDU 32A | Eaton / Panduit / APC switched-metered | 1,643 | 2,300 | 4,299 | ≈₹1.6–4.1 lakh (calc) | ~22 kW cap (calc) | – | [Hummingbird](https://www.hummingbirdnetworks.com/racks-infrastructure/?page=15); [IP Security Depot](https://www.ipsecuritydepot.com/brands/panduit/?page=348) | undated |
| 3-phase PDU 60–63A | Panduit 60A IP44 / APC 63A 400 V 42-outlet | 2,392 | 3,142 | 4,110 | ≈₹2.3–3.9 lakh (calc) | ~43 kW cap (calc) | – | [Hummingbird APC](https://www.hummingbirdnetworks.com/apc-racks-accessories/?page=2); [IP Security Depot](https://www.ipsecuritydepot.com/brands/panduit/?page=348) | undated |
| Liquid-cooling CDU | per kW hardware / per unit 100–500 kW | 150/kW; 12,000/unit | 250/kW; ~32,000 (250 kW in-rack, GB300) | 400/kW (630/kW installed); 35,000/unit | per rack cooling ₹10–20 lakh (found) | – | Liquid | [DatacenterScope](https://datacenterscope.com/cooling/liquid-cooling-cost/); [Data Gravity](https://www.datagravity.dev/p/how-much-does-an-nvidia-nvl72-cost); [Proactive](https://proactive.co.in/blog-details/what-a-gpu-server-really-costs) | 2026 |
| Rear-door heat exchanger (system) | RDHx incl. distribution, per kW | 1,800/kW | 2,500/kW | 3,200/kW | – | – | Air-assist liquid | [Adam Silva](https://www.adamsilvaconsulting.com/insights/data-center-cooling-economics-2026) | 2026 |
| Direct-to-chip liquid (system) | DLC at 16-rack scale, per kW | 3,500/kW | 4,250/kW | 5,000/kW | – | – | DLC | [Adam Silva](https://www.adamsilvaconsulting.com/insights/data-center-cooling-economics-2026) | 2026 |
| OEM support yrs 1–3 | standard 3-yr warranty | included | included | uplift for 4-hr/mission-critical (n/s) | – | – | – | [Data Gravity](https://www.datagravity.dev/p/how-much-does-an-nvidia-nvl72-cost) | 2026 |
| AMC yrs 4–5 | % of hardware value per year | 5% | 8–10% | 12% | e.g. ₹42–63 lakh/yr on a ₹5.2 cr B300 (calc) | – | – | [Introl](https://introl.com/blog/gpu-infrastructure-tco-model-5-year-enterprise-ai-deployment) | 2026 |
| Spares allowance | % of capex per year | – | 4% | – | – | – | – | [CloudRift](https://www.cloudrift.ai/blog/the-true-cost-of-gpu-ownership) | 2026 |
| Used H100 / H200 (resale ref.) | per GPU, used | H100 12,000; H200 27,155 (executed median) | H100 15,000–25,000; H200 30,000–35,000 | H100 28,000; H200 38,248 (ask median) | – | – | – | [Compute Exchange](https://compute.exchange/hardware-market/used-gpus/used-h200); [Mercatus](https://www.mercatus-ai.com/blog/h100-resale-value); [ServnetUK](https://www.servnetuk.com/research/gpu-residual-value-study-2026) | 2026-Q3 |

### Inferences
- **Indicative per-node all-in capex for a single production inference node in Pune.** Scope: server, a share of the networking, a rack/PDU share and an import uplift, excluding the facility build. Rounded inference from the table:
  - **B300**: about $600–700k, or about ₹5.7–6.7 crore landed pre-GST.
  - **B200**: about $430–520k.
  - **H200**: about $360–430k.
  - **MI355X**: about $330–460k plus DLC facility costs.
- An **OCR side-cluster** of 2x 2-GPU RTX PRO 6000 2U servers costs about $135k, or about ₹1.3 crore calc.
- These are planning ranges. The binding numbers must come from INR-landed OEM/distributor quotes.

### Gaps
- MI355X server, Dell/HPE/Lenovo B200/B300, 3- and 5-year OEM support, in-row coolers and Indian distributor INR quotes are all unpublished or unavailable. Confirm each with RFQs to Dell India, HPE India, Supermicro India/Rashi, Netweb (Tyrone), Ingram Micro India and Redington.
- Power figures marked "n/s" (not sourced) or "inferred" should be checked against OEM datasheets before final electrical design.
