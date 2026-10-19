# India Import Duty, GST, ITC, Depreciation and Incentives for an On-Prem AI Cluster (Stark Digital, Pune, as of 19 Oct 2026)

Scope: Pune (Maharashtra) private IT-services company, GST-registered, importing or buying GPU servers and datacenter equipment. All rates are as of October 2026 unless marked. **[CHANGED 2025]** and **[CHANGED 2026]** tags mark rule changes. "Primary" means a government document (Budget TRU letter, gazette notification, CBIC/ICAI notification copy). "Commentary" means a Big-4, law-firm, blog or tool site.

Formula used throughout (customs law structure, per the Budget TRU letters cited below):
- Assessable value (AV) = CIF in INR (transaction value + freight + insurance to the Indian port/airport). The notional 1% landing charge no longer applies (see Q3).
- BCD = AV x BCD%. AIDC = AV x AIDC% (only on specific goods). SWS = 10% of BCD (nil where exempt).
- IGST = 18% x (AV + BCD + AIDC + SWS).
- "Landed tax %" = (BCD + AIDC + SWS + IGST) / AV. "Non-recoverable % with ITC" = (BCD + AIDC + SWS) / AV, because only the IGST is creditable.

---

## Q1. Duty and IGST by HS code (BCD, SWS, AIDC, IGST, exemptions)

### Takeaway
Complete servers (8471 41/49/50), storage units (8471 70), GPU boards, memory and other computer parts (8473 30) and ICs (8542 31) carry **0% BCD (ITA-1 items), so SWS is nil and only 18% IGST is payable**. The whole 18% is recoverable as ITC. Datacenter infrastructure is dutiable:
- Ethernet switches: 10% BCD. **[CHANGED 2025]** for carrier-grade switches.
- Routers and other 8517 62 90 items: 20% tariff BCD.
- UPS (8504 40): 20% tariff, or 0% if the ITA exemption is accepted. CESTAT rulings in 2024–2026 favour importers.
- Lithium-ion batteries: 20% BCD.
- VRLA batteries: 15% BCD.
- Precision air conditioning (8415): 20% BCD.
- Chillers (8418 69): 15% BCD.
- DG sets: 7.5–10% BCD.
- Fire extinguishers: 7.5% BCD.
- Furniture-type racks (9403): 20% BCD + 5% AIDC with SWS nil. **[CHANGED 2025]**

All of these goods carry 18% IGST/GST.

### Cited Findings

**Rate data source used for 8-digit BCD.** EximPe's HSN finder says it sources "CBIC + ICEGATE · Duty & GST rates as at May 13, 2026". It shows the tariff or standard BCD for each 8-digit item and IGST under Schedule II of Notification 09/2025-Integrated Tax (Rate) — [EximPe 84714900](https://eximpe.com/hsncode-finder/84714900). Note: EximPe's calculator shows an "AIDC" equal to the BCD % on every line (for example "AIDC 20%" on switches). This contradicts the Budget TRU letters, which levy AIDC only on specified goods. Treat it as a tool artifact; the AIDC figures below come from the TRU letters, not EximPe.

