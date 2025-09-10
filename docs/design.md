# TODOアプリケーション設計書

## 1. 概要

PythonベースのTODOアプリケーションの設計書です。このアプリケーションは、タスク管理機能を提供し、REST APIを通じて操作可能な構成となっています。

## 2. 基本機能

### 2.1 コア機能
- **タスク管理（CRUD操作）**
  - タスクの作成（Create）
  - タスクの読み取り（Read）
  - タスクの更新（Update）
  - タスクの削除（Delete）

### 2.2 タスク属性
- **ステータス管理**: 未完了/完了の切り替え
- **優先度設定**: 高（high）/中（medium）/低（low）
- **期限管理**: 期限日の設定と管理
- **カテゴリ分類**: タスクのカテゴリによる分類
- **検索・フィルタリング**: ステータス、カテゴリ、期限での絞り込み

## 3. 技術スタック

### 3.1 バックエンド
| 技術 | 用途 |
|------|------|
| **FastAPI** | 高速で現代的なWeb APIフレームワーク |
| **SQLAlchemy** | ORM（Object-Relational Mapping） |
| **SQLite** | 軽量データベース（開発環境用） |
| **Pydantic** | データバリデーションとシリアライゼーション |
| **Python 3.9+** | プログラミング言語 |

### 3.2 フロントエンド（オプション）
- **Streamlit**: Pythonベースの簡易UIフレームワーク
- **React/Vue.js**: SPA構築用（REST API経由での連携）

## 4. プロジェクト構成

```
todo-app/
├── app/
│   ├── __init__.py           # パッケージ初期化
│   ├── main.py               # FastAPIアプリケーションのエントリポイント
│   ├── models.py             # SQLAlchemyデータベースモデル
│   ├── schemas.py            # Pydanticスキーマ定義
│   ├── database.py           # データベース接続設定
│   ├── crud.py               # CRUD操作の実装
│   └── routers/
│       └── todos.py          # TODOエンドポイントの定義
├── tests/
│   └── test_todos.py         # ユニットテスト
├── requirements.txt          # 依存パッケージリスト
├── .env                      # 環境変数設定
├── .gitignore               # Git除外設定
└── README.md                # プロジェクト説明書
```

## 5. データモデル

### 5.1 Todoテーブル

| フィールド名 | データ型 | 説明 | 制約 |
|------------|---------|------|------|
| id | Integer | 一意識別子 | PRIMARY KEY, AUTO INCREMENT |
| title | String(100) | タスクのタイトル | NOT NULL |
| description | Text | タスクの詳細説明 | NULLABLE |
| status | Boolean | 完了状態（True: 完了, False: 未完了） | DEFAULT: False |
| priority | String(10) | 優先度（high/medium/low） | DEFAULT: 'medium' |
| category | String(50) | カテゴリ | NULLABLE |
| due_date | DateTime | 期限日時 | NULLABLE |
| created_at | DateTime | 作成日時 | NOT NULL, DEFAULT: CURRENT_TIMESTAMP |
| updated_at | DateTime | 更新日時 | NOT NULL, DEFAULT: CURRENT_TIMESTAMP |

## 6. API エンドポイント

### 6.1 基本エンドポイント

| メソッド | エンドポイント | 説明 | リクエストボディ | レスポンス |
|---------|--------------|------|----------------|-----------|
| GET | `/todos` | 全タスク取得 | - | Todo[] |
| GET | `/todos/{id}` | 特定タスク取得 | - | Todo |
| POST | `/todos` | タスク作成 | TodoCreate | Todo |
| PUT | `/todos/{id}` | タスク更新 | TodoUpdate | Todo |
| DELETE | `/todos/{id}` | タスク削除 | - | Message |
| GET | `/todos/filter` | フィルタリング検索 | QueryParams | Todo[] |

### 6.2 クエリパラメータ（フィルタリング）

- `status`: 完了状態でフィルタ（completed/pending）
- `priority`: 優先度でフィルタ（high/medium/low）
- `category`: カテゴリでフィルタ
- `due_date_from`: 期限開始日
- `due_date_to`: 期限終了日

## 7. スキーマ定義

### 7.1 TodoBase（基本スキーマ）
```python
{
    "title": str,
    "description": str | None,
    "priority": str = "medium",
    "category": str | None,
    "due_date": datetime | None
}
```

### 7.2 TodoCreate（作成用スキーマ）
TodoBaseを継承

### 7.3 TodoUpdate（更新用スキーマ）
```python
{
    "title": str | None,
    "description": str | None,
    "status": bool | None,
    "priority": str | None,
    "category": str | None,
    "due_date": datetime | None
}
```

### 7.4 Todo（レスポンススキーマ）
```python
{
    "id": int,
    "title": str,
    "description": str | None,
    "status": bool,
    "priority": str,
    "category": str | None,
    "due_date": datetime | None,
    "created_at": datetime,
    "updated_at": datetime
}
```

## 8. セキュリティ考慮事項

- SQLインジェクション対策: SQLAlchemyのORMを使用
- データバリデーション: Pydanticによる入力検証
- CORS設定: 必要に応じてCORSミドルウェアを設定
- 認証・認可: 将来的にJWT認証を実装可能

## 9. 拡張可能性

### 9.1 将来的な機能追加
- ユーザー認証システム
- タスクの共有機能
- リマインダー通知
- タスクのタグ付け
- ファイル添付機能
- タスクの繰り返し設定

### 9.2 スケーラビリティ
- PostgreSQL/MySQLへの移行対応
- Redis によるキャッシング
- 非同期タスク処理（Celery）

## 10. 開発環境セットアップ

### 10.1 必要要件
- Python 3.9以上
- pip または poetry

### 10.2 インストール手順
```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate  # Windows

# 依存パッケージのインストール
pip install -r requirements.txt

# アプリケーションの起動
uvicorn app.main:app --reload
```

## 11. テスト戦略

- ユニットテスト: pytest を使用
- APIテスト: FastAPIのTestClientを使用
- カバレッジ目標: 80%以上

## 12. デプロイメント

### 12.1 開発環境
- ローカル環境でuvicornを使用

### 12.2 本番環境
- Docker コンテナ化
- Gunicorn + Uvicorn workers
- Nginx によるリバースプロキシ