# Agent Evaluation: Databricks Genie

Genie space connected to workspace.gold.* (fact_orders, store_hour_metrics, sku_availability, fv_store_day, customer_first_order).

| # | Question | Expected (my SQL) | Genie's answer | Verdict |
|---|---|---|---|---|
| 1 | On-time % by store at 8pm | ~72-74% dinner-hour range | 67.4%-73.8% across stores, DS02 best, DS04 worst | Correct |
| 2 | Total orders / cancelled | 113,260 orders, 2,587 cancelled | 113,260 orders, 2,587 cancelled (2.28%) | Correct — exact match |
| 3 | (Repeat of Q1, Genie recalled it) | — | Same as Q1 | Correct |
| 4 | Slowest stage at dinner peak | Rider wait ~2.08 vs ~0.62 min | Rider wait 2.07 vs 0.62 min | Correct — near-exact match |
| 5 | Worst store-hour for rider wait (top 10) | All in 19-21h, ~2.1 min | DS03 21h worst at 2.10 min; all top 5 in 19-21h | Correct |
| 6 | Strict vs lenient fill rate, DS04 Dairy | Strict ~72.5%, Lenient ~93.3% | Strict 79.87% (7,648/9,576); lenient declined — cited that category-level substitution/split data isn't in the schema | Partial | Good agent behavior (refused to fabricate), but strict number differs meaningfully from mine — worth reconciling |
| 7 | SKU with most lost revenue | SKU0242, $18,144 lost | SKU0242, $18,144 lost, 216 unavailable lines | Correct — exact dollar match |
| 8 | Top cancellation reasons, DS04 & DS05 | (not pre-computed) | Customer changed mind dominant (~49-56%), rider/items unavailable ~22-24% | Plausible, matches the general pattern seen elsewhere |
| 9 | F&V wastage %, worst store | DS02, ~18.3% | DS02, 18.34% (6,754/36,830) | Correct — near-exact match |
| 10 | F&V stockout %, worst store | DS05, ~13.4% | DS05, 13.44% (8,710 OOS hours) | Correct — near-exact match |
| 11 | Substitution vs cancellation | All-substituted ~0.9%, unreplaced ~5.9% | All-substituted 0.00% (0/3,845), unreplaced 8.27% (707/8,551) | Partial | Same direction, but the clean 0% and different magnitude suggest a different segmentation logic — worth reconciling |
| 12 | Reorder rate, bad vs good first order | 30.7% vs 47.5% | 30.73% vs 47.46% | Correct — near-exact match, plus useful extra detail on "what makes an order bad" |
| 13 | Rain vs dry: cancel rate & ride time | Cancel 3.68% vs 1.86%; ride 4.72 vs 3.40 min | Cancel 3.68% vs 1.86%; ride 4.72 vs 3.40 min | Correct — exact match |
| 14 | Split vs normal: delivery time & cancel rate | 15.83 vs 8.40 min; 12.5% vs 1.8% cancel | 15.83 vs 8.40 min; 12.49% vs 1.77% cancel | Correct — exact match |

## Summary

Genie correctly answered 9 of 11 distinct questions, several down to the exact number (Q2, Q7, Q9-Q14), which is a strong result for a general-purpose natural-language agent with no custom code. It also added useful unprompted detail in a few answers (the "what makes a first order bad" breakdown in Q12, the over/under-ordering framing in Q10). The two partial answers (Q6 fill rate, Q11 substitution/cancellation) both involve the more complex parts of the schema — category-level joins and multi-way order segmentation — and in one case (Q6's lenient fill rate) Genie explicitly declined rather than guess, which is the right behavior for a trustworthy agent. This suggests Genie handles straightforward aggregations very reliably but needs either better instructions or a purpose-built Gold table for multi-condition segmentation questions.