**Computers and parts (ITA-1 items)**
- 8471 41 10 (micro computer), 8471 41 90, 8471 49 00 ("presented in the form of systems"), 8471 50 00 (processing units), 8471 70 20 (hard disc drives) and 8471 70 90 (other storage units, e.g. SSD/NVMe arrays): **BCD 0%, SWS nil, IGST 18%, total 18%** — [EximPe 84714900](https://eximpe.com/hsncode-finder/84714900); same stack on [84715000](https://eximpe.com/hsncode-finder/84715000), [84717020](https://eximpe.com/hsncode-finder/84717020) and [84717090](https://eximpe.com/hsncode-finder/84717090).
- The 6-digit page for 8471 41 shows "Basic Customs Duty Free", meaning a "Free" tariff rate in the First Schedule — [EximPe 847141](https://eximpe.com/hsncode-finder/847141).
- 8473 30 10 (microprocessors), 8473 30 20 (motherboards), 8473 30 30 (other mounted PCBs, the usual heading for GPU accelerator boards/modules) and 8473 30 99: **BCD 0%, IGST 18%** — [EximPe 84733030](https://eximpe.com/hsncode-finder/84733030), [84733099](https://eximpe.com/hsncode-finder/84733099).
- 8542 31 00 (processors/controllers ICs, i.e. bare GPU/CPU chips): **BCD 0%, IGST 18%** — [EximPe 85423100](https://eximpe.com/hsncode-finder/85423100).
- ITA-1 legal basis: Notification 24/2005-Customs (1 Mar 2005) exempts listed ITA goods, including "8471" and "8473 30", "from the whole of the duty of customs" — [Taxguru copy of 24/2005](https://taxguru.in/custom-duty/notification-242005customs-duty-dated-01032005.html); [India Budget archive copy](https://www.indiabudget.gov.in/budget_archive/ub2005-06/cen/cus2405.pdf).
- Commentary on classification: complete DGX/HGX-class systems are usually declared under 8471 49 or 8471 50. GPU modules or HGX baseboards imported alone go under 8473 30. 0% BCD under ITA-1 is "typical", but specific configurations should be checked — [Carra Globe H200 guide](https://carraglobe.com/importing-nvidia-h200-servers/). This is commentary, not law.

**Network equipment**
- **[CHANGED 2025]** The Budget 2025 TRU letter says: "BCD is being reduced from 20% to 10% on Ethernet Switches - Carrier grade classified under tariff item 8517 62 90, 8517 69 90 [S. No 20 of Notification No. 57/2017-Customs ... as amended by Notification No.10/2025-Customs, dated 1st February, 2025]" (Primary) — [TRU letter, Budget 2025-26](https://www.indiabudget.gov.in/budget2025-26/doc/cen/dojstru1.pdf).
- India Briefing (5 Feb 2025) says the cut "aligns them with non-carrier-grade switches to prevent classification disputes". So non-carrier-grade datacenter/enterprise Ethernet switches were already at 10% — [India Briefing](https://www.india-briefing.com/news/india-revises-customs-tariff-under-union-budget-2025-26-36054.html/).
- The 8517 62 90 tariff (standard) rate is shown as **20%**. That rate applies to "other" reception/conversion/transmission apparatus not covered by the 10% switch entry, which in practice may include routers — [EximPe 85176290](https://eximpe.com/hsncode-finder/85176290); [Cusbuzz/Proactive summary in search: "up to 20%"](https://proactive.co.in/blog-details/hsn-gst-cisco-hardware-india).
- 2022 baseline: Notification 57/2017 S. No. 20 gave 10% to a specified list including carrier Ethernet switches, packet transport and MPLS-TP products, with others at 20% (MAIT representation to DoT on non-carrier Ethernet switches, PoE switches and transceivers) — [MAIT 2022](https://www.mait.com/uploads/publication_document/6c4b761a28b734fe93831e3fb400ce8719092022%20%e2%80%93%20Representation%20to%20Shri%20R%20K%20Pathak,%20DDG%20(IC),%20DoT%20reg.%20addendum%20to%20Technical%20write-up%20on%20non-carrier%20ethernet%20switches,%20POE%20switches,%20and%20Transceivers.pdf). This framing conflicts with India Briefing on which category sat at 10% before 2025. Both agree **all Ethernet switches are at 10% from 2 Feb 2025**.
- 8517 79 90 (parts of 8517 apparatus; one possible heading for optical transceivers/modules): **BCD 15%**. 8517 79 10 (populated PCBs of telecom apparatus): **BCD 20%** — [EximPe 85177990](https://eximpe.com/hsncode-finder/85177990), [85177910](https://eximpe.com/hsncode-finder/85177910).
- 8544 70 10 / 8544 70 90 (optical fibre cables): **BCD 0%**, IGST 18% — [EximPe 85447090](https://eximpe.com/hsncode-finder/85447090).
- 8544 42 20 / 8544 42 99 (insulated conductors fitted with connectors, ≤1,000 V; DAC/copper patch cables): **BCD 15%** — [EximPe 85444299](https://eximpe.com/hsncode-finder/85444299).

**Racks and enclosures**
- **[CHANGED 2025]** Heading 9403 ("Other furniture and parts thereof"): tariff cut from 25% to 20% (effective 1 May 2025). From 2 Feb 2025 these goods attract "20% BCD + 5% AIDC. SWS is being exempted" [S. No. 32 of Notification 4/2025-Customs; S. No. 16D of Notification 6/2025-Customs (AIDC); S. No. I(iv) of Notification 7/2025-Customs] (Primary) — [TRU letter, Budget 2025-26](https://www.indiabudget.gov.in/budget2025-26/doc/cen/dojstru1.pdf).
- Notification 07/2025-Customs (1 Feb 2025) amended SWS exemption Notification 11/2018-Customs to insert "9401, 9403, 9404, 9405" in the SWS-exempt list, effective 2 Feb 2025 (Primary) — [Notification 07/2025-Customs](https://www.indiabudget.gov.in/doc/cen/cus0725.pdf). EximPe shows 9403 20 90 BCD at 20% — [EximPe 94032090](https://eximpe.com/hsncode-finder/94032090).
- 7308 90 90 (steel structures/parts, if the rack or cage is classified as a structure): **BCD 15%** — [EximPe 73089090](https://eximpe.com/hsncode-finder/73089090).
- 8538 10 90 (parts for switchgear boards/cabinets of 8537): **BCD 7.5%**. 8538 90 00: **BCD 15%** — [EximPe 85381090](https://eximpe.com/hsncode-finder/85381090), [85389000](https://eximpe.com/hsncode-finder/85389000).

**Power: UPS and batteries**
- 8504 40 10 (electric inverter), 8504 40 40 and 8504 40 90 (other static converters; UPS is usually declared under 8504 40 10 or 40 90): **tariff BCD 20%** — [EximPe 85044090](https://eximpe.com/hsncode-finder/85044090), [85044010](https://eximpe.com/hsncode-finder/85044010).
- ITA exemption for UPS: Notification 25/2005-Customs (1 Mar 2005), S. No. 4, covers "static converters" of 8504 40 for ADP machines and telecom apparatus. Customs has disputed whether UPS qualify — [CESTAT Mumbai order](https://cestat.gov.in/weborders/file/mumbai/417807); [TaxTMI on Chennai CESTAT, Apr 2024](https://www.taxtmi.com/tmi_blog_details?id=870055).
  - Two Tribunal final orders treat UPS as eligible: Cyber Power System India (CESTAT Kolkata, Final Order 75186/2024, 31 Jan 2024) and Prostarm Info Systems (CESTAT, Final Order A/85259-85260/2025, 22 Jan 2025).
  - In Commissioner of Customs (NS-V) v. Intex Technologies (CESTAT Mumbai, reported 4 Sep 2026), Revenue withdrew five appeals against Nhava Sheva orders dated 29 Jul 2025 involving Intex, Dynamic Conglomerate, Prostarm, Vertiv and Cyber Power. Revenue accepted that the UPS eligibility issue under S. No. 4 was settled in favour of importers — [Taxguru](https://taxguru.in/custom-duty/revenue-withdraws-ups-customs-exemption-appeals-issue-settled-cestat-mumbai.html).
  - Contrary older authority: Madras HC, Socomec UPS (2015) — [CESTAT order citing it](https://cestat.gov.in/weborders/file/mumbai/509903).
- 8507 60 00 (lithium-ion accumulators): **BCD 20%**. 8507 20 00 (other lead-acid, i.e. VRLA): **BCD 15%** — [EximPe 8507 heading guide](https://eximpe.com/hsn/battery-hsn-code); [EximPe 85076000](https://eximpe.com/hsncode-finder/85076000). Older aggregators show 10%. Seair's page still shows pre-2017 education cess, so it is stale — [Seair](https://www.seair.co.in/custom-duty/hs-code-85076000.aspx).
- **[CHANGED 2026]** Budget 2026 extended the BCD exemption on capital goods for Li-ion cell manufacturing to BESS batteries (Notification 01/2026-Customs, S. No. 5, from 2 Feb 2026). This is for manufacturers, not for importing finished batteries (Primary) — [TRU letter, Budget 2026-27](https://www.indiabudget.gov.in/doc/cen/dojstru1.pdf).

**Cooling**
- 8415 10 10, 8415 81 10, 8415 82 10 and 8415 82 90 (air-conditioning machines, including split/precision units): **BCD 20%** — [EximPe 84158210](https://eximpe.com/hsncode-finder/84158210), [84158290](https://eximpe.com/hsncode-finder/84158290).
- **[CHANGED 2026]** AC parts under 8415 90 (other than indoor/outdoor units of split systems) move to new tariff item 8415 90 90 at 10% in the First Schedule from 1 May 2026, with "no change in the applicable rate of duty" (Primary) — [TRU letter, Budget 2026-27](https://www.indiabudget.gov.in/doc/cen/dojstru1.pdf).
- 8418 69 10 and 8418 69 90 (other refrigerating equipment; process/chiller units): **BCD 15%** — [EximPe 84186990](https://eximpe.com/hsncode-finder/84186990).

**Generators and fire**
- 8502 11 00 (diesel generating sets ≤75 kVA): **BCD 10%**. 8502 12 00 (75–375 kVA) and 8502 13 xx (>375 kVA): **BCD 7.5%** — [EximPe 85021100](https://eximpe.com/hsncode-finder/85021100), [85021200](https://eximpe.com/hsncode-finder/85021200), [85021310](https://eximpe.com/hsncode-finder/85021310).
- 8424 10 00 (fire extinguishers, whether or not charged; clean-agent cylinder systems are commonly declared here): **BCD 7.5%** — [EximPe 84241000](https://eximpe.com/hsncode-finder/84241000).

**IGST on all of the above**
- All of these headings sit in **Schedule II (9% CGST, i.e. 18% GST/IGST)** of Notification 9/2025-Central Tax (Rate) dated 17 Sep 2025, effective 22 Sep 2025 (Primary, ICAI-updated copy):
  - S. No. 286 (7308), 404 (8415), 407 (8418), 413 (8424, fire extinguishers), 456 (8471), 458 (8473), 475 (8502), 477 (8504, other than EV chargers), 480 (8507).
  - S. No. 490 (8517, "All goods"), 508 (8536), 509 (8537), 510 (8538), 514 (8542), 516 (8544), 612 (9403, other furniture).
  - Source: [Notification 9/2025-CT(Rate), ICAI copy](https://d23z1tp9il9etb.cloudfront.net/download/gstlaw/NOTIFICATION%20NO.%209_2025-CENTRAL%20TAX%20(RATE)1759486688.pdf).
- IGST on imports applies under the parallel Notification 09/2025-Integrated Tax (Rate) — [EximPe 8471](https://eximpe.com/hsncode-finder/8471).

**AIDC and SWS**
- AIDC is levied under Section 124 of the Finance Act 2021, and SWS under Section 110 of the Finance Act 2018 (Primary) — [TRU letter, Budget 2026-27](https://www.indiabudget.gov.in/doc/cen/dojstru1.pdf).
- **[CHANGED 2025]** Budget 2025 policy: apply "no more than one cess or surcharge" on industrial goods, and exempt SWS on 82 tariff lines that carry a cess. The TRU letter lists AIDC on solar cells/modules, furniture, toys parts and similar items. No AIDC was imposed on computers, switches, UPS, batteries, AC or DG sets — [PIB, Budget 2025 tariff rationalisation](https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2098364&reg=3&lang=1); [TRU letter, Budget 2025-26](https://www.indiabudget.gov.in/budget2025-26/doc/cen/dojstru1.pdf).

### Inferences
- For a GPU cluster, more than 90% of the capex by value (GPU servers, GPU boards, NVMe storage, DIMMs) attracts **0% BCD**. Import cost is mainly a cash-flow issue: 18% IGST is paid at the Bill of Entry and recovered later through ITC.
- The dutiable items are mostly facility gear: networking (10–20%), UPS (0–20%), Li-ion (20%), PAC (20%), DG (7.5–10%) and racks (20% + 5% AIDC). Buying these domestically from Indian distributors removes customs duty from the buyer's books. The distributor's own duty is built into the price, but the buyer only pays 18% GST, which is fully creditable.
- Optical transceivers have no settled classification. Some importers use 8517 62 90 (which could mean 10% as switch components or 20% as "other") and others use 8517 79 90 (15%). Model 10–20% BCD and get a broker opinion or a CAAR advance ruling.

### Gaps
- I could not open the CBIC/ICEGATE tariff or the consolidated text of Notification 24/2005 / 25/2005 / 57/2017 directly. The 8-digit BCD figures come from EximPe's ICEGATE-derived dataset (as at 13 May 2026), and the Budget changes from the primary TRU letters.
- **A customs broker should confirm:** whether routers under 8517 62 90 get 10% or 20%; the transceiver classification; and whether 8544 42 DAC cables can claim ITA-1 nil duty.
- Not verified: whether 24/2005, 25/2005 and 57/2017 survived as standalone notifications after the 24 Oct 2025 consolidation into Notification 45/2025-Customs (see Q2). The published superseded list I saw did not include them.
- Fire detection/suppression panels (8531 / 8537) and clean-agent gas (Chapter 29/38) rates were not retrieved. EximPe had no data for 8537 10 00.

---

## Q2. Recent changes: Budget 2025, Notification 45/2025 consolidation, GST 2.0 (Sep 2025), Budget 2026

### Takeaway
2025 brought four changes:
- Budget 2025 rationalised tariff slabs, cut carrier-grade switch BCD to 10%, and replaced SWS with AIDC on furniture (9403).
- A consolidated "jumbo" exemption Notification 45/2025-Customs took effect on 1 Nov 2025, with effective rates unchanged.
- GST 2.0, effective 22 Sep 2025, moved air-conditioners, accumulators (batteries) and diesel engines from 28% to 18%. Computers, servers, UPS, switches and DG sets stay at 18%.
- Budget 2026 (1 Feb 2026) made **no rate change** to servers, GPUs, network gear, UPS, batteries, AC or DG sets. It mainly migrated exemption rates into the First Schedule from 1 May 2026 with "no change in applicable rate".

### Cited Findings

**Budget 2025 (1 Feb 2025)**
- **[CHANGED 2025]** The Budget removed "seven customs tariff rates for industrial goods over and above the seven tariff rates removed in Budget 2023-24. This will leave only eight tariff rates, including 'zero' rate." It proposed to "exempt the Social Welfare Surcharge on 82 tariff lines that are subject to a cess" — [PIB](https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2098364&reg=3&lang=1); [ETV Bharat](https://www.etvbharat.com/en/!bharat/union-budget-2025-26-customs-tariff-enn25020106509).
- Where BCD was reduced, AIDC was imposed to keep effective incidence broadly unchanged (Deloitte comment quoted) — [Moneylife](https://www.moneylife.in/article/budget-2025-indirect-tax-and-customs-duty-reforms/76268.html).
- **[CHANGED 2025]** Carrier-grade Ethernet switches: 20% → 10% BCD. Furniture 9403: 25% → 20% BCD + 5% AIDC, SWS exempted (Primary) — [TRU letter 2025-26](https://www.indiabudget.gov.in/budget2025-26/doc/cen/dojstru1.pdf).
- **[CHANGED 2025]** Interactive flat panel displays: BCD 10% → 20% (relevant only if buying displays) — [India Briefing](https://www.india-briefing.com/news/india-revises-customs-tariff-under-union-budget-2025-26-36054.html/).

**Notification 45/2025-Customs (24 Oct 2025, effective 1 Nov 2025)**
- **[CHANGED 2025]** It supersedes Notification 50/2017-Customs and 30 standalone notifications. Exemptions and concessions continue, "barring two minor changes". Companion Notification 44/2025-Customs realigns the SWS (11/2018), AIDC (11/2021) and health cess exemption notifications to it — [A2Z Taxcorp](https://a2ztaxcorp.net/consolidation-of-customs-notifications-applicable-w-e-f-november-01-2025/); [Taxguru FAQ](https://taxguru.in/custom-duty/consolidated-customs-notifications-faq-2025.html); [WorldTradeScanner text: "Duty Rates and Conditions Remain the Same as Before"](https://worldtradescanner.com/Ntfn%2045-24.10.2025.htm).

**GST 2.0 (56th GST Council meeting; Notification 9/2025-CT(Rate) dated 17 Sep 2025, effective 22 Sep 2025)**
- **[CHANGED 2025]** The notification supersedes Notification 1/2017-CT(Rate). The new structure is Schedule I 2.5% CGST (5% total), Schedule II 9% (18%), Schedule III 20% (40%), plus special schedules (Primary) — [Notification 9/2025-CT(Rate), ICAI copy](https://d23z1tp9il9etb.cloudfront.net/download/gstlaw/NOTIFICATION%20NO.%209_2025-CENTRAL%20TAX%20(RATE)1759486688.pdf).
- AC 8415, fridges/chillers 8418, ADP machines 8471, parts 8473, DG sets 8502, transformers/static converters 8504, accumulators 8507, 8517, ICs 8542, cables 8544, furniture 9403 and steel structures 7308 are all in **Schedule II (18%)**. 8408 compression-ignition (diesel) engines are also in Schedule II at S. No. 395 (Primary) — same source.
- Commentary: AC moved from 28% to 18% from 22 Sep 2025. Computers and laptops were already at 18% and were unchanged — [Bajaj Finserv](https://www.bajajfinserv.in/gst-rate-on-air-conditioners); [Daily Jagran](https://www.thedailyjagran.com/india/gst-2-0-tax-rates-acs-refrigerators-tvs-get-cheaper-but-mobiles-laptops-stay-pricy-know-why-10268671).
- Monitors/projectors and "electric accumulators previously falling within that slab" (i.e. non-Li-ion batteries such as VRLA, which were at 28%) moved to 18% — [Lexplosion](https://lexplosion.in/key-highlights-on-the-outcome-of-the-56th-gst-council-meeting/); [BankBazaar](https://bankbazaar.com/tax/gst-council.html).

**Budget 2026 (1 Feb 2026)**
- **[CHANGED 2026]** Customs changes were made through Notifications 01/2026 to 05/2026-Customs. Most took effect 2 Feb 2026, and others on 1 Apr or 1 May 2026 (Primary) — [TRU letter, Budget 2026-27](https://www.indiabudget.gov.in/doc/cen/dojstru1.pdf).
- What the Chapter 84/85 entries cover:
  - nuclear fuel elements (Nil);
  - extension of the BESS capital-goods exemption;
  - lapse on 31 Mar 2026 of Nil BCD on cash dispensers and parts (8472 90/8473 40, not 8473 30);
  - an exemption for microwave-oven inputs including 8504 31 00;
  - lapse of film/TV equipment exemptions;
  - migration of the 8415 90 (10%) and 8507 90 separator (5%) rates into the First Schedule "with no change in the applicable rate" from 1 May 2026.
- No entry changes 8471, 8473 30, 8517 62, 8504 40, 8507 60 or 8502 (Primary) — same source.
- **[CHANGED 2026]** SWS: all of heading 9503 (toys) is exempt from SWS from 2 Feb 2026. SWS is levied on 9804 personal-import goods from 1 Apr 2026, when the 9804 tariff falls from 20% to 10%. Neither change affects datacenter equipment (Primary) — same source; [Taxguru summary](https://taxguru.in/income-tax/budget-2026-key-customs-excise-gst-legislative-duty-changes.html).
- **[CHANGED 2026]** The review of exemptions extended 102 exemptions to 31 Mar 2028. 22 lapse on 31 Mar 2026, and 14 unconditional exemptions were omitted from 2 Feb 2026 — [Taxguru summary of TRU letter](https://taxguru.in/income-tax/budget-2026-key-customs-excise-gst-legislative-duty-changes.html).
- GST legislative proposals in Finance Bill 2026 (post-sale discounts, provisional refunds for inverted duty structure, intermediary place of supply) do not directly affect a buyer's ITC on capital goods — same source.

### Inferences
- The question asked whether "AIDC replaced SWS". That happened only for the 82 cess-bearing lines, which for this bill of materials means furniture-type racks (9403). For every other item the stack is still BCD + 10% SWS + 18% IGST.
- GST 2.0 lowers non-recoverable cost only where ITC is blocked or unavailable: domestic purchases of VRLA batteries and ACs that end up as blocked credits under Section 17(5) because they are installed as building HVAC. With full ITC the 28% → 18% move only helps cash flow.

### Gaps
- I did not see the PIB press release for the 56th GST Council meeting directly (search snippets only). The prior 28% rate for 8408 diesel engines is not confirmed by a source I opened.
- Whether the ITA notifications (24/2005, 25/2005) and Notification 57/2017 were folded into 45/2025 or remain standalone was not established. The rates appear unchanged either way (CBIC said effective rates are unchanged), but the notification serial numbers a broker cites on the Bill of Entry may differ.

---

## Q3. Import formalities and costs (IEC, IMS licensing, BIS/CRS, valuation, broker/port, freight, FX)

### Takeaway
To import servers (HS 8471), Stark Digital needs three things:
1. An **IEC**: ₹500, lifetime validity, mandatory annual update between April and June.
2. An **Import Management System (IMS) authorisation from DGFT**. The 2023 "restricted" regime for laptops, tablets, AIO PCs, ultra-small PCs and **servers under 8471 is still in force for calendar 2026** under Policy Circular 08/2025-26 (17 Dec 2025). Applications run 22 Dec 2025 to 15 Dec 2026, and authorisations are valid to 31 Dec 2026.
3. Products that are BIS-registered where CRS applies.

On valuation:
- Assessable value is CIF at actual cost. **The 1% notional landing charge was abolished in 2017.**
- For GPU servers, air freight and insurance are typically well under 1% of value, because these goods have very high value per kg.
- Broker fees are a few thousand to ~₹25k per Bill of Entry.
- The bank FX margin, typically ~0.25–2% depending on how it is negotiated, is the largest "soft" cost.

### Cited Findings

**IEC**
- Government fee ₹500, non-refundable, paid online; lifetime validity — [EximPe IEC guide](https://eximpe.com/blog/taxation-compliance/iec-code-registration-documents-fees-activation-verification).
- Mandatory annual update between 1 Apr and 30 Jun, even if nothing has changed (DGFT Notification 58/2015-20, 12 Feb 2021). Missing it auto-deactivates the IEC from 1 July. The annual confirmation is free (Trade Notice 31/2021-22 cited) — [SetIndiaBiz](https://www.setindiabiz.com/iec-renewal); [EximPe renewal guide](https://eximpe.com/blog/b2b/renew-update-check-iec-code-status-online).

**IMS authorisation for IT hardware**
- DGFT Policy Circular No. 08/2025-26, 17 Dec 2025, signed by the DDGFT, continues the regime started by DGFT Notifications 23/2023 (3 Aug 2023), 26/2023 (4 Aug 2023) and 38/2023 (19 Oct 2023). Those notifications made "laptops, tablets, all-in-one PCs, ultra small form factor computers, and servers under HSN 8471" Restricted.
- The circular's terms:
  - "Importers shall apply in the Import Management System for Import Authorization on the DGFT Website."
  - "The application portal will be open from 22.12.2025 to 15.12.2026."
  - "Any Authorization issued for the import of restricted IT Hardware under IMS shall be valid till 31.12.2026."
  - Multiple applications and online amendments are allowed. MeitY may carry out a mid-term review. DGFT may amend or withdraw the procedure.
- Source: [Taxguru](https://taxguru.in/dgft/import-authorisation-mandated-restricted-hardware-remains-ims-2026.html); [WorldTradeScanner circular text](https://worldtradescanner.com/08-Pol.Circular-17.12.2025.htm); [SJ Exim](https://sjexim.services/2025/12/18/import-management-system-guidelines-for-restricted-it-hardware/).
- Commentary: servers under 8471 "cannot be cleared without an authorisation obtained in advance", and the Indian importer of record must hold an IEC — [Carra Globe case study](https://carraglobe.com/case-study-ai-server-import-india/).
- Conflict: EximPe's ITC-HS field shows "Import policy: Free" for 8471 41/49/50. This is probably the base ITC(HS) policy before the restriction, and it conflicts with the DGFT circular — [EximPe 84714900](https://eximpe.com/hsncode-finder/84714900).

**BIS / CRS**
- IS 13252 is the standard for laptops, notebooks and tablets under the Compulsory Registration Scheme — [IEEE/BIS presentation](https://ewh.ieee.org/r6/ocs/pses/India%20Presentation.pdf).
- **[CHANGED 2025]** A vendor blog reports MeitY S.O. 4997(E) dated 29 Oct 2025, which replaces IS 13252 (Part 1):2010 / IS 616:2017 with IS/IEC 62368-1:2023 under CRS — [Seyecs blog](https://blogs.seyecs.com/bis-crs-registration/). Not verified against the gazette.
- Commentary flags "BIS holds" on AI GPU imports in 2026 — [Carra Globe AI GPU compliance](https://carraglobe.com/ai-gpu-import-compliance/).

**Customs valuation (assessable value)**
- Notification 91/2017-Customs (N.T.), 26 Sep 2017, substituted Rule 10(2) of the Customs Valuation Rules 2007:
  - The notional 1% of CIF for landing charges "stands abolished". Loading, unloading and handling charges at the place of importation are no longer added.
  - Transport and insurance up to the place of importation remain includible.
  - Where transport cost cannot be ascertained, the rule uses 20% of FOB.
- Background: the Supreme Court's 2015 Wipro ruling. Implementation: CBIC Circular 39/2017-Customs and JNCH Public Notice 132/2017.
- Sources: [Corporate Law Reporter](https://corporatelawreporter.com/cbec-amends-customs-valuation-rules-notification-no-912017-nt-dated-26-09-17/); [Taxguru](https://taxguru.in/?p=1057652); [JNCH PN 132/2017](https://www.jawaharcustoms.gov.in/pdf/PN-2017/PN_132.pdf).

**Broker (CHA) and port charges**
- CHA fees: roughly ₹3,000–10,000 per air AWB and ₹8,000–25,000 per sea shipment. Agency fee ₹5,000–12,000 per Bill of Entry, plus ₹2,000–5,000 for documentation and ₹5,000–20,000 for special clearances such as BIS. GST applies on the fees — [EximPe CHA guide](https://eximpe.com/blog/b2b/freight-forwarder-vs-customs-house-agent); [StartupGrantsIndia](https://www.startupgrantsindia.com/services/customs-clearance-cha-services/fees). Commentary, indicative only.
- Port/airport handling and warehouse charges are levied separately by the terminal operator. I found no published figure for Mumbai CSIA cargo — [StartupGrantsIndia](https://www.startupgrantsindia.com/services/customs-clearance-cha-services/fees).

**Air freight**
- 2026 international air freight is typically $3–7/kg, or $4–10/kg all-in with surcharges — [FreightAmigo 2026](https://www.freightamigo.com/sc/blog/logistics/air-freight-costs-in-2026-prices-rates-per-kg-and-key-insights/).
- Typical surcharges: fuel 15–25%, security $0.15–0.25/kg, handling $0.10–0.20/kg. Chargeable weight is the greater of actual or volumetric weight at 167 kg/CBM — [Cogoport](https://www.cogoport.com/knowledge-center/resources/shipping-terms/air-freight-rates-india-mumbai-delhi-shipping-calculator).
- Asia–North America spot rates are about $5.70–7.50/kg (proxy lane) — [FreightAmigo](https://www.freightamigo.com/sc/blog/logistics/air-freight-costs-in-2026-prices-rates-per-kg-and-key-insights/).

**FX and banking**
- Banks build the FX margin into the TT selling rate used for outward remittances — [Vested Finance](https://vestedfinance.com/understanding-the-interbank-rate-and-bank-fx-markups/).
- Reported retail spreads: HDFC/ICICI ~1.5–2%, SBI ~1–2% with higher flat fees. Intermediary bank fees are $5–25 per wire. These are retail/SME figures, not negotiated corporate trade-finance pricing — [Winvesta](https://www.winvesta.in/blog/hidden-international-payment-charges-every-indian-business-pays).

### Inferences
- **Freight as a share of value (illustration, my assumptions):** a GPU server worth roughly US$250k shipped at 150 kg chargeable weight costs $600–1,500 in air freight at $4–10/kg. That is about 0.25–0.6% of value. Insurance is generally a fraction of a percent. Model freight + insurance at **~0.5–1% of FOB** for GPU servers. Use a higher percentage, about 3–8%, for heavy, low-value items such as batteries, racks, PAC units and DG sets, which usually go by sea.
- The customs exchange rate is the CBIC-notified rate for the Bill of Entry date, not the bank's rate. The model should keep these separate: the bank TT rate drives the INR cash cost, while the CBIC rate drives the duty base. (Practice knowledge; not sourced in this session.)
- **Plan IMS lead time.** Apply before the PO ships, and file a fresh application if any shipment will land after 31 Dec 2026, because the 2027 regime is not yet published.

### Gaps
- Not verified this session: the CVR Rule 10(2) proviso fallback for insurance (commonly cited as 1.125% of FOB) and the air-freight cap.
- No source found for import LC commission or usance rates, negotiated corporate FX spreads, or Mumbai airport cargo terminal tariffs.
- IMS conditions for 2026 not found: whether MeitY registration is needed, quantity or value caps, and exemptions for R&D, repair or re-import (the 2023 regime had some).
- I could not confirm from the official CRS list whether rack servers (as distinct from laptops and desktops) are in the BIS CRS Schedule. **Ask the vendor or importer of record for the BIS R-number.**

---

## Q4. GST input tax credit: imports, blocked credits (Section 17(5)), Safari Retreats, plant and machinery

### Takeaway
A GST-registered IT services company **can claim the full IGST paid at import (or the GST on domestic purchase)** on servers, GPUs, network gear, racks, UPS, batteries and DG sets as ITC on capital goods. The conditions:
- The Bill of Entry must show in GSTR-2B through ICEGATE.
- The goods must be used for taxable or zero-rated business supplies.
- No income-tax depreciation may be claimed on the GST component (Section 16(3)).

ITC is **blocked** under Section 17(5)(c)/(d) for works contracts and goods/services used to construct immovable property (civil works, embedded electrical wiring, building HVAC), except where the item is "plant and machinery". The Supreme Court's Safari Retreats judgment (3 Oct 2024) opened a functionality-test route. The **Finance Act 2025 retrospectively (from 1 Jul 2017) changed "plant or machinery" to "plant and machinery"**, largely closing that route. CBIC notified the Finance Act 2025 GST provisions effective 1 Oct 2025.

### Cited Findings

**ITC on IGST paid at import**
- Rule 36(1)(d) of the CGST Rules lists the Bill of Entry as a valid document for ITC on import IGST. Commentary applies the Section 16(4) time limit to it, though some argue it does not — [TaxTMI forum](https://www.taxtmi.com/forum/issue?id=116138).
- BCD and SWS are not creditable; IGST is — [Cashfree](https://www.cashfree.com/blog/gst-on-imports-customs-duty/).
- Timing in GSTR-2B depends on the ICEGATE reference date: the later of the out-of-charge date, duty payment date or amendment date (CBIC advisory 18 Oct 2021 cited) — [TaxTMI forum](https://www.taxtmi.com/forum/issue?id=116138).
- A 2025 advance ruling held that a TR-6 challan for differential IGST is not a valid ITC document. Credit is available only once a reassessed Bill of Entry is uploaded — [TaxHeal](https://www.taxheal.com/r-2025-53.html).
- Section 16(3): ITC on the tax component of capital goods is not allowed if depreciation is claimed on that tax component under the Income-tax Act — [HNA LLP](https://hnallp.com/a/capital-goods-and-its-gst-implication).
- The Kerala HC (2026, banks under 17(4)) read this narrowly: the bar applies only to the tax component on which depreciation is actually claimed — [EY alert, Mar 2026](https://www.ey.com/en_in/technical/alerts-hub/2026/03/kerala-hc-holds-banks-eligibility-of-50pc-itc-cannot-be-denied-where-it); [Taxmann](https://www.taxmann.com/post/blog/banks-50-itc-on-capital-goods-cannot-be-denied-hc).

**Safari Retreats and the Finance Act 2025 amendment**
- Supreme Court, *Chief Commissioner of CGST v. Safari Retreats Pvt Ltd*, Civil Appeal No. 2948 of 2023, decided **3 Oct 2024**. The Court:
  - upheld the validity of Sections 17(5)(c) and (d);
  - held that "plant or machinery" in clause (d) is not the same as "plant and machinery";
  - held that whether a building is a "plant" depends on a functionality test, and remanded the matter to the Orissa HC.
  - Sources: [Lawyer E News](https://lawyerenews.com/legal_detail/shopping-malls-may-qualify-as-plant-for-input-tax-credit-under-gst-a-functionality-test-required-supreme-court); [Taxguru](https://taxguru.in/?p=1080251); [CAclubindia](https://caclubindia.com/articles/itc-will-be-allowed-when-immovable-property-falls-under-definition-of-plan-machinery-sc-52661.asp).
- Review petition (Diary No. 1188 of 2025) dismissed — Grant Thornton alert dated **23 May 2025** — [Grant Thornton Bharat](https://www.grantthornton.in/link/57f26307cc91461781abe8064d7bf354.aspx). Conflict: one Taxguru item dates the dismissal to August 2026 — [Taxguru](https://taxguru.in/?p=1080251). Grant Thornton's dated alert is the more reliable source.
- **[CHANGED 2025]** The Finance Act 2025 (assent 29 Mar 2025) substituted "plant and machinery" for "plant or machinery" in Section 17(5)(d), retrospectively from 1 Jul 2017. It added Explanation 2 so that the phrase is read as "plant and machinery" notwithstanding any judgment. The provision is Section 119 of the Finance Act 2025 per NLIU.
  - Sources: [BDO alert](https://bdo.in/en-gb/insights/alerts-updates/indirect-tax-alert-effective-dates-for-implementation-of-the-provisions-of-the-finance-act-2025); [NLIU Law Review](https://nliulawreview.nliu.ac.in/?p=7728); [Grant Thornton](https://www.grantthornton.in/link/57f26307cc91461781abe8064d7bf354.aspx); [Taxo: Finance Act notified 29.03.2025](https://taxo.online/latest-news/30-03-2025-the-finance-act-no-7-2025-has-been-notified-by-the-government-on-29-03-2025/).
- **[CHANGED 2025]** CBIC notified **1 Oct 2025** as the effective date for key GST provisions of the Finance Act 2025, including the Section 17(5) amendment — [Taxguru](https://taxguru.in/goods-and-service-tax/gst-amendments-finance-act-2025-effective-oct-1-2025-notified.html); [Taxo 18.09.2025](https://taxo.online/latest-news/18-09-2025-cbic-notifies-1st-october-2025-as-effective-date-for-key-gst-provisions-of-finance-act-2025/).
- After the amendment, a GSTAT decision denied ITC on a resort building, treating the retrospective amendment as overriding Safari Retreats — [Taxo](https://taxo.online/?p=552105).
- One commentary notes the clause (d) block applies only to construction "on own account". It does not apply to construction for sale, lease or licence — [TaxTMI article](https://www.taxtmi.com/article/detailed?id=13488).

**Plant and machinery vs immovable property (advance rulings)**
- Rulings denying ITC:
  - AAAR Gujarat (Varachha Co-op Bank, 2023): central AC plant, lifts, electrical fittings and fire-safety extinguishers in a building under construction are immovable property, so ITC is blocked.
  - AAAR/AAR Gujarat (Wago): HVAC/ventilation installed through a works contract is immovable and "ceases to be a plant and machinery".
  - Fujitec: lifts are immovable property.
  - AAR Karnataka (Tarun Realtors, a mall): transformers, DG sets, AHUs, lifts and electrical wiring treated as blocked.
  - Sources: [TaxTMI](https://www.taxtmi.com/article/detailed?id=12687); [Busy.in, Tarun Realtors](https://busy.in/caselaw/tarun-realtors-private-limited-authority-for-advance-ruling-karnataka); [Taxscan](https://www.taxscan.in/?p=76771).
- Rulings allowing ITC:
  - AAR Gujarat (GETCO/Alleima): cables, wires and electrical equipment that can be dismantled and relocated are movable, so they are not hit by 17(5)(c)/(d). Ducts and manholes were treated as plant and machinery relying on CBIC Circular 219/23/2024-GST.
  - AAR UP (Tianyin Worldtech): works contracts for plant and machinery are outside the block.
  - Sources: [TaxHeal](https://www.taxheal.com/?p=110779); [Busy.in, Tianyin](https://busy.in/caselaw/tianyin-worldtech-india-private-limited-authority-for-advance-ruling-uttar-pradesh).

### Inferences
- **Servers, GPUs, storage, switches, racks, rack PDUs, plug-in UPS and batteries** are movable goods and not "construction". ITC is available.
- **DG sets, transformers, large UPS and precision AC units** fall within the "plant and machinery" definition in the Explanation to Section 17. It covers apparatus "fixed to earth by foundation or structural support" used for outward supply, including the foundation, but excludes "land, building or any other civil structures". So ITC is generally available when these are bought as equipment and invoiced separately.
  - Risk rises when they are supplied as part of a single works contract for building services; see Tarun Realtors and the HVAC rulings.
  - **Practical step:** buy the equipment on a separate supply invoice. Put installation on its own invoice, as installation of P&M rather than a "works contract for building".
- **Blocked credits:** civil works, false floor and ceiling, embedded electrical wiring, central HVAC ducting and building fire systems that become part of the building. Model these at 18% GST as a non-recoverable cost.
- **Depreciation choice:** claim ITC and capitalise only the net-of-GST cost for income-tax depreciation. Claiming both is barred by Section 16(3).

### Gaps
- I did not open the CGST Act text for the Explanation defining "plant and machinery". The wording above is my statement of the statutory text and should be confirmed by a CA.
- The exact CBIC notification number that brought Section 17(5)(d) into force on 1 Oct 2025 was not retrieved.
- No AAR found specific to server rooms or datacenter halls (raised floor, containment, in-row cooling). **A CA should review the build-out contract structure.**

---

## Q5. Cloud services tax: domestic vs foreign providers, Section 195/DTAA, equalisation levy

### Takeaway
- Cloud bought from **AWS India (Amazon Web Services India Pvt Ltd)** or other Indian-billed entities carries **18% GST** (IGST interstate, or CGST+SGST), creditable when the customer's GSTIN is on the invoice.
- Cloud **billed from abroad** (AWS Inc. etc.) to a GST-registered business is an import of services. The recipient pays **18% IGST under reverse charge** and can usually claim it as ITC.
- **Withholding:** the Delhi HC (May 2025) held that AWS cloud fees are neither royalty nor fees for included services under the India–US DTAA. Section 195 TDS on standard cloud subscriptions is therefore generally nil with treaty documentation.
- **Equalisation levy:** the 2% e-commerce levy was abolished from 1 Aug 2024 and the 6% online-ads levy from 1 Apr 2025. There is no equalisation levy in 2026.

### Cited Findings
- AWS India bills Indian customers of AWS India at CGST 9% + SGST 9% (Delhi customers) or IGST 18% (other states). Business customers add their GSTIN in Tax Settings so a valid tax invoice is issued, and invoices flow into the GST portal's Invoice Management System.
- Some Indian customers are billed by **Amazon Web Services, Inc.** (a non-resident OIDAR supplier), which charges IGST only on non-business sales. Adding a GSTIN prevents IGST being charged on AWS Inc. purchases.
- **[CHANGED 2025]** Since 6 Nov 2025, AWS India is the Marketplace operator for India-incorporated sellers.
- Source: [AWS Tax Help – India](https://aws.amazon.com/tax-help/india/).
- Import of services (IGST Act s.2(11)): supplier outside India, recipient in India. The recipient pays IGST under RCM (IGST s.5(3)). OIDAR place of supply is the recipient's location (s.13(12)), and the RCM IGST is generally creditable — [Clevercoins](https://clevercoins.org/?p=8997); [Treelife](https://treelife.in/?p=16468).
- **[2025 ruling]** Delhi High Court (Justices Vibhu Bakhru and Tejas Karia, ITA 150/2025 and 154/2025, May 2025) upheld the ITAT. AWS provided "standardised, automated services". There was no transfer of a right to use equipment (so not equipment royalty), and support did not "make available" technical knowledge under Art. 12(4)(b) of the India–US DTAA. The case arose from Snapdeal's remittances for "Hosting and Bandwidth Charges" without TDS — [Delhi HC judgment](https://delhihighcourt.nic.in/app/showFileJudgment/VIB29052025ITA1502025_153957.pdf); [LiveLaw](https://www.livelawbiz.com/high-court/delhi-high-court/payments-made-to-aws-for-cloud-computing-services-not-taxable-delhi-high-court-296433); [K&S](https://ksandk.com/tax/taxation-of-cloud-computing-services-in-india/).
- **[CHANGED 2025]** The 6% equalisation levy on online advertising was removed from 1 Apr 2025 through Finance Bill 2025 amendments: Section 163 of the Finance Act 2016 does not apply on or after 1 Apr 2025 — [Business Today, 24 Mar 2025](https://businesstoday.in/latest/policy/story/equalisation-levy-of-6-on-online-ads-likely-to-be-scrapped-from-april-1-469169-2025-03-24); [YourStory](https://yourstory.com/2025/03/equalisation-levy-online-advertisements-abolished-google-meta-x-ads).
- The 2% levy on e-commerce supplies was abolished on 1 Aug 2024 — [Xflow](https://www.xflowpay.com/blog/equalisation-levy).

### Inferences
- With full ITC, the GST cost of cloud is cash-flow only for either billing route, so cloud and on-prem are compared at pre-GST prices. **Without ITC**, cloud carries 18% on every hour consumed. On-prem carries 18% on servers plus BCD + SWS on the dutiable facility items.
- Foreign-billed cloud adds compliance work: RCM IGST payment in cash (RCM liability cannot be paid from the ITC ledger), Section 195 analysis, and Form 15CA/15CB for the remittance. That favours an Indian-billed entity.

### Gaps
- Not verified: the Google Cloud India and Microsoft India billing entities and the GST treatment on their invoices.
- The section number of the TDS-on-non-resident provision under the Income-tax Act 2025 (the successor to s.195), and whether the 15CA/15CB process changed in 2026, were not checked.
- Whether Revenue appealed the Delhi HC AWS ruling to the Supreme Court was not checked.

---

## Q6. Depreciation: Income-tax rates, "computers" classification, additional depreciation, Schedule II lives, new Income-tax Act 2025

### Takeaway
- **Income-tax depreciation (WDV):** computers including software **40%**, general plant and machinery **15%**, furniture and fittings (including electrical fittings) **10%**, non-residential buildings **10%**, intangibles **25%**. These are unchanged under the new **Income-tax Act 2025, in force from 1 Apr 2026**, where depreciation moved to Section 34 per Taxguru; other commentary says 33 or 35.
- **Servers and GPU servers qualify as "computers" at 40%.** Case law extends the 40% rate to integrated peripherals, including servers and in some rulings UPS, switches and optical fibre used with computer systems.
- **Additional depreciation (old s.32(1)(iia)) is only for manufacturing or power businesses**, so Stark Digital is not eligible.
- **Companies Act Schedule II:** servers and networks **6 years**, end-user devices **3 years**, general plant and machinery 15 years, electrical installations 10 years.

### Cited Findings
- **[CHANGED 2026]** The Income-tax Act 2025 received Presidential assent on 21 Aug 2025 and came into force on 1 Apr 2026, replacing the 1961 Act. It uses a single "tax year". The Income-tax Rules 2026 were notified on 20 Mar 2026. The government says no new tax rate or policy change was introduced — [Taxguru](https://taxguru.in/income-tax/income-tax-act-2025-force-1st-april-2026.html); [Taxmann](https://www.taxmann.com/post/blog/president-gives-assent-to-income-tax-act-2025); [Deccan Herald](https://www.deccanherald.com/business/centre-notifies-income-tax-act-2025-law-to-come-into-effect-from-april-1-2026-3693171); [TaxHeal](https://www.taxheal.com/?p=120640).
- **Rates under the 2025 Act (Taxguru, 8 Apr 2026):** depreciation is in Section 34, re-enacting s.32. Rates: computers and software 40% (perpetual licences only, not SaaS); P&M general 15%; buildings 5% residential / 10% non-residential; furniture and fittings 10%; intangibles 25%. Block-of-assets and WDV are retained, and the opening WDV at 31 Mar 2026 carries forward — [Taxguru](https://taxguru.in/?p=1036553).
- Conflict on section numbering: Patron Accounting says Section 33 / Appendix I of the Rules — [Patron](https://www.patronaccounting.com/blog/depreciation-rules-2026-rates-block-assets); TaxClue says Section 35 — [TaxClue](https://taxclue.in/blog/depreciation-income-tax-act-2025).
- **Additional depreciation:** allowable "only on plant and machinery installed by an assessee engaged in the manufacture or production of articles or things" (ITAT order under the 1961 Act) — [ITAT order](https://itat.gov.in/public/files/upload/1744880460-K2d5W9-1-TO.pdf). Taxguru on the 2025 Act says it is limited to "businesses engaged in manufacturing or power generation" — [Taxguru](https://taxguru.in/?p=1036553).

**Is a GPU server a "computer"?**
- *CIT v. BSES Yamuna Powers Ltd* (Delhi HC, ITA 1267/2010, 31 Aug 2010): printers, scanners and servers "form an integral part of the computer system" and take the higher computer rate (60% then, 40% now). Revenue's appeal was dismissed in limine — [Delhi HC order](https://delhihighcourt.nic.in/app/downloadOrderbByDate/ITA/1267/2010/31-08-2010); [Legitquest](https://www.legitquest.com/case/commissioner-of-income-tax-v-bses-yamuna-powers-ltd/93BAB).
- UPS: ITAT in International Tractors allowed the higher rate on UPS and computer peripherals — [ITAT order](https://itat.gov.in/public/files/upload/1532336061-5756,%206239%20+%20C.O.%20130,%20173%20-%20RKP%20+%20SK%20-%20International%20Tractors%20Ltd..pdf). The Hyderabad ITAT (Adarsh Co-op) was fact-dependent on UPS — [ITAT order](https://itat.gov.in/public/files/upload/1523964898-1336%20H%2015%20Adarsh%20Cooperative%20urban%20bank%20ltd.pdf).
- Other cases summarised by Taxguru (10 Nov 2021):
  - Ushodaya (Hyderabad SB): switches, hubs, modems and cables supporting I/O are part of the computer.
  - Datacraft (ITAT Mumbai): routers and switches qualify only when functionally integrated with computers.
  - PCIT v. GVK Jaipur Expressway (SC): optical fibre used for a computer configuration is part of the computer.
  - OnMobile (ITAT Bangalore): server-dependent boards are computers.
  - Contra: Federal Bank (Kerala HC), EPABX is not a computer.
  - Source: [Taxguru](https://taxguru.in/income-tax/rate-depreciation-computer-accessories-peripherals.html).
- Contra trend: the Madras HC (Dinamalar) held that "computerized machines" are not computers and get 15% — [TaxHeal](https://taxheal.com/computerized-machines-are-not-computers-60-depreciation-not-allowed.html).

**Companies Act Schedule II**
- Part C, Computers and data processing units: "Servers and networks" 6 years; "End user devices, such as desktops, laptops, etc." 3 years — [Advocatekhoj, Schedule II](https://www.advocatekhoj.com/library/bareacts/companies2013/schedule2.php); [Tally](https://tallysolutions.com/business-guides/depreciation-on-computer-guide/).
- P&M general 15 years; electrical installations and equipment 10 years — [CalcGuru](https://calcguru.in/?p=5903); [Tally](https://tallysolutions.com/business-guides/depreciation-rate-companies-act-2013/).
- For companies not in the prescribed class, useful life "shall not be longer than" Part C. Prescribed-class companies may differ if they disclose the justification. Residual value is generally ≤5% — [search summary of Schedule II](https://www.advocatekhoj.com/library/bareacts/companies2013/schedule2.php).

### Inferences
- **For the cost model (tax):**
  - GPU servers, GPU boards, storage and memory: 40% WDV.
  - Network switches, routers, transceivers and fibre: 40% has a reasonable basis as part of the server/network computer system, but expect a dispute risk of 15%.
  - UPS and batteries dedicated to IT load: 40% is arguable, but use 15% for conservatism.
  - PAC, chillers, DG sets and fire suppression: 15%.
  - Racks and electrical fittings: 10%.
  - Civil works and server-room building improvements: 10% as building.
- **Half-year rule:** under the 1961 Act, assets put to use for less than 180 days in the year get half the rate. Taxguru says the WDV mechanics are retained, but this rule was not separately verified for the 2025 Act.
- **Books (Schedule II):** servers and networks 6 years straight line. A GPU cluster with a realistic economic life of 3–5 years can use a shorter, technically justified life, because Schedule II caps the life rather than fixing it.

### Gaps
- The official 2025 Act section number and the Rules 2026 depreciation appendix were not opened directly; the sources conflict on 33, 34 or 35.
- Not verified: whether Section 115BAA-type concessional-regime companies (22% rate) still face the 40% depreciation cap and the bar on additional depreciation under the 2025 Act.
- The exact holding of the *Datacraft* Special Bench on routers and switches is summarised differently across sources. **A CA should read the original before relying on 40% for network gear.**
- Schedule II building lives (60 years non-factory / 30 years factory, RCC) are not sourced here.

---

## Q7. Incentives: Maharashtra (IT/ITeS Policy 2023, Data Centre / Green DC Park policy) and Central schemes

### Takeaway
Under the Maharashtra IT/ITeS Policy 2023 (effective 27 Jun 2023, 5 years), Pune is **Zone I**. A registered IT unit in an IT park gets the following:
- Partial stamp duty exemption.
- Electricity duty exemption for 10 years (Zone I).
- Power at industrial (not commercial) tariff.
- Property tax at residential rates.

A registered **Data Centre unit** gets more:
- 100% stamp duty exemption.
- Electricity duty exemption: permanent under the 2023 policy, now **20 years** under a June 2026 notification.
- Open access, industry/infrastructure status and additional FSI.
- **No ₹1/unit power subsidy in Zone I.**

All benefits need registration with the Directorate of Industries (DoI), and for stamp duty a DoI NOC. There is no capital subsidy for buying IT hardware unless the unit is an "Emerging Technology" unit (20% capped at ₹1 crore). At the Centre, IndiaAI subsidises **access** to empanelled GPU clouds (about ₹65–150/GPU-hour), not private hardware purchases.

### Cited Findings

**IT/ITeS Policy 2023**
- Effective 27 Jun 2023, valid 5 years. Zone I = municipal corporation areas of Mumbai and the Pune Metropolitan Region — [Taxguru, 18 Feb 2025](https://taxguru.in/corporate-law/maharashtra-information-technology-enabled-services-policy-2023.html).
- IT/ITeS units:
  - Stamp duty: 100% for new units in IT parks outside Zone I; 75% in Zone I; 50% for new units in private IT parks in Zone I; 100% for SEZ/STPI units.
  - Electricity duty: 10 years in Zone I, 15 years elsewhere.
  - Power at industrial rates under the MERC tariff order; property tax "at par with residential rates".
  - Eligibility: IT/ITeS turnover must be more than 75% of total turnover. Expansion needs at least 25% additional fixed capital investment.
  - Stamp duty waiver requires a Commencement Certificate or RERA approval and a DoI NOC.
  - Source: [Taxguru](https://taxguru.in/corporate-law/maharashtra-information-technology-enabled-services-policy-2023.html).
- Emerging Technology units: 20% capital subsidy on investment excluding land and building, capped at ₹1 crore over 5 years, for the first 50 new units with at least ₹5 crore investment and 20 employees. Also ₹1/unit power subsidy for 5 years — same source.
- Data centres:
  - 100% stamp duty exemption on land or premises for new or expanded data centres.
  - Electricity duty exemption for new and existing DC units registered with DoI (described as permanent in the 2023 policy).
  - ₹1/unit power subsidy for 5 years only outside Zone I.
  - Open access, industry and infrastructure status, additional FSI.
  - Source: [Taxguru](https://taxguru.in/corporate-law/maharashtra-information-technology-enabled-services-policy-2023.html); [Quatro Hive](https://quatrohive.com/indias-data-centre-policy-landscape-balancing-incentives-with-complexity/).

**June 2026 electricity duty notification**
- **[CHANGED 2026]** Notification CEI-2025/CR-158/Energy-1, dated 22 Jun 2026, under the Maharashtra Electricity Duty Act 2016, supports the IT/ITeS Policy 2023 and the Integrated Green Data Centre Parks policy:
  - New IT/ITeS units in designated IT parks: 10 years (Zone I) / 15 years (other zones).
  - SEZ and 100% EOU IT units: permanent.
  - **Data Centre units (new and existing): 20 years.**
  - The exemption runs from the start of operations; no refund of duty paid before sanction; MSEDCL annual inspections; AVGC and emerging-tech units generally excluded.
  - Source: [TeamLease RegTech, 24 Jun 2026](https://teamleaseregtech.com/updates/article/57168/govt-of-maharashtra-issued-a-notification-regarding-electricity-duty-e/).
- Conflict: DCD describes "up to 60 percent exemption on electricity duty for 15 years" for Maharashtra data centres — [DCD](https://www.datacenterdynamics.com/en/opinions/state-governments-the-new-kingmakers-in-indias-hyperscale-data-center-race/).
- An October 2024 amendment added incentives for the first three Integrated Green Data Centre Parks (details not retrieved) — [Lexology](https://www.lexology.com/library/detail.aspx?g=05e7c507-d1f8-4d31-a278-06b5e7ac706f); [RP Realty Plus](https://www.rprealtyplus.com/interviews/incentives-laws-for-data-centres-in-maharashtra-118963.html).

**Central schemes (IndiaAI)**
- IndiaAI compute portal rates are reported between about ₹65 and ₹150 per GPU-hour:
  - ~₹65/GPU-hour; ~₹67 average with up to 40% subsidy; ~₹92 post-subsidy for H100-class — [Tensordata](https://tensordata.com/blog/gpu-cloud-pricing-india-2026); [CareerIndia](https://www.careerindia.com/news/indiaai-mission-2026-access-subsidized-gpus-boost-ai-careers-scale-startups-011-66885.html).
  - ~₹100/hour in a PIB factsheet and ~₹150/GPU-hour bid cost per the Minister — [Outlook Business](https://www.outlookbusiness.com/start-up/ai-computing-in-india-costs-less-than-half-of-global-market-rate-says-vaishnaw).
- Lok Sabha figures (Aug 2026): 93.18 lakh GPU-hours sanctioned across 237 projects, 15 empanelled providers — [Communications Today](https://communicationstoday.co.in/indiaai-mission-faces-gap-between-capacity-and-deployed-gpus); [Business Standard, Jun 2026](https://business-standard.com/technology/artificial-intelligence/india-ai-compute-race-subsidised-gpu-capability-gap-126062900734_1.html).
- Subsidised access targets startups, academia and researchers. Requests above 5,000 GPU-hours or 50 GPUs go to a review committee — [CareerIndia](https://www.careerindia.com/news/indiaai-mission-2026-access-subsidized-gpus-boost-ai-careers-scale-startups-011-66885.html).

### Inferences
- An **in-office server room** at Stark Digital's Pune premises probably does not qualify as a "Data Centre unit" without DoI registration. The data-centre definition and any minimum-capacity criteria were not found.
- As an IT unit, Stark Digital gets Zone I benefits only if it is a registered IT/ITeS unit, ideally in a designated IT park:
  - **Industrial power tariff (vs commercial).** Usually the largest recurring benefit for a GPU cluster.
  - Electricity duty exemption, Zone I, 10 years.
  - Property tax at residential rates.
- A GPU cluster could count as "AI / Emerging Technology". The 20% capital subsidy (≤₹1 crore) could then apply to hardware capex for a new unit with at least ₹5 crore investment and 20 employees. Confirm with DoI.
- Central manufacturing schemes (PLI IT Hardware 2.0, SPECS, ECMS) pay manufacturers, not buyers. A buyer benefits only indirectly, by buying India-assembled servers that avoid customs duty and IMS licensing.

### Gaps
- I did not open the official Maharashtra GR or the Data Centre / Green DC Park policy PDFs (maitri.mahaonline.gov.in, di.maharashtra.gov.in). Figures rest on Taxguru, TeamLease and DCD summaries, and they conflict on the electricity duty term.
- Not found: the LOI and registration procedure, eligibility thresholds (MW/racks) for "Data Centre unit", and whether the 2026 notification's 20 years replaces the 2023 "permanent" exemption.
- Not found: the MSEDCL industrial vs commercial (IT) tariff numbers for FY 2026-27.
- No source opened for PLI IT Hardware 2.0, SPECS or ECMS eligibility and status in 2026. Treat the statement above as unverified.

---

## Q8. Consolidated landed-tax table (synthesis for the cost model)

### Takeaway
Use the table below as the per-item tax parameter set. "Landed tax %" is the total tax paid at import on assessable value (CIF). "Non-recoverable" is the part that stays in cost when full ITC is claimed: BCD + AIDC + SWS for imports, 0% for domestic purchases. Without ITC, the full landed tax % stays in cost. For domestic purchases, the tax is 18% GST, fully recoverable where ITC is available.

### Cited Findings

Column notes:
- **SWS/AIDC:** SWS = 10% of BCD unless noted.
- **Landed tax %:** gross on CIF. The non-recoverable % with ITC is in brackets.
- **Depr. rate:** Income-tax WDV.
- Sources are those cited in Q1–Q7. "TRU25" = [Budget 2025 TRU letter](https://www.indiabudget.gov.in/budget2025-26/doc/cen/dojstru1.pdf). "TRU26" = [Budget 2026 TRU letter](https://www.indiabudget.gov.in/doc/cen/dojstru1.pdf). "GST-N9" = [Notification 9/2025-CT(Rate)](https://d23z1tp9il9etb.cloudfront.net/download/gstlaw/NOTIFICATION%20NO.%209_2025-CENTRAL%20TAX%20(RATE)1759486688.pdf). "EX" = EximPe ICEGATE-derived tariff page for the code.

| Item | HS code | BCD | SWS / AIDC | IGST / GST | Landed tax % (non-recoverable with ITC) | ITC claimable | Depr. rate (IT Act 2025, WDV) | Sch. II life | Source |
|---|---|---|---|---|---|---|---|---|---|
| GPU server / complete system (DGX/HGX, rack server) | 8471 49 00 / 8471 50 00 / 8471 41 | 0% (ITA-1; tariff "Free") | SWS nil; no AIDC | 18% | **18.00% (0%)** | Y (s.16; BoE in GSTR-2B; no depr. on IGST, s.16(3)) | 40% (computer) | 6 yrs (servers & networks) | [EX 84714900](https://eximpe.com/hsncode-finder/84714900); [24/2005](https://taxguru.in/custom-duty/notification-242005customs-duty-dated-01032005.html); GST-N9 S.No.456 (Sch II) |
| GPU accelerator board / HGX baseboard / motherboard / DIMM memory | 8473 30 30 / 8473 30 20 / 8473 30 99 | 0% | nil | 18% | **18.00% (0%)** | Y | 40% (part of computer) | 6 yrs | [EX 84733030](https://eximpe.com/hsncode-finder/84733030); GST-N9 S.No.458 |
| GPU / CPU chips (bare ICs) | 8542 31 00 | 0% | nil | 18% | **18.00% (0%)** | Y | 40% | 6 yrs | [EX 85423100](https://eximpe.com/hsncode-finder/85423100); GST-N9 S.No.514 |
| Storage drives / storage arrays (HDD, SSD) | 8471 70 20 / 8471 70 90 | 0% | nil | 18% | **18.00% (0%)** | Y | 40% | 6 yrs | [EX 84717020](https://eximpe.com/hsncode-finder/84717020); GST-N9 S.No.456 |
| Ethernet switch (DC/enterprise and carrier grade) **[CHANGED 2025]** | 8517 62 90 / 8517 69 90 | 10% (57/2017 S.No.20 as amended by 10/2025) | SWS 1% | 18% | **30.98% (11.00%)** | Y | 40% arguable (integrated with computers); 15% conservative | 6 yrs (networks) | TRU25; [India Briefing](https://www.india-briefing.com/news/india-revises-customs-tariff-under-union-budget-2025-26-36054.html/); GST-N9 S.No.490 |
| Router / other 8517 62 90 apparatus (if not under the 10% entry) | 8517 62 90 | 20% (tariff) — broker to confirm | SWS 2% | 18% | **43.96% (22.00%)** | Y | 40% arguable / 15% | 6 yrs | [EX 85176290](https://eximpe.com/hsncode-finder/85176290) |
| Optical transceivers / modules (classification disputed) | 8517 62 90 or 8517 79 90 | 10–20% (as 8517 62) or 15% (as parts 8517 79 90) | SWS 1–2% | 18% | **30.98–43.96% (11–22%)**; 37.47% (16.5%) at 15% | Y | 40% arguable | 6 yrs | [EX 85177990](https://eximpe.com/hsncode-finder/85177990); [MAIT](https://www.mait.com/uploads/publication_document/6c4b761a28b734fe93831e3fb400ce8719092022%20%e2%80%93%20Representation%20to%20Shri%20R%20K%20Pathak,%20DDG%20(IC),%20DoT%20reg.%20addendum%20to%20Technical%20write-up%20on%20non-carrier%20ethernet%20switches,%20POE%20switches,%20and%20Transceivers.pdf) |
| Optical fibre cables | 8544 70 10 / 8544 70 90 | 0% | nil | 18% | **18.00% (0%)** | Y | 40% (GVK Jaipur, fibre for computer config) / 15% | 6 yrs | [EX 85447090](https://eximpe.com/hsncode-finder/85447090); [Taxguru case summary](https://taxguru.in/income-tax/rate-depreciation-computer-accessories-peripherals.html) |
| Copper DAC / patch cables with connectors | 8544 42 xx | 15% | SWS 1.5% | 18% | **37.47% (16.50%)** | Y | 40% arguable / 15% | 6 yrs | [EX 85444299](https://eximpe.com/hsncode-finder/85444299); GST-N9 S.No.516 |
| Server racks / cabinets (furniture classification) **[CHANGED 2025]** | 9403 20 90 | 20% (tariff cut from 25% from 1 May 2025) | **SWS exempt; AIDC 5%** | 18% | **47.50% (25.00%)** | Y (movable) | 10% (furniture & fittings) | 10 yrs (furniture & fittings; verify) | TRU25 Ch.94; [Notif 07/2025-Cus](https://www.indiabudget.gov.in/doc/cen/cus0725.pdf); [EX 94032090](https://eximpe.com/hsncode-finder/94032090); GST-N9 S.No.612 |
| Racks / cages (as steel structure) | 7308 90 90 | 15% | SWS 1.5% | 18% | **37.47% (16.50%)** | Conditional (blocked if part of building structure) | 15% / 10% | 15 yrs | [EX 73089090](https://eximpe.com/hsncode-finder/73089090); GST-N9 S.No.286 |
| Enclosure / switchgear parts | 8538 10 90 / 8538 90 00 | 7.5% / 15% | SWS 0.75% / 1.5% | 18% | **27.74% (8.25%)** / **37.47% (16.50%)** | Y | 15% | 10 yrs (electrical) | [EX 85381090](https://eximpe.com/hsncode-finder/85381090); GST-N9 S.No.510 |
| UPS (static converter) | 8504 40 10 / 8504 40 90 | 20% tariff; **0% if 25/2005 S.No.4 ITA exemption allowed** (CESTAT 2024–26 favours importers) | SWS 2% / nil | 18% | **43.96% (22.00%)** or **18.00% (0%)** with ITA claim | Y (P&M / movable) | 40% (BSES Yamuna, International Tractors) contested; 15% conservative | 10 yrs (electrical installations) / 6 yrs if treated as part of network (judgement) | [EX 85044090](https://eximpe.com/hsncode-finder/85044090); [Taxguru CESTAT Intex](https://taxguru.in/custom-duty/revenue-withdraws-ups-customs-exemption-appeals-issue-settled-cestat-mumbai.html); GST-N9 S.No.477 |
| Lithium-ion batteries (UPS/BESS) | 8507 60 00 | 20% | SWS 2% | 18% | **43.96% (22.00%)** | Y | 15% (40% arguable if part of IT UPS) | 10 yrs (or shorter technical life with justification) | [EX 85076000](https://eximpe.com/hsncode-finder/85076000); GST-N9 S.No.480 |
| VRLA lead-acid batteries **[GST 28%→18% Sep 2025]** | 8507 20 00 | 15% | SWS 1.5% | 18% | **37.47% (16.50%)** | Y | 15% | 10 yrs (or shorter) | [EximPe 8507](https://eximpe.com/hsn/battery-hsn-code); [Lexplosion](https://lexplosion.in/key-highlights-on-the-outcome-of-the-56th-gst-council-meeting/); GST-N9 S.No.480 |
| Precision air conditioning (CRAC/in-row) **[GST 28%→18% Sep 2025]** | 8415 81 / 8415 82 / 8415 10 | 20% | SWS 2% | 18% | **43.96% (22.00%)** | Conditional (Y as standalone P&M; blocked if building HVAC via works contract) | 15% (P&M) | 15 yrs (P&M) | [EX 84158210](https://eximpe.com/hsncode-finder/84158210); [Bajaj](https://www.bajajfinserv.in/gst-rate-on-air-conditioners); GST-N9 S.No.404; [AAAR HVAC rulings](https://www.taxtmi.com/article/detailed?id=12687) |
| Chillers / refrigerating units | 8418 69 90 | 15% | SWS 1.5% | 18% | **37.47% (16.50%)** | Conditional (as above) | 15% | 15 yrs | [EX 84186990](https://eximpe.com/hsncode-finder/84186990); GST-N9 S.No.407 |
| Diesel generator set ≤75 kVA | 8502 11 00 | 10% | SWS 1% | 18% | **30.98% (11.00%)** | Conditional (P&M on foundation → Y; risk if bundled into building works contract, cf. Tarun Realtors) | 15% | 15 yrs | [EX 85021100](https://eximpe.com/hsncode-finder/85021100); GST-N9 S.No.475 |
| Diesel generator set >75 kVA | 8502 12 00 / 8502 13 xx | 7.5% | SWS 0.75% | 18% | **27.74% (8.25%)** | Conditional (as above) | 15% | 15 yrs | [EX 85021200](https://eximpe.com/hsncode-finder/85021200); GST-N9 S.No.475 |
| Fire suppression (clean-agent cylinders / extinguishers) | 8424 10 00 (detection panels 8531/8537 not checked) | 7.5% | SWS 0.75% | 18% | **27.74% (8.25%)** | Conditional (blocked if part of building fire system, cf. Varachha AAAR) | 15% (or 10% as fittings) | 15 yrs / 10 yrs | [EX 84241000](https://eximpe.com/hsncode-finder/84241000); GST-N9 S.No.413 |
| Any of the above bought domestically (Indian distributor) | — | n/a | n/a | 18% GST (Sch II) | **18% (0%)** | Y (subject to s.17(5) for building-linked items) | as above | as above | GST-N9 |
| Server-room civil works, raised floor, embedded wiring, building HVAC (works contract) | services (SAC 9954) / goods into building | n/a | n/a | 18% GST | **18% (18%) — fully non-recoverable** | **N** (s.17(5)(c)/(d); "plant and machinery" amendment, Finance Act 2025, retro 1 Jul 2017) | 10% (building) / 10% (electrical fittings) | building life (not verified) | [BDO](https://bdo.in/en-gb/insights/alerts-updates/indirect-tax-alert-effective-dates-for-implementation-of-the-provisions-of-the-finance-act-2025); [Grant Thornton](https://www.grantthornton.in/link/57f26307cc91461781abe8064d7bf354.aspx) |
| Cloud GPU from Indian-billed entity (e.g. AWS India) | SAC 9983 (services) | n/a | n/a | 18% GST on invoice | **18% (0%)** | Y (GSTIN on invoice) | revenue expense (not depreciated) | n/a | [AWS Tax Help India](https://aws.amazon.com/tax-help/india/) |
| Cloud GPU billed from abroad (AWS Inc. etc.) | import of service / OIDAR | n/a | n/a | 18% IGST via RCM (paid in cash) | **18% (0%)** | Y (RCM credit) | revenue expense; s.195 TDS generally nil under DTAA (Delhi HC AWS, 2025); no equalisation levy from 1 Apr 2025 | n/a | [Clevercoins](https://clevercoins.org/?p=8997); [Delhi HC AWS](https://delhihighcourt.nic.in/app/showFileJudgment/VIB29052025ITA1502025_153957.pdf); [Business Today](https://businesstoday.in/latest/policy/story/equalisation-levy-of-6-on-online-ads-likely-to-be-scrapped-from-april-1-469169-2025-03-24) |

Worked arithmetic for the stacks (on AV = 100):
- **0% BCD:** IGST 18 → 18.00%.
- **7.5%:** BCD 7.5 + SWS 0.75 = 8.25; IGST 0.18 x 108.25 = 19.485 → 27.74%.
- **10%:** 10 + 1 = 11; IGST 19.98 → 30.98%.
- **15%:** 15 + 1.5 = 16.5; IGST 20.97 → 37.47%.
- **20%:** 20 + 2 = 22; IGST 21.96 → 43.96%.
- **9403 racks:** BCD 20 + AIDC 5 + SWS 0 = 25; IGST 22.5 → 47.50%.

Formula basis: SWS is levied under s.110 of the Finance Act 2018, AIDC under s.124 of the Finance Act 2021, and IGST is charged on value plus duties — [TRU26](https://www.indiabudget.gov.in/doc/cen/dojstru1.pdf); [EximPe calculation note](https://eximpe.com/hsncode-finder/84714900).

### Inferences
- **Blended effect for a typical GPU cluster BOM.** Assume GPU servers, storage and networking are about 85–90% of capex and facility gear the rest. Then:
  - Gross import tax on CIF is about 19–22%.
  - With full ITC, the non-recoverable customs cost is only about **1–3% of total CIF**, mostly from switches, UPS, PAC, batteries and racks.
  - Without ITC, about 19–22% stays in cost.
- The ITC-vs-no-ITC difference is almost entirely the 18% IGST/GST. For a GST-registered IT exporter or domestic supplier, the IGST is a 1–2 month working-capital cost, not a final cost.
- **Inputs for the cost model:**
  - Freight + insurance about 0.5–1% of FOB for servers by air, 3–8% for heavy facility gear (assumption).
  - CHA + port handling about ₹10–40k per Bill of Entry.
  - Bank FX margin about 0.25–2% on the remittance, depending on what is negotiated.
  - IMS authorisation and BIS checks are lead-time items rather than cash costs.

### Gaps
- **A licensed customs broker should confirm, by HS line:** router and transceiver BCD (10%, 15% or 20%); whether the ITA 25/2005 S. No. 4 exemption is accepted at Nhava Sheva / Mumbai Air Cargo for datacenter UPS; and the rack classification (9403 vs 7308 vs 8473 30).
- **A CA should confirm:** the ITC split between P&M and blocked works-contract items in the server-room build-out; the 40% vs 15% depreciation position on network, UPS and batteries; and the section and rule references under the Income-tax Act 2025.
- Not verified: the BIS CRS applicability to rack servers, and the 2027 IMS regime.
