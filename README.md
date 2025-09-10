# TODOアプリケーション

PythonとFastAPIで構築されたモダンなTODOアプリケーション。

## 機能

- TODOアイテムの作成、読み取り、更新、削除
- RESTful API設計
- Python型ヒントによる型安全性
- FastAPIによる高速で効率的な処理

## 必要要件

- Python 3.11以上
- uv（依存関係管理用）

## インストール

1. リポジトリのクローン:
```bash
git clone <リポジトリURL>
cd <プロジェクトディレクトリ>
```

2. uvを使用した依存関係のインストール:
```bash
uv sync
```

## 使用方法

### アプリケーションの実行

開発サーバーの起動:
```bash
uv run uvicorn app.main:app --reload
```

APIは `http://localhost:8000` でアクセス可能です

### APIドキュメント

サーバー起動後、以下にアクセスできます:
- インタラクティブAPIドキュメント（Swagger UI）: `http://localhost:8000/docs`
- 代替APIドキュメント（ReDoc）: `http://localhost:8000/redoc`

## 開発

### テストの実行
```bash
uv run pytest
```

### リンティングとフォーマット
```bash
uv run ruff check .
uv run ruff format .
```

### 型チェック
```bash
uv run mypy .
```

## プロジェクト構造

```
.
├── app/
│   ├── main.py          # FastAPIアプリケーションのエントリーポイント
│   ├── models/          # データモデル
│   ├── routers/         # APIルートハンドラー
│   └── services/        # ビジネスロジック
├── tests/               # テストファイル
├── pyproject.toml       # プロジェクト設定と依存関係
├── CLAUDE.md           # 開発手順
└── README.md           # このファイル
```

## ライセンス

[ライセンス情報は後日追加予定]
