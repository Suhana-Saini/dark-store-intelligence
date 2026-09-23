### Memo 1: Inventory & Supply Chain — Revenue Loss & Waste-vs-Stockout Paradox

**To:** Leadership & Supply Chain Operations

**From:** Data Analytics Team

**Subject:** High-Impact Lost Revenue in Personal Care & Perishable Trade-Offs Across Dark Stores

#### Executive Summary

An analysis of $377,321 in total lost revenue from unavailable items reveals a heavy concentration in non-perishable lines, led by Personal Care. Concurrently, dark store stockout and wastage management show extreme operational divergence: DS02 over-indexes on inventory to avoid stockouts at the cost of high waste, while DS05 minimizes waste at the expense of severe out-of-stock rates.

#### Key Findings & Numbers

* **Personal Care Loss Concentration:** Personal Care accounts for **$87,987 (23.3%)** of overall lost revenue across 27 SKUs, driven by the highest average lost revenue per SKU at **$327** (compared to Fruits & Vegetables at $106/SKU). Seven of the top 15 worst-performing SKUs are in Personal Care, led by **SKU0242 ($18,144 lost)**.
* **Substitution Prevention Power:** Substitution is highly effective at rescuing revenue. Orders where all missing items were substituted experienced a **0.00% cancellation rate** (0 of 3,845 orders). Conversely, orders with unreplaced missing items suffered an **8.27% cancellation rate** (707 of 8,551 orders)—more than 4.4x higher than the baseline rate (1.86%).
* **The DS02 vs. DS05 Perishables Dilemma:**
* **DS02:** Operates a low stockout rate (**0.20%**, 127 OOS SKU hours) but wastes **18.34%** of received Fruits & Vegetables (6,754 of 36,830 units)—3.2x higher than DS05.
* **DS05:** Achieves an industry-leading low waste rate (**5.79%**), but suffers an alarming **13.44% stockout rate** (8,710 OOS SKU hours)—over 6x higher than any other store.



#### Recommendations

1. **Prioritize Top Personal Care SKUs:** Re-evaluate safety stock levels and reorder triggers for high-value Personal Care SKUs (specifically SKU0242, SKU0257, SKU0249, SKU0250).
2. **Automate Substitution Workflows:** Expand smart-substitution options at checkout to eliminate unreplaced item occurrences.
3. **Calibrate Produce Ordering Rules:** Standardize inventory replenishment formulas across stores; adopt a middle-ground forecasting model for DS02 (to reduce waste) and DS05 (to eliminate severe stockouts).

---

### Memo 2: Order Fulfillment & Network Bottlenecks — Split Order Performance & Rider Wait Times

**To:** Dark Store Operations & Logistics

**From:** Data Analytics Team

**Subject:** Operational Impact of Split Orders and Rider Capacity Constraints During Dinner Peak

#### Executive Summary

Fulfillment performance degrades sharply during evening peak hours (7:00 PM – 9:00 PM) due to rider capacity bottlenecks rather than store-level pick/pack delays. Furthermore, split orders (fulfillment across multiple stores) introduce major operational overhead, driving severe delivery delays and customer cancellations.

#### Key Findings & Numbers

* **Dinner Peak Bottleneck (7 PM – 9 PM):** Average rider wait time surges to **2.07 minutes** during the 7–9 PM dinner peak compared to **0.62 minutes** during non-peak hours—a **234% increase**.
* Rider wait time represents **21% of total delivery time** during peak hours (vs. 7–8% normally).
* Store pick-and-pack times remain stable at **~2.86 minutes** throughout the day, proving that store pickers are not the bottleneck.
* Store **DS03 at 9 PM** exhibits the highest systemic rider wait time average (**2.10 minutes**), while **DS04** shows the worst on-time delivery rate at 8 PM (**67.39%**).


* **Split Order Friction:**
* **Delivery Speed:** Split orders average **15.83 minutes** total delivery time compared to **8.40 minutes** for normal single-shipment orders (**88% slower**).
* **Cancellation Multiplier:** Split orders have a **12.49% cancellation rate** (681 of 5,451 orders) compared to **1.77%** for normal orders (**7.1x higher**).
* **Primary Cancellation Cause:** **56.39%** of split order cancellations are explicitly driven by `delay_customer_cancelled` (vs. 6.56% for normal orders).



#### Recommendations

