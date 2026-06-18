# アーキテクチャ設計

## ファイル構成

```
claude_blogs/
├── index.html              # トップページ（記事一覧）
├── manifest.json           # PWAマニフェスト
├── sw.js                   # Service Worker
├── articles.json           # ビルド時に自動生成（コミット不要）
├── src/                    # 記事HTMLを置くディレクトリ
│   └── .gitkeep
├── docs/                   # 設計ドキュメント
└── .github/
    └── workflows/
        └── deploy.yml      # GitHub Actions（ビルド＆デプロイ）
```

## ビルドパイプライン

### トリガー

- `main` ブランチへのpush時に自動実行
- `workflow_dispatch` による手動実行も可能

### ビルドステップ

1. `src/*.html` をスキャン
2. 各HTMLから `<title>`・`<meta name="date">`・`<meta name="description">`・OGPタグを抽出（Python標準ライブラリ `html.parser` を使用）
3. 日付降順にソートして `articles.json` を生成
4. GitHub Pages へデプロイ

### articles.json スキーマ

```json
[
  {
    "title": "記事タイトル",
    "description": "記事の概要",
    "date": "YYYY-MM-DD",
    "path": "src/article.html"
  }
]
```

## フロントエンド設計

### スタイリング

- 外部フレームワーク不使用
- CSS変数ベースのデザインシステム
- `prefers-color-scheme` メディアクエリでダークモード自動対応

### PWA

| 項目 | 内容 |
|------|------|
| `start_url` | `/claude_blogs/` |
| `scope` | `/claude_blogs/` |
| `display` | `standalone` |
| キャッシュ戦略 | Stale While Revalidate |
| キャッシュ対象 | `index.html`・`sw.js`・`manifest.json`・`articles.json`・`src/*.html` |

## URL設計

| ページ | URL |
|--------|-----|
| トップ | `https://masui-s.github.io/claude_blogs/` |
| 記事 | `https://masui-s.github.io/claude_blogs/src/[filename].html` |
