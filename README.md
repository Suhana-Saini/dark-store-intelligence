![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=Databricks&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Spark SQL](https://img.shields.io/badge/Spark_SQL-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

# Dark Store Intelligence

An end-to-end analytics project on **synthetic** quick-commerce data, built to practice and showcase
data engineering, SQL analysis, and AI-agent evaluation.

## Problem statement

Quick-commerce platforms promise 10-15 minute delivery, but that promise breaks in specific,
findable ways: rider shortages at peak hours, stockouts hidden by substitutions, poor perishable
inventory management, and a bad first order that quietly costs future revenue. This project builds
a realistic (synthetic) dataset of a 6-store dark-store operation, engineers it through a proper
Bronze/Silver/Gold pipeline, and answers 12 concrete operational questions with SQL, then evaluates
whether a natural-language AI agent (Databricks Genie) can answer the same questions correctly.

## Approach

1. **Generate** a synthetic dataset in Python (Bronze layer): 6 stores, 60 days, ~113K orders,
   ~970K raw events, hourly inventory, fruit and veg wastage. with deliberately planted realism — duplicate events, late/out-of-order
   arrivals, missing rider IDs, split orders, and 6 planted operational patterns.
2. **Clean** it into a Silver layer: deduplicate events, reconstruct one clean timeline per shipment,
   recover recoverable missing values (with every fix flagged, never silently guessed).
3. **Model** it into a Gold layer: order-level facts, store-hour operational metrics, SKU
   availability, fruit & veg wastage, and customer first-order/reorder behavior.
4. **Analyze** with 12 SQL questions covering delivery delays, stockouts, wastage, cancellations,
   and customer retention.
5. **Evaluate an AI agent** (Databricks Genie) against the same 12 questions, to see where a
   natural-language interface gets it right and where it needs better guardrails.

## Key findings (synthetic data — illustrates method, not real business results)

- **Dinner-hour rider shortage**: on-time delivery drops to ~72% between 7-9pm vs ~88% other hours,
  and the delay is concentrated almost entirely in rider wait time, not picking or riding.
- **Substitutions and split orders hide real stockout severity**: DS04's dairy fill rate looks like
  93% (lenient) but is actually 72.5% (strict) — the gap is silent operational risk.
- **Perishables trade-off**: DS02 overstocks fruit & veg (18.3% wastage, near-zero stockouts);
  DS05 understocks (13.4% stockouts, low wastage). Neither is optimal.
- **First impressions compound**: customers with a bad first order reorder within 7 days at 30.7%,
  vs 47.5% for a good first order — a ~17-point gap.
- **Rain and split orders both predict cancellation risk** (roughly 2x and 7x baseline respectively).

## Tech stack

Python (generator) · Databricks Free Edition (PySpark, Delta, Spark SQL) · SQL (Bronze/Silver/Gold,
12-question analysis) · Databricks Genie (AI agent evaluation) · GitHub

## Repo structure
```
dark-store-intelligence/
├── README.md
├── docs/
│ ├── design.md — data model, planted patterns, event lifecycle
│ ├── Insights-memos/ —  written few insight memos
│ ├── notes.md — my own explanations of key design decisions
│ ├── agent_eval.md — Genie evaluation against my own SQL answers
│ └── Agent_Screenshots/
├── Notebooks/
│ ├── 01_generate_data
│ ├── 02_silver
│ ├── 03_data_quality
│ ├── 04_gold
│ └── 05_analysis
```


## Data quality

9 automated checks run after the Silver layer (deduplication correctness, row reconciliation,
timestamp ordering, referential integrity) — see `Notebooks/03_data_quality`.

## What I'd do next

- **Move from static to near-real-time.** Right now Gold tables are built by running notebooks manually.
  The natural next step is Databricks Jobs & Workflows on an hourly schedule, so Gold refreshes on its own —
  and the agent's answers reflect the last hour of data, not a one-time snapshot. Connecting Genie to a
  scheduled/streaming source needs more research than a batch table, so this is a planned enhancement.
- **Add views on top of Gold** for lightweight dashboards, without duplicating data — a natural pairing
  with the hourly refresh above.
- Add a simple demand forecast baseline for fruit & veg replenishment.
- Rebuild Silver as a proper Lakeflow pipeline or dbt project with tests.
- Expand the Genie evaluation to more edge-case and ambiguous questions.

**Why this matters more than it sounds:** scheduling and views are technical upgrades, but the actual
goal behind them is putting fresh data in front of people who aren't SQL users. A store ops lead or a
junior analyst should be able to ask a plain-language question and get a current answer, instead of
waiting on someone to write a query. That's time and effort saved on both sides — not just a pipeline
that runs faster.

## Limitations

All data is synthetic and its patterns were deliberately planted, so findings demonstrate method and
pipeline quality, not real business impact. The 12 questions and their expected answers were computed
in SQL and used as ground truth for the Genie evaluation.

## AI assistance

The data generator design, pipeline scaffolding, and SQL were built with AI assistance (Claude). I ran,
reviewed, tested, and extended every piece myself — including debugging real data quality issues,
recalibrating the generator's planted patterns, and evaluating the Genie agent's answers against my own
analysis.

## Agent approach

Two approaches were attempted for a custom natural-language agent over the Gold tables:
1. **Google ADK** with its local web UI — blocked by GitHub Codespaces port-forwarding restrictions
   (JS assets returned 403 Forbidden; unresolved after trying public port visibility, different browsers,
   and the ADK API server as a fallback).
2. **Direct Gemini API calls** (google-genai SDK) with the same tool layer — hit repeated 503 "model
   overloaded" errors from Google's servers that didn't clear with retries.

Given both routes hit external infrastructure issues outside the project's control, the natural-language
layer for this project uses **Databricks Genie**, built into the platform, over the same Gold tables.
See `docs/agent_eval.md` for its evaluation against the project's own SQL analysis.