1. **Dynamic Rider Staging:** Reallocate rider shift schedules toward 7:00 PM – 9:00 PM peak blocks, prioritizing rider availability at high-wait hubs (DS03, DS01, DS04).
2. **Split-Order Threshold Optimization:** Restrict split-order creation unless high-margin threshold conditions are met, or set accurate delivery expectations (>15 mins) at checkout for split shipments.

---

### Memo 3: Customer Experience & Retention — First Impression Impact & Weather Resilience

**To:** Growth, Customer Experience & Operations

**From:** Data Analytics Team

**Subject:** Quantifying First-Order Experience Impact on 7-Day Reorder Rates & Weather Vulnerabilities

#### Executive Summary

First impressions heavily dictate customer lifetime value: experiencing a delay, cancellation, or missing item on an initial order permanently dampens repeat ordering. Additionally, bad weather significantly degrades fleet performance and increases customer churn during rainy days.

#### Key Findings & Numbers

* **The First-Order Effect (7-Day Reorder Rate):**
* Customers with a **good first order** exhibit a **47.46% 7-day reorder rate** (averaging 0.89 orders in the next 7 days).
* Customers with a **bad first order** (cancelled, late, or missing items) have a **30.73% 7-day reorder rate** (averaging 0.46 orders)—a **35% drop in repeat engagement**.
* Late deliveries constitute the largest share of bad initial experiences (1,895 customers out of 3,280 impacted).


* **Rainy Day Operations:**
* **Cancellation Rate Spike:** Order cancellations jump from **1.86%** on dry days (1,613 / 86,810) to **3.68%** on rainy days (974 / 26,450)—a **98% increase**.
* **Ride Time Inflation:** Average ride times increase by **39%** (from 3.40 mins to 4.72 mins), elevating total delivery time to 10.46 minutes.
* **Rider Unavailability Shift:** On rainy days, `rider_unavailable` becomes the cause for **32.24%** of all cancellations (up from 9.80% on dry days).



#### Recommendations

1. **VIP Delivery Priority for First-Time Users:** Route first-time customer orders to top-performing riders and nearest stores to ensure on-time delivery.
2. **Proactive CX Recovery:** Automatically trigger customer apology credits or vouchers when a first order experiences a late delivery or missing item.
3. **Rainy Day Surge Incentive Models:** Introduce localized rider pay surges during rainy conditions to maintain fleet coverage and suppress the 32% rider unavailability bottleneck.

---

### Memo 4: Store Operations & Network Diagnostics — Cancellation Drivers & Store Performance Variance

**To:** Store Operations & General Management

**From:** Data Analytics Team

**Subject:** Comprehensive Analysis of Order Cancellation Mechanics & Store-Level Metrics

#### Executive Summary

Across 113,260 total system orders, 2,587 were cancelled (**2.28% overall cancellation rate**). Store-level analysis shows that while customer behavior drives most baseline cancellations, operational friction (delays and rider availability) accounts for major localized spikes.

#### Key Findings & Numbers

* **System Baseline:**
* Total Orders: **113,260**
* Delivered Orders: **110,673 (97.72%)**
* Cancelled Orders: **2,587 (2.28%)**


* **Store Cancellation Drivers (DS04 vs. DS05 Breakdown):**
* **DS04** (491 cancellations, 2.98% rate):
* Customer changed mind: **49.08%** (241)
* Delay - customer cancelled: **26.88%** (132)
* Rider unavailable: **15.48%** (76)
* Items unavailable: **8.55%** (42)


* **DS05** (473 cancellations, 2.51% rate):
* Customer changed mind: **55.81%** (264)
* Delay - customer cancelled: **21.99%** (104)
* Rider unavailable: **14.16%** (67)
* Items unavailable: **8.03%** (38)




* **Store On-Time Delivery Performance at 8 PM:**
1. **DS02:** 73.82% (Best)
2. **DS03 / DS06:** 72.55%
3. **DS01:** 71.55%
4. **DS05:** 71.08%
5. **DS04:** 67.39% (Worst)



#### Recommendations

1. **Targeted Interventions at DS04:** Investigate operational bottlenecks specific to store DS04, which trails the network in both 8 PM on-time performance (67.39%) and overall cancellation rate (2.98%).
2. **Checkout Confirmation Optimization:** Address the top cancellation reason (`customer_changed_mind`, ~50-55% across stores) by adding a brief order verification step before order dispatch to reduce impulse cancellations.
