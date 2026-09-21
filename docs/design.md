# Dark Store Intelligence: Design (v2)

**Note:** All data is synthetic. Patterns and data problems are planted on purpose so the analysis has something real to find. Findings are true by construction, and this project shows method, not business results.

## 1. Order lifecycle events (12)

| # | Event | Trigger | Repeats/branches? |
|---|---|---|---|
| 1 | order_placed | Customer places order in app | No |
| 2 | order_accepted | Dark store accepts the order | No |
| 3 | picking_started | Picker starts collecting items | No |
| 4 | item_unavailable | An ordered item is out of stock | Yes, once per missing item |
| 5 | item_substituted | A replacement is offered and accepted | Yes, per item |
| 6 | order_split | Missing items get shipped from a second nearby store | Branch: creates a second sub-order |
| 7 | packing_completed | All items in the sub-order packed | Once per sub-order |
| 8 | rider_assigned | Rider assigned | Yes, if reassigned |
| 9 | rider_arrived_at_store | Rider reaches the store | Once per sub-order |
| 10 | order_picked_up | Rider leaves with the order | Once per sub-order |
| 11 | order_delivered | Delivered to customer | Once per sub-order |
| 12 | order_cancelled | Cancelled, with a reason | Branch: possible before pickup |

Events 3 onward carry a `sub_order_id`. A normal order has exactly one sub-order. A split order has two.

## 2. Tables

| Table | Grain (one row per...) | Key |
|---|---|---|
| stores | dark store | store_id |
| skus | product | sku_id |
| customers | customer | customer_id |
| orders | customer order | order_id |
| sub_orders | shipment of an order from one store | sub_order_id |
| order_items | order line (order + SKU) | order_id, sku_id |
| order_events | event on an order or sub-order | event_id |
| inventory_snapshots | store + SKU + hour | store_id, sku_id, snapshot_ts |
| wastage_log | store + perishable SKU + day | store_id, sku_id, date |
| daily_context | calendar day | date (is_rainy, is_weekend) |

## 3. Deliberate data problems (the raw feed is messy)

- About 1.5% of events appear twice (same event_id, later ingested_at).
- About 1% of events arrive late and out of order (ingested_at well after event_ts).
- About 0.5% of rider events have a null rider_id.

## 4. Business questions

1. What % of orders arrive within the promised time, by store and hour? (For split orders, use the last sub-order delivered.)
2. Which stage (accept, pick, pack, rider wait, ride) causes most delay at peak hours?
3. Which stores and hours have the longest rider wait?
4. What is the fill rate (qty delivered / qty ordered) by store and category?
5. Which SKUs are most often unavailable, and how much revenue is lost?
6. How many orders are cancelled, and why, by store?
7. For fruits and vegetables: which stores waste too much, and which stock out too often?
8. Do substitutions reduce cancellations?
9. Do customers whose first order was late or partial reorder less within 7 days?
10. Do rainy days slow delivery and raise cancellations?
11. Are split orders slower and more likely to be cancelled than normal orders?
12. Do a small share of SKUs cause most of the lost revenue?

## 5. Planted patterns (most important first)

| Pattern | Why it happens in real life | Answers Q | How it shows up |
|---|---|---|---|
| Dinner-hour rider shortage (7-10pm) | Everyone orders at once, riders are limited | 2, 3 | Rider wait 2-3x longer at all stores |
| Rainy days | Riders slow down or go offline, customers cancel after waiting | 1, 6, 10 | Ride time +30-50%, more cancellations |
| F&V: DS02 overstocks, DS05 understocks | Perishable ordering is hard to get right | 7 | DS02 high wastage, DS05 many stockouts |
| DS04 dairy restocking gap in evenings | Restock timing misses the evening peak | 4, 5, 12 | High dairy stockouts at DS04 in evenings |
| Split orders (about 5% of orders) | Nearest store lacks some items | 11 | About 8 minutes slower, higher cancellation |
| Bad first experience | Late or partial orders hurt trust | 9 | Lower 7-day reorder rate |
