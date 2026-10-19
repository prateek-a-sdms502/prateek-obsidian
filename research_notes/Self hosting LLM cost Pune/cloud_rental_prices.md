# Cloud GPU rental prices for an Indian LLM-serving company (H200 / B200 / B300 / GB200-GB300 / MI300X-MI355X / H100 / L40S / RTX PRO 6000), as of 19 Oct 2026

Research date: 2026-10-19. Unless flagged, prices were read from provider pages, provider price APIs or price files on 2026-10-15 to 2026-10-19.

**Units and conventions:**
- "/GPU-hr" means per GPU per hour. "Node" means an 8-GPU server unless stated.
- Per-GPU rates I derived from node prices are marked "(derived)".
- Unless marked otherwise, prices exclude GST and other taxes.
- **Hours.** 24/7 = 730 h/month. Business hours = 10 h × 22 days = 220 h/month.
- **FX.** INR-equivalents of USD prices use ₹95.18/USD, the open.er-api.com rate for 19 Oct 2026. See the FX block in the Indian-providers section.

---

## 1. Global hyperscalers (AWS, Google Cloud, Azure, Oracle OCI): on-demand vs committed, and India-region availability

### Takeaway
Hyperscalers are the most expensive option, at 1.5–3× neocloud rates. AWS India regions cost more than US East:
- **AWS Mumbai:** 8×H200 (p5en) is $75.96/hr on-demand, or $9.49/GPU-hr.
- **AWS Mumbai B200:** 8×B200 (p6-b200) is $160.65/hr, or $20.08/GPU-hr.
- **AWS Hyderabad:** 8×B300 (p6-b300) is $200.81/hr, or $25.10/GPU-hr.

Commitment cuts AWS rates by 40–60%: a 3-yr EC2 Instance Savings Plan brings H200 to about $4.10/GPU-hr and B200 to about $8.68/GPU-hr in Mumbai.

India-region availability by provider:
- **AWS:** lists H100/H200/B200 on-demand in Mumbai and B200/B300 in Hyderabad.
- **Google Cloud:** lists A3 Ultra (H200) in Mumbai and Delhi.
- **Azure:** lists only ND GB200 v6 (South India) among the target GPUs.
- **OCI:** third-party listings show H100/H200 bare-metal shapes in Mumbai and Hyderabad. OCI list prices are uniform: H200 $10, B200 $14, B300 $15, GB200 $16, GB300 $18, MI300X $6 and MI355X $8.60 per GPU-hr.

### Cited Findings

**AWS: EC2 on-demand, Linux.** Source is the AWS public price JSON (hawkFilePublicationDate 2026-10-15) that feeds the EC2 on-demand pricing page.

| Instance | Region | On-demand $/node-hr | $/GPU-hr (derived) |
|---|---|---|---|
| p5en.48xlarge (8×H200) | Mumbai | $75.9552 | $9.49 |
| p5en.48xlarge (8×H200) | N. Virginia | $63.296 | $7.91 |
| p6-b200.48xlarge (8×B200) | Mumbai | $160.645 | $20.08 |
| p6-b200.48xlarge (8×B200) | Hyderabad | $160.65 | $20.08 |
| p6-b200.48xlarge (8×B200) | N. Virginia | $113.93 | $14.24 |
| p6-b300.48xlarge (8×B300) | Hyderabad | $200.81 | $25.10 |
| p6-b300.48xlarge (8×B300) | N. Virginia | $142.416 | $17.80 |
| p5.48xlarge (8×H100) | Mumbai | $66.048 | $8.26 |
| p5.48xlarge (8×H100) | N. Virginia | $55.04 | $6.88 |
| g7e.48xlarge (8×RTX PRO 6000 Blackwell) | Mumbai | $54.135 | $6.77 |
| g7e.48xlarge (8×RTX PRO 6000 Blackwell) | N. Virginia | $33.144 | $4.14 |
| g6e.48xlarge (8×L40S) | Mumbai | $36.187 | $4.52 |
| g6e.48xlarge (8×L40S) | N. Virginia | $30.13 | $3.77 |

Region notes: p6-b300 is not listed in Mumbai, and p5/p5en are not listed in Hyderabad. Sources: [AWS price JSON – Mumbai](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/Asia%20Pacific%20(Mumbai)/Linux/index.json), [Hyderabad](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/Asia%20Pacific%20(Hyderabad)/Linux/index.json), [N. Virginia](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/US%20East%20(N.%20Virginia)/Linux/index.json). All 2026-10-15.

