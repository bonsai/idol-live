# Data Strategy

## Decision

**JSONL first, SQLite second, BigQuery later.**

### JSONL — canonical

Use JSONL for:

- events
- providers
- artists
- venues
- observations
- source snapshots / fetch metadata
- hypotheses
- marketing signals

JSONL is append-friendly, diffable, Git-friendly, and can be loaded into BigQuery later.

### SQLite — derived

SQLite is useful for:

- deduplication
- joins
- local search
- incremental enrichment
- QA
- feature generation
- fast AW queries

The SQLite file should be reproducible from JSONL and can be ignored by Git.

### BigQuery / BigQuery ML — later

When the dataset becomes large enough, load JSONL into BigQuery and build analytical tables/features there. BigQuery directly supports newline-delimited JSON, so the JSONL contract does not need to be replaced.

### Firebase

Keep Firebase as an optional future product/runtime layer only if a user-facing realtime application needs it. It should not become the canonical research database.

### Cloudflare / D1

Not part of the new architecture.

## Intelligence loop

```
crawl
→ observe
→ normalize
→ dedupe
→ enrich
→ measure
→ hypothesize
→ collect again
→ accumulate longitudinal data
→ feature engineering
→ ML
```

The key asset is not the database engine. It is the **historical observation graph**: provider × event × artist × venue × date × price/condition × source.
