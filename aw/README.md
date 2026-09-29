# AW — idol-live

AW is the driver for the data-growth loop.

## Loop

```
Issue / intent
  ↓
AW
  ↓
Python collectors
  ↓
JSONL observations
  ↓
normalize / dedupe / enrich
  ↓
SQLite derived index
  ↓
quality / coverage metrics
  ↓
Git commit
  ↓
repeat
```

## Rules

- Python is the implementation language.
- Browser UI is plain JavaScript + HTML/CSS only.
- No Vue.
- No TypeScript.
- No Cloudflare Workers / Pages / D1 dependency.
- JSONL is the canonical data layer.
- SQLite is a rebuildable local/CI index, not the source of truth.
- Provider URLs are first-class data.
- Keep raw observations where possible so later ML can learn from historical states.
- Marketing intelligence is derived from the accumulated event/provider/artist/venue observations.
- ML comes later; first grow clean longitudinal data.

## Data growth targets

1. provider coverage
2. event coverage
3. source freshness
4. free-condition normalization
5. artist / venue / provider relationships
6. repeated observations over time
7. marketing signals
8. later: BigQuery / BigQuery ML

## Commands

The intended AW entrypoints will be Python scripts under `aw/`.