Cross-checks:
- Vantage lists p6-b200.48xlarge at $113.933/hr on-demand and $81.579 spot. It lists p5en.48xlarge at $63.296 on-demand and $41.014 spot. Both are US figures, updated 10/19/2026. — [Vantage p6-b200](https://instances.vantage.sh/aws/ec2/p6-b200.48xlarge), [Vantage p5en](https://instances.vantage.sh/aws/ec2/p5en.48xlarge)
- Third-party sites quote p6-b300.48xlarge at $142.416/hr in us-east-1. — [Holori](https://calculator.holori.com/aws/ec2/p6-b300.48xlarge)

**AWS Savings Plans, per node-hour, India regions.** Source is the AWS Savings Plans price file, version 20261013035015, published 2026-10-13. Per-GPU figures are derived. "EC2 ISP" is the EC2 Instance Savings Plan. "NU" is no upfront and "AU" is all upfront.

| Instance | Region | EC2 ISP 1-yr NU | EC2 ISP 3-yr NU | EC2 ISP 3-yr AU | Compute SP 1-yr NU |
|---|---|---|---|---|---|
| p5en (8×H200) | Mumbai | $47.85 ($5.98/GPU) | $32.81 ($4.10) | $28.56 ($3.57) | $59.82 ($7.48) |
| p6-b200 (8×B200) | Mumbai and Hyderabad | No 1-yr EC2 ISP | $69.40 ($8.68) | $60.40 ($7.55) | $126.51 ($15.81) |
| p6-b300 (8×B300) | Hyderabad | No 1-yr EC2 ISP | $86.75 ($10.84) | $75.50 ($9.44) | $158.14 ($19.77) |
| p5 (8×H100) | Mumbai | $41.61 ($5.20) | $28.53 ($3.57) | Not extracted | Not extracted |
| g7e (8×RTX PRO 6000) | Mumbai | $34.11 ($4.26) | $23.39 ($2.92) | Not extracted | Not extracted |
| g6e (8×L40S) | Mumbai | $22.80 ($2.85) | $15.63 ($1.95) | Not extracted | Not extracted |

Sources: [AWS SP price file ap-south-1](https://pricing.us-east-1.amazonaws.com/savingsPlan/v1.0/aws/AWSComputeSavingsPlan/20261013035015/ap-south-1/index.json), [ap-south-2](https://pricing.us-east-1.amazonaws.com/savingsPlan/v1.0/aws/AWSComputeSavingsPlan/20261013035015/ap-south-2/index.json)

- **June 2025 price cut and Savings Plans for P6-B200.** AWS cut P5 on-demand prices by about 44% and P5en by about 25% from 1 June 2025. In the same announcement it made P6-B200 available through Savings Plans. P6-B200 originally launched on 15 May 2025 through Capacity Blocks only. — [AWS What's New, June 2025](https://aws.amazon.com/about-aws/whats-new/2025/06/pricing-usage-model-ec2-instances-nvidia-gpus)
- **AWS Capacity Blocks for ML.** These are fixed-duration reservations bought in advance. Prices are per instance-hour, with per-accelerator-hour in parentheses:
  - **Mumbai:** p5en $63.158 ($7.895); p5e $54.924 ($6.866); p5.48xlarge $47.757 ($5.970); p6-b200 $113.666 ($14.208).
  - **Hyderabad:** p6-b200 $113.666 ($14.208); p6-b300 $129.168 ($16.146).
  - **GB200 UltraServers (p6e) are not in India.** They are offered only in the US East (Dallas) Local Zone: u-p6e-gb200x72 at $761.904/hr and u-p6e-gb200x36 at $380.952/hr, both $10.582/GPU-hr.
  - AWS says the current prices will next be updated in January 2027. — [AWS Capacity Blocks pricing](https://aws.amazon.com/ec2/capacityblocks/pricing/), accessed 2026-10-19
  - **Conflict on p6-b300.** One search snippet attributed a p6-b300 Capacity Block rate of $93.60/hr ($11.70/GPU) in Oregon to the same AWS page. The page fetched on 2026-10-19 showed $129.168 for all listed p6-b300 regions, so the $93.60 figure is likely stale. — [search snippet via Holori/AWS](https://calculator.holori.com/aws/ec2/p6-b300.48xlarge)

**Google Cloud.** Default region is us-central1, from Google's accelerator-optimized pricing page (accessed 2026-10-19). Prices are per 8-GPU machine-hour, with per-GPU in parentheses.
- **a3-ultragpu-8g (8×H200):**
  - On-demand $84.81 ($10.60)
  - DWS Flex-start $42.40 ($5.30)
  - DWS Calendar mode $59.36 ($7.42)
  - Spot $50.80 ($6.35)
  - 1-yr resource CUD $58.47 ($7.31)
  - 3-yr resource CUD $37.21 ($4.65)
- **a4-highgpu-8g (8×B200):**
  - On-demand "N/A" (no standard on-demand)
  - DWS Flex-start $64.44 ($8.06)
  - DWS Calendar $90.22 ($11.28)
  - Spot $39.63 ($4.95)
  - 1-yr CUD $88.93 ($11.12)
  - 3-yr CUD $56.71 ($7.09)
- **a3-megagpu-8g (8×H100):** on-demand $93.40 ($11.68); 1-yr CUD $64.21; 3-yr CUD $40.65.
- **g4-standard-384 (8×RTX PRO 6000):**
  - On-demand $36.00 ($4.50)
  - Flexible CUD $30.24 (1-yr) / $20.88 (3-yr)
  - DWS Flex-start $18.00
  - Spot $13.03
  - Resource CUD $24.84 (1-yr, $3.11/GPU) / $15.84 (3-yr, $1.98/GPU)
- **A4X (GB200) and GB300/B300 machine types have no public price on this page.** — [Google Cloud accelerator-optimized pricing](https://cloud.google.com/products/compute/pricing/accelerator-optimized?hl=en)
- **Google Cloud India regions:**
  - A3 Ultra (8×H200) on-demand is $101.77/hr in Mumbai (asia-south1), or $12.72/GPU-hr. Spot there is $54.72. The comparable us-central1 figures are $84.81 and $50.80. Observed 2026-10-19 04:52 UTC. — [Spare Cores a3-ultragpu-8g](https://sparecores.com/server/gcp/a3-ultragpu-8g)
  - Spare Cores lists an A4 (8×B200) spot price in Delhi (asia-south2) of $13.92/hr ($1.74/GPU), with no on-demand price. This is unusually low and may be a data artifact. — [Spare Cores a4-highgpu-8g](https://sparecores.com/server/gcp/a4-highgpu-8g)
  - Google's GPU regions page (cached copies) lists A3 Ultra in asia-south1-b (Mumbai) and asia-south2-c (Delhi), and G4 in asia-south2-c. No India zone lists A4 in those copies, which conflicts with the Spare Cores A4 Delhi spot listing. — [GCP GPU regions/zones](https://docs.cloud.google.com/compute/docs/gpus/gpu-regions-zones)
- **Conflict on A3 Ultra on-demand.** Thunder Compute treats GCP H200 as "reservation only" at a normalized $10.85/GPU-hr, but Google's own page shows an on-demand price. — [Thunder Compute H200 comparison, 16 Oct 2026](https://www.thundercompute.com/blog/nvidia-h200-pricing)

**Microsoft Azure.** Source is the Azure Retail Prices API, queried 2026-10-19. Linux pay-as-you-go prices are per VM-hour. Reservation totals were converted to per-hour by dividing by 8,760 h (1-yr) or 26,280 h (3-yr), so the reservation hourly figures are derived.
- **ND96isr_H200_v5 (8×H200):**
  - East US 2: $84.80/hr ($10.60/GPU)
  - 1-yr RI: about $46.52/hr ($5.82/GPU)
  - 3-yr RI: about $42.22/hr ($5.28/GPU)
  - Reservation prices effective 2026-08-01.
  - **Not priced in any India region.**
- **ND96isr_MI300X_v5 (8×MI300X):**
  - East US 2 and West US 3: $48.00/hr ($6.00/GPU)
  - 1-yr RI: about $30.72 ($3.84/GPU)
  - 3-yr RI: about $21.07 ($2.63/GPU)
  - Spot: $8.87 ($1.11/GPU)
  - **Not in India.**
- **ND128isr_NDR_GB200_v6 (4×GB200 per VM):**
  - East US: $108.16/hr ($27.04/GPU); 1-yr RI about $69.22; 3-yr RI about $47.59.
  - **South India: $163.32/hr ($40.83/GPU); 1-yr RI about $104.52 ($26.13/GPU); 3-yr RI about $71.86 ($17.97/GPU).** This is the only target-GPU ND SKU priced in an India region. The other India ND SKUs are A100 v4 (South India).
- **ND96isr_H100_v5 (8×H100):** East US $98.32/hr ($12.29/GPU); 1-yr about $62.92; 3-yr about $43.16.
- **RTX PRO 6000 (NC…RTXPRO6000BSE_v6) SKUs are priced in Central India.** For example, NC336ds_xl is $23.226/hr in Central India versus $16.59/hr in East US. GPUs per SKU were not confirmed.
- No GB300 or MI355X SKUs appear in the API. — [Azure Retail Prices API](https://prices.azure.com/api/retail/prices)
- Aggregators (Jul–Aug 2026) cite similar Azure figures: H200 at $10.60–13.78/GPU-hr and MI300X at $6.00/GPU-hr. — [Spheron Azure H200](https://www.spheron.network/blog/azure-h200-pricing-2026/), [Spheron Azure MI300X](https://www.spheron.network/blog/azure-mi300x-pricing-2026/)

**Oracle OCI.** Source is Oracle's public price-list API (pay-as-you-go, per GPU-hour), queried 2026-10-19. Oracle's HTML GPU pricing page returned HTTP 403.

| GPU | USD/GPU-hr | INR/GPU-hr (Oracle INR price list) |
|---|---|---|
| H200 | $10.00 | ₹955.45 |
| B200 | $14.00 | ₹1,337.63 |
| GB200 | $16.00 | ₹1,528.72 |
| GB300 | $18.00 | ₹1,719.81 |
| B300 | $15.00 | ₹1,433.18 |
| H100 | $10.00 | ₹955.45 |
| MI300X | $6.00 | ₹573.27 |
| MI355X | $8.60 | ₹821.69 |
| L40S | $3.50 | ₹334.41 |
| RTX PRO 6000 | $4.50 | Not shown |

- Optional NVIDIA AI Enterprise licence add-ons are priced per GPU-hr: H100/H200 $2.50, B200 $3.50, GB200 $4.00. — [OCI price list API (USD)](https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/?currencyCode=USD), [OCI price list API (INR)](https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/?currencyCode=INR)
- **OCI India regions.** Northflank lists BM.GPU.H200.8 and BM.GPU.H100.8 in Mumbai 1 and Hyderabad 1. This is third-party, not Oracle-confirmed capacity. — [Northflank OCI H200](https://northflank.com/cloud/oci/instances/BM.GPU.H200.8), [Northflank OCI H100](https://northflank.com/cloud/oci/instances/BM.GPU.H100.8)

### Inferences
- **AWS India premium.** On-demand is about 20% higher in Mumbai than US East for p5en ($75.96 vs $63.30) and about 41% higher for p6-b200 ($160.65 vs $113.93).
- **AWS Capacity Blocks in India.** Blocks carry no India premium; they cost the same as US. For short, planned bursts, a Mumbai Capacity Block (p6-b200 at $14.21/GPU-hr) is about 29% cheaper than Mumbai on-demand B200 ($20.08).
- **AWS 3-yr EC2 Instance Savings Plan** is the cheapest AWS route:
  - About $4.10/GPU-hr for H200 and $8.68 for B200 (Mumbai), and $10.84 for B300 (Hyderabad).
  - At ₹95.18/USD, that is about ₹390, ₹826 and ₹1,032 per GPU-hr.
  - That is still above Indian neoclouds for B200 (Yotta 3-yr ₹378, E2E committed ₹683).
- **Google Cloud has no on-demand B200 (A4) price.** The practical routes are spot, DWS Flex-start (≤7-day jobs, $8.06/GPU-hr in us-central1) or CUDs. For a 24/7 serving node, the 3-yr CUD ($7.09/GPU-hr) is the relevant B200 figure.
- **Azure has no H200, MI300X or B200 in India.** Its India-region GB200 v6 is very expensive at $40.83/GPU-hr on-demand. Azure is not competitive for India-resident H200/B200 serving.
- **OCI prices are uniform across regions.** If OCI capacity exists in Mumbai or Hyderabad, it costs the same as the US. Even so, OCI's $10/GPU-hr for H200 sits at the high end versus neoclouds.

### Gaps
- **AWS India pricing gaps.** I found no AWS reserved-instance pricing for P5en or P6; Savings Plans cover them, and per AWS, RIs are not supported for P6-B200. I also found no official AWS INR price for India regions; AISPL bills in INR, but INR list rates were not checked.
- **GCP gaps:**
  - India-region CUD, DWS and on-demand prices for A3 Ultra in Delhi, and for A4 in India, were not confirmed on Google's own page.
  - A4X (GB200) and any GB300/B300 machine types are not publicly priced.
- **GCP CUD discounts in India.** Not verified. Expect them to be proportionate to us-central1, since US CUDs run about 31% below on-demand for 1-yr and 56% for 3-yr.
- **OCI committed-use pricing.** Annual Universal Credits discounts are negotiated and not in the public price list.
- **Hyperscaler capacity.** A price listing in a region does not prove capacity. On-demand P6 or A3 Ultra in India requires quota approval, which I could not verify.

---

## 2. GPU clouds (neoclouds and marketplaces): on-demand and reserved rates

### Takeaway
Neocloud on-demand rates in Oct 2026 per GPU-hr:
- **H200:** about $4.5–6.3
- **B200:** about $6.7–8.6
- **B300:** about $9.0–10.0
- **MI300X:** about $2.6–3.5

Reservations of 3–6+ months bring H200 to about $3.4–4.0 and B200 to about $6.8–7.8. CoreWeave advertises up to 60% off for commitment and Nebius up to 35%.

Prices rose in late 2026. Nebius raised on-demand prices about 17–21% on 1 Oct 2026, and Blackwell is supply-constrained. Marketplaces such as Vast.ai and Hyperbolic undercut on H200 (about $4.0–4.6) but rarely offer 8-GPU nodes with InfiniBand.

### Cited Findings

**CoreWeave (North America, on-demand per instance-hr, per-GPU derived):**
- GB200 NVL72 (4 GPUs/instance): $42.00 ($10.50/GPU)
- B200 8×: $68.80 ($8.60); spot $34.11 ($4.26)
- B300 8×: contact sales; spot $35.84 ($4.48)
- H200 8×: $50.44 ($6.31); spot $20.93
- H100 8×: $49.24 ($6.16)
- RTX PRO 6000 8× high-mem: $20.00 ($2.50)
- L40S 8×: $18.00 ($2.25)
- GB300 NVL72: contact sales
- "Up to 60% discounts over our On-Demand prices for committed usage." Egress and internet transfer are free.
- [CoreWeave pricing](https://www.coreweave.com/pricing), accessed 2026-10-19

**Lambda (on-demand per GPU-hr, 8× instances):**
- B200 $6.69; H100 SXM $3.99; A100 80GB $2.79. The 1× B200 is $6.99.
- No H200 or B300 on-demand listed.
- **1-Click Clusters (2 weeks–1 year):**
  - B200: 16 GPUs $9.86, 64 GPUs $9.36, 256+ GPUs $8.87
  - H100: 16 GPUs $6.16, 64 GPUs $5.85, 256 GPUs $5.54
  - 1-yr+ terms: contact sales. Clusters run from 16 to 2,000+ GPUs.
- [Lambda pricing](https://lambda.ai/pricing), accessed 2026-10-19
- GetDeploying showed Lambda B200 as out of stock on 18–19 Oct 2026. — [GetDeploying B200](https://getdeploying.com/gpus/nvidia-b200)

**Nebius (on-demand per GPU-hr):**
- B300 $9.50; B200 $8.50; H200 $5.40; H100 $4.50; RTX PRO 6000 $1.80; L40S from $1.55
- GB200 and GB300 NVL72: contact sales
- Commitment: "up to 35% less than on-demand"
- [Nebius prices](https://nebius.com/prices), accessed 2026-10-19
- **1 Oct 2026 increase:** H100 $3.85→$4.50 (+17%), H200 $4.50→$5.40 (+20%), B200 $7.15→$8.50 (+19%), B300 $7.85→$9.50 (+21%). Preemptible pricing moved to dynamic spot. — [UsagePricing capture of Nebius change](https://usagepricing.com/blueprint/activity/nebius-ai-2026-09-24-gpu-price-increase)

**Crusoe (on-demand per GPU-hr):**
- B200 $8.50; H200 $5.40; H100 $4.50; MI300X $3.45; L40S $1.50
- GB200 and MI355X: contact sales. Reserved: contact sales.
- No ingress/egress charges. Billed "per-hour (or per-second) with no minimum commitment."
- [Crusoe pricing](https://www.crusoe.ai/cloud/pricing), accessed 2026-10-19

**Together AI GPU clusters (per GPU-hr):**

| GPU | Preemptible | On-demand | 3–30 days | 31–90 days | 91–180 days | 181+ days |
|---|---|---|---|---|---|---|
| B300 | $4.99 | $9.99 | Contact | Contact | Contact | Contact |
| B200 | $4.09 | $8.19 | $7.99 | $7.79 | $6.79 | Contact |
| H200 | $2.99 | $5.99 | $4.99 | $4.15 | $3.99 | Contact |
| H100 | $1.99 | $3.99 | $3.69 | $3.45 | $3.19 | Contact |

GB200 and GB300 NVL72 are reserved only (contact). — [Together AI pricing](https://www.together.ai/pricing), accessed 2026-10-19

**RunPod (on-demand per GPU-hr, Secure Cloud / Community Cloud):**
- B300 $8.99 / $6.94; B200 $7.99 / $5.98; H200 $5.29 / $3.59; H100 SXM $3.99 / $2.69
- RTX PRO 6000 $2.49 / $1.69; L40S $1.09 / $0.79
- Instant Cluster H200 SXM: $6.35 (unit not stated on page)
- Reserved clusters (1/3/6/12 months): contact sales
- Network volume storage: $0.07/GB-mo under 1 TB, $0.05 over 1 TB; high-performance $0.14
- Per-second or per-hour billing views
- [RunPod pricing](https://www.runpod.io/pricing), accessed 2026-10-19
- Thunder Compute recorded RunPod H200 rising from $4.59 (9 Oct) to $5.29 (16 Oct 2026). — [Thunder Compute](https://www.thundercompute.com/blog/nvidia-h200-pricing)

**Vast.ai (marketplace).** Public offers API, rentable on-demand offers, queried 2026-10-19. Per GPU-hr, including host markup:

| GPU | Offers | Min | Median | 8-GPU offers (median) |
|---|---|---|---|---|
| H200 | 16 | $2.76 | $4.61 | 6 ($4.80) |
| B200 | 10 | $6.25 | $9.00 | 2 ($9.13) |
| B300 | 7 | $5.90 | $9.92 | 2 ($7.91) |
| H100 SXM | 18 | $1.33 | $2.40 | 2 ($2.40) |
| RTX PRO 6000 WS | 47 | $1.00 | $1.40 | Not extracted |
| L40S | 26 | $0.40 | $0.66 | Not extracted |

No MI300X offers. Two H100 offers had India geolocation; none of the B200, B300, RTX PRO 6000, L40S or MI300X queries returned an India-located offer. — [Vast.ai bundles API](https://console.vast.ai/api/v0/bundles/)

Thunder Compute separately reports a Vast.ai H200 median of $4.24 (range $4.13–4.90) across 7 US/CA hosts, excluding bandwidth. — [Thunder Compute, 16 Oct 2026](https://www.thundercompute.com/blog/nvidia-h200-pricing)

**Hyperbolic:**
- H200 $3.99/GPU-hr on-demand. Thunder Compute calls it the lowest tracked rate on 16 Oct 2026. — [Thunder Compute](https://www.thundercompute.com/blog/nvidia-h200-pricing)
- B200 $5.99/GPU-hr on-demand (aggregator, Aug–Sep 2026). Reserved clusters: custom quotes. — [ComputePrices Hyperbolic B200](https://computeprices.com/providers/hyperbolic/gpus/b200), [ComputePrices Hyperbolic H200](https://computeprices.com/providers/hyperbolic/gpus/h200)

**DigitalOcean GPU Droplets (per GPU-hr, on-demand / 12-month reserved):**
- H200 $4.47 / $3.40; H100 $4.41 / $3.26
- B300: reserved $7.94; spot $6.17
- MI300X $2.59 / $1.91; MI325X $3.80 / $2.88
- MI350X: reserved $4.76; spot $3.50
- MI355X: spot only, $5.50
- L40S $1.57
- Billing is per second with a 5-minute minimum. **Powered-off Droplets keep billing until destroyed.**
- H100/H200/MI300X/MI325X Droplets include a 720 GiB boot disk, 5 TiB scratch NVMe and 15,000 GiB of transfer.
- [DigitalOcean GPU Droplet pricing](https://www.digitalocean.com/pricing/gpu-droplets), accessed 2026-10-19

**AMD-focused clouds:**
- **Hot Aisle:** MI300X VMs (1×/2×/4×) at $2.99/GPU-hr; 8× bare metal at $3.39/GPU-hr, billed by the minute. No MI325X/MI355X prices listed. — [Hot Aisle pricing](https://hotaisle.xyz/pricing/), accessed 2026-10-19. Spheron reports a 1-month minimum for Hot Aisle bare metal. — [Spheron AMD pricing](https://www.spheron.network/blog/amd-mi300x-mi355x-pricing-2026/)
- **TensorWave:** MI355X "starting at" $2.95/GPU-hr (custom contract, 8×) and MI300X from $1.71 (quote-driven). TensorWave's own /pricing URL returned 404. — [GetDeploying MI355X, 19 Oct 2026](https://getdeploying.com/gpus/amd-mi355x), [Spheron AMD pricing, Aug–Sep 2026](https://www.spheron.network/blog/amd-mi300x-mi355x-pricing-2026/)
- **Spheron's AMD survey (prices dated 16–21 Aug 2026):**
  - CoreWeave MI355X: $7.20 on-demand, $4.25 with a 1-yr reservation
  - OCI MI355X: $8.60
  - Vultr MI355X: $2.59 preemptible
  - Vultr MI300X: $1.85 preemptible; $1.75 on 24-month prepay
  - Cirrascale MI300X: $3.85, minimum $22,499/month
  - Vultr's two pages disagree on its 48-month prepaid rate ($2.650 vs $2.290).
  - [Spheron AMD pricing](https://www.spheron.network/blog/amd-mi300x-mi355x-pricing-2026/)

**Vultr:**
- The pricing page blocked automated fetches (HTTP 403).
- B200: $3.20/GPU-hr spot, 8×, "out of stock" on GetDeploying (19 Oct 2026). An aggregator listed $3.50/hr for 8× (12 Sep 2026); the unit (per GPU vs per node) is unclear. — [GetDeploying B200](https://getdeploying.com/gpus/nvidia-b200), [ComputePrices Vultr MI355X](https://computeprices.com/providers/vultr/gpus/mi355x)
- MI355X: $2.59 spot, 8×, out of stock. — [GetDeploying MI355X](https://getdeploying.com/gpus/amd-mi355x)

**Cross-provider indices:**
- **Mercatus (13 Sep 2026)**, volume-weighted average $/GPU-hr:
  - B300 $8.89 (7 providers, +5.3% over 30 days)
  - B200 $6.39 (12 providers)
  - MI300X $4.98
  - H200 $4.43 (20 providers)
  - H100 $3.84 (27 providers)
  - [Mercatus GPU rental prices](https://www.mercatus-ai.com/blog/gpu-rental-prices)
- **GetDeploying (week of 12 Oct 2026)**, median on-demand, GPU clouds vs hyperscalers: H100 $4.50 vs $7.89; H200 $5.40 vs $10.85; B200 $8.50 vs $14.24. — [GetDeploying GPU price index](https://getdeploying.com/gpu-price-index)
- **B300 cheapest verified in-stock on-demand: $7.99/GPU-hr (UpCloud).** The GB300 reference on-demand is $18.00/GPU-hr. — [GetDeploying B300](https://getdeploying.com/gpus/nvidia-b300)

### Inferences
- **H200 8-GPU node 24/7 (730 h)** at ₹95.18/USD:
  - RunPod Secure $5.29: about ₹29.4 lakh/month
  - Nebius/Crusoe $5.40: ₹30.0 lakh
  - Together 91–180-day reserved $3.99: ₹22.2 lakh
  - DigitalOcean 12-month $3.40: ₹18.9 lakh
- **B200 8-GPU node 24/7:** Lambda $6.69 ≈ ₹37.2 lakh; RunPod $7.99 ≈ ₹44.4 lakh; Nebius/Crusoe $8.50 ≈ ₹47.3 lakh; CoreWeave $8.60 ≈ ₹47.8 lakh.
- **Business hours (220 h/month)** cuts on-demand bills to about 30% of 24/7 only where billing is per-second, per-minute or per-hour and instances are destroyed or stopped. Reserved capacity is billed whether used or not. DigitalOcean bills powered-off Droplets.
- **AMD is the cheapest high-memory option.** MI300X (192 GB) runs $2.6–3.5/GPU-hr on-demand and MI355X (288 GB) about $2.95 from TensorWave on contract. Availability of 8× MI355X on-demand outside OCI ($8.60) is thin.
- **Late-2026 direction is up, not down.** Nebius raised prices, RunPod H200 rose, and the B300 index is up 5% month over month. Lock-in quotes now may beat waiting.

### Gaps
- **Unpublished rates:** Lambda H200/B300 on-demand, CoreWeave and Nebius committed rates, and Crusoe reserved. All are "contact sales".
- **Unverified primary pages:** TensorWave, Vultr and Hyperbolic first-party pages could not be fetched (404, 403, not fetched). Their figures come from aggregators.
- **Hyperbolic and Vast.ai reserved rates:** not published.
- **MI325X neocloud rates** beyond DigitalOcean (and the IndiaAI calculator below) were not found.

---

## 3. Indian providers: INR rates, terms and GST treatment (plus INR/USD FX)

### Takeaway
Indian clouds publish INR rates, excluding 18% GST, that are well below hyperscalers.

Per GPU-hr:
- **E2E Networks:** B200 ₹759 on-demand / ₹683 committed; H200 ₹503 / ₹463; RTX PRO 6000 ₹237.
- **Yotta Shakti bare metal:** B200 ₹473 (monthly/1-yr) falling to ₹378 (3-yr); B300 ₹1,056 (1-yr) falling to ₹672 (3-yr); H100 ₹351 monthly.
- **Tata Vayu:** 8×H200 ₹4,247/node-hr on-demand (₹531/GPU) falling to ₹3,085 on 3-yr (₹386/GPU).
- **Krutrim:** H100 ₹213.
- **Neysa:** 8×H200 $13,810.58/month on a 36-month term, about $2.37/GPU-hr.

Most Indian B200/B300 capacity is sold on monthly-plus terms. The current exchange rate is about ₹95.2/USD (19 Oct 2026). E2E's own USD and INR lists imply ₹95.0/USD, and Oracle's INR list implies about ₹95.5.

### Cited Findings

**E2E Networks.** Pricing page as .md, generated 2026-10-16. INR prices exclude 18% GST, and GST invoices are issued. Rates are per GPU-hr for 1× instances:
- **B200 180GB:** ₹759.05 on-demand; ₹683.05 committed; USD list $7.99
- **H200 141GB:** ₹502.55; ₹462.65 committed; spot ₹88; USD $5.29
- **H100:** ₹379.05; ₹347.70 committed; spot ₹70; USD $3.99
- **RTX PRO 6000 96GB:** ₹236.55; ₹217.55 committed; USD $2.49
- **L40S:** ₹102; USD $1.20
- **A100 80GB:** ₹189
- Monthly and annual plans are "Contact Sales", with 1/3/6/12-month terms. 8× configurations and B300/MI300X are not listed.
- Regions: Delhi NCR and Chennai.
- Compute billed hourly, no minimum commitment.
- **Storage:** block ₹10,000/TB-month (₹13.7/hr); SFS ₹12,000 per 1,000 GB-month; object ₹2.5/GB beyond 250 GB; parallel FS ₹70/GB-month.
- No egress price listed.
- [E2E pricing](https://www.e2enetworks.com/pricing.md)
- **E2E B200 cluster.** E2E announced its B200 cluster live on 1 June 2026, built on NVIDIA-Certified HGX B200 systems with InfiniBand. — [E2E blog](https://www.e2enetworks.com/blog/b200-live-blog). Inc42 reports E2E's GPU fleet at about 5,100 GPUs (Q1 FY27). — [Inc42](https://inc42.com/buzz/e2e-networks-reports-₹44-cr-profit-in-q1-revenue-zooms-3-3x-yoy/)
- **Conflicting E2E figures.** A search snippet of an E2E page claimed USD $6.99 (B200) and $4.54 (H200) with per-minute billing. Another aggregator claimed H200 at $2.20 and B200 at $4.90. Both conflict with the 2026-10-16 rate card. — [Spheron India 2026](https://www.spheron.network/blog/gpu-cloud-india-2026/), [eCorpIT](https://ecorpit.com/india-gpu-cloud-rental-pricing-h100-b200-2026/)

**Yotta Shakti Cloud:**
- **Bare metal, per GPU-hr in INR:**

| Term | B200 | B300 | H100 | L40S |
|---|---|---|---|---|
| Monthly | ₹473 | Not listed | ₹351 | ₹197 |
| 6 months | ₹473 | Not listed | ₹338 | ₹175 |
| 1 year | ₹473 | ₹1,056 | ₹263 | ₹159 |
| 2 years | ₹437 | ₹864 | ₹253 | ₹145 |
| 3 years | ₹378 | ₹672 | Not listed | Not listed |
| 4 years | ₹316 | ₹480 | Not listed | Not listed |
| Probably 5 years | ₹279 | ₹380 | Not listed | Not listed |

  - The page shows two "4 Years" tables; the second is probably the 5-year rate.
  - No H200 rate. Ingress and egress are included free. InfiniBand is charged separately. GST is not mentioned.
  - [Yotta bare metal](https://shakticloud.ai/bare-metal-service/), accessed 2026-10-19
- **Pricing page:**
  - On-demand VM 1×H100 ₹356/hr; 1×L40S ₹137/hr
  - SLURM cluster 8×H100 SXM5: ₹386/GPU-hr
  - **InfiniBand interconnect: ₹16,060/GPU, charged separately; the unit period is not stated.**
  - Kubernetes/SLURM management fee: ₹4.5–11.25 lakh per cluster
  - Standalone egress: ₹5.99/GB
  - Block storage ₹4–9.5/GB-month; file ₹8/GB-month; high-speed ₹9.9/GB-month
  - VMs bill hourly on demand and monthly for dedicated
  - [Yotta pricing](https://shakticloud.ai/pricing)
  - Search tooling flagged parts of the pricing page as indexed about 264 days earlier, and Yotta's homepage still said B200 "coming soon". Treat the B200 and B300 rates as potentially stale. — [Yotta](https://shakticloud.ai/)

**Tata Communications Vayu AI Cloud.** Official PDF, modified 2 Feb 2026, so stale by about 8 months. Prices are per node-hour in INR:

| SKU | On-demand | 3-month | 6-month | 1-yr | 3-yr | 4-yr |
|---|---|---|---|---|---|---|
| GPU.BM.H200SXM.8X | ₹4,247 | ₹4,128 | ₹3,663 | ₹3,256 | ₹3,085 | ₹2,931 |
| GPU.BM.H200NVL.8X | ₹4,122 | Not extracted | Not extracted | ₹3,160 | ₹2,994 | Not extracted |
| GPU.BM.H100SXM.8X | ₹3,905 | Not extracted | Not extracted | ₹2,994 | ₹2,836 | ₹2,694 |
| GPU.BM.L40S.4X | ₹1,174 | Not extracted | Not extracted | ₹900 | ₹853 | Not extracted |

- 1×H200 NVL VMs start at ₹402/hr.
- Object storage ₹1.50/GB-month.
- No B200/B300 SKUs in this list.
- [Tata Vayu GPUaaS price list PDF](https://www.tatacommunications.com/hubfs/library/documents/Tata%20Communications%20Vayu%20AI%20Cloud%20GPU%20as%20a%20Service.pdf)

**Neysa (Velocis).** USD only on the page. Billed to the minute, and "node pricing flat across every term from 1 to 36 months".
- H200 SXM from $4.72/GPU-hr
- 8×H200: $13,810.58/month (36-month reserved)
- 8×H100: $12,422.59/month
- 8×MI300X: $12,981.96/month
- 8×L40S: $4,302.79/month
- 8×B300 and RTX PRO 6000: on request. B200 not listed.
- Storage $0.10/GB-month; bandwidth beyond 10 TB $0.04/GB.
- [Neysa pricing](https://neysa.ai/pricing), accessed 2026-10-19

**Jarvislabs.** Page shows USD. INR is available via a currency toggle but was not captured.
- H200 SXM $4.59/GPU-hr; H100 SXM $3.49; RTX PRO 6000 $2.19
- Billed per minute, with pause/resume.
- Commitment discounts: 2% (1 month), 3% (3 months), 5% (6 months), 9% (1 year).
- H200 InfiniBand clusters and 25+ GPUs: contact sales.
- Storage $0.10/GB-month; egress free in-region.
- Region: India (Noida) is mentioned for CPU VMs.
- [Jarvislabs pricing](https://jarvislabs.ai/pricing), accessed 2026-10-19
- **Conflicting H200 figures.** Jarvislabs' own blog and GetDeploying cite H200 at $3.99 on-demand ($4.22 on a 12-month term). — [Jarvislabs H200 blog (Aug 2026)](https://jarvislabs.ai/blog/h200-price), [GetDeploying H200](https://getdeploying.com/gpus/nvidia-h200)
- eCorpIT reports Jarvislabs H100 at ₹217.89/hr in a July 2026 snapshot. — [eCorpIT](https://ecorpit.com/india-gpu-cloud-rental-pricing-h100-b200-2026/)

**Ola Krutrim Cloud (official docs).** Rates are per instance-hour:
- **H100 ×1:** ₹213 on-demand. Reserved rates, all listed as per-hour: ₹198 monthly, ₹186 for 6 months, ₹173 for 1 year.
- H100 ×4: ₹852.
- AI Pod H100 ×8: ₹1,700/hr (₹212.5/GPU).
- No H200, B200 or B300.
- [Krutrim pricing docs](https://docs.cloud.olakrutrim.com/basics/pricing/cpu-and-gpu)

**Other Indian providers:**
- **Sify:** announced hourly GPU-cloud pricing for partners supporting H100, H200, B200, GB200 NVL72 and GB300 NVL72. No rates were published, and the press-release date was not captured. — [Sify press release](https://seekingalpha.com/pr/20110424-sify-announces-pay-per-use-colocation-pricing-at-all-nvidia-certified-ai-ready-hyperscale)
- **CtrlS:** no public GPU rates found; consultative pricing. — [search results summary (WHTop listing)](https://www.whtop.com/plans/ctrls.com/152306)
- **Netweb:** primarily a hardware OEM; no GPU-cloud rate card found.
- **Reliance/Jio:** Reliance plans to commission 120 MW of AI compute at Jamnagar by end-2026, with an initial GB300 fleet. No public pricing. — [Republic World, 19 Jun 2026](https://www.republicworld.com/business/jio-reliance-intelligence-sovereign-ai-nvidia-infrastructure-call-agent-2026-06-19-129041), [Free Press Journal, AGM 2026](https://www.freepressjournal.in/amp/business/reliance-agm-2026-120-mw-ai-infrastructure-by-year-end-ambani-unveils-indias-sovereign-ai-vision)
- **Cyfuture AI / AceCloud (July 2026 snapshot):** Cyfuture H100 ₹329/hr on-demand and ₹219/hr on a 12-month plan, per-second billing. AceCloud H100 HGX from ₹1,80,000/month (₹1,62,000/month on a 12-month term). — [eCorpIT, 23 Jul 2026](https://ecorpit.com/india-gpu-cloud-rental-pricing-h100-b200-2026/)

**FX (INR/USD):**
- ₹95.1849/USD on 19 Oct 2026 00:02 UTC. — [open.er-api.com](https://open.er-api.com/v6/latest/USD)
- E2E's parallel lists imply ₹95.0/USD. For example, ₹759.05 / $7.99 = 95.0, and ₹502.55 / $5.29 = 95.0. — [E2E pricing](https://www.e2enetworks.com/pricing.md)
- Oracle's INR price list implies ₹95.545/USD (₹955.45 vs $10.00 for H200). — [OCI INR price list](https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/?currencyCode=INR)
- Asia Business Outlook (28 Apr 2026) converted ₹290.7 to $3.1, implying about ₹93.8. — [Asia Business Outlook](https://www.asiabusinessoutlook.com/news/indiaai-lowers-nvidia-b200-gpu-prices-in-compute-tender-nwid-11806.html)
- The rupee first breached 95/USD on 30 March 2026 and hit fresh lows on 30 April 2026. Reports of a 95.71 close in May come from weaker, duplicated sources. — [Angel One](https://www.angelone.in/news/economy/rupee-slips-past-95-per-dollar-to-record-low-on-april-30-2026), [5paisa](https://www.5paisa.com/index.php/news/rupee-hits-record-low-breaches-95-per-us-dollar-amid-oil-surge)
- eCorpIT used roughly ₹84–95/USD, implying about ₹85 in its conversions, which is stale. — [eCorpIT](https://ecorpit.com/india-gpu-cloud-rental-pricing-h100-b200-2026/)

### Inferences
- **8×B200 node monthly cost** (Indian providers, pre-GST):
  - E2E on-demand ₹759.05/GPU-hr: about ₹44.3 lakh/month 24/7, or about ₹13.4 lakh at 220 h/month (if billed only when running)
  - E2E committed ₹683.05: about ₹39.9 lakh/month 24/7
  - Yotta bare metal ₹473 (monthly term): about ₹27.6 lakh/month. Monthly bare metal is effectively billed 24/7.
  - Yotta 3-yr ₹378: about ₹22.1 lakh/month
- **8×H200 node monthly cost, 24/7:**
  - E2E on-demand ₹502.55: about ₹29.3 lakh/month
  - Tata on-demand ₹4,247/node-hr: about ₹31.0 lakh; on 3-yr ₹3,085: about ₹22.5 lakh
  - Neysa 36-month: $13,810.58, about ₹13.1 lakh/month at ₹95.18. That is far cheaper, but it is a 36-month commitment.
- **Price ranking.** Yotta's B200 (₹473 monthly) is cheaper than AWS Mumbai's 3-yr Savings Plan B200 (about ₹826/GPU-hr). Indian clouds win on B200 by about 40–75% before GST input-credit considerations.
- **Yotta B300 premium.** Yotta's B300 1-yr rate (₹1,056) is more than double its B200 1-yr rate (₹473). On longer terms the gap narrows to about 1.4–1.8×.

### Gaps
- **No public INR rates** for Neysa, Jarvislabs (toggle not captured), Sify, CtrlS, Netweb or Reliance/Jio.
- **E2E rate card gaps:** no 8×B200/H200 node price and no egress price on the rate card.
- **Yotta gaps:** no H200 price; the InfiniBand ₹16,060/GPU charge has an unclear period; GST treatment is not stated. B200 and B300 page freshness is uncertain.
- **Tata's price list is from Feb 2026** and may be stale. It shows no B200/B300.

---

## 4. IndiaAI Mission subsidized compute: rates, eligibility, process, conditions

### Takeaway
The official IndiaAI compute portal price calculator (last updated 14 Oct 2026) lists pre-subsidy, GST-exclusive rates per instance-hour across on-demand and 1/6/12-month reserved:
- **8×B200:** ₹2,325.6/hr (₹290.7/GPU-hr); 12-month ₹2,008.8
- **8×B300:** ₹2,808 (₹351/GPU)
- **8×H200 SXM:** ₹1,125 (₹140.6/GPU)
- **8×H100 SXM:** ₹1,224 (₹153/GPU)
- **8×MI300X:** ₹1,416.5; **8×MI325X:** ₹1,351.8
- **8×RTX PRO 6000:** ₹916.8; **8×L40S:** ₹540

An IndiaAI subsidy of up to 40% may apply, subject to approval.

Eligibility is limited to:
- researchers and academia
- DPIIT startups and MSMEs meeting revenue or funding thresholds
- IndiaAI fellows and students
- early-stage startups and researchers
- government entities

Requests go through a monthly cycle: apply between the 1st and 25th, and results come out on the 10th of the next month. A general private company outside these categories does not appear eligible.

### Cited Findings

**Price calculator** (₹ per instance-hour, excl. GST; "Last Updated: 14-10-2026"). The NVIDIA columns are on-demand / 1-month / 6-month / 12-month reserved:
- **B200SXM.8x:** 2,325.6 / 2,217.6 / 2,109.6 / 2,008.8. The 1× is 290.7 / 277.2 / 263.7 / 251.1.
- **B300SXM.8x:** 2,808 / 2,736 / 2,664 / 2,556. The 1× is 351.
- **H200SXM.8x:** 1,125 / 1,100 / 945 / 785. The 1× is 140 / 135 / 118 / 100.
- **Calculator inconsistency.** H200SXM.2X is 510 (₹255/GPU) and H200SXM.4X is 1,020. These don't scale linearly from 1× or 8×, likely because different empanelled vendors set the price for each configuration.
- **H200NVL.8x:** 1,171 / 1,148.91 / 1,126.81 / 1,104.72. **H200PCIE.8X:** 3,236.8, an outlier.
- **H100SXM.8x:** 1,224 / 1,072.8 / 1,000.8 / 936. The 1× is 153. **H100NVL.8X:** 1,349.92.
- **RTX.PRO.6000.8x:** 916.8 / 873.2 / 831.6 / 792. The 1× is 114.6.
- **L40S.8x:** 540 / 396 / 396 / 360. The 1× is 67.5.

The AMD/MI-series rows list on-demand / 1-month / 6-month / 12-month:

| Instance | On-demand | 1-month | 6-month | 12-month |
|---|---|---|---|---|
| MI300X.8X | 1,416.5 | 1,389.9 | 1,363.2 | 1,336.0 |
| MI300X.1X | 168.2 | Not captured | Not captured | Not captured |
| MI325X.8X | 1,351.8 | 990 | 820.8 | 684 |
| MI325X.1X | 169.2 | Not captured | Not captured | Not captured |

- **Other rows:** Gaudi 3 8x 1,224; TPU v6e (GCP) and AWS Inferentia/Trainium rows also appear.
- **Subsidy:** "Max Subsidy (Max upto 40% subject to approval from IndiaAI)". "All prices are exclusive of GST and other taxes."
- Source: [IndiaAI price calculator](https://compute.indiaai.gov.in/indiaaipricecalculator)

**Eligibility** (official portal home page, accessed 2026-10-19):
- **Researchers and academia:** h-index ≥5, or AI/ML journal publications with impact factor >2.5, or 150+ citations.
- **Startups and MSMEs:** DPIIT recognition, AI/ML experience, and either annual revenue of ₹50 lakh or funding of ₹100 lakh.
- **IndiaAI Fellowship awardees.**
- **Students:** AI/ML projects and an aligned academic profile.
- **Early-stage startups:** 4 years of AI/ML experience plus a letter from the IndiaAI CEO or an officer of Joint Secretary rank or above.
- **Government entities:** a letter from a Director, MD, GM or authorized officer.
- **Early-stage researchers.**
- Source: [IndiaAI compute portal](https://compute.indiaai.gov.in/)

**Process and conditions** (same portal):
- Log in via DigiLocker, e-Pramaan or Jan Parichay, then complete user verification and registration with documents.
- Submit a compute request with a draft bill from the rate list, including any subsidy request.
- **Under 5,000 GPU-hours:** auto-approved. **Above 5,000 GPU-hours:** needs approval from the Program Monitoring and Evaluation Committee (PMEC).
- Requests are accepted from the 1st to the 25th of each month. Approved users are published on the 10th of the following month.
- **Approvals are valid for 30 calendar days, and services must start within that window.**
- Users bear costs beyond the subsidy, and payment goes to the service provider per its billing cycle.
- Source: [IndiaAI compute portal](https://compute.indiaai.gov.in/)
- A secondary source adds that requests seeking subsidy or more than 50 GPUs also go to PMEC. — [CareerIndia](https://www.careerindia.com/news/indiaai-compute-gpu-slots-2026-apply-subsidised-access-pricing-guide-011-64797.html)

**Tender context:**
- **B200 rate cut.** IndiaAI cut the B200 rate by 10% in the 4th tender round, from about ₹323 to ₹290.7/hr for a single GPU and ₹2,325.6/hr for 8 GPUs. Selected firms must match L1 rates and deploy at least 1,000 compute units within six months. The pricing has no ingress/egress fees. — [Asia Business Outlook, 28 Apr 2026](https://www.asiabusinessoutlook.com/news/indiaai-lowers-nvidia-b200-gpu-prices-in-compute-tender-nwid-11806.html)
- **Business Standard (Oct 2026), via search snippet** (direct fetch blocked, HTTP 403):
  - The average L1 across the first three rounds was about ₹115/GPU-hr, and the H100 L1 was about ₹140.
  - L1 prices are subsidised, so providers cannot offer them to global firms at those rates.
  - More than 38,000 GPUs were onboarded across three rounds.
  - [Business Standard](https://www.business-standard.com/amp/technology/tech-news/successful-gpu-bidders-likely-to-offer-compute-capacity-to-global-firms-126101100603_1.html)
- **Approved projects.** The portal reported 190 approved projects: 78 government, 46 startups/MSMEs, 30 early-stage startups and 27 researchers/academia. This is from a secondary search summary citing official figures, date unclear. — [CareerIndia](https://www.careerindia.com/news/indiaai-mission-2026-access-subsidized-gpus-boost-ai-careers-scale-startups-011-66885.html)
- **Secondary claims (unverified, low reliability):**
  - Effective subsidised H100 is about ₹92/hr and standard GPUs about ₹67/hr.
  - Foundation-model builders get 100% subsidy, e.g. Sarvam with 4,096 H100s backed by ₹98.68 crore.
  - These don't reconcile exactly with 40% off the calculator rates. — [eCorpIT](https://ecorpit.com/india-gpu-cloud-rental-pricing-h100-b200-2026/)

### Inferences
- **With the full 40% subsidy** (derived):
  - 8×H200 SXM: ₹1,125 → ₹675/node-hr (₹84/GPU-hr)
  - 8×B200: ₹2,325.6 → ₹1,395/node-hr (₹174/GPU-hr)
  - 8×B300: ₹2,808 → ₹1,685/node-hr (₹211/GPU-hr)
- **Even without subsidy,** IndiaAI rates are about 40–72% below E2E and Yotta list prices. Examples: B200 ₹290.7 is 62% below E2E's ₹759 and 39% below Yotta's ₹473; H200 ₹140.6 is 72% below E2E's ₹503.
- **Monthly cost, 24/7, before subsidy and GST:**
  - 8×B200 at the 12-month IndiaAI rate: ₹2,008.8 × 730 ≈ ₹14.7 lakh/month
  - 8×H200 at the 12-month rate: ₹785 × 730 ≈ ₹5.7 lakh/month
- **Fit for a commercial LLM-serving company.** Eligibility is the binding constraint. A company that is not a DPIIT-recognized startup or MSME meeting the ₹50 lakh revenue / ₹1 crore funding test, or a government project, likely cannot use the portal.
- **Fit for always-on serving.** The 30-day validity and monthly cycle make the portal awkward for always-on production. Long reserved approvals would be needed.

### Gaps
- **Unread portal PDFs:** "Empanelled GPUs" and the "Users Ready Reckoner". They may list providers per rate and the rules on commercial use, re-sale and data localisation.
- **Provider mapping:** which empanelled provider serves each calculator row.
- **Production use:** whether subsidised compute can be used for commercial production inference rather than R&D was not confirmed.
- **Subsidy cap:** the exact cap per project and per user was not stated on the pages read.

---

## 5. Ancillary costs: storage, egress, support, minimum commitments, billing granularity

### Takeaway
- **Storage:** about $0.05–0.10/GB-month (₹4–12/GB-month at Indian clouds) for block or shared file storage. Parallel filesystems cost much more (E2E ₹70/GB-month).
- **Egress:**
  - Free at CoreWeave, Crusoe, Nebius networking and Jarvislabs in-region.
  - Free inside Yotta bare-metal prices; ₹5.99/GB standalone.
  - IndiaAI pricing has none.
  - AWS Mumbai charges $0.1093/GB for the first 10 TB/month.
  - OCI's first 10 TB/month is free.
- **Billing granularity:** per second (DigitalOcean, RunPod, Crusoe option) or per minute (Jarvislabs, Neysa, Hot Aisle). E2E is hourly per its rate card. Yotta bare metal and Neysa reserved are monthly or longer.
- **Business-hours-only use** only saves money on per-second, per-minute or per-hour on-demand billing. Instances must be destroyed or stopped where stopped instances are not billed.

### Cited Findings

**Storage:**

| Provider | Price | Source |
|---|---|---|
| AWS Mumbai | EBS gp3 $0.0912/GB-month ($91.2/TB-month); io2 $0.131/GB-month | [AWS EBS price JSON](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ebs.json), accessed 2026-10-19 |
| E2E | Block ₹10,000/TB-month; SFS ₹12,000/TB-month; object ₹2.5/GB-month; parallel FS ₹70/GB-month | [E2E](https://www.e2enetworks.com/pricing.md) |
| Yotta | Block ₹4–9.5/GB-month; file ₹8; object ₹2.5–3.6; high-speed ₹9.9 (min 500 GB) | [Yotta](https://shakticloud.ai/pricing) |
| Tata Vayu | Object ₹1.50/GB-month | [Tata PDF](https://www.tatacommunications.com/hubfs/library/documents/Tata%20Communications%20Vayu%20AI%20Cloud%20GPU%20as%20a%20Service.pdf) |
| CoreWeave | Distributed file $0.07/GB-month; object hot $0.06 | [CoreWeave](https://www.coreweave.com/pricing) |
| Nebius | Shared FS $0.08/GiB-month; block $0.053–0.118; object standard $0.0147 | [Nebius](https://nebius.com/prices) |
| Crusoe | Persistent $0.08/GiB-month; shared $0.07 | [Crusoe](https://www.crusoe.ai/cloud/pricing) |
| RunPod | Network volume $0.07/GB-month (<1 TB), $0.05 (>1 TB); high-performance $0.14 | [RunPod](https://www.runpod.io/pricing) |
| Neysa | $0.10/GB-month; WEKA $0.11 | [Neysa](https://neysa.ai/pricing) |
| Jarvislabs | $0.10/GB-month | [Jarvislabs](https://jarvislabs.ai/pricing) |

**Egress:**

| Provider | Egress | Source |
|---|---|---|
| AWS Mumbai | Internet out $0.1093/GB (next 10 TB), $0.085 (next 40 TB), $0.082 (next 100 TB), $0.080 (>150 TB); inter-region out $0.086/GB | [AWS data transfer JSON](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/datatransfer/USD/current/datatransfer.json) |
| CoreWeave | Free | [CoreWeave](https://www.coreweave.com/pricing) |
| Crusoe | No ingress/egress charge | [Crusoe](https://www.crusoe.ai/cloud/pricing) |
| Nebius | Networking free; object standard egress $0.015/GiB | [Nebius](https://nebius.com/prices) |
| Yotta | Included in bare-metal and VM prices; ₹5.99/GB standalone | [Yotta](https://shakticloud.ai/pricing) |
| Neysa | $0.04/GB beyond 10 TB | [Neysa](https://neysa.ai/pricing) |
| IndiaAI | No ingress/egress fees | [Asia Business Outlook](https://www.asiabusinessoutlook.com/news/indiaai-lowers-nvidia-b200-gpu-prices-in-compute-tender-nwid-11806.html) |
| OCI | First 10 TB/month outbound free | [Oracle networking pricing](https://www.oracle.com/cloud/networking/pricing) |
| DigitalOcean | H100/H200 Droplets include 15,000 GiB of transfer | [DigitalOcean](https://www.digitalocean.com/pricing/gpu-droplets) |

- **OCI egress above 10 TB.** Third parties put it at about $0.0085/GB. One unverified source claims OCI dropped all egress charges in Feb 2026. — [Oracle networking pricing](https://www.oracle.com/cloud/networking/pricing)

**Billing granularity:**

| Provider | Granularity | Source |
|---|---|---|
| DigitalOcean | Per second, 5-minute minimum; powered-off Droplets still billed | [DigitalOcean](https://www.digitalocean.com/pricing/gpu-droplets) |
| Jarvislabs | Per minute, with pause/resume | [Jarvislabs](https://jarvislabs.ai/pricing) |
| Neysa | To the minute | [Neysa](https://neysa.ai/pricing) |
| Hot Aisle | Per minute | [Hot Aisle](https://hotaisle.xyz/pricing/) |
| Crusoe | Per hour or per second, no minimum | [Crusoe](https://www.crusoe.ai/cloud/pricing) |
| RunPod | Per-hour and per-second pricing views | [RunPod](https://www.runpod.io/pricing) |
| E2E | Compute billed hourly, no minimum commitment | [E2E](https://www.e2enetworks.com/pricing.md) |
| Yotta | VMs hourly; dedicated monthly | [Yotta](https://shakticloud.ai/pricing) |
| Nebius | Spot prices may change every 15 minutes | [Nebius](https://nebius.com/prices) |

**Minimum commitments and terms:**

| Provider | Terms | Source |
|---|---|---|
| Lambda clusters | 16+ GPUs; 2 weeks to 1 year | [Lambda](https://lambda.ai/pricing) |
| Together reserved | From 3 days | [Together](https://www.together.ai/pricing) |
| DigitalOcean reserved | 12 months | [DigitalOcean](https://www.digitalocean.com/pricing/gpu-droplets) |
| Vultr | 24/36/48-month prepay for lowest AMD rates | [Spheron AMD](https://www.spheron.network/blog/amd-mi300x-mi355x-pricing-2026/) |
| Cirrascale MI300X | $22,499/month minimum | [Spheron AMD](https://www.spheron.network/blog/amd-mi300x-mi355x-pricing-2026/) |
| Hot Aisle bare metal | 1 month | [Spheron AMD](https://www.spheron.network/blog/amd-mi300x-mi355x-pricing-2026/) |
| Tata | 3/6/12/36/48 months | [Tata PDF](https://www.tatacommunications.com/hubfs/library/documents/Tata%20Communications%20Vayu%20AI%20Cloud%20GPU%20as%20a%20Service.pdf) |
| E2E | 1/3/6/12 months via sales | [E2E](https://www.e2enetworks.com/pricing.md) |
| AWS Savings Plans | 1 or 3 years | [AWS SP price file](https://pricing.us-east-1.amazonaws.com/savingsPlan/v1.0/aws/AWSComputeSavingsPlan/20261013035015/ap-south-1/index.json) |
| GCP CUD | 1 or 3 years | [GCP](https://cloud.google.com/products/compute/pricing/accelerator-optimized?hl=en) |
| GCP DWS Flex-start | Short jobs (see section 1) | [GCP](https://cloud.google.com/products/compute/pricing/accelerator-optimized?hl=en) |

**Other platform fees:**
- Yotta: Kubernetes/SLURM management ₹4.5–11.25 lakh per cluster; InfiniBand ₹16,060/GPU. — [Yotta](https://shakticloud.ai/pricing)
- CoreWeave: public IP $4/month; Direct Connect from $1,250/month. — [CoreWeave](https://www.coreweave.com/pricing)
- Neysa: Kubernetes HA master $463.33/month; load balancer $341.07/month. — [Neysa](https://neysa.ai/pricing)

### Inferences
- **Business-hours vs 24/7.** For an 8-GPU on-demand node run 220 h instead of 730 h, the bill falls to 30%. Examples: E2E 8×B200 ₹13.4 lakh vs ₹44.3 lakh/month, and RunPod 8×H200 $9,310 vs $30,890/month.
- **Committed or monthly capacity.** For Yotta monthly bare metal, Neysa reserved, AWS Savings Plans or GCP CUDs, business-hours usage gives no saving. Model these at 730 h.
- **Egress for serving.** Egress is minor for LLM token streaming but matters for model-weight pulls and logs. For example, 5 TB/month out of AWS Mumbai ≈ $547.

### Gaps
- **Support plans:** I did not research hyperscaler premium support pricing (AWS Business/Enterprise, GCP Enhanced/Premium, Azure Pro Direct, OCI) or Indian-provider premium support; none came up in the sources.
- **Hyperscaler billing granularity:** AWS, GCP, Azure and OCI GPU billing granularity is commonly documented as per-second with a 1-minute minimum for AWS Linux and GCP, but I did not verify it in this research.
- **Persistent-storage prices** for GCP Hyperdisk/Filestore, Azure Managed Lustre and OCI File Storage were not collected.

---

## 6. Taxes: GST, reverse charge, TDS and equalisation levy

### Takeaway
**Indian providers** charge 18% GST on top of list prices. For example, E2E and IndiaAI rates both exclude GST. A GST-registered company can claim input tax credit.

**Hyperscalers billing through Indian entities** charge 18% GST forward on the invoice:
- AWS via Amazon Internet Services Pvt Ltd (AISPL): CGST+SGST in Delhi, IGST elsewhere.
- Google Cloud India Pvt Ltd: 18% regardless of GSTIN.

**Foreign providers billing from abroad** under B2B, such as Google Asia Pacific with a valid GSTIN, Lambda, CoreWeave or RunPod, don't charge GST. The Indian business self-assesses 18% IGST under reverse charge and can claim ITC.

**Withholding.** Section 195 is now Section 393(2) under the Income-tax Act 2025, from 1 Apr 2026. The Delhi High Court (2025) held that AWS cloud fees are not royalty or fees for included services under the India-US DTAA, which supports nil or low withholding for US providers. Both equalisation levies are abolished: 2% from 1 Aug 2024 and 6% from 1 Apr 2025.

### Cited Findings
- **Indian-provider GST:**
  - E2E: "Prices exclude 18% GST; GST invoices are issued." — [E2E pricing](https://www.e2enetworks.com/pricing.md)
  - IndiaAI: "All prices are exclusive of GST and other taxes." — [IndiaAI calculator](https://compute.indiaai.gov.in/indiaaipricecalculator)
- **AWS India (official tax-help page, per search snippet).** AWS India charges SGST 9% + CGST 9% to customers in Delhi and IGST 18% elsewhere. Business customers should add their GSTIN for a correct tax invoice. — [AWS tax help – India](https://aws.amazon.com/tax-help/india/)
- **AWS billing entity (reseller source).** Indian customers are billed by AISPL in INR. AISPL INR list prices can differ slightly from USD pricing, and GST-registered businesses can claim ITC. — [PrecisionTech (AWS partner)](https://precisiontech.in/cloud/amazon-aws-cloud/aws-pricing/aws-pricing-in-pune/)
- **Google Cloud.** Services sold by Google Cloud India Private Limited to Indian billing addresses carry 18% GST regardless of GSTIN. From 1 Feb 2025, India-based customers contracted with Google Asia Pacific are charged 0% GST with a valid GSTIN and 18% without. Google's page also points to India TDS rules. — [Google Cloud VAT/GST overview](https://docs.cloud.google.com/billing/docs/resources/vat-overview)
- **Azure (weak source).** A reseller claims direct Microsoft billing is in USD without Indian GST, while CSP resellers can issue INR invoices with 18% GST. — [itforsme (reseller)](https://itforsme.in/pricing/azure-india)
- **B2B imports of cloud/OIDAR services:**
  - The registered Indian recipient pays 18% IGST under reverse charge and may claim ITC. Place of supply falls under Section 13(12) of the IGST Act.
  - A foreign provider serving only B2B buyers generally doesn't need OIDAR registration. Unregistered (B2C) buyers trigger the supplier's OIDAR registration and 18% GST. — [Treelife](https://treelife.in/legal/oidar-registration-in-india/), [Xflowpay](https://www.xflowpay.com/blog/oidar-services)
  - The recipient issues a self-invoice and pays reverse-charge GST in cash; ITC is available. — [DisyTax](https://disytax.com/?p=24111)
- **Withholding (TDS) on foreign payments:**
  - From 1 April 2026, the Income-tax Act 2025 replaces section 195 with Section 393(2) (Table Sl. No. 17), and Form 144 replaces Form 27Q. — [TDSMAN blog](https://blog.tdsman.com/2026/07/tds-on-payments-to-non-residents-section-3932-section-195/), [India Briefing](https://india-briefing.com/news/section-393-income-tax-act-2025-tds-rules-rates-compliance-guide-44450.html/)
  - **Delhi High Court, CIT v. Amazon Web Services Inc (2025 DHC 4622-DB).** The court dismissed the Revenue's appeals (AY 2014-15 and 2016-17). It held that cloud-computing fees are not "equipment royalty" under Article 12(3) of the India-US DTAA, and support services don't "make available" technical knowledge under Article 12(4)(b). Absent a permanent establishment, the fees are not taxable under ss. 9(1)(vi)/(vii). — [LiveLaw](https://www.livelaw.in/amp/high-court/delhi-high-court/payments-made-to-aws-for-cloud-computing-services-not-taxable-delhi-high-court-296433), [Taxmann](https://www.taxmann.com/post/blog/cloud-services-not-taxable-as-royalty-under-india-us-dtaa-hc), [Verdictum](https://www.verdictum.in/court-updates/high-courts/delhi-high-court/the-commissioner-of-income-tax-v-amazon-web-services-inc-2025-dhc-4622-db-india-us-dtaa-1579284)
  - Earlier tribunal rulings had treated cloud and hosting payments as potential royalty, including EPRSS (ITAT Pune) and Edgeverve (ITAT Bangalore, remanded). — [itatonline EPRSS](https://itatonline.org/archives/eprss-prepaid-recharge-services-india-p-ltd-s-91vii-royalty-40ai-law-explained-on-whether-payment-of-web-hosting-charges-to-amazon-web-services-llc-usa-aws-constitutes-royalty-under/), [itatonline Edgeverve](https://itatonline.org/digest/edgeverve-systems-ltd-v-acitit-2020-182-itd-526-bang-trib/)
- **Equalisation levy:**
  - The 2% levy on e-commerce supply ended on 1 Aug 2024.
  - The 6% levy on online advertising was abolished from 1 Apr 2025 via amendments to the Finance Bill 2025. — [Deccan Herald](https://www.deccanherald.com/amp/story/business/govt-to-abolish-google-tax-amid-trumps-tariff-threat-3462385), [Business Today](https://businesstoday.in/latest/policy/story/equalisation-levy-of-6-on-online-ads-likely-to-be-scrapped-from-april-1-469169-2025-03-24), [Xflowpay](https://www.xflowpay.com/blog/equalisation-levy)

### Inferences
- **GST is cost-neutral if ITC is claimed.** For a GST-registered Indian company making taxable supplies, the 18% GST is broadly neutral whether the provider is Indian (forward charge) or foreign (reverse charge). It is a cash-flow item, not a cost. Reverse-charge GST must be paid in cash before ITC is claimed.
- **Foreign GPU clouds without a DTAA-friendly structure.** A Form 15CA/CA certificate (or the new-Act equivalent) is likely still needed per remittance. Paying from India may require a CA opinion, or withholding if the provider's treaty position is unclear; this follows from the AWS ruling being US-specific.
- **Gross-up risk.** Some US GPU clouds require gross-up clauses. If withholding were applied (e.g., at royalty rates), the effective cost could rise by the withholding percentage.

### Gaps
- **TDS on domestic cloud payments:** the applicable rate under the new Section 393 table (formerly 194C at 2% or 194J at 2%/10%) was not found in authoritative form.
- **Microsoft Azure's Indian billing entity and GST practice:** not confirmed from Microsoft sources.
- **Further appeal:** whether the Revenue appealed the Delhi HC AWS ruling to the Supreme Court is unknown.
- **New-Act withholding rates:** the exact rate in Section 393(2) for non-resident "royalty/FTS" payments was not extracted.

---

## 7. Price trend: 2024 to 2026, and outlook for 2027–2028

### Takeaway
- **2024 to late 2025: H100 fell sharply.** The hyperscaler median dropped from $9.34 (H2 2024) to $6.26 (H2 2025), about 33% (Silicon Data), and AWS cut P5 on-demand about 44% in June 2025.
- **2026: prices turned back up.** H100 is up about 17% year on year (Oct 2025 → Oct 2026), all-model prices are up about 18%, and B200 rose about 79% in three months to about $8.01 (SemiAnalysis index, late Sep 2026).
- **Causes cited:** HBM and memory shortages and sold-out Blackwell/CoWoS supply.
- **No credible quantitative 2027–2028 forecast was found.** Analysts expect the B200 premium to persist into early 2027.

### Cited Findings
- **Silicon Data H100 monthly medians:**
  - Hyperscaler: $7.92 (Jan–May 2024) → $9.34 (Jun–Dec 2024) → $8.96 (Jan–May 2025) → $6.94 (Jun 2025) → $6.26 (Jul–Dec 2025)
  - Neocloud: $2.99 (H2 2024) → $3.33 (H2 2025)
  - Marketplace: $2.58 (H2 2024) → $1.95 (H2 2025)
  - [Silicon Data H100 price history](https://www.silicondata.com/blog/h100-rental-price-over-time)
- **GetDeploying (week of 12 Oct 2026):** H100 median on-demand $3.50 across 40 providers, +17% year on year (Oct '25 → Oct '26) and +4.8% over 4 weeks. All-model index +18% year on year and +9% over 4 weeks. — [GetDeploying GPU price index](https://getdeploying.com/gpu-price-index)
- **SemiAnalysis index via Shattered:** B200 at $8.01/GPU-hr in late Sep 2026, up 79% in three months. In Sep 2026, B200 cost 21% more per unit of compute than H100, versus 18% cheaper in June 2026. — [Shattered.io](https://shattered.io/nvidia-b200-cloud-price-79-percent-surge-2026/)
- **Thunder Compute:** the mean H200 on-demand across 11 providers rose from $5.95 (5 Aug 2026) to $6.20 (16 Oct 2026), +4.2%. — [Thunder Compute H200](https://www.thundercompute.com/blog/nvidia-h200-pricing)
- **Mercatus (13 Sep 2026), 30-day change:** B300 +5.3%, B200 0.0%, H200 −0.8%, H100 −0.4%. Over 90 days, H100 rose from $3.62 to $3.84. — [Mercatus](https://www.mercatus-ai.com/blog/gpu-rental-prices)
- **Nebius raised on-demand prices 17–21%** effective 1 Oct 2026. — [UsagePricing](https://usagepricing.com/blueprint/activity/nebius-ai-2026-09-24-gpu-price-increase)
- **AWS June 2025 cuts:** P5 −44% and P5en −25% on-demand. — [AWS](https://aws.amazon.com/about-aws/whats-new/2025/06/pricing-usage-model-ec2-instances-nvidia-gpus)
- **IndiaAI's 4th tender round cut B200 by 10%** (₹323 → ₹290.7). — [Asia Business Outlook](https://www.asiabusinessoutlook.com/news/indiaai-lowers-nvidia-b200-gpu-prices-in-compute-tender-nwid-11806.html)
- **Thunder Compute's account of causes** (vendor blog):
  - A memory shortage since late 2024, with memory prices up 200–400% (TrendForce cited).
  - NVIDIA Blackwell allocation reserved through 2026 into 2027, and CoWoS sold out with relief "Q4 2026 at the earliest".
  - It gives no explicit 2027–2028 price forecast. — [Thunder Compute market trends](https://www.thundercompute.com/blog/ai-gpu-rental-market-trends)
- **Forecasts:**
  - Shattered expects the B200 premium over H100 to persist into early 2027, smaller neoclouds to raise list prices, and memory-driven pricing to apply to Rubin. — [Shattered.io](https://shattered.io/nvidia-b200-cloud-price-79-percent-surge-2026/)
  - A low-quality blog claims H100 marketplace rates will drift toward $1/hr by mid-2027. This is speculative and not from a primary analyst. — [Shattered.io H100](https://shattered.io/h100-h200-b200-cloud-gpu-pricing-2026/)

### Inferences
- **Budget for flat to rising prices through mid-2027,** not the 30–50% annual declines of 2024–25. Hopper (H100/H200) is likelier to soften first as Blackwell and Rubin capacity lands; B200 and B300 are likelier to stay tight.
- **Rupee depreciation compounds USD-priced rentals for INR budgets.** The rupee went from roughly ₹84–85 in 2024 (per eCorpIT's conversions) to about ₹95 in 2026. That is about 11–13% higher INR cost even at flat USD prices.

### Gaps
- No consistent 2024→2026 year-on-year series for H200 or B200 was found. B200 only became broadly rentable in mid-2025.
- No named-analyst quantitative forecast for 2027–2028 rental rates (SemiAnalysis, Epoch, etc.) was found.

---

## 8. Practical availability: 8×B200/B300 on-demand in India, and multi-node InfiniBand clusters

### Takeaway
On paper, 8×B200 on-demand is listed in India by:
- **AWS:** p6-b200 in Mumbai and Hyderabad at $160.65/hr, plus Capacity Blocks at $113.67.
- **E2E:** B200 ₹759/GPU-hr on-demand, but the rate card shows only 1× pricing; 8× nodes and clusters go via sales.

8×B300 on-demand is listed in India only by AWS Hyderabad: p6-b300 at $200.81/hr, or Capacity Blocks at $129.17. Yotta's B300 is reserved-only, from a 1-year term.

Google Cloud has H200 (A3 Ultra) in Mumbai and Delhi but no on-demand B200 anywhere; only spot, DWS and CUDs. Azure's only target-GPU SKU in India is GB200 v6 (South India).

Multi-node InfiniBand clusters (16–32+ GPUs):
- **Indian providers:** E2E B200 InfiniBand cluster, live June 2026; Yotta SLURM clusters with InfiniBand at extra cost; IndiaAI empanelled 8× configurations.
- **Global, short terms:** Lambda 1-Click Clusters (16+ GPUs, 2-week minimum); Together reserved (from 3 days); RunPod Instant Clusters.

### Cited Findings
- **AWS India price listings:** p6-b200 on-demand in Mumbai and Hyderabad; p6-b300 on-demand in Hyderabad; p5en/p5 in Mumbai. — [AWS price JSON Mumbai](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/Asia%20Pacific%20(Mumbai)/Linux/index.json), [Hyderabad](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/Asia%20Pacific%20(Hyderabad)/Linux/index.json)
- **AWS Capacity Blocks:** p6-b200 in Mumbai and Hyderabad; p6-b300 in Hyderabad. GB200 UltraServers only in the Dallas Local Zone. — [AWS Capacity Blocks](https://aws.amazon.com/ec2/capacityblocks/pricing/)
- **GCP:**
  - A3 Ultra (H200) is in asia-south1-b and asia-south2-c, and G4 (RTX PRO 6000) is in asia-south2-c. No India A4 zone appears in cached copies of the docs. — [GCP GPU regions](https://docs.cloud.google.com/compute/docs/gpus/gpu-regions-zones)
  - A4 has no on-demand price; only DWS, spot and CUD. — [GCP pricing](https://cloud.google.com/products/compute/pricing/accelerator-optimized?hl=en)
  - Spare Cores shows an A4 spot price in Delhi, which conflicts with the docs. — [Spare Cores](https://sparecores.com/server/gcp/a4-highgpu-8g)
- **Azure:** the only India ND SKUs priced are GB200 v6 (South India) and A100 v4. — [Azure Retail Prices API](https://prices.azure.com/api/retail/prices)
- **OCI:** H100 and H200 bare-metal shapes listed in Mumbai and Hyderabad (third-party). — [Northflank](https://northflank.com/cloud/oci/instances/BM.GPU.H200.8)
- **E2E:** B200 cluster live 1 June 2026 with InfiniBand; about 5,100 GPUs. — [E2E blog](https://www.e2enetworks.com/blog/b200-live-blog), [Inc42](https://inc42.com/buzz/e2e-networks-reports-₹44-cr-profit-in-q1-revenue-zooms-3-3x-yoy/)
- **Yotta:**
  - B200 bare metal from monthly terms (₹473); B300 only from 1-yr (₹1,056). — [Yotta bare metal](https://shakticloud.ai/bare-metal-service/)
  - SLURM cluster 8×H100 at ₹386/GPU-hr; InfiniBand ₹16,060/GPU extra; management fee ₹4.5–11.25 lakh per cluster. — [Yotta pricing](https://shakticloud.ai/pricing)
- **IndiaAI:** B200SXM.8x and B300SXM.8x are offered on-demand through empanelled providers, approval required. — [IndiaAI calculator](https://compute.indiaai.gov.in/indiaaipricecalculator)
- **Global cluster options:**

| Provider | Offer | Source |
|---|---|---|
| Lambda 1-Click Clusters | 16–2,000+ GPUs; 2 weeks to 1 year; B200 $9.86/GPU-hr at 16 GPUs | [Lambda](https://lambda.ai/pricing) |
| Together | Reserved from 3–30 days; B200 $7.99, H200 $4.99 | [Together](https://www.together.ai/pricing) |
| RunPod | Instant Cluster H200 $6.35; reserved clusters 1–12 months by quote | [RunPod](https://www.runpod.io/pricing) |
| Jarvislabs | H200 InfiniBand clusters and 25+ GPUs by sales | [Jarvislabs](https://jarvislabs.ai/pricing) |
| CoreWeave | GB200 NVL72 at $10.50/GPU-hr on-demand (4-GPU instances) | [CoreWeave](https://www.coreweave.com/pricing) |

- **Stock snapshots (18–19 Oct 2026):**
  - Lambda B200 (8×) out of stock.
  - RunPod B200 Secure (1×) in stock; Community out of stock.
  - Vultr B200 spot out of stock.
  - For B300, the cheapest verified in-stock on-demand was $7.99 (UpCloud). Many B300 8× listings are out of stock or pre-order.
  - [GetDeploying B200](https://getdeploying.com/gpus/nvidia-b200), [GetDeploying B300](https://getdeploying.com/gpus/nvidia-b300)
- **Supply:** B200 and B300 are "extremely limited". Most Blackwell allocation is reserved by hyperscalers through 2026 into 2027 (vendor blog). — [Thunder Compute](https://www.thundercompute.com/blog/ai-gpu-rental-market-trends)

### Inferences
- **8×B200 on-demand in India.** The realistic options are AWS Mumbai or Hyderabad, at about 2.6× E2E's list per GPU-hour and subject to quota, or E2E via sales. A 16–32 GPU B200 InfiniBand cluster in India means E2E or Yotta under a monthly-or-longer contract.
- **8×B300 in India.** It is effectively reserved-only except AWS Hyderabad. AWS on-demand there is about $25.10/GPU-hr (≈ ₹2,389). Capacity Blocks are $16.15 (≈ ₹1,537). Yotta's 1-yr rate is ₹1,056. IndiaAI is ₹351 for eligible users.
- **Data residency.** If India residency isn't required, US neoclouds (Lambda, Together, Nebius, CoreWeave) offer 16–64 GPU B200/H200 clusters on 3-day to 2-week minimums. Their rates are about ₹600–940/GPU-hr for B200 at ₹95.18/USD. Network latency from Pune to US/EU regions would need separate measurement.

### Gaps
- **No live capacity check in India:** I couldn't confirm real-time capacity or quota for AWS p6 or GCP A3 Ultra in India regions, nor E2E's 8× B200 lead time. That requires console or sales checks.
- **E2E and Yotta cluster terms:** minimum cluster sizes and terms are not published.
- **Pune to US/EU latency:** latency figures for remote neocloud serving were not researched.

---

## Consolidated rental price table

### Takeaway
All rows were read from provider pages, provider price APIs or price files, or aggregators, between 2026-10-15 and 2026-10-19 unless a different date is given.
- **Conversions:** per-GPU figures derived from node prices are rounded. INR equivalents (not shown) use ₹95.18/USD.
- **Tax notes:**
  - "GST 18% extra" means the price excludes GST and an Indian supplier adds it.
  - "RCM" means a foreign B2B supplier; the buyer self-assesses 18% IGST under reverse charge.
  - "Fwd GST (Indian entity)" means the hyperscaler's Indian entity charges 18% on the invoice.
- **Reserved columns:** "—" means not published.

### Cited Findings

**Hyperscalers**

| provider | region | GPU | unit | on_demand_price | reserved_1yr | reserved_3yr | currency | GST/tax note | availability note | source | date |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AWS p5en.48xlarge | Mumbai (ap-south-1) | 8×H200 | node-hr (per GPU) | 75.96 (9.49) | 47.85 (5.98) EC2 ISP NU | 32.81 (4.10) EC2 ISP NU | USD | Fwd GST (AISPL) | Listed; quota needed; Capacity Block 63.16 | [AWS JSON](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/Asia%20Pacific%20(Mumbai)/Linux/index.json), [SP](https://pricing.us-east-1.amazonaws.com/savingsPlan/v1.0/aws/AWSComputeSavingsPlan/20261013035015/ap-south-1/index.json) | 2026-10-15 / 2026-10-13 |
| AWS p5en.48xlarge | N. Virginia | 8×H200 | node-hr | 63.30 (7.91) | — | — | USD | Fwd GST (AISPL) | Ref. US price | [AWS JSON](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/US%20East%20(N.%20Virginia)/Linux/index.json) | 2026-10-15 |
| AWS p6-b200.48xlarge | Mumbai and Hyderabad | 8×B200 | node-hr | 160.65 (20.08) | Compute SP 126.51 (15.81); no 1-yr EC2 ISP | 69.40 (8.68) EC2 ISP NU | USD | Fwd GST (AISPL) | Listed on-demand; Capacity Block 113.67 (14.21) | [AWS JSON](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/Asia%20Pacific%20(Mumbai)/Linux/index.json), [CB](https://aws.amazon.com/ec2/capacityblocks/pricing/) | 2026-10-15 / 2026-10-19 |
| AWS p6-b300.48xlarge | Hyderabad (ap-south-2) | 8×B300 | node-hr | 200.81 (25.10) | Compute SP 158.14 (19.77) | 86.75 (10.84) EC2 ISP NU | USD | Fwd GST (AISPL) | Only India B300 on-demand listing; Capacity Block 129.17 (16.15) | [AWS JSON](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/Asia%20Pacific%20(Hyderabad)/Linux/index.json), [SP](https://pricing.us-east-1.amazonaws.com/savingsPlan/v1.0/aws/AWSComputeSavingsPlan/20261013035015/ap-south-2/index.json) | 2026-10-15 / 2026-10-13 |
| AWS u-p6e-gb200x72 | US East Dallas Local Zone | 72×GB200 | UltraServer-hr (per GPU) | Capacity Block only: 761.90 (10.58) | — | — | USD | Fwd GST (AISPL) | Not in India | [AWS CB](https://aws.amazon.com/ec2/capacityblocks/pricing/) | 2026-10-19 |
| AWS p5.48xlarge | Mumbai | 8×H100 | node-hr | 66.05 (8.26) | 41.61 (5.20) | 28.53 (3.57) | USD | Fwd GST (AISPL) | Listed | [AWS JSON](https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/Asia%20Pacific%20(Mumbai)/Linux/index.json) | 2026-10-15 |
| AWS g7e.48xlarge | Mumbai | 8×RTX PRO 6000 | node-hr | 54.14 (6.77) | 34.11 (4.26) | 23.39 (2.92) | USD | Fwd GST (AISPL) | Listed | same | 2026-10-15 |
| AWS g6e.48xlarge | Mumbai | 8×L40S | node-hr | 36.19 (4.52) | 22.80 (2.85) | 15.63 (1.95) | USD | Fwd GST (AISPL) | Listed | same | 2026-10-15 |
| GCP a3-ultragpu-8g | Mumbai (asia-south1) | 8×H200 | node-hr | 101.77 (12.72) | — (us-central1: 58.47) | — (us-central1: 37.21) | USD | Fwd GST if Google Cloud India Pvt Ltd; 0% with GSTIN if Google Asia Pacific | Also in Delhi; spot 54.72 | [Spare Cores](https://sparecores.com/server/gcp/a3-ultragpu-8g), [GCP](https://cloud.google.com/products/compute/pricing/accelerator-optimized?hl=en) | 2026-10-19 |
| GCP a3-ultragpu-8g | us-central1 | 8×H200 | node-hr | 84.81 (10.60) | 58.47 (7.31) CUD | 37.21 (4.65) CUD | USD | as above | DWS Flex 42.40; Calendar 59.36 | [GCP](https://cloud.google.com/products/compute/pricing/accelerator-optimized?hl=en) | 2026-10-19 |
| GCP a4-highgpu-8g | us-central1 | 8×B200 | node-hr | No on-demand; DWS Flex 64.44 (8.06); spot 39.63 | 88.93 (11.12) CUD | 56.71 (7.09) CUD | USD | as above | No India on-demand; Delhi spot listing unverified | [GCP](https://cloud.google.com/products/compute/pricing/accelerator-optimized?hl=en) | 2026-10-19 |
| GCP g4-standard-384 | us-central1 | 8×RTX PRO 6000 | node-hr | 36.00 (4.50) | 24.84 (3.11) | 15.84 (1.98) | USD | as above | G4 also in Delhi (asia-south2-c) | [GCP](https://cloud.google.com/products/compute/pricing/accelerator-optimized?hl=en) | 2026-10-19 |
| Azure ND96isr_H200_v5 | East US 2 | 8×H200 | VM-hr | 84.80 (10.60) | ~46.52 (5.82) | ~42.22 (5.28) | USD | RCM if billed from abroad; Fwd GST via Indian CSP (unverified) | Not in India | [Azure API](https://prices.azure.com/api/retail/prices) | 2026-10-19 |
| Azure ND128isr_NDR_GB200_v6 | South India | 4×GB200 | VM-hr | 163.32 (40.83) | ~104.52 (26.13) | ~71.86 (17.97) | USD | as above | Only target-GPU SKU priced in India | [Azure API](https://prices.azure.com/api/retail/prices) | 2026-10-19 |
| Azure ND96isr_MI300X_v5 | East US 2 | 8×MI300X | VM-hr | 48.00 (6.00) | ~30.72 (3.84) | ~21.07 (2.63) | USD | as above | Not in India; spot 8.87 | [Azure API](https://prices.azure.com/api/retail/prices) | 2026-10-19 |
| OCI BM.GPU.H200.8 | All regions (uniform list) | H200 | GPU-hr | 10.00 (₹955.45) | — | — | USD/INR | INR list via Oracle India (GST treatment not verified) | Mumbai/Hyderabad per Northflank | [OCI API](https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/?currencyCode=USD) | 2026-10-19 |
| OCI B200 / B300 / GB200 / GB300 | Uniform | B200 / B300 / GB200 / GB300 | GPU-hr | 14.00 / 15.00 / 16.00 / 18.00 | — | — | USD | as above | India availability unverified | [OCI API](https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/?currencyCode=USD) | 2026-10-19 |
| OCI MI300X / MI355X | Uniform | MI300X / MI355X | GPU-hr | 6.00 / 8.60 | — | — | USD | as above | India availability unverified | [OCI API](https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/?currencyCode=USD) | 2026-10-19 |

**Neoclouds and marketplaces**

| provider | region | GPU | unit | on_demand_price | reserved_1yr | reserved_3yr | currency | GST/tax note | availability note | source | date |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CoreWeave | North America | 8×B200 / 8×H200 / GB200 (4/inst) | GPU-hr | 8.60 / 6.31 / 10.50 | Up to 60% off (quote) | Quote | USD | RCM | B300 and GB300: contact sales | [CoreWeave](https://www.coreweave.com/pricing) | 2026-10-19 |
| Lambda | US | 8×B200 / 8×H100 | GPU-hr | 6.69 / 3.99 | Clusters (2 weeks–1 year): B200 9.86 (16 GPUs) to 8.87 (256+) | Contact | USD | RCM | B200 8× out of stock 18–19 Oct | [Lambda](https://lambda.ai/pricing) | 2026-10-19 |
| Nebius | EU/US | B300 / B200 / H200 / H100 | GPU-hr | 9.50 / 8.50 / 5.40 / 4.50 | Up to 35% off (quote) | Quote | USD | RCM | +17–21% from 1 Oct 2026 | [Nebius](https://nebius.com/prices) | 2026-10-19 |
| Crusoe | US/EU | B200 / H200 / MI300X | GPU-hr | 8.50 / 5.40 / 3.45 | Contact | Contact | USD | RCM | MI355X and GB200: contact | [Crusoe](https://www.crusoe.ai/cloud/pricing) | 2026-10-19 |
| Together AI | US | B300 / B200 / H200 | GPU-hr | 9.99 / 8.19 / 5.99 | B200 6.79 / H200 3.99 (91–180 days); 181+ days: contact | Contact | USD | RCM | GB200/GB300 reserved only | [Together](https://www.together.ai/pricing) | 2026-10-19 |
| RunPod Secure | Global | B300 / B200 / H200 | GPU-hr | 8.99 / 7.99 / 5.29 | Contact | Contact | USD | RCM | Community: 6.94 / 5.98 / 3.59 | [RunPod](https://www.runpod.io/pricing) | 2026-10-19 |
| Vast.ai | Global marketplace | H200 / B200 / B300 | GPU-hr (median) | 4.61 / 9.00 / 9.92 | — | — | USD | RCM | Few 8× offers; no India B200 | [Vast API](https://console.vast.ai/api/v0/bundles/) | 2026-10-19 |
| Hyperbolic | US | H200 / B200 | GPU-hr | 3.99 / 5.99 | Quote | Quote | USD | RCM | Aggregator data | [Thunder](https://www.thundercompute.com/blog/nvidia-h200-pricing), [ComputePrices](https://computeprices.com/providers/hyperbolic/gpus/b200) | 2026-10-16 / Aug–Sep 2026 |
| DigitalOcean | US | H200 / MI300X / MI325X | GPU-hr | 4.47 / 2.59 / 3.80 | 3.40 / 1.91 / 2.88 (12 months) | — | USD | RCM | B300 reserved 7.94; MI355X spot 5.50 | [DigitalOcean](https://www.digitalocean.com/pricing/gpu-droplets) | 2026-10-19 |
| Hot Aisle | US | MI300X | GPU-hr | 2.99 (VM) / 3.39 (8× bare metal) | — | — | USD | RCM | MI355X not priced | [Hot Aisle](https://hotaisle.xyz/pricing/) | 2026-10-19 |
| TensorWave | US | MI355X / MI300X | GPU-hr | Contract: from 2.95 / from 1.71 | Quote | Quote | USD | RCM | Own page 404; aggregator | [GetDeploying](https://getdeploying.com/gpus/amd-mi355x) | 2026-08-31 check |
| Vultr | Global | MI355X / B200 / MI300X | GPU-hr | Spot: 2.59 / 3.20; MI300X preemptible 1.85 | MI300X: 1.75 (24-month prepay) | — | USD | RCM | Out of stock (B200, MI355X) | [GetDeploying B200](https://getdeploying.com/gpus/nvidia-b200), [Spheron AMD](https://www.spheron.network/blog/amd-mi300x-mi355x-pricing-2026/) | 2026-10-19 / Aug 2026 |
| Jarvislabs | India (Noida) / other | H200 / H100 / RTX PRO 6000 | GPU-hr | 4.59 / 3.49 / 2.19 | −9% (1 year) | — | USD (INR toggle) | GST 18% if Indian billing (not stated) | H200 also cited at 3.99 elsewhere | [Jarvislabs](https://jarvislabs.ai/pricing) | 2026-10-19 |

**Indian providers and IndiaAI**

| provider | region | GPU | unit | on_demand_price | reserved_1yr | reserved_3yr | currency | GST/tax note | availability note | source | date |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E2E Networks | Delhi NCR / Chennai | B200 | GPU-hr | 759.05 | 683.05 (committed, term n/s) | — | INR | GST 18% extra | B200 IB cluster live Jun 2026; 8× via sales | [E2E](https://www.e2enetworks.com/pricing.md) | 2026-10-16 |
| E2E Networks | Delhi NCR / Chennai | H200 | GPU-hr | 502.55 | 462.65 (committed) | — | INR | GST 18% extra | Spot ₹88 | [E2E](https://www.e2enetworks.com/pricing.md) | 2026-10-16 |
| E2E Networks | Delhi NCR / Chennai | RTX PRO 6000 / H100 / L40S | GPU-hr | 236.55 / 379.05 / 102 | 217.55 / 347.70 / — | — | INR | GST 18% extra | 1× listed | [E2E](https://www.e2enetworks.com/pricing.md) | 2026-10-16 |
| Yotta Shakti Cloud | Navi Mumbai / Greater Noida | 8×B200 bare metal | GPU-hr | No on-demand; monthly 473 | 473 | 378 (4-yr 316) | INR | GST not stated (expect 18% extra) | Data transfer incl.; IB extra; possibly stale | [Yotta BM](https://shakticloud.ai/bare-metal-service/) | Accessed 2026-10-19 |
| Yotta Shakti Cloud | same | 8×B300 bare metal | GPU-hr | Not offered | 1,056 | 672 (4-yr 480) | INR | as above | Reserved-only | [Yotta BM](https://shakticloud.ai/bare-metal-service/) | Accessed 2026-10-19 |
| Yotta Shakti Cloud | same | 8×H100 bare metal / cluster | GPU-hr | Monthly 351; SLURM cluster 386 | 263 | — | INR | as above | IB ₹16,060/GPU extra | [Yotta](https://shakticloud.ai/pricing) | Accessed 2026-10-19 |
| Tata Comm. Vayu | India | 8×H200 SXM bare metal | node-hr (per GPU) | 4,247 (531) | 3,256 (407) | 3,085 (386) | INR | GST not stated (expect 18% extra) | No B200/B300 | [Tata PDF](https://www.tatacommunications.com/hubfs/library/documents/Tata%20Communications%20Vayu%20AI%20Cloud%20GPU%20as%20a%20Service.pdf) | 2026-02-02 (stale) |
| Tata Comm. Vayu | India | 8×H100 SXM bare metal | node-hr | 3,905 (488) | 2,994 | 2,836 | INR | as above | — | same | 2026-02-02 (stale) |
| Neysa Velocis | India | 8×H200 / 8×MI300X / 8×H100 | node-month (36-mo term) | H200 from 4.72/GPU-hr | Flat 1–36 months | 13,810.58 / 12,981.96 / 12,422.59 per month (≈2.37 / 2.22 / 2.13 per GPU-hr) | USD | GST not stated | B300 on request; B200 not listed | [Neysa](https://neysa.ai/pricing) | 2026-10-19 |
| Ola Krutrim | India | H100 | GPU-hr | 213 | 173 | — | INR | GST not stated | No H200/B200 | [Krutrim](https://docs.cloud.olakrutrim.com/basics/pricing/cpu-and-gpu) | Accessed 2026-10-19 |
| IndiaAI (empanelled) | India | 8×B200 SXM | node-hr (per GPU) | 2,325.6 (290.7) | 2,008.8 (12-mo) | — | INR | Excl. GST; up to 40% subsidy | Eligibility-gated; monthly approval cycle | [IndiaAI calc](https://compute.indiaai.gov.in/indiaaipricecalculator) | 2026-10-14 |
| IndiaAI (empanelled) | India | 8×B300 SXM | node-hr | 2,808 (351) | 2,556 (12-mo) | — | INR | as above | as above | same | 2026-10-14 |
| IndiaAI (empanelled) | India | 8×H200 SXM | node-hr | 1,125 (140.6) | 785 (12-mo) | — | INR | as above | 2×/4× rows inconsistent | same | 2026-10-14 |
| IndiaAI (empanelled) | India | 8×MI300X / 8×MI325X | node-hr | 1,416.5 / 1,351.8 | 1,336 / 684 | — | INR | as above | as above | same | 2026-10-14 |
| IndiaAI (empanelled) | India | 8×H100 SXM / 8×RTX PRO 6000 / 8×L40S | node-hr | 1,224 / 916.8 / 540 | 936 / 792 / 360 | — | INR | as above | as above | same | 2026-10-14 |

### Inferences
- **India-resident 8×B200 serving, 24/7, cheapest to dearest** (pre-GST, per GPU-hr):

| Route | ₹/GPU-hr | ≈ ₹ lakh/month (8 GPUs) |
|---|---|---|
| IndiaAI 12-month, if eligible | 251 | 14.7 |
| Yotta 3-yr | 378 | 22.1 |
| Yotta monthly | 473 | 27.6 |
| E2E committed | 683 | 39.9 |
| E2E on-demand | 759 | 44.3 |
| AWS Mumbai 3-yr EC2 ISP | ≈ 826 | 48.2 |
| AWS Capacity Block | ≈ 1,352 | 79.0 |
| AWS on-demand | ≈ 1,911 | 111.6 |

- **India-resident 8×H200 serving, 24/7, cheapest to dearest:**

| Route | Rate | ≈ ₹ lakh/month (8 GPUs) |
|---|---|---|
| IndiaAI 12-month | ₹98/GPU-hr | 5.7 |
| Neysa 36-month | ≈ ₹225/GPU-hr | 13.1 |
| Tata 3-yr | ₹386/GPU-hr | 22.5 |
| AWS Mumbai 3-yr | ≈ ₹390/GPU-hr | 22.8 |
| E2E committed | ₹463/GPU-hr | 27.0 |
| E2E on-demand | ₹503/GPU-hr | 29.3 |
| Tata on-demand | ₹531/GPU-hr | 31.0 |
| GCP Mumbai on-demand | ≈ ₹1,211/GPU-hr | 70.7 |

- **Business hours (220 h)** apply only to the on-demand rows. E2E 8×B200 on-demand would be about ₹13.4 lakh/month, and E2E 8×H200 about ₹8.8 lakh/month.

### Gaps
- **Unpublished Indian reserved rates:** E2E's "committed" term length, and Yotta and Tata GST treatment.
- **Missing provider data:** India-region GCP CUD rates, and OCI India GPU capacity.
- **Live availability:** see the Gaps in sections 1–8.
