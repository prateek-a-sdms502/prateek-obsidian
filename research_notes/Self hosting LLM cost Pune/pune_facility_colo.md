# Facility capex/opex inputs: high-density GPU server room in Baner (Pune) vs colocation in Pune / Navi Mumbai (as of Oct 2026)

Scope: inputs for a cost model covering 1–8 GPU servers of about 10–15 kW each (racks of 30–60 kW, possibly one ~130 kW liquid-cooled NVL72). All figures are INR unless stated. "Inference" bullets are my own arithmetic or reasoning, not sourced facts. FX assumption for USD figures: about ₹88/USD (not verified for Oct 2026; JM Financial's Mar-2025 figures imply about ₹86/USD).

Source quality warning: the MERC tariff numbers come from the primary order and are reliable. Most equipment, colocation, salary and fit-out prices come from marketplace listings (IndiaMART/TradeIndia), vendor blogs or modelled salary sites. Treat those as ±30–50% planning numbers and get quotes before committing.

---

## 1. Electricity (MSEDCL): tariffs, charges, LT/HT threshold, HT connection cost, building load

### Takeaway
The governing tariff is MERC's post-remand review order (Case 75 of 2025, dated 25 Mar 2026), which applies from 1 Jul 2025 (FY26) and 1 Apr 2026 (FY27). The FY2026-27 HT-I(A) industrial rate is ₹650/kVA/month plus ₹8.44 + ₹0.81 wheeling = ₹9.25/kVAh. The HT-II commercial rate is ₹650/kVA/month plus ₹13.72 + ₹0.81 = ₹14.53/kVAh. MERC classifies data centres as Industrial. Data-centre units also get a 20-year electricity-duty exemption under a June 2026 GoM notification. Together these make the all-in industrial rate about ₹10.3–11.9/kWh, against about ₹19–20/kWh for commercial (HT-II). Getting registered as a data centre or IT unit is therefore the biggest single lever in the power opex. The LT limit is about 150 kW / 187 kVA in Municipal Corporation areas. So setups of about 4 or fewer air-cooled servers fit on LT, while 8 servers or an NVL72 rack need HT, or a share of the building's HT supply.

### Cited Findings

**Tariff order status and history**
- MERC's MYT order of 28 Mar 2025 (Case 217 of 2024) set tariffs for FY2025-26 to FY2029-30. MERC stayed it on 2 Apr 2025, and a review order of 25 Jun 2025 applied from 1 Jul 2025. The Bombay HC set the review order aside on 3 Nov 2025. The Supreme Court then remanded the matter on 17 Nov 2025 and extended the deadline on 9 Feb 2026. MERC re-issued the review order on 25 Mar 2026, effective 1 Jul 2025, with the same FY26 tariff as the June 2025 order — [MERC post-remand order, Case 75 of 2025, 25 Mar 2026](https://www.mahadiscom.in/wp-content/uploads/2026/07/Tariff-Order_Case-No.-75-of-2025-dated-25th-March-2026.pdf)
- Rulings in the MYT Order that the review did not modify "shall remain in force" — [MERC post-remand order, para 25](https://www.mahadiscom.in/wp-content/uploads/2026/07/Tariff-Order_Case-No.-75-of-2025-dated-25th-March-2026.pdf)
- **Data centres are in the Industrial category.** The MYT order "categorized high priority industries such as Data Centers and Semi-conductor units under Industrial category" and gave a 10% wheeling-charge discount to data centres using 100% green energy (open access or Green Tariff) — [MERC Press Note, MSEDCL MYT Order, Mar 2025](https://merc.gov.in/wp-content/uploads/2025/03/Press-Note_MSEDCL-MYT-Order_English.pdf)

**HT tariffs, FY2026-27 (effective 1 Apr 2026), HT supply (11/22/33 kV), from Annexure II of the post-remand order** — [MERC post-remand order](https://www.mahadiscom.in/wp-content/uploads/2026/07/Tariff-Order_Case-No.-75-of-2025-dated-25th-March-2026.pdf)

| Category | Demand charge (₹/kVA/month) | Energy (₹/kVAh) | Wheeling (₹/kVAh) | Total variable (₹/kVAh) |
|---|---|---|---|---|
| HT-I(A) Industry | 650 | 8.44 | 0.81 | 9.25 |
| HT-II Commercial | 650 | 13.72 | 0.81 | 14.53 |
| (EHV, no wheeling) HT-I(A) / HT-II | 650 | 8.44 / 13.72 | – | 8.44 / 13.72 |

- **FY2025-26 HT rates (from 1 Jul 2025):** HT-I(A) ₹600/kVA/month, energy ₹8.68 and wheeling ₹0.74, total ₹9.42/kVAh. HT-II ₹600/kVA/month, ₹14.03 + ₹0.74 = ₹14.77/kVAh. The FY2024-25 rates were ₹549/kVA/month with ₹9.59 (HT-I) and ₹14.77 (HT-II) total variable — [MERC post-remand order](https://www.mahadiscom.in/wp-content/uploads/2026/07/Tariff-Order_Case-No.-75-of-2025-dated-25th-March-2026.pdf)
- **Later years:** the order also publishes FY2027-28 to FY2029-30 schedules. The category average billing rate (ABR) for HT-I falls from ₹10.78 (FY26) to ₹10.71 (FY27), ₹10.64 (FY28), ₹10.00 (FY29) and ₹9.97 (FY30). HT-II goes from ₹16.83 to ₹16.78, ₹16.58, ₹15.93 and ₹15.87 — [MERC post-remand order, Table 11](https://www.mahadiscom.in/wp-content/uploads/2026/07/Tariff-Order_Case-No.-75-of-2025-dated-25th-March-2026.pdf)

**LT tariffs, FY2026-27 (effective 1 Apr 2026)** — [MERC post-remand order, Annexure II](https://www.mahadiscom.in/wp-content/uploads/2026/07/Tariff-Order_Case-No.-75-of-2025-dated-25th-March-2026.pdf)

| Category | Fixed/demand | Energy (₹/kVAh for ≥20 kW) | Wheeling | Total variable |
|---|---|---|---|---|
| LT-II(A) Non-residential 0–20 kW | ₹540/conn/month | 8.51 | 1.60 | 10.11 |
| LT-II(B) >20–≤50 kW | ₹550/kVA/month | 12.40 | 1.52 | 13.92 |
| LT-II(C) >50 kW | ₹550/kVA/month | 14.89 | 1.52 | 16.42 |
| LT-V(B)(i) Industry 0–20 kW | ₹650/conn/month | 6.26 | 1.60 | 7.86 |
| LT-V(B)(ii) Industry >20 kW | ₹420/kVA/month | 7.66 | 1.52 | 9.19 |

- **FY2025-26 LT (from 1 Jul 2025):** LT-II(B) ₹525/kVA + 12.83 + 1.39 = ₹14.22. LT-II(C) ₹525/kVA + 15.22 + 1.39 = ₹16.61. LT-V(B)(ii) ₹400/kVA + 7.76 + 1.39 = ₹9.15 — [MERC post-remand order](https://www.mahadiscom.in/wp-content/uploads/2026/07/Tariff-Order_Case-No.-75-of-2025-dated-25th-March-2026.pdf)
- Energy and wheeling charges for loads of 20 kW and above are billed in ₹/kVAh — [MERC post-remand order, Annexure II note](https://www.mahadiscom.in/wp-content/uploads/2026/07/Tariff-Order_Case-No.-75-of-2025-dated-25th-March-2026.pdf). The MYT order approved kVAh billing for LT consumers above 20 kW — [MERC Press Note](https://merc.gov.in/wp-content/uploads/2025/03/Press-Note_MSEDCL-MYT-Order_English.pdf)
- **Power factor:** there is no separate PF incentive or penalty. MSEDCL states that "kVAh billing provides inbuilt incentive which automatically takes care of power factor incentive and disincentive" — [MERC post-remand order, para 4.6.9](https://www.mahadiscom.in/wp-content/uploads/2026/07/Tariff-Order_Case-No.-75-of-2025-dated-25th-March-2026.pdf)
- **Other incentives:** the Load Factor Incentive, Incremental Consumption Rebate, Bulk Supply Rebate (revised), ToD rebate and prompt-payment rebate continue for industry. An incremental-consumption rebate of ₹0.75/kWh applies to specified LT categories, including LT-Industry and LT-Commercial — [MERC Press Note](https://merc.gov.in/wp-content/uploads/2025/03/Press-Note_MSEDCL-MYT-Order_English.pdf)

**Time-of-Day (ToD), revised in the post-remand order, Table 8** — [MERC post-remand order](https://www.mahadiscom.in/wp-content/uploads/2026/07/Tariff-Order_Case-No.-75-of-2025-dated-25th-March-2026.pdf)
- 00:00–09:00: 0%. The original MYT order's night rebate of −10% (00–06 h) was removed.
- Solar hours 09:00–17:00: −15% of energy charge (Apr–Sep) and −25% (Oct–Mar) in FY26 and FY27, rising to −20% and −30% from FY28.
- Peak 17:00–24:00: "+20%#". The original MYT order's note said "ToD Charge for LT/HT Industrial & Commercial Category is 25%" — [MERC Press Note](https://merc.gov.in/wp-content/uploads/2025/03/Press-Note_MSEDCL-MYT-Order_English.pdf). The "#" footnote text was not captured in my extraction, so confirm whether +20% or +25% applies to HT industrial and commercial.

**Electricity duty (ED), tax on sale, FAC**
- **ED rates (Maharashtra Electricity Duty Act 2016):** Commercial (Part B) is 21% of consumption charges and Residential is 16%, from the September 2016 billing month. Industrial (Part F) was 9.30% in 2016 — [MSEDCL Commercial Circular 273 (2016)](https://www.mahadiscom.in/consumer/wp-content/uploads/2018/02/Comm_Cir_273.pdf)
- **Industrial ED was cut to 7.50%** of consumption charges from the August 2020 billing month — [MSEDCL Commercial Circular 329, 1 Sep 2020](https://www.mahadiscom.in/consumer/wp-content/uploads/2020/09/Commercial-Circular-329-Revision-in-Rate-of-ED-of-Industrial-Consumer.pdf). Some 2026 bill-calculator sites still show 9.3% for industrial, which looks outdated — [billunits.in](https://billunits.in/state-calculators/msedcl-bill-calculator/)
- **ED exemption for IT, ITeS and data centres:** GoM notification CEI-2025/CR-158/Energy-1 of 22 Jun 2026 (Maharashtra IT/ITeS Policy 2023 and Integrated Green Data Centre Parks policy) grants new and existing data centre units a 20-year exemption. New IT/ITeS units in designated IT parks get 10 years in Zone-1 and 15 years in other zones. SEZ and 100% EOU IT/ITeS units get a permanent exemption. MSEDCL inspects compliance annually, there is no refund of duty paid before sanction, and AVGC/emerging-tech units are generally excluded — [TeamLease RegTech summary, 24 Jun 2026](https://teamleaseregtech.com/updates/article/57168/govt-of-maharashtra-issued-a-notification-regarding-electricity-duty-e/). Older commentary on the 2023 policy described the DC exemption as permanent — [Grant Thornton / search summaries](https://www.grantthornton.in/globalassets/1.-member-firms/india/assets/pdfs/maharashtra-industries-investment-and-services-policy.pdf)
- **IT/ITeS policy power benefits:** the 2023 policy is described as giving power at industrial rates, plus a ₹1/unit subsidy for 5 years for new data centres outside Zone-1. The policy runs 5 years from 27 Jun 2023 — [Cyril Amarchand Mangaldas blog](https://corporate.cyrilamarchandblogs.com/2023/07/key-highlights-of-maharashtra-it-ites-policy-2023-it-ites-units-iitts-and-data-centers/); [Mondaq](https://mondaq.com/india/real-estate/1360458/it-ites-policy-of-maharashtra-2023-pivotal-for-it-industry). A reported 2026 overhaul of the Green DC Parks policy gives ₹1/unit for 10–20 years depending on investment, but this is a secondary report — [Whalesbook](https://www.whalesbook.com/news/English/real-estate/Maharashtra-Expands-Green-Data-Centre-Policy-Investor-Impact/6a30b10ad017fdb509977cc9)
- **How MSEDCL applies the industrial tariff to IT/ITeS units:** MSEDCL Commercial Circular 212 (2013) applies industrial tariff to IT/ITeS units only after a field inspection and a valid LoI or registration certificate in the unit's own name. Supply during construction is billed at commercial tariff. Consumer-forum cases show MSEDCL reverting units to commercial tariff and recovering arrears where permanent registration was missing, and in one case it rejected a park-level registration for an individual tenant — [MSEDCL Comm. Circular 212](https://www.mahadiscom.in/consumer/wp-content/uploads/2018/02/Comm_Cir_212.pdf); [CGRF Pune order example](https://www.mahadiscom.in/wp-content/uploads/2018/03/Pune35_1520592376917.pdf)
- **Tax on Sale of Electricity (TOSE):** a single Jan-2025 industrial bill sample shows about 19.04 paise/unit alongside 21% ED. This is unverified — [Scribd bill sample](https://www.scribd.com/document/913142723/E-bill). The statute sets per-unit rates by area and consumer type — [Maharashtra Tax on Sale of Electricity Act 1963](https://indiankanoon.org/doc/43083419/)
- **Fuel Adjustment Charge (FAC):** it varies monthly and can be zero, positive or negative. News reports of an August FAC rise cite +20 to +55 paise/unit overall, +25 to +35 paise for small industries and +35 to +60 paise for commercial. The figures conflict and I found no MERC order — [Pune Pulse](https://www.mypunepulse.com/msedcl-august-electricity-bill-why-your-bill-may-rise-and-how-much-extra-you-may-pay/); [india.com](https://www.india.com/news/india/electricity-bill-hike-msedcl-hikes-maharashtra-power-tariffs-check-how-much-extra-will-mumbai-nashik-nagpur-thane-pune-customers-will-be-charged-8501662/)
- **Open access:** MERC did not allow Additional Surcharge on open access or Grid Support Charges for rooftop solar. Banking is allowed except in the evening peak (17:00–24:00), and banking rules were later re-ruled in the review — [MERC Press Note](https://merc.gov.in/wp-content/uploads/2025/03/Press-Note_MSEDCL-MYT-Order_English.pdf)

**LT vs HT threshold and HT voltage bands**
- LT supply is capped at about 150 kW / 187 kVA in Municipal Corporation areas and about 80 kW / 100 kVA elsewhere. A multi-consumer building on single-point supply can go to 480 kW / 600 kVA in MC areas. These are the MERC SoP-framework figures, and I could not confirm them against the 2021 Supply Code text — [MERC Explanatory Memorandum SoP 2017](https://merc.gov.in/wp-content/uploads/2022/07/Explanatory-Memorandum_SoP_2017.pdf)
- MSEDCL's Schedule of Charges LT slabs run up to "other loads above 80 kW but up to 150 kW". HT starts above that — [MSEDCL Schedule of Charges w.e.f. 1 Apr 2020](https://www.mahadiscom.in/consumer/wp-content/uploads/2020/04/Circular-Schedule-of-Charges-for-various-services-of-MSEDCL-w.e.f.-01.04.2020.pdf)
- HT voltage by contract demand: 11 kV up to 3,000 kVA (5,000 kVA with an express feeder), 22 kV up to 7,500 kVA (10,000 kVA express), 33 kV up to 10,000 kVA (20,000 kVA express). This comes from a 2015 MERC order (Case 138 of 2014) — [MSEDCL guideline (Non-SoP)](https://www.mahadiscom.in/consumer/wp-content/uploads/2019/09/Guidelines-Non-SoP.pdf)

**HT connection charges (MSEDCL Schedule of Charges w.e.f. 1 Apr 2020; older, flag)** — [MSEDCL SoC 2020](https://www.mahadiscom.in/consumer/wp-content/uploads/2020/04/Circular-Schedule-of-Charges-for-various-services-of-MSEDCL-w.e.f.-01.04.2020.pdf)
- Service connection charges, overhead: 11 kV up to 1,000 kVA ₹2,20,000; 11 kV 1,000–5,000 kVA ₹2,58,000; 22 kV up to 1,000 kVA ₹2,60,000; 22 kV 1,000–10,000 kVA ₹3,17,000.
- Service connection charges, underground: 11 kV up to 1,000 kVA ₹2,53,000; 11 kV 1,000–5,000 kVA ₹2,64,000; 22 kV up to 1,000 kVA ₹3,05,000; 22 kV 1,000–10,000 kVA ₹3,23,000.
- If the consumer's licensed electrical contractor does the works, MSEDCL charges supervision at 1.30% of normative charges instead. Road-opening charges are at actuals, augmentation for load extension is at actuals, and GST is extra on all items.
- HT metering cubicle with CT/PT (if bought from MSEDCL): 11 kV ₹85,000, 22 kV ₹1,30,000, 33 kV ₹1,90,000. HT ToD meter: ₹2,420–₹5,930. Application/registration for HT up to 33 kV: ₹2,500. HT ToD meter testing at TQA lab: ₹15,000.
- **Extension of load:** where works are needed, normative charges apply on the total load (existing plus additional) at the applicable slab, and augmentation is recovered at actuals.
- **Security deposit:** under the 2021 Supply Code, consumers on a monthly billing cycle deposit 2 months' average bill (previously 1 month). For new HT/EHV consumers it equals "twice of the estimated monthly bill" based on contract demand. It is recalculated annually, and any shortfall is billed as Additional Security Deposit — [MSEDCL Security Deposit estimation sheet](https://wssebill.mahadiscom.in/wss/images/SecurityDeposite_Estimation.pdf); [Hitavada, Apr 2026](https://www.thehitavada.com/Encyc/2026/4/23/msedcl-asks-consumers-to-pay-additional-deposit.html)
- **Transformer prices (asking prices, unverified):** 1,000 kVA 11/0.433 kV oil type ₹6.95 lakh (list valid to 31 Mar 2025), ₹9.5 lakh (Paramex), ₹14.75 lakh (T-Power, EEL-2) and ₹14.9 lakh (Vadodara). 500 kVA ₹4.5 lakh (same dated list) to ₹10 lakh — [servostabilizer.org.in](https://www.servostabilizer.org.in/product/1000-kva-transformer-price/); [IndiaMART Paramex](https://www.indiamart.com/proddetail/1000-kva-11-0-433-distribution-transformer-16989799233.html); [T-Power](https://www.tpowertransformer.in/power-distribution-transformer.html)

**Building supply and outages in Baner**
- Baner–Balewadi residents reported 2–3 hours of daily outages in peak summer 2025, caused by old cables and PMC/Metro digging. A new EHV substation for Aundh–Baner–Balewadi (1.2 lakh consumers) is underway — [Pune Pulse](https://www.mypunepulse.com/?p=90027)
- A 220 kV cable fault in Hinjewadi in July 2025 hit 52,000+ consumers including 70–90 IT firms, with some HT consumers restored later. In April 2025 a 220 kV trip blacked out 66,200 consumers including 200 IT companies for about 3 hours — [The Week, Jul 2025](https://www.theweek.in/wire-updates/national/2025/07/08/bes29-mh-power-outage.html); [Pune Pulse](https://www.mypunepulse.com/?p=141100)
- Statewide MSEDCL reliability data for Jan–Mar 2024 shows monthly SAIDI of about 78–108 minutes and SAIFI of about 0.8–1.1. The table's labels are ambiguous and the data is not Pune-specific — [MERC SoP report Q4 FY24](https://merc.gov.in/wp-content/uploads/2025/02/Q4_SOP-Report_March-2024-Qtr-1.pdf)

### Inferences
- **Effective all-in ₹/kWh for a flat 24×7 load, FY27.** Assumptions: PF about 0.99 so kVAh ≈ kWh; billing demand ≈ facility kW; load factor 80–100%, so the demand charge is ₹650/(730 or 584 h) ≈ ₹0.89–1.11/kWh; ED applied to all consumption charges; TOSE ₹0.19; FAC 0 to +₹0.55.
  - HT-I(A) industrial: ₹9.25 + 0.89–1.11 = ₹10.1–10.4. With 7.5% ED it is ₹10.9–11.1, and with TOSE and FAC about **₹11.1–11.9/kWh**. With the 20-year DC ED exemption it is about **₹10.3–10.9/kWh**.
  - HT-II commercial: ₹14.53 + 0.89–1.11 = ₹15.4–15.6. With 21% ED it is ₹18.7–18.9, and with TOSE and FAC about **₹18.9–19.7/kWh**.
  - LT-II(C) commercial >50 kW: ₹16.42 + ₹0.75–0.94 (at ₹550/kVA). With 21% ED that is about **₹20.8–21.7/kWh**. LT-II(B) 20–50 kW: about **₹17.8–18.6/kWh**.
  - LT-V(B)(ii) industrial >20 kW: ₹9.19 + ₹0.58–0.72. With 7.5% ED that is about **₹10.5–11.4/kWh**.
- **ToD is roughly neutral for a flat GPU load.** With +20% peak, a 24 h flat profile nets about +0.8% (Apr–Sep) and −2.5% (Oct–Mar) of the energy charge, about −0.8% annually. With +25% peak it is about +2.3% and −1.0%, about +0.6% annually.
- **Example annual energy bills.** One 12.5 kW server at PUE 1.5 draws 18.75 kW, or about 164,000 kWh/yr. That costs about ₹18 lakh/yr at ₹11/kWh (industrial) and about ₹31 lakh/yr at ₹19 (HT commercial). Eight servers (100 kW IT, 150 kW facility, about 1.31 GWh/yr) cost about ₹1.45 crore/yr industrial versus ₹2.5 crore/yr commercial.
- **Connection type.** Eight servers at 15 kW is 120 kW IT, or about 170–200 kW facility at PUE 1.4–1.6. That exceeds the about 150 kW / 187 kVA LT limit, so HT 11 kV (or a sub-metered share of the landlord's HT supply) is needed. Up to about 4 air-cooled servers (≤60 kW IT, ≤100 kW facility) fits LT-II(C) or LT-V(B) at the same building. A single NVL72 (about 130 kW IT, about 150–170 kW facility) is at or above the LT limit.
- Baner is within Pune Municipal Corporation limits, so the MC-area LT limit applies. This is my understanding and was not verified in this research.
- **HT one-time MSEDCL-side cost for ≤1,000 kVA at 11 kV:** about ₹2.2–2.5 lakh SCC (or 1.3% supervision if self-executed), about ₹0.85 lakh metering cubicle, plus a security deposit of about 2 months' bill. For a 150 kW facility at ₹11/kWh the bill is about ₹12 lakh/month, so the deposit is about ₹24 lakh, refundable. The consumer-side 11 kV RMU, transformer, HT cabling, LT panel and civil work typically dominate. The transformer alone is about ₹4.5–15 lakh for 500–1,000 kVA.

### Gaps
- I did not find the "#" footnote for the HT industrial/commercial peak ToD surcharge (+20% vs +25%). Verify in the order or MSEDCL's commercial circular for FY27.
- The current FY27 FAC per category is not confirmed. I found no MERC FAC order for Aug–Oct 2026.
- The TOSE rate rests only on one bill sample. I found no official current schedule.
- Whether Pune falls in "Zone-1" for IT/ITeS ED exemption, and the exact registration route for a small in-office GPU room (IT unit LoI vs data-centre unit registration), are unconfirmed. MSEDCL's enforcement history suggests that registration in the unit's own name is essential.
- The current (post-2020) MSEDCL Schedule of Charges is not found; the 2020 figures may have been revised.
- No sourced figures for: 11 kV RMU price, CEIG / Electrical Inspector inspection fees and timelines, HT connection release timelines (SoP), or whether a dedicated HT substation room is mandated (CEA Safety Regulations).
- No source found for typical sanctioned loads of Baner Grade-A office buildings, or for landlord sub-metering practices and pass-through rates.

---

## 2. Cooling: cost per kW, achievable PUE, sizing

### Takeaway
India-specific cooling prices are only available as marketplace asking prices. Precision DX air units list at about ₹1.0–1.5 lakh per TR (about ₹28–43k per kW of cooling, equipment only). A consultancy puts about ₹6 crore per MW (₹60k/kW) for system-level DC cooling. Global consultant benchmarks give rear-door heat exchangers at about $1,800–3,200/kW and direct-to-chip at about $3,500–5,000/kW for small (16-rack) deployments. Indian DCs run at a PUE of about 1.5–1.6. A small Pune room is likely to sit nearer 1.6–2.0 with air cooling, while liquid cooling with dry coolers can do much better.

### Cited Findings
- 5 TR DX precision ACs list at ₹7.25 lakh (New Delhi) and ₹7.5 lakh (Vertiv/Emerson). A Mumbai listing for a 5 TR Vertiv is ₹5 lakh, and a 3 TR 415 V unit is ₹3 lakh. Very low listings (₹60k per 5 TR, ₹2.5 lakh per 30 TR) look erroneous — [IndiaMART directory](https://dir.indiamart.com/impcat/precision-air-conditioners.html); [IndiaMART Mumbai](https://dir.indiamart.com/mumbai/precision-air-conditioners.html); [Aajjo](https://www.aajjo.com/product/precision-air-conditioner)
- About ₹6 crore per MW of cooling load for a large colocation DC — [Blackridge Research](https://www.blackridgeresearch.com/blog/large-colocation-data-center-construction-cost-in-india-complete-capex-opex-breakdown)
- Rear-door heat exchanger (Vertiv) setup: $1,800–3,200/kW. Direct-to-chip: $3,500–5,000/kW (16-rack comparison) — [Adam Silva Consulting, 2026](https://www.adamsilvaconsulting.com/insights/data-center-cooling-economics-2026). Another source puts the DLC premium over air at $2,500–4,500/kW — [Core Insights Review, Sep 2026](https://www.coradvisors.net/2026/09/liquid-vs-air-cooling-cost-comparison-data-centers-2026.html)
- CDU prices conflict by about 10×: $75–150k per 500 kW, $80–200k each, and $12–35k per CDU for 100–500 kW — [Introl](https://introl.com/blog/liquid-vs-air-cooling-ai-data-centers); [datacenterscope](https://datacenterscope.com/cooling/liquid-cooling-cost/)
- Liquid-cooled facilities carry a 7–10% construction premium over air-cooled at equal IT capacity. A Schneider comparison found air-cooled $7.02/W vs liquid-cooled $6.98/W at 10 kW/rack, with liquid getting cheaper as density rises — [Core Insights Review](https://www.coradvisors.net/2026/09/liquid-vs-air-cooling-cost-comparison-data-centers-2026.html)
- Schneider (India, Jul 2026) says direct-to-chip is NVIDIA's recommended approach for high-density AI, and that rear-door heat exchangers top out well below current AI rack needs — [Schneider Electric blog, 30 Jul 2026](https://blog.se.com/datacenter/2026/07/30/planning-liquid-cooling-for-new-ai-data-centre-builds-in-india/)
- STT GDC's Pune Innovation Lab tests in-row cooling (up to 30 kW/rack), RDHx, direct-to-chip and immersion (up to 100 kW/rack) — [STT GDC Pune Innovation Lab](https://www.sttelemediagdc.com/in-en/pune-innovation-lab)
- **PUE benchmarks:** many Indian facilities run at about 1.5–1.6 — [Indian Infrastructure / NITI Aayog consultant, Dec 2025](https://indianinfrastructure.com/2025/12/10/powering-the-ai-era-why-efficiency-standards-must-guide-indias-data-centre-build-out/). Legacy facilities ran at 1.8–2.0, and modern hyperscale is near 1.2 — [CII blog](https://ciiblog.in/indias-data-center-revolution-fuelling-infrastructure-transformation/). JM Financial models PUE 1.5 and notes that facilities older than 10 years exceed 1.5 — [JM Financial Data Centre 101, Mar 2025](https://jmflresearch.com/JMnew/JMCRM/analystreports/pdf/Data-Centre-101_27Mar25.pdf). Yotta's 2020 colocation offer fixed PUE at 1.65 for billing — [Yotta offer page](https://www.yotta.com/upgrade-to-yotta-colocation-offer/)
- **ASHRAE thermal envelope:** recommended inlet 18–27 °C, allowable A1 15–32 °C. Dew-point limits (about 17 °C for A1) constrain humid monsoon operation. Dry coolers are sized on dry-bulb and evaporative systems on wet-bulb — [ASHRAE reference card](https://xp20.ashrae.org/datacom1_4th/ReferenceCard.pdf); [Haskoning](https://www.haskoning.com/en/newsroom/blogs/2025/mastering-data-centre-efficiency-with-ashrae-standards)

### Inferences
- **Air cooling (PAC / in-row) per kW of IT:** equipment at about ₹28–43k per kW of cooling capacity (1 TR = 3.517 kW). With N+1 redundancy, piping, outdoor units and installation, about ₹45–90k per kW of IT is a reasonable planning range for a small room. Air is practical up to about 30 kW/rack with in-row units and containment.
- **RDHx:** about ₹1.6–2.8 lakh/kW of IT at ₹88/USD (global consultant figures; Indian supply may be cheaper). It suits 30–60 kW racks. Yotta uses it for 50–60 kW.
- **Direct-to-chip (CDU + dry cooler/chiller):** about ₹3.1–4.4 lakh/kW at small scale (global figures). For one NVL72 at about 130 kW, the facility-side liquid loop (CDU, dry cooler, trim chiller, piping) could be about ₹1.5–5 crore. This is very uncertain and needs vendor quotes.
- **PUE for the cost model:**
  - Small office server room with DX PACs in Pune: about 1.6–2.0. Summer peaks near 40 °C lower DX efficiency, and dehumidification and reheat in the monsoon add load.
  - Small room with in-row units and containment: about 1.4–1.6.
  - DLC with warm-water dry coolers: about 1.15–1.3. Pune's dry-bulb stays below about 35 °C for most hours, but a trim chiller is needed for the hottest pre-monsoon hours.
  - Large colocation DC: about 1.4–1.6 (Indian average).
- **Sizing notes:** size heat rejection for IT load plus UPS losses (about 3% at 97% efficiency), lighting and pumps (about +10–15%). Use N+1 units. 1 TR ≈ 3.5 kW, so a 100 kW IT room needs about 32–36 TR net, plus redundancy.

### Gaps
- No Indian quotes found for in-row coolers, RDHx, CDUs or dry coolers in INR. No Pune ASHRAE design dry-bulb/wet-bulb or free-cooling-hour data was found.
- No measured PUE data for small Indian server rooms.

---

## 3. Power backup: UPS, batteries, DG sets, diesel

### Takeaway
Modular online UPS lists at about ₹9–19k per kVA in India. Vertiv's India modular line (APM Plus) quotes up to 97% double-conversion and 99% eco-mode efficiency. LFP batteries retail at about ₹20–35k/kWh vs lead-acid at about ₹8–15k/kWh. A 500 kVA CPCB IV+ DG set lists at about ₹39–47 lakh (≈₹7.8–9.4k/kVA) plus 18% GST. It burns about 0.24–0.28 L/kWh at 75% load. Diesel in Pune was about ₹98.6/L in Jul–Sep 2026, so DG energy costs about ₹24–28/kWh in fuel alone.

### Cited Findings
- **Modular UPS listings (India):** ABB modular 100 kVA about ₹18.9 lakh, and a 160 kVA hot-swap modular unit about ₹14.95 lakh. Listings are undated and battery inclusion is unclear — [IndiaMART modular UPS](https://dir.indiamart.com/impcat/modular-ups.html)
- **Lithium-ion premium:** Li-ion adds 20–60% upfront cost vs lead-acid. Global modular UPS bands are $8–25k per 10–20 kVA system and $20–100k per 20–100 kVA — [OpenPR market report](https://www.openpr.com/news/4529180/three-phase-modular-ups-market-to-reach-us-4-45-billion-by-2032)
- **Li-ion TCO:** a 10-year TCO is 39% lower than VRLA despite the capital premium, with "fewer battery replacements (perhaps none)" over UPS life — [Schneider Electric white paper (2022)](https://download.schneider-electric.com/doc/SPD_VAVR-A5AJXY/VAVR-A5AJXY_R1_EN.pdf)
- **UPS efficiency:** Vertiv Liebert APM Plus (India, 50–500 kW) up to 97% double conversion and 99% eco-mode. Liebert APM2 up to 97.5% (global sheet). Liebert eXM up to 97% / 99% — [Vertiv India newsroom](https://www.vertivco.com/en-in/about/newsroom/news-releases/vertiv-introduces-five-capacities-of-liebert-exm/); [CRN India](https://www.crn.in/?p=54993)
- **Battery prices:** India LFP ₹20–35k/kWh vs lead-acid ₹8–15k/kWh in 2026 (solar-retail guide) — [QuickEstimate](https://quickestimate.co/blog/solar-battery-price-india). BNEF 2025 global averages: pack $108/kWh, LFP $81/kWh, stationary $70/kWh — [pv magazine India, Dec 2025](https://www.pv-magazine-india.com/2025/12/10/global-lithium-ion-battery-pack-prices-fall-to-108-kwh-says-bnef)
- **GST on batteries:** electric accumulators other than lithium-ion went from 28% to 18% under GST 2.0 (from 22 Sep 2025). HSN 8507 is listed at 18% — [Swarajya](https://swarajyamag.com/amp/story/news-brief%2Fgst-20-what-gets-cheaper-what-gets-costlier-from-22-september); [Jurishour](https://www.jurishour.in/?p=1457804)
- **DG sets, 500 kVA CPCB IV+ (asking prices):** Kirloskar ₹39 lakh (Navi Mumbai) and ₹41.5 lakh + 18% GST (Jaipur). Cummins (CI 500D5P) ₹43.2 lakh. Sudhir-Cummins ₹43.5 lakh. Greaves CPCB IV ₹47.1 lakh — [IndiaMART Kirloskar](https://www.indiamart.com/proddetail/kirloskar-500-kva-diesel-generator-cpcb-iv-2855145327955.html); [IndiaMART Cummins](https://www.indiamart.com/proddetail/500kva-cpcb-iv-plus-cummins-diesel-generator-2853438686512.html); [TradeIndia](https://www.tradeindia.com/products/500-kva-kirloskar-diesel-generator-c8038346.html); [IndiaMART Greaves](https://www.indiamart.com/proddetail/500kva-diesel-generator-21625551562.html). One buying guide gives ₹29 lakh (Cummins silent) to ₹42 lakh (premium Kirloskar silent) — [Alibaba guide](https://electronics.alibaba.com/buyingguides/500kva-generator-price-guide-what-you-actually-pay-in-2024)
- **DG fuel consumption:** about 215 g/kWh ≈ 0.256 L/kWh at 75% load, or about 76 L/h for a 500 kVA (400 kW) set at 300 kW — [Jubaili Bros](https://jubailibros.com/blogs/fuel-and-efficiency/how-much-fuel-does-a-diesel-generator-consume). An industry FAQ gives 75–85 L/h for 500 kVA at 75% — [Depco](https://www.depco.com/faq/diesel-generator-efficiency/). An Indian listing quotes 72.2 L/h at 75% — [Aajjo](https://www.aajjo.com/product/500-kva-diesel-generator-in-delhi-sanjay-diesels)
- **Diesel price, Pune:** ₹98.63/L on 7 Sep 2026 — [energy.thecore.in](https://energy.thecore.in/fuel/petrol-price/pune). ₹98.66/L on 28 Jul 2026 — [Upstox](https://upstox.com/diesel-price/diesel-price-in-pune/). ₹90.52/L on 13 May 2026 — [Business Today](https://www.businesstoday.in/fuel-price/diesel-price-in-pune-today). ₹90.34/L on 8 Feb 2026 — [BankBazaar](https://tmw.bankbazaar.com/fuel/diesel-price-pune.html)
- **DG AMC (vendor listings, scope unclear):** ₹6.5–8k/yr (10–500 kVA, Delhi), ₹12k/yr (7.5–2,000 kVA, Pune), ₹15–35k/yr (Ahmedabad). An unverified 2,250 kVA Cummins TCO sheet uses ₹4.2 lakh/yr — [IndiaMART Sky Light](https://m.indiamart.com/skylight-power-solution/genset-amc-service.html); [Scribd TCO](https://www.scribd.com/document/437635310/TCO)
- **Grid outage context** is in section 1: Baner summer outages of 2–3 h/day in 2025, and 220 kV failures in Hinjewadi.

### Inferences
- **UPS sizing:** for 100 kW IT at N+1 modular, about 125–150 kVA, which is about ₹12–28 lakh before batteries. UPS losses are about 3% (97%) in double-conversion, or about 1% in eco-mode.
- **Battery for 10 minutes at 150 kW** is 25 kWh usable, or about 35–50 kWh nominal after DoD and ageing margin. That is about ₹7–17 lakh LFP or ₹3–7 lakh VRLA. VRLA replacement every 3–5 years vs Li-ion 8–10+ years (user-provided cycles, consistent with Schneider's "perhaps none" statement) usually makes Li-ion cheaper over 10 years.
- **DG sizing:** a 150–200 kW facility needs about a 250–320 kVA DG. Per-kVA prices for smaller sets are likely higher than the 500 kVA ₹7.8–9.4k/kVA, so budget about ₹22–32 lakh plus 18% GST for 250–320 kVA (extrapolated, not sourced).
- **DG running cost:** 0.24–0.28 L/kWh × ₹98.6/L ≈ ₹23.7–27.6/kWh. That is about 2.2–2.5× the HT industrial grid cost. At 2–3 h/day of outages (Baner summer worst case) on a 150 kW load, fuel alone is about ₹2.3–3.7 lakh/month in outage months.
- **Diesel taxation:** diesel is outside GST (VAT and excise apply), so there is no input tax credit. This is general knowledge and was not verified here.

### Gaps
- No dated Vertiv/Schneider India price list for modular UPS per kVA, and none for Li-ion UPS cabinets per kWh in India.
- No DG prices for 250 kVA or 1,000 kVA CPCB IV+, and no reliable comprehensive-AMC price.
- The diesel price for 19 Oct 2026 is not confirmed. The latest found is ₹98.63 on 7 Sep 2026.
- No Pune-specific annual SAIDI/SAIFI data.

---

## 4. Building, safety, permits and Baner lease

### Takeaway
IT-grade raised floor costs about ₹200–450/sq ft installed (heavy-duty ₹400–650). Clean-agent suppression for a small server room is about ₹1–4.5 lakh per pre-engineered system. VESDA units are about ₹1.15–4.75 lakh each. Office floors are designed for about 2.5 kN/m² (computer rooms 3.5 kN/m²), far below the roughly 15–25 kN/m² footprint pressure of a 1–1.5 t rack, so structural review and load spreading are mandatory. Pune Grade-A office rents average about ₹82–90/sq ft/month, and Baner/Balewadi asking rents run about ₹35–125 (new warm shell about ₹100) plus about ₹12 maintenance.

### Cited Findings
- **Raised floor:** IT grade ₹200–450/sq ft installed (300–600 mm void). Data-hall heavy grade ₹400–650/sq ft. Epoxy seal ₹40–90/sq ft. A calculator default is about ₹320/sq ft + 18% GST ≈ ₹378 all-in — [StudioMatrx flooring guide](https://www.studiomatrx.org/guides/data-centre-flooring-india); [StudioMatrx calculator](https://www.studiomatrx.org/utilities/raised-access-floor-calculator)
- **Whole-DC benchmarks:** JM Financial puts average Indian colocation capex at ₹465 mn/MW (USD 5.4 mn), about ₹24.2k per sq ft, with a range of ₹333–592 mn/MW — [JM Financial, Mar 2025](https://jmflresearch.com/JMnew/JMCRM/analystreports/pdf/Data-Centre-101_27Mar25.pdf). Cushman & Wakefield's India median is $6.8 mn/MW. CareEdge puts new capacity at ₹60–70 crore/MW — [verified.realestate summary](https://corporate.verified.realestate/insights/data-centre-investment-economics-capex). Turner & Townsend (2025) puts Mumbai DC construction at $6.64/W — [Storyboard18](https://www.storyboard18.com/digital/mumbai-ranks-second-cheapest-city-worldwide-for-data-centre-construction-83986.htm)
- **Floor loading (IS 875 Part 2):** office general 2.5 kN/m² UDL, office with storage 4 kN/m², and computer rooms 3.5 kN/m² UDL / 4.5 kN concentrated. Sources conflict slightly — [Infralens handbook](https://infralens.in/handbook/live-loads); [Infralens IS 875](https://infralens.in/code/IS-875-Part-2-1987)
- **Clean-agent suppression (IndiaMART, per system):** pre-engineered Novec 1230 for a server room ₹1.55 lakh. FM-200/Novec DC system ₹2 lakh/set. 18 kg Novec 1230 six-cylinder system ₹4.5 lakh/set. Low-end listings at ₹20–54k look like small modules — [IndiaMART](https://www.indiamart.com/proddetail/data-center-server-room-fire-suppression-fm-200-novac-1230-25406075362.html); [IndiaMART Novec directory](https://dir.indiamart.com/impcat/novec-1230-fire-suppression-system.html). US benchmark: Novec 1230 $30–80k per room, FM-200 $25–75k per room — [Firetron](https://firetron.com/fire-suppression-systems/best-fire-suppression-systems-data-centers-server-rooms/)
- **VESDA (dealer asking prices):** VLF-250 (≤250 m²) ₹1.23–1.55 lakh. VLF-500 (≤500 m²) ₹1.15–1.75 lakh. VESDA-E VEP ₹4.75 lakh. Generic ASD from ₹70k — [TradeIndia](https://www.tradeindia.com/manufacturers/vesda-system.html); [IndiaMART ASSD](https://m.indiamart.com/impcat/air-sampling-smoke-detection-system.html)
- **Pune office rents:** H1 2026 average transacted rent ₹81.7/sq ft/month (+6% YoY) on a record 6.6 mn sq ft half-year leasing (Knight Frank) — [Punekar News](https://www.punekarnews.in/pune-records-highest-ever-half-year-office-leasing-in-h1-2026-residential-sales-remain-resilient-as-launches-rise-17-yoy/). Q1 CY26 market rent ₹90.2/sq ft/month with 15.5% vacancy — [CRE Matrix](https://www.crematrix.com/blog/india-office-market-q1-cy26-key-trends-and-city-wise-performance/)
- **Baner/Balewadi asking rents:** about ₹35–125/sq ft/month across listings. A 31,000 sq ft Balewadi warm shell asks ₹100/sq ft. A High Street listing asks ₹90/sq ft chargeable + ₹12/sq ft maintenance on carpet — [myHQ SBH Balewadi](https://myhq.in/office-space-for-rent/sbh--balewadi); [NoBroker Baner](https://www.nobroker.in/furnished-office-space-for-rent-in-baner-pune); [Purple Realtors](https://purplerealtors.com/Resale-Rental/For-Lease-5100-sqft-Office-Space-Available-in-High-Street-Baner-Balewadi-Pune/Balewadi/Pune/100)
- **Fire NOC:** PMC fire NOC is part of PMC building approvals, and costs depend on project size and type. No rate schedule was found — [Casagrand blog](https://www.casagrand.co.in/blog/cost-of-construction-in-pune-detailed-breakdown-for-homebuyers/). The PMRDA fire NOC checklist applies outside PMC/PCMC limits only — [PMRDA checklist 2025](https://www.pmrda.gov.in/wp-content/uploads/2025/03/Provisional-NOC-File-Checklist.pdf)

### Inferences
- **Rack floor pressure:** a 1.0–1.5 t rack on a 0.6 × 1.2 m footprint (0.72 m²) puts about 14–20 kN/m² on its footprint. That is roughly 4–8× the 2.5–3.5 kN/m² office/computer-room design load. A structural engineer's check plus steel load-spreading plinths (or ground-floor/podium placement) is needed. An NVL72-class rack (about 1.4 t) is the worst case.
- **Room size and fit-out:** a room for 2–4 racks plus a UPS/battery room is about 400–800 sq ft. A rough fit-out excluding M&E is about ₹1,500–3,500/sq ft. That covers raised floor or plinths, cable trays, earthing pits, access control, CCTV, fire-rated partitions, clean-agent suppression and VESDA, so about ₹6–28 lakh. This is my estimate assembled from the component prices above, not a sourced figure.
- **Lease for 600–1,000 sq ft in Baner:** at ₹80–110/sq ft plus ₹12 maintenance, about ₹0.55–1.2 lakh/month, plus 18% GST on commercial rent (general knowledge) and typically 6–10 months' deposit (market convention, not sourced). Landlords may restrict DG, battery or chemical-agent installation, and floor loading may be the binding constraint.

### Gaps
- No sourced per-sq-ft costs for cable trays, access control, CCTV or earthing in Pune.
- No PMC Fire Brigade NOC fee schedule or timelines for a server-room fit-out inside an existing building.
- No Baner micro-market Grade-A rent from a broker report (only listings and citywide averages).

---

## 5. Colocation in Pune and Navi Mumbai: providers, pricing, high density, fees

### Takeaway
The best dated benchmark is JM Financial's (Mar 2025) monthly recurring revenue (MRR) per kW, excluding power. Pune is about ₹7,688/kW/month for sub-250 kW deals versus Mumbai ₹9,750. Power is passed through on top at tariff × PUE, which JM models at ₹10/kWh × 1.5. That makes all-in Pune colocation for 100 kW IT about ₹18–19k per kW-month (about ₹18.6 lakh/month + 18% GST). Pune has STT GDC (5 sites), Nxtra (Pune II at 21 MW, Pune III at 40 MW due Q4 2026), AdaniConneX, Iron Mountain/Web Werks, NES Data and others. No Pune operator publicly advertises liquid-cooled racks. Navi Mumbai does: Sify claims 130+ kW/rack and NVIDIA DGX-Ready status, Yotta NM1 claims RDHx at 50–60 kW and DLC up to 80 kW, RackBank claims up to 150 kW, and CapitaLand/Vertiv has a 30 MW DLC deployment. No Indian price list for liquid-cooled racks was found.

### Cited Findings
- **JM Financial MRR (₹/kW/month, excluding power), from Exhibit 60** — [JM Financial Data Centre 101, 27 Mar 2025](https://jmflresearch.com/JMnew/JMCRM/analystreports/pdf/Data-Centre-101_27Mar25.pdf):

| Deal size | Mumbai | Pune | Chennai | Blended |
|---|---|---|---|---|
| Sub-250 kW | 9,750 | 7,688 | 8,625 | 8,652 |
| 250 kW–1 MW | 8,438 | 7,238 | 8,250 | 7,913 |
| 1–5 MW | 7,313 | 6,750 | 7,500 | 7,194 |
| 5 MW+ | 6,938 | 6,188 | 6,563 | 6,638 |

  JM's 2030E average MRR is Mumbai ₹9,866 and Pune ₹8,475. Its 1 MW P&L assumes MRR ₹9,500/kW growing 6%/yr, with utilities "typically a pass-through on top of the rentals". It models electricity at ₹10/kWh × 730 h = ₹7,300/kW-month at PUE 1.5. The same source estimates Pune capacity at about 68 MW in 2024 and 183 MW by 2030E.
- **Yotta NM1 offers:**
  - Undated "celebration offer": enclosed 48U rack with up to 6 kVA bundled at ₹4,99,999 (the period, monthly or annual, is unclear). It includes 5 remote-hand tickets per month and 25 Mbps internet, with a one-time charge of ₹49,999 and taxes extra — [Yotta celebration offer](https://www.yotta.com/lp/yotta-nm1-datacenter-colocation-celebration-offer/)
  - 2020 offer: ₹99,999/month for 5 × 42U racks, with power at ₹7.57/unit and PUE 1.65 fixed for 3 years. It includes 2 copper cross-connects, 25 remote-hand tickets per year and 100 Mbps; taxes extra; valid until 31 Jul 2020 (old) — [Yotta upgrade offer](https://www.yotta.com/upgrade-to-yotta-colocation-offer/)
- **Third-party India colocation estimates (vendor blogs, low reliability):** full rack ₹60k–1.2 lakh/month with 4–6 kW (up to 30 kW high-density option), and metered power above the allowance at ₹10–12/kWh — [itforsme Yotta page](https://www.itforsme.in/pricing/yotta-colocation-india). ₹12–25k per kW/month all-in, and Mumbai full rack ₹55–90k/month — [Cyfuture](https://cyfuture.cloud/kb/colocation/colocation-prices-across-major-data-centers-in-india-and-abroad). Published lists include Xenax ₹74,999/month for a 42U rack with 10 kW A+B, and RackBank ₹87,000/month for a 42U rack with 6 kVA — [Xenax](https://xenaxcloud.com/blog/full-rack-colocation-pricing/); [RackBank](https://www.rackbank.in/colocation/)
- **Remote hands and cross-connects (vendor blog, conflicting):** remote hands ₹500–1,500/hr in one article and ₹2,000–5,000/hr in another. Cross-connects ₹3,000–6,000, with the billing unit unclear — [Cyfuture KB](https://cyfuture.cloud/kb/howto/how-much-does-server-colocation-cost-in-india)
- **Pune facilities:** 22 facilities from 10 providers. STT GDC Pune 1–5 (Dighi, Alandi Road) with about 81 MW operational. Nxtra Pune and Pune II (21 MW), with Pune III (40 MW) under construction. AdaniConneX at about 19.2 MW operational with 67 MW under construction. Microsoft (Pimpri DC1, 28 MW). Iron Mountain, Tata Communications, Net4, NES Data (Pune; Talegaon 10 MW under construction), NICSI and Silvernox. No liquid cooling is mentioned for any of them — [Baxtel Pune](https://baxtel.com/data-center/pune). Nxtra Pune III has an estimated Q4 2026 launch — [Baxtel via search](https://baxtel.com/data-center/pune)
- Iron Mountain (formerly Web Werks) PUN-1 in Hinjewadi: 38,000 sq ft, carrier-neutral, 1.6 MW — [Iron Mountain Pune](https://www.ironmountain.com/data-centers/locations/apac/pune-data-center)
- **Navi Mumbai high-density / liquid-cooled options:**
  - Sify (Rabale/Airoli/Vashi) advertises 130+ kW per rack and NVIDIA DGX-Ready certification for liquid cooling — [Sify Mumbai DC](https://www.sifytechnologies.com/data-center/mumbai-data-center/)
  - Yotta uses RDHx for 50–60 kW per rack and DLC up to 80 kW — [itforsme / Yotta material](https://www.itforsme.in/pricing/yotta-colocation-india)
  - RackBank Navi Mumbai (WST1) claims up to 150 kW per rack with hybrid DLC — [RackBank Mumbai](https://www.rackbank.com/ai-datacenters/mumbai.html)
  - Vertiv deployed DLC for 30 MW of AI capacity at CapitaLand's CLDC Mumbai 01 in Airoli (Oct 2026) — [TechNode Global, 16 Oct 2026](https://technode.global/2026/10/16/vertiv-capitaland-mumbai-liquid-cooling/)
  - Colt DCS/RMZ started building Mumbai 3 (64 MW, hybrid air + DLC, pre-let to a hyperscaler) — [PR Newswire](https://www.prnewswire.com/news-releases/colt-dcs-and-rmz-begin-construction-of-third-data-centre-in-mumbai-to-support-growing-ai-demand-302908543.html)
- **GPU colocation price benchmarks (US/UK, not India):** $130–300/kW/month in US markets. The liquid-cooling surcharge is $500–2,000/rack/month in one source and $1,000–4,000/rack/month in another. A UK 30 kW liquid-cooled rack is £2,500–4,000/month. Power billing, cross-connects and remote hands add 25–30% — [aidatacenterfinder](https://aidatacenterfinder.com/blog/colocation-pricing-2026); [ClusterBid](https://clusterbid.com/blog/gpu-colocation-pricing-guide-2026-power-space-interconnect)

### Inferences
- **Power pass-through model:** monthly power ≈ IT kW × 730 h × PUE × tariff.
  - In Pune or Navi Mumbai, a DC registered as industrial with the 20-year ED exemption has a cost base of about ₹10–11/kWh. Operators also add a margin, which Yotta's ₹10–12/kWh metered rate suggests.
  - At ₹10/kWh and PUE 1.5 that is ₹10,950/kW-IT/month. At PUE 1.3 (liquid-cooled hall) it is about ₹9,490.
- **All-in Pune colocation for sub-250 kW (2024 MRR basis):** ₹7,688 + ₹10,950 ≈ ₹18.6k per kW-IT/month. The Mumbai equivalent is about ₹20.7k. Escalating MRR 6%/yr to 2026 gives Pune MRR about ₹8.6k and all-in about ₹19.6k/kW-month.
  - 1 server (12.5 kW IT): about ₹2.3–2.5 lakh/month.
  - 8 servers (100 kW IT): about ₹18.6–19.6 lakh/month, or about ₹2.2–2.4 crore/yr.
  - All plus 18% GST, which is input-creditable for a GST-registered business.
- **One NVL72 (about 130 kW):** applying Mumbai MRR plus a liquid premium gives roughly ₹12.7 lakh MRR + ₹9.5k × 130 ≈ ₹12.3 lakh power, about ₹25 lakh/month before any CDU/liquid surcharge. A US-style liquid surcharge of $1–4k/rack/month adds about ₹0.9–3.5 lakh. This is speculative, and real quotes from Sify, Yotta or RackBank are needed.
- **Location:** Pune colocation is about 20% cheaper on MRR than Mumbai, but Pune's high-density supply is unadvertised. For 30–130 kW racks in 2026, Navi Mumbai (about 150 km from Baner) is the realistic option unless STT GDC Pune or Nxtra Pune III offers DLC on request.
- **Remote hands:** with a few incidents a month, budget about ₹5–25k/month, or use bundled tickets (Yotta bundles 5 tickets/month). Cross-connects are often bundled in small numbers and otherwise about ₹3–6k each (unit unclear).

### Gaps
- No 2026 Indian per-kW price for liquid-cooled or >30 kW racks from any operator.
- No public pricing or facility detail found for NTT Mumbai, CtrlS Navi Mumbai, Princeton Digital Group MUM1/2 or Equinix MB1–MB4. I found no Sify, Yotta or NTT facility in Pune.
- The JM MRR data is a 2024-basis sell-side estimate, not a rate card. Actual small-deal (1–2 rack) retail pricing can be much higher per kW.
- No authoritative cross-connect or remote-hands rate card (only vendor blogs).

---

## 6. Connectivity: enterprise ILL in Pune

### Takeaway
Indicative ILL rates (before 18% GST, 12-month term, tier-1 fibre zones) are about ₹25–38k/month for 100 Mbps and about ₹70k–2.5 lakh/month for 1 Gbps, with most quotes at ₹0.9–1.5 lakh. Installation is ₹15–50k if fibre must be extended. No official Tata, Airtel or Jio rate cards were found.

### Cited Findings
- **Bands:** 10 Mbps ₹6–7k, 50 Mbps ₹12–20k, 100 Mbps ₹25–38k, 500 Mbps ₹75–95k, 1 Gbps ₹1.5 lakh+ per month before 18% GST. Installation is ₹15–50k (often waived on 24–36-month terms). SLA ranges from 99.5% (low tiers) to 99.99% (1 Gbps). Addresses outside commercial corridors cost 30–50% more — [itforsme ILL India](https://www.itforsme.in/pricing/internet-leased-line-india)
- 1 Gbps can cost ₹70k–2.5 lakh/month — [Internet Express, 2026](https://internetexpress.co.in/1-gbps-leased-line-cost-in-india/). A Tata reseller lists 1 Gbps at ₹90k/month and 10 Mbps at about ₹8k — [Positive Communication](https://positivecommunication.in/tata-leased-line/)
- One blog says Airtel ILL starts at ₹20k/month (10 Mbps–1 Gbps) and Jio is ₹15–50k/month for 100 Mbps–1 Gbps (single source) — [ACT blog, Apr 2025](https://actcorpdotblog.wordpress.com/2025/04/02/top-leased-line-plans-in-india-for-businesses/)

### Inferences
- Plan for two diverse ILLs (for example Tata + Airtel) on an LLM-serving room. At 1 Gbps each that is about ₹1.8–3 lakh/month + GST; at 100 Mbps each about ₹50–75k/month. Baner is an established commercial corridor, so it is likely within the base bands.

### Gaps
- No Pune-specific or carrier-official ILL quotes; all figures are reseller or blog estimates.

---

## 7. People and insurance

### Takeaway
Salary data for Pune is thin and comes mostly from modelled sites. A mid-level MLOps/LLM-infra engineer is about ₹17–35 LPA (GPU/infra specialists about ₹13–21 LPA on a small sample, senior ₹38–65 LPA). A Linux sysadmin is about ₹3–10 LPA (average about ₹5–6 LPA). NOC operators are about ₹2–6 LPA. A DC operator with 7–9 years' experience is about ₹6.5–7.5 LPA. One 24×7 seat needs about 4.5–5 FTE. The only EEI rates found are the old public-sector tariff (1.0% general, 1.25% for computers with AMC, 2.5% without). Current de-tariffed market rates are likely lower but unverified.

### Cited Findings
- **MLOps, Pune:** ₹6–16 LPA (2025, unsourced table) — [GeeksforGeeks](https://geeksforgeeks.org/mlops-engineer-salary-in-india-2024). AI/ML engineer in Pune ₹17.4–19.2 LPA (citing AmbitionBox) — [IIT KGP Online blog](https://online.iitkgp.ac.in/blog/ai-ml-engineer-salary-india)
- **MLOps, India by experience (Jul 2026):** entry ₹8–15L, mid (3–5 years) ₹20–35L, senior ₹38–65L — [OwnYourCareer](https://www.ownyourcareer.in/careers/mlops-engineer/salaries). Mid-career band ₹20–45L — [CorpReady](https://corpready.in/salary/mlops-engineer). GenAI/LLM engineers ₹12–40L (0–5 years) and ₹45–85L (6–8 years) — [CareerIndia 2026](https://www.careerindia.com/news/india-ai-gpu-hiring-2026-salary-packages-job-roles-access-subsidized-compute-011-66277.html)
- **GPU engineer, India (Glassdoor, 7 submissions):** average ₹17 LPA, 25th–75th percentile ₹12.7–21 LPA, 90th percentile ₹23 LPA — [Glassdoor India](https://static.glassdoor.co.in/Salaries/gpu-salary-SRCH_KO0,3_P2.htm)
- **Linux sysadmin, Pune (Payscale 2026):** average base about ₹4.8 LPA, 10th–90th percentile ₹2.8–9.9 LPA. "Linux Systems Administrator" average about ₹5.9 LPA, 25th–75th percentile ₹3.6–8.8 LPA — [Payscale Linux SA Pune](https://www.payscale.com/research/IN/Job=Linux_System_Administrator/Salary/68d9e97c/Pune); [Payscale Linux Systems Admin Pune](https://www.payscale.com/research/IN/Job=Linux_Systems_Administrator/Salary/c9a5d216/Pune)
- **NOC engineer, Pune (Payscale):** average about ₹2.55 LPA with a 90th percentile of about ₹10 LPA. With switching/routing skills the average is ₹3.6 LPA — [Payscale NOC Pune](https://www.payscale.com/research/IN/Job=Network_Operations_Center_(NOC)_Engineer/Salary/4bc4a2d1/Pune)
- **Data centre operator, Pune (Glassdoor, 1 submission):** ₹6.45–7.51 LPA at 7–9 years — [Glassdoor India](https://static.glassdoor.co.in/Salaries/data-centre-operator-salary-SRCH_KO0,20.htm)
- **EEI (old public-sector tariff):** sum insured at present-day replacement value; rate 1.00%, rising by 100% without an AMC; computers 1.25% with AMC and 2.50% without — [National Insurance EEI](https://nationalinsurance.nic.co.in/en/industrial-risk-insurance/electronic-equipment-insurance). The sum insured should be new replacement value including duty, freight and installation — [Royal Sundaram](https://stage2.royalsundaram.in/business-insurance/engineering-insurance/electronic-equipment-insurance). A co-op bank's 2026 tender insured about ₹9.46 crore of data-centre electronics under EEI, but the rates were not visible — [KCC Bank tender 2026](https://kccbhp.bank.in/wp-content/uploads/2026/02/Format_Insurance-2026.pdf)

### Inferences
- **24×7 coverage:** 8,760 h/yr ÷ about 1,900–2,000 productive h per FTE gives about 4.4–4.6 FTE per seat, or about 5 with leave and training.
  - At NOC/technician rates of ₹3–7 LPA that is about ₹15–35 lakh/yr per 24×7 seat, plus about 10–20% for benefits, shift allowance and management.
  - Many small operators instead use day-shift engineers with on-call cover plus colocation remote hands.
- **Planning CTCs (Pune, 2026):**
  - MLOps/LLM infra engineer: about ₹18 / 28 / 45 LPA (low / typical / high).
  - Linux/HPC sysadmin: about ₹5 / 9 / 18 LPA. HPC/GPU-cluster skills push towards the top of that range.
  - DC facility technician (electrical/HVAC): about ₹3 / 5 / 8 LPA. This is extrapolated from DC operator/NOC data, with no direct source.
  - NOC operator: about ₹2.5 / 4 / 6 LPA.
- **EEI planning range:** about 0.3–1.25% of sum insured per year. Old tariff floor 1.0–1.25% (with AMC); de-tariffed market likely 0.3–0.8% (unverified). GST is 18% on the premium, which is general knowledge. For ₹3–25 crore of GPU servers that is about ₹1–30 lakh/yr. Fire/burglary (property) cover may be separate.

### Gaps
- No AmbitionBox/Naukri Pune data for MLOps, HPC, DC facility technician or NOC roles. Payscale/Glassdoor samples are small or modelled.
- No current market EEI rate (% of SI) from an insurer quote or tender award for servers or GPUs.

---

## 8. Consolidated cost-model input table

### Takeaway
The key swing factors are the electricity category (industrial/DC-registered at about ₹10.3–11.9/kWh vs commercial at about ₹19–21/kWh) and liquid-cooling capex. Colocation in Pune is about ₹18–20k per kW-IT/month all-in for small deals, while high-density/liquid colocation realistically means Navi Mumbai with quote-based pricing. All marketplace prices are asking prices.

### Inferences
- "Typical" values are my central picks from the cited ranges. Where a row says "inference", it is derived arithmetic rather than a direct quote.
- GST notes:
  - **Electricity** is outside or exempt from GST, and electricity duty applies instead. This is general knowledge, not verified here.
  - **18%** applies to MSEDCL service charges, equipment (DG, UPS, Li-ion, AC/PAC after 22 Sep 2025), colocation, ILL, rent and insurance premiums. MSEDCL service charges, DG and ILL at 18% are sourced; the rest are general knowledge.
  - **Diesel** is outside GST.

### Gaps
- See the section-level gaps above. The table rows marked "unverified" or "inference" should be replaced by quotes.

### Cited Findings: consolidated table

| item | unit | low_inr | typical_inr | high_inr | notes (incl. GST) | source | date |
|---|---|---|---|---|---|---|---|
| HT-I(A) industrial demand charge | ₹/kVA/month | 600 | 650 | 650 | FY26 ₹600 (from 1 Jul 2025); FY27 ₹650. No GST; ED applies. Data centres are classified Industrial | [MERC Case 75/2025 post-remand](https://www.mahadiscom.in/wp-content/uploads/2026/07/Tariff-Order_Case-No.-75-of-2025-dated-25th-March-2026.pdf) | 25 Mar 2026 |
| HT-I(A) industrial energy + wheeling | ₹/kVAh | 9.25 | 9.25 | 9.42 | FY27 8.44 + 0.81; FY26 8.68 + 0.74; EHV has no wheeling (8.44) | same | 25 Mar 2026 |
| HT-II commercial demand charge | ₹/kVA/month | 600 | 650 | 650 | FY26 / FY27 | same | 25 Mar 2026 |
| HT-II commercial energy + wheeling | ₹/kVAh | 14.53 | 14.53 | 14.77 | FY27 13.72 + 0.81; FY26 14.03 + 0.74 | same | 25 Mar 2026 |
| LT-II(B) commercial 20–50 kW | ₹/kVA/month; ₹/kVAh | 525; 13.92 | 550; 13.92 | 550; 14.22 | FY27 550 & 12.40 + 1.52; FY26 525 & 14.22 | same | 25 Mar 2026 |
| LT-II(C) commercial >50 kW | ₹/kVA/month; ₹/kVAh | 525; 16.42 | 550; 16.42 | 550; 16.61 | FY27 550 & 14.89 + 1.52; FY26 525 & 16.61 | same | 25 Mar 2026 |
| LT-V(B)(ii) industry >20 kW | ₹/kVA/month; ₹/kVAh | 400; 9.15 | 420; 9.19 | 420; 9.19 | FY27 420 & 7.66 + 1.52 | same | 25 Mar 2026 |
| ToD solar rebate (09–17 h) | % of energy charge | −25 | −20 (annual average) | −15 | FY26–27: −15% Apr–Sep, −25% Oct–Mar; −20/−30% from FY28 | same, Table 8 | 25 Mar 2026 |
| ToD peak surcharge (17–24 h) | % of energy charge | +20 | +20 | +25 | Order shows +20%#; MYT note said +25% for LT/HT industrial & commercial. Confirm | same; [MERC press note](https://merc.gov.in/wp-content/uploads/2025/03/Press-Note_MSEDCL-MYT-Order_English.pdf) | Mar 2025 / Mar 2026 |
| Power-factor incentive/penalty | – | – | built into kVAh billing | – | No separate PF incentive; kVAh billing for HT and LT >20 kW | same, para 4.6.9 | 25 Mar 2026 |
| Electricity duty, industrial | % of consumption charges | 0 | 7.5 | 7.5 | 0% if DC unit exempt (20 yrs, notif. 22 Jun 2026) | [MSEDCL Circ. 329](https://www.mahadiscom.in/consumer/wp-content/uploads/2020/09/Commercial-Circular-329-Revision-in-Rate-of-ED-of-Industrial-Consumer.pdf); [TeamLease](https://teamleaseregtech.com/updates/article/57168/govt-of-maharashtra-issued-a-notification-regarding-electricity-duty-e/) | Sep 2020 / Jun 2026 |
| Electricity duty, commercial | % of consumption charges | 21 | 21 | 21 | IT/ITeS units in IT parks may be exempt for 10–15 yrs | [MSEDCL Circ. 273](https://www.mahadiscom.in/consumer/wp-content/uploads/2018/02/Comm_Cir_273.pdf) | Sep 2016 |
| Tax on sale of electricity | ₹/kWh | 0.15 | 0.19 | 0.19 | Single bill sample (19.04 paise); unverified | [Scribd bill](https://www.scribd.com/document/913142723/E-bill) | Jan 2025 |
| FAC | ₹/kWh | 0 | 0.30 | 0.60 | Monthly variable; news reports +20 to +60 paise for Aug | [Pune Pulse](https://www.mypunepulse.com/msedcl-august-electricity-bill-why-your-bill-may-rise-and-how-much-extra-you-may-pay/) | 2026 (unclear) |
| All-in grid cost, HT industrial (DC-registered) | ₹/kWh | 10.3 | 10.8 | 11.9 | Inference: flat load, 80–100% LF; low end ED-exempt; high end with 7.5% ED + TOSE + FAC | derived from MERC order | Oct 2026 |
| All-in grid cost, HT commercial | ₹/kWh | 18.9 | 19.2 | 19.7 | Inference, with 21% ED | derived | Oct 2026 |
| All-in grid cost, LT-II(C) commercial | ₹/kWh | 20.8 | 21.2 | 21.7 | Inference, with 21% ED | derived | Oct 2026 |
| LT supply limit (MC area) | kW / kVA | 150 / 187 | 150 / 187 | 480 / 600 | 480/600 for multi-consumer single-point buildings; 80/100 outside MC areas | [MERC SoP memo](https://merc.gov.in/wp-content/uploads/2022/07/Explanatory-Memorandum_SoP_2017.pdf) | 2017 (flag) |
| HT service connection charge, 11 kV ≤1,000 kVA | ₹ one-time | 220,000 | 253,000 | 305,000 | Overhead 2.20 L / underground 2.53 L; 22 kV UG 3.05 L; or 1.3% supervision if LEC executes; +18% GST | [MSEDCL SoC 2020](https://www.mahadiscom.in/consumer/wp-content/uploads/2020/04/Circular-Schedule-of-Charges-for-various-services-of-MSEDCL-w.e.f.-01.04.2020.pdf) | 1 Apr 2020 (older) |
| HT metering cubicle (CT/PT) | ₹ one-time | 85,000 | 85,000 | 130,000 | 11 kV ₹85k; 22 kV ₹1.3 L; + HT ToD meter ₹2.4–5.9k; +GST | same | 1 Apr 2020 |
| HT application/registration | ₹ one-time | 2,500 | 2,500 | 2,500 | +GST | same | 1 Apr 2020 |
| Security deposit (HT) | months of bill | 2 | 2 | 2 | ≈2× estimated monthly bill; recalculated annually; refundable | [MSEDCL SD sheet](https://wssebill.mahadiscom.in/wss/images/SecurityDeposite_Estimation.pdf) | 2021 Code / 2026 |
| Distribution transformer 500 kVA, 11/0.433 kV | ₹ each | 450,000 | 700,000 | 1,000,000 | Asking prices; usually ex-GST (18%) | [servostabilizer.org.in](https://www.servostabilizer.org.in/product/1000-kva-transformer-price/); IndiaMART | ≤Mar 2025 |
| Distribution transformer 1,000 kVA | ₹ each | 695,000 | 950,000 | 1,490,000 | Asking prices; ex-GST | [IndiaMART](https://www.indiamart.com/proddetail/1000-kva-11-0-433-distribution-transformer-16989799233.html); [T-Power](https://www.tpowertransformer.in/power-distribution-transformer.html) | 2025 |
| Precision AC (DX PAC) | ₹ per TR | 100,000 | 125,000 | 150,000 | Equipment only (₹5–7.5 L per 5 TR); GST 18% after 22 Sep 2025 (was 28%) | [IndiaMART PAC](https://dir.indiamart.com/impcat/precision-air-conditioners.html); [Vision IAS GST](https://visionias.in/current-affairs/upsc-daily-news-summary/article/2025-09-04/the-indian-express/economy/gst-20-unveiled-new-rates-will-come-into-effect-september-22) | 2025–26 |
| Air cooling installed (PAC/in-row, N+1) | ₹ per kW IT | 45,000 | 60,000 | 90,000 | Inference from PAC prices + ₹6 cr/MW benchmark; +18% GST | [Blackridge](https://www.blackridgeresearch.com/blog/large-colocation-data-center-construction-cost-in-india-complete-capex-opex-breakdown) | 2025 |
| Rear-door heat exchanger | ₹ per kW IT | 158,000 | 220,000 | 282,000 | $1,800–3,200/kW at ₹88/USD; small deployment; global | [Adam Silva](https://www.adamsilvaconsulting.com/insights/data-center-cooling-economics-2026) | 2026 |
| Direct-to-chip liquid (CDU + heat rejection) | ₹ per kW IT | 220,000 | 350,000 | 440,000 | $2,500–5,000/kW; global; very uncertain for India | same; [Core Insights](https://www.coradvisors.net/2026/09/liquid-vs-air-cooling-cost-comparison-data-centers-2026.html) | 2026 |
| PUE, small air-cooled room (Pune) | ratio | 1.5 | 1.7 | 2.0 | Inference; Indian DC average 1.5–1.6, legacy 1.8–2.0 | [Indian Infrastructure](https://indianinfrastructure.com/2025/12/10/powering-the-ai-era-why-efficiency-standards-must-guide-indias-data-centre-build-out/); [CII](https://ciiblog.in/indias-data-center-revolution-fuelling-infrastructure-transformation/) | Dec 2025 |
| PUE, liquid-cooled (DLC + dry cooler) | ratio | 1.15 | 1.25 | 1.35 | Inference | – | Oct 2026 |
| PUE, colocation (billing) | ratio | 1.4 | 1.5 | 1.65 | JM model 1.5; Yotta 2020 offer 1.65 | [JM Financial](https://jmflresearch.com/JMnew/JMCRM/analystreports/pdf/Data-Centre-101_27Mar25.pdf); [Yotta](https://www.yotta.com/upgrade-to-yotta-colocation-offer/) | Mar 2025 / 2020 |
| Modular online UPS | ₹ per kVA | 9,300 | 15,000 | 19,000 | Listings (160 kVA ₹14.95 L; 100 kVA ₹18.9 L); battery inclusion unclear; +18% GST | [IndiaMART](https://dir.indiamart.com/impcat/modular-ups.html) | undated |
| UPS efficiency (double conversion / eco) | % | 96 | 97 | 99 | Vertiv APM Plus 97% / 99% eco | [Vertiv India](https://www.vertivco.com/en-in/about/newsroom/news-releases/vertiv-introduces-five-capacities-of-liebert-exm/) | 2017–2025 |
| Li-ion (LFP) battery | ₹ per kWh | 20,000 | 27,000 | 35,000 | Retail solar-storage proxy; 18% GST; life 8–10+ yrs | [QuickEstimate](https://quickestimate.co/blog/solar-battery-price-india) | 2026 |
| VRLA / lead-acid battery | ₹ per kWh | 8,000 | 11,000 | 15,000 | GST cut 28% to 18% (22 Sep 2025); replace every 3–5 yrs | same; [Swarajya](https://swarajyamag.com/amp/story/news-brief%2Fgst-20-what-gets-cheaper-what-gets-costlier-from-22-september) | 2026 |
| DG set 500 kVA CPCB IV+ | ₹ per kVA | 7,800 | 8,500 | 9,400 | ₹39–47 L per set; +18% GST | [IndiaMART Kirloskar](https://www.indiamart.com/proddetail/kirloskar-500-kva-diesel-generator-cpcb-iv-2855145327955.html); [IndiaMART Cummins](https://www.indiamart.com/proddetail/500kva-cpcb-iv-plus-cummins-diesel-generator-2853438686512.html) | 2025–26 |
| DG set 250–320 kVA CPCB IV+ | ₹ per set | 2,200,000 | 2,700,000 | 3,200,000 | Inference (extrapolated; small sets cost more per kVA); +18% GST | – | Oct 2026 |
| DG AMC | ₹ per year | 12,000 | 60,000 | 420,000 | Vendor listings, scope unclear; ₹4.2 L for a 2,250 kVA set | [IndiaMART](https://m.indiamart.com/skylight-power-solution/genset-amc-service.html); [Scribd](https://www.scribd.com/document/437635310/TCO) | undated |
| Diesel, Pune | ₹ per litre | 90.3 | 98.6 | 98.7 | Outside GST; Feb 2026 ₹90.3, Sep 2026 ₹98.63 | [energy.thecore.in](https://energy.thecore.in/fuel/petrol-price/pune); [Upstox](https://upstox.com/diesel-price/diesel-price-in-pune/) | 7 Sep 2026 |
| DG fuel consumption at 75% load | litres per kWh | 0.24 | 0.256 | 0.28 | 500 kVA about 72–85 L/h at 300 kW | [Jubaili](https://jubailibros.com/blogs/fuel-and-efficiency/how-much-fuel-does-a-diesel-generator-consume); [Depco](https://www.depco.com/faq/diesel-generator-efficiency/) | 2025–26 |
| DG energy cost (fuel only) | ₹ per kWh | 23.7 | 25.2 | 27.6 | Inference: L/kWh × ₹98.6 | derived | Oct 2026 |
| Grid outages, Baner (summer) | hours per day | 0 | 1 | 3 | Residents report 2–3 h/day in summer 2025; 220 kV events in Hinjewadi | [Pune Pulse](https://www.mypunepulse.com/?p=90027); [The Week](https://www.theweek.in/wire-updates/national/2025/07/08/bes29-mh-power-outage.html) | 2025 |
| Raised floor, IT grade | ₹ per sq ft | 200 | 320 | 650 | 400–650 heavy; ₹320 + 18% GST ≈ ₹378 | [StudioMatrx](https://www.studiomatrx.org/guides/data-centre-flooring-india) | 2026 |
| Server-room fit-out excl. M&E | ₹ per sq ft | 1,500 | 2,500 | 3,500 | Inference (floor/plinths, trays, earthing, access control, CCTV, partitions, fire); +18% GST | – | Oct 2026 |
| Office floor design load | kN/m² | 2.5 | 3.5 | 4.0 | Rack footprint about 14–20 kN/m², so structural check needed | [Infralens IS 875](https://infralens.in/handbook/live-loads) | 1987 code |
| Clean-agent suppression (Novec/FM-200), small room | ₹ per system | 100,000 | 200,000 | 450,000 | Pre-engineered; US $25–80k per room; +18% GST | [IndiaMART](https://dir.indiamart.com/impcat/novec-1230-fire-suppression-system.html); [Firetron](https://firetron.com/fire-suppression-systems/best-fire-suppression-systems-data-centers-server-rooms/) | 2025–26 |
| VESDA detector | ₹ per unit | 115,000 | 155,000 | 475,000 | VLF-250/500 ₹1.15–1.75 L; VEP ₹4.75 L; pre-tax | [TradeIndia](https://www.tradeindia.com/manufacturers/vesda-system.html) | undated |
| Office lease, Baner/Balewadi | ₹ per sq ft per month | 35 | 90 | 125 | Pune average ₹81.7 (H1 2026) to ₹90.2 (Q1 CY26); + ~₹12 maintenance; +18% GST | [Punekar News/Knight Frank](https://www.punekarnews.in/pune-records-highest-ever-half-year-office-leasing-in-h1-2026-residential-sales-remain-resilient-as-launches-rise-17-yoy/); [CRE Matrix](https://www.crematrix.com/blog/india-office-market-q1-cy26-key-trends-and-city-wise-performance/); [myHQ](https://myhq.in/office-space-for-rent/sbh--balewadi) | 2026 |
| Colo MRR, Pune, sub-250 kW (excl. power) | ₹ per kW per month | 6,188 | 7,688 | 8,475 | 5 MW+ to 2030E range; +18% GST | [JM Financial](https://jmflresearch.com/JMnew/JMCRM/analystreports/pdf/Data-Centre-101_27Mar25.pdf) | Mar 2025 |
| Colo MRR, Mumbai, sub-250 kW (excl. power) | ₹ per kW per month | 6,938 | 9,750 | 9,866 | +18% GST | same | Mar 2025 |
| Colo power pass-through | ₹ per kWh × PUE | 7.57 × 1.65 | 10 × 1.5 | 12 × 1.5 | Yotta 2020 ₹7.57; JM model ₹10; blog ₹10–12 metered | [Yotta](https://www.yotta.com/upgrade-to-yotta-colocation-offer/); [JM](https://jmflresearch.com/JMnew/JMCRM/analystreports/pdf/Data-Centre-101_27Mar25.pdf); [itforsme](https://www.itforsme.in/pricing/yotta-colocation-india) | 2020–2026 |
| Colo all-in, Pune (MRR + power) | ₹ per kW-IT per month | 16,000 | 18,600 | 25,000 | Inference (7,688 + 10 × 730 × 1.5); blog range ₹12–25k; +18% GST | derived; [Cyfuture](https://cyfuture.cloud/kb/colocation/colocation-prices-across-major-data-centers-in-india-and-abroad) | Oct 2026 |
| Colo full rack, retail (4–10 kW incl.) | ₹ per rack per month | 55,000 | 75,000 | 120,000 | Xenax ₹74,999 (10 kW); RackBank ₹87k (6 kVA); +18% GST | [Xenax](https://xenaxcloud.com/blog/full-rack-colocation-pricing/); [RackBank](https://www.rackbank.in/colocation/) | 2025–26 |
| Colo liquid-cooling surcharge | ₹ per rack per month | 44,000 | 130,000 | 352,000 | US benchmark $500–4,000 at ₹88/USD; no Indian rate found | [ClusterBid](https://clusterbid.com/blog/gpu-colocation-pricing-guide-2026-power-space-interconnect); [aidatacenterfinder](https://aidatacenterfinder.com/blog/colocation-pricing-2026) | 2026 |
| Colo setup / one-time | ₹ one-time | 0 | 49,999 | 100,000 | Yotta celebration offer ₹49,999 | [Yotta](https://www.yotta.com/lp/yotta-nm1-datacenter-colocation-celebration-offer/) | undated |
| Remote hands | ₹ per hour | 500 | 1,500 | 5,000 | Often bundled (Yotta 5 tickets/month); +18% GST | [Cyfuture](https://cyfuture.cloud/kb/howto/how-much-does-server-colocation-cost-in-india) | 2025 |
| Cross-connect | ₹ each (unit unclear) | 3,000 | 4,500 | 6,000 | Often bundled (Yotta 2 copper); +18% GST | same | 2025 |
| ILL 100 Mbps | ₹ per month | 25,000 | 30,000 | 38,000 | +18% GST; install ₹15–50k | [itforsme ILL](https://www.itforsme.in/pricing/internet-leased-line-india) | 2026 |
| ILL 1 Gbps | ₹ per month | 70,000 | 120,000 | 250,000 | Tata reseller ₹90k; +18% GST | [Internet Express](https://internetexpress.co.in/1-gbps-leased-line-cost-in-india/); [Positive Comm.](https://positivecommunication.in/tata-leased-line/) | 2026 |
| MLOps / LLM infra engineer, Pune | ₹ CTC per year | 1,700,000 | 2,800,000 | 4,500,000 | Senior up to ₹65 L; no GST | [OwnYourCareer](https://www.ownyourcareer.in/careers/mlops-engineer/salaries); [IIT KGP](https://online.iitkgp.ac.in/blog/ai-ml-engineer-salary-india); [Glassdoor GPU](https://static.glassdoor.co.in/Salaries/gpu-salary-SRCH_KO0,3_P2.htm) | Jul–Aug 2026 |
| Linux / HPC sysadmin, Pune | ₹ CTC per year | 480,000 | 900,000 | 1,800,000 | Payscale avg ₹4.8–5.9 L; 90th percentile ₹9.9 L; HPC premium is inference | [Payscale](https://www.payscale.com/research/IN/Job=Linux_System_Administrator/Salary/68d9e97c/Pune) | 2026 |
| DC facility technician (electrical/HVAC) | ₹ CTC per year | 300,000 | 500,000 | 800,000 | Inference from DC operator (₹6.45–7.51 L at 7–9 yrs) and NOC data | [Glassdoor DC operator](https://static.glassdoor.co.in/Salaries/data-centre-operator-salary-SRCH_KO0,20.htm) | 2026 |
| NOC operator, Pune | ₹ CTC per year | 250,000 | 400,000 | 600,000 | Payscale avg ₹2.55–3.6 L | [Payscale NOC](https://www.payscale.com/research/IN/Job=Network_Operations_Center_(NOC)_Engineer/Salary/4bc4a2d1/Pune) | 2026 |
| 24×7 shift coverage | FTE per seat | 4.4 | 5 | 5.5 | Inference: 8,760 h ÷ about 1,900–2,000 h | derived | Oct 2026 |
| EEI insurance premium | % of sum insured per year | 0.3 | 0.75 | 1.25 | Old tariff 1.0% (computers 1.25% with AMC, 2.5% without); market rate unverified; +18% GST | [National Insurance](https://nationalinsurance.nic.co.in/en/industrial-risk-insurance/electronic-equipment-insurance) | old tariff |
| DC capex benchmark (large build) | ₹ per kW IT | 33,300 | 46,500 | 70,000 | JM ₹333–592 mn/MW; CareEdge ₹60–70 cr/MW; includes building | [JM Financial](https://jmflresearch.com/JMnew/JMCRM/analystreports/pdf/Data-Centre-101_27Mar25.pdf); [verified.realestate](https://corporate.verified.realestate/insights/data-centre-investment-economics-capex) | 2025 |
