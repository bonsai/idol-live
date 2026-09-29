# idol-live

アイドルイベントの JSONL参照・表示先。

## Boundary

idol-live はデータ生成系でもDBでもアプリ実装repoでもない。

- データを持たない
- クロールしない
- Pythonで選別しない
- canonical schemaを持たない
- UIコードを持たない

イベントデータの生成は bonsai/idol-db が担当する。

idol-db: Goでcrawl → Pythonでselect / normalize / publish → generated JSONL

idol-live: generated JSONLをreference only

## Contract

idol-live が参照するのは idol-db が生成した JSONL のみ。
イベントの正本は idol-db。探索方法・選別ロジックは idol-db / idol-research 側にある。

## Rule

DBがクロールしてデータを生成する。idol-liveは生成済みJSONLを参照するだけ。

このrepoにはコードやイベントデータを置かない。
