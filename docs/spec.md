# 要件仕様書

## プロジェクト概要

Claudeに作成してもらったブログ記事（HTML）を公開するためのGitHub Pages + PWA対応サイト。
URL: `https://masui-s.github.io/claude_blogs/`

## 機能要件

### トップページ

- `src/*.html` に存在する記事を一覧表示する
- 各記事に表示する情報: タイトル・投稿日・概要
- 並び順: 投稿日の新しい順（降順）
- 記事タイトルをクリックすると該当記事へ遷移する

### 記事ページ

- `src/` 配下のHTMLファイルをそのまま表示する
- 特別な変換・ラッピングは行わない

### PWA対応

- `manifest.json` によりホーム画面へのインストールを可能にする
- Service Worker によりオフラインキャッシュを実装する
- キャッシュ戦略: Stale While Revalidate（キャッシュを即時返却しつつバックグラウンドで更新）

## 記事HTMLのメタデータ仕様

記事HTMLの `<head>` には以下のタグを含める（Claudeに記事作成を依頼する際のテンプレート）：

```html
<title>記事タイトル</title>
<meta name="description" content="記事の概要">
<meta name="date" content="YYYY-MM-DD">

<!-- OGP -->
<meta property="og:title" content="記事タイトル">
<meta property="og:description" content="記事の概要">
<meta property="og:type" content="article">
```

ビルド時にこれらのタグから `articles.json` を自動生成する。

## 非機能要件

- プッシュ通知・バックグラウンド同期は対象外
- ダークモード対応（システム設定に自動追従）
