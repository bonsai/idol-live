# Architecture

## idol-live = reference only

idol-db → generated JSONL → idol-live → reference → user-facing live view

idol-live does not own crawler, raw data, canonical data, research, selection logic, or application source code.

The source of truth is bonsai/idol-db.

Go crawls. Python decides. idol-live references.
