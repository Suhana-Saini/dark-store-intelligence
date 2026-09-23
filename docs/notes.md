# Dark Store Intelligence — Technical Notes & Self-Check

## 8. Self-Check ("Explain it back")

### 8.1 Bronze vs Silver vs Gold: What does each layer promise?
* **Bronze (Raw Ingestion Layer):** Contains raw, unmodified source data directly ingested from event streams and operational databases. It preserves original source structures, history, and raw state without applying data cleaning or business transformations.
* **Silver (Cleaned & Standardized Layer):** Provides deduplicated, typed, filtered, and cleaned tables with enforced schemas. It resolves data quality issues (e.g., handling missing rider IDs, deduplicating events by `event_id`, flagging late arrivals) while preserving the true event business timestamp (`event_ts`).
* **Gold (Business Analytics Layer):** Contains highly structured, dimensional, and aggregated data models (star schemas, facts, and aggregate dimensions). It is optimized for fast SQL queries, reporting, executive dashboards, and consumption by AI agents/Genie.

---

### 8.2 Why is `orders` different from `sub_orders`?
* **`orders` (Customer Order Level):** Represents the single checkout transaction created by the customer. Grain: 1 row per customer order.
* **`sub_orders` (Shipment / Fulfillment Level):** Represents individual shipments sent to dark stores to fulfill an order. In split-order scenarios, a single `order_id` is divided into multiple `sub_order_id` records (e.g., `-S1` primary store, `-S2` secondary store) when a single dark store cannot fulfill all items.

---

### 8.3 What does `ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY ingested_at)` do?
* This window function partitions the data by unique `event_id` and orders duplicate rows based on when they were ingested (`ingested_at`).
* Filtering by `WHERE rn = 1` keeps only the first ingested copy of each event, successfully removing downstream duplicate events caused by system retries or re-sends.

---

### 8.4 In `fact_orders`, why do stage times come from the first shipment but on-time from the last?
* **Stage Times (Picking / Packing / Assignment):** Come from the **first shipment (`-S1`)** because store fulfillment and initial picking start immediately when the customer places the order.
* **On-Time Delivery Status:** Calculated from the **last delivered shipment (`-S2` or final shipment)** because from a customer experience standpoint, an order is not considered complete until all items/shipments have reached the customer's location.

---

### 8.5 Which planted pattern is the hardest to detect, and why?
* **Missing Rider IDs (`rider_id IS NULL` on intermediate events):** This is the hardest pattern to detect because events like `rider_assigned` or `rider_arrived_at_store` often omit rider IDs in real-world messy feeds. 
* Detecting and imputing them requires joining across sibling events within the same `sub_order_id` using window/aggregate functions (`max_by(rider_id, event_ts)`), since standard null checks will not catch missing values across sequence states.

---

### 8.6 What in this project is a genuine finding, and what is true only because we planted it?
* **Genuine Findings (Methodological & Analytical Reality):** The behavior of operational metrics (e.g., rider wait times inflating during the 7-9 PM dinner peak, split orders suffering from higher cancellation rates and longer durations, and bad first-order delivery experiences reducing 7-day customer retention).
* **True by Construction (Planted Data Artifacts):** The exact numbers (e.g., 113,260 orders, 14,386 duplicate events, 9,736 late events, and specific store-level OOS/wastage trade-offs) are synthetically generated and planted by design in the Python generator to validate pipeline resilience and SQL accuracy.
