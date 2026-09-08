# idol-live

> アイドルの「無銭・フリーライブ」を探し、比較し、予定化するためのライブ検索プロダクト。

## Intent → AW → Vue

このrepoは、最初から画面を手作業で作るのではなく、**意図（Intent）を仕様化し、AWで設計・実装タスクへ分解し、Vue UIへ落とす**ことを基本方針とする。

### Product intent

- 期間を指定してアイドルライブを検索する
- 「無銭」「フリー」「観覧無料」などの条件を正規化する
- 完全無料と「0円＋1D」などを区別する
- 日付・地域・会場・出演者・料金・条件・情報源を一覧できる
- JSONを正規データとして保持し、VueはJSON/APIを表示する
- 情報源URLと取得日時を追跡できる

### Domain model

```text
Event
├── date
├── start_at / end_at
├── title
├── artists[]
├── venue
├── area
├── admission
│   ├── price
│   ├── currency
│   └── label
├── free_status
│   ├── free
│   ├── drink_required
│   ├── reservation_required
│   └── conditions[]
├── source_url
└── fetched_at
```

### Vue information architecture

```text
App
├── SearchBar
│   ├── date range
│   ├── area
│   └── free condition
├── EventSummary
├── EventList
│   └── EventCard
│       ├── DateBadge
│       ├── ArtistList
│       ├── Venue
│       ├── PriceBadge
│       └── Conditions
└── EventDetail
    └── SourceLink
```

### AW workflow

```text
Intent
  ↓
Domain / Ontology
  ↓
Schema (JSON)
  ↓
User stories / Issues
  ↓
Vue information architecture
  ↓
Components
  ↓
Implementation
  ↓
Validation / UI review
  ↓
Deploy
```

AW should treat the repository itself as the source of truth and generate actionable issues from the intent and schema. Avoid premature component implementation before the domain and acceptance criteria are defined.

## MVP acceptance criteria

1. 期間（例: 9/14〜9/20）を指定できる
2. 東京のアイドルライブを日付順に表示できる
3. 無銭 / フリー / 観覧無料を区別して表示できる
4. 0円でもドリンク代等がある場合は明示する
5. イベント詳細から情報源へ遷移できる
6. JSON fixtureだけでローカル動作確認できる
7. PC / スマホの両方で閲覧できる

## Deployment

Vue + Vite を GitHub Pages の GitHub Actions から自動デプロイする。

## Planned structure

```text
idol-live/
├── data/
│   └── events.json
├── src/
│   ├── components/
│   ├── views/
│   ├── composables/
│   └── types/
├── docs/
│   └── intent.md
└── .github/
    └── workflows/
```
