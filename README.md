# Django Todo アプリケーション

モダンでシンプルなTodoアプリケーションです。Djangoで構築され、美しいダークテーマのUIを持っています。

## 機能

- ✅ Todo項目の追加
- ✅ Todo項目の完了/未完了の切り替え
- ✅ Todo項目の削除
- ✅ Todo項目の検索
- ✅ レスポンシブなモダンUI
- ✅ リアルタイムフィードバック

## セットアップ

### 1. 仮想環境の作成とアクティベート

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate     # Windows
```

### 2. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 3. データベースマイグレーション

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 開発サーバーの起動

```bash
python manage.py runserver
```

アプリケーションは http://localhost:8000 でアクセスできます。

## 使用方法

1. **Todo の追加**: 画面右上の「+」ボタンをクリックして新しいTodoを追加
2. **Todo の完了**: チェックボックスをクリックして完了/未完了を切り替え
3. **Todo の削除**: Todoアイテムにホバーして表示される削除ボタンをクリック
4. **Todo の検索**: 上部の検索バーでTodoを検索

## 技術スタック

- **Backend**: Django 5.2.2
- **Frontend**: HTML, CSS (Tailwind CSS)
- **Database**: SQLite (開発用)
- **JavaScript**: バニラJS (モーダル機能)

## プロジェクト構造

```
test_todo/
├── manage.py
├── requirements.txt
├── README.md
├── todo/                    # メインアプリケーション
│   ├── models.py           # Todoモデル
│   ├── views.py            # ビューロジック
│   ├── urls.py             # URL設定
│   ├── admin.py            # 管理パネル設定
│   └── templates/todo/     # テンプレートファイル
│       ├── base.html
│       ├── todo_list.html
│       └── add_todo.html
└── todoproject/            # プロジェクト設定
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## カスタマイズ

アプリケーションは簡単にカスタマイズできます：

- **スタイル**: `todo/templates/todo/base.html` でTailwind CSSクラスを編集
- **機能**: `todo/models.py` でTodoモデルにフィールドを追加
- **ビュー**: `todo/views.py` で新しい機能を追加

## 開発者向け

### 管理パネル

スーパーユーザーを作成して管理パネルにアクセス：

```bash
python manage.py createsuperuser
```

http://localhost:8000/admin でアクセスできます。

### テストデータの追加

```bash
python manage.py shell
>>> from todo.models import Todo
>>> Todo.objects.create(title="サンプルTodo", completed=False)
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。 