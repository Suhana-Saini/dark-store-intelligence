# dark-store-intelligence


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
