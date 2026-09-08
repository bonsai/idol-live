# Architecture

## Responsibility
- Design is stored in GitHub Issues.
- AW workflow is the driver that turns intent into executable design/code tasks.
- Application code lives in this repository.
- Event/source data lives under `.data/` and is not mixed with application code.

## Flow
Intent → Issue (design) → AW workflow → generated implementation tasks → Vue code → `.data` fixtures → review

## MVP
1. Search idol live events by date range.
2. Normalize free-admission concepts: 無銭 / フリー / 観覧無料 / 0円.
3. Preserve conditions such as 1D, reservation, priority tickets and paid benefits.
4. List events chronologically.
5. Event detail with source URL.
6. Responsive Vue UI.

## Data boundary
`.data/` is the canonical local dataset/fixture boundary. Schema and ingestion rules are design concerns and should be tracked in Issues; runtime data files belong under `.data/`.
