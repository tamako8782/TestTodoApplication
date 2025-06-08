# Django + Flutter Todo アプリケーション

**Django REST API バックエンド + Flutter モバイルフロントエンドによる完全なフルスタック Todo アプリケーション**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Django](https://img.shields.io/badge/Django-5.2.2-green.svg)](https://djangoproject.com/)
[![Flutter](https://img.shields.io/badge/Flutter-3.32.2-blue.svg)](https://flutter.dev/)

## 🚀 クイックスタート

### 1. リポジトリのクローン
```bash
git clone git@github.com:tamako8782/TestTodoApplication.git
cd TestTodoApplication
```

### 2. 環境変数の設定
```bash
# 環境変数のテンプレートをコピー
cp .env.example .env
cp todo_flutter_app/.env.example todo_flutter_app/.env

# .envファイルを実際の値に編集
# - Django: SECRET_KEY, ALLOWED_HOSTS など
# - Flutter: API_BASE_URL (Django サーバーの URL)
```

### 3. Django バックエンドの起動
```bash
# 仮想環境の作成
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 依存関係のインストール
pip install -r requirements.txt

# データベースのセットアップ
python manage.py makemigrations
python manage.py migrate

# Django サーバーの起動
python manage.py runserver 0.0.0.0:8000
```

### 4. Flutter アプリの起動
```bash
cd todo_flutter_app

# Flutter 依存関係のインストール
flutter pub get

# 好みのプラットフォームで実行
flutter run --dart-define-from-file=.env
```

## 📋 機能

### ✅ バックエンド (Django REST API)
- **CRUD 操作**: Todo の作成、読み取り、更新、削除
- **検索機能**: タイトルによる Todo フィルタリング
- **RESTful API 設計**: 一貫性のあるエンドポイント構造
- **ページネーション対応**: 効率的なデータ読み込み
- **CORS 設定**: クロスオリジンリソース共有
- **環境ベース設定**: セキュアな設定管理

### ✅ フロントエンド (Flutter モバイルアプリ)
- **クロスプラットフォーム対応**: iOS, Android, Web, Desktop
- **Material Design**: モダンでレスポンシブな UI
- **ダークテーマ**: 美しいダークモードインターフェース
- **リアルタイム同期**: バックエンドとの即座な更新
- **環境設定**: 動的 API エンドポイント
- **エラーハンドリング**: ユーザーフレンドリーなエラーメッセージ

## 🏗️ アーキテクチャ

```
┌─────────────────┐    HTTP API     ┌─────────────────┐
│   Flutter App   │ ◄─────────────► │  Django Backend │
│                 │     JSON        │                 │
│  • iOS/Android  │                 │  • REST API     │
│  • Web/Desktop  │                 │  • SQLite DB    │
│  • Material UI  │                 │  • Admin Panel  │
└─────────────────┘                 └─────────────────┘
```

## 🛠️ 技術スタック

| コンポーネント | 技術 | バージョン |
|-----------|------------|---------|
| **バックエンド** | Django | 5.2.2 |
| **API フレームワーク** | Django REST Framework | 最新 |
| **データベース** | SQLite | 内蔵 |
| **フロントエンド** | Flutter | 3.32.2 |
| **状態管理** | Provider | 最新 |
| **HTTP クライアント** | http package | 最新 |
| **UI デザイン** | Material Design | 最新 |

## 📁 プロジェクト構造

```
TestTodoApplication/
├── 📄 README.md                     # このファイル
├── 📄 LICENSE                       # MIT ライセンス
├── 📄 requirements.txt              # Python 依存関係
├── 📄 .env.example                  # Django 環境変数テンプレート
├── 📄 .gitignore                    # Git 除外ルール
├── 📂 doc/                          # ドキュメント
│   ├── 📄 README.md                 # 完全な開発ガイド
│   ├── 📄 01_flutter_setup.md       # Flutter 環境構築
│   ├── 📄 02_xcode_config.md        # Xcode 設定
│   ├── 📄 03_deployment.md          # 本番デプロイ
│   ├── 📄 04_testing.md             # テスト実装
│   ├── 📄 05_troubleshooting.md     # よくある問題と解決方法
│   └── 📄 06_django_api.md          # REST API ドキュメント
├── 📂 todoproject/                  # Django プロジェクト設定
│   ├── 📄 settings.py               # Django 設定
│   ├── 📄 urls.py                   # URL ルーティング
│   └── 📄 wsgi.py                   # WSGI 設定
├── 📂 todo/                         # Django アプリ
│   ├── 📄 models.py                 # データモデル
│   ├── 📄 api_views.py              # REST API エンドポイント
│   ├── 📄 serializers.py            # DRF シリアライザー
│   ├── 📄 tests.py                  # バックエンドテスト (19テスト)
│   └── 📂 templates/                # HTML テンプレート
└── 📂 todo_flutter_app/             # Flutter アプリケーション
    ├── 📄 pubspec.yaml              # Flutter 依存関係
    ├── 📄 .env.example              # Flutter 環境変数テンプレート
    ├── 📂 lib/                      # Dart ソースコード
    │   ├── 📄 main.dart             # アプリエントリーポイント
    │   ├── 📂 models/               # データモデル
    │   ├── 📂 services/             # API サービス
    │   ├── 📂 screens/              # UI 画面
    │   └── 📂 widgets/              # 再利用可能コンポーネント
    ├── 📂 test/                     # Flutter テスト
    └── 📂 ios/android/web/...       # プラットフォーム固有ファイル
```

## 🚀 開発ガイド

### 前提条件
- **Python 3.8+** with pip
- **Flutter SDK 3.0+**
- **Git** バージョン管理
- **コードエディター** (VS Code 推奨)

### ステップバイステップセットアップ

1. **環境セットアップ** 🔧
   - `.env.example` → `.env` にコピー (Django と Flutter 両方)
   - データベースと API 設定を構成

2. **バックエンド開発** 🖥️
   - Django REST API から開始
   - `http://localhost:8000/api/` でエンドポイントをテスト

3. **フロントエンド開発** 📱
   - Flutter アプリを構成
   - Django API に接続
   - 好みのプラットフォームでテスト

4. **統合テスト** 🧪
   - Django テスト実行: `python manage.py test`
   - Flutter テスト実行: `flutter test`

5. **本番デプロイ** 🚀
   - [デプロイガイド](doc/03_deployment.md) を参照

## 📚 ドキュメント

| ガイド | 説明 | 対象読者 |
|-------|-------------|----------|
| **[プロジェクト概要](doc/README.md)** | 完全な開発の旅程 | 全開発者 |
| **[Flutter セットアップ](doc/01_flutter_setup.md)** | Flutter 環境とアプリ作成 | モバイル開発者 |
| **[Xcode 設定](doc/02_xcode_config.md)** | iOS 開発セットアップ | iOS 開発者 |
| **[デプロイ](doc/03_deployment.md)** | 本番デプロイガイド | DevOps エンジニア |
| **[テスト](doc/04_testing.md)** | 包括的テストスイート | QA エンジニア |
| **[トラブルシューティング](doc/05_troubleshooting.md)** | よくある問題と解決方法 | 全開発者 |
| **[REST API](doc/06_django_api.md)** | API エンドポイントドキュメント | バックエンド開発者 |

## 🧪 テスト

### バックエンドテスト
```bash
# Django テストをすべて実行
python manage.py test

# カバレッジ付き
pip install coverage
coverage run manage.py test
coverage report
```

### フロントエンドテスト
```bash
cd todo_flutter_app

# Flutter テスト実行
flutter test

# 統合テスト
flutter drive --target=test_driver/app.dart
```

## 🛠️ 開発ワークフロー

1. **機能開発**
   - バックエンド: API エンドポイント追加 → テスト作成 → ドキュメント更新
   - フロントエンド: UI 追加 → API 接続 → テスト作成

2. **コード品質**
   - Python: PEP 8 に従い、black フォーマッターを使用
   - Dart: dart format 規約に従う

3. **バージョン管理**
   - 機能ブランチ: `feature/your-feature-name`
   - コミットメッセージ: conventional commits を使用

## 🔧 設定

### 環境変数

**Django (`.env`)**
```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,your-server-ip
CORS_ALLOW_ALL_ORIGINS=True
```

**Flutter (`todo_flutter_app/.env`)**
```env
API_BASE_URL=http://your-server-ip:8000/api
APP_NAME=Todo Flutter App
APP_VERSION=1.0.0
```

## 🤝 コントリビューション

1. リポジトリをフォーク
2. 機能ブランチを作成: `git checkout -b feature/amazing-feature`
3. 変更をコミット: `git commit -m 'Add amazing feature'`
4. ブランチにプッシュ: `git push origin feature/amazing-feature`
5. プルリクエストを開く

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下で公開されています - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🙋‍♂️ サポート

- **ドキュメント**: 詳細なガイドは [doc/](doc/) フォルダをチェック
- **問題報告**: バグ報告や機能リクエストは Issue を作成
- **質問**: GitHub Discussions を利用

---

**Django と Flutter で ❤️ を込めて構築** 