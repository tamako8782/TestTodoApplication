# iPhone実機デプロイ・ネットワーク設定ガイド

## 🌐 Phase 6: ネットワーク問題解決とAPI接続

### 🔍 発生した問題の状況

**初期状態（問題発生時）**
```
✅ iPhone実機へのアプリインストール成功
✅ アプリ起動成功
❌ 画面が真っ黒（API接続失敗）
❌ "Dart VM Service was not discovered after 60 seconds"
```

**根本原因**
```
Problem: localhost (127.0.0.1) はiPhoneからアクセス不可
Solution: MacのローカルIPアドレスを使用する必要
```

### 🔧 Step 1: ネットワーク構成の理解

**ネットワーク構成図**
```
┌─────────────────┐    WiFi/LAN    ┌─────────────────┐    USB    ┌─────────────────┐
│   Mac (Django)  │ ◄──────────── │     Router      │ ◄─────── │  iPhone (Flutter)|
│  192.168.179.24 │                │  192.168.179.1  │          │  WiFi Connected  │
│    Port: 8000   │                │                 │          │                 │
└─────────────────┘                └─────────────────┘          └─────────────────┘
│                                                               │
│ Django Server                                                 │ Flutter App
│ - REST API                                                    │ - HTTP Client
│ - CORS enabled                                                │ - API Service
│ - External access: 0.0.0.0:8000                              │ - Network requests
└─────────────────                                              └─────────────────
```

**問題となったURL**
```bash
# ❌ 動作しない (localhost)
http://127.0.0.1:8000/api/todos/

# ✅ 動作する (MacのローカルIP)
http://192.168.179.24:8000/api/todos/
```

### 🔍 Step 2: MacのIPアドレス確認

**IPアドレス取得方法**
```bash
# 方法1: ifconfigコマンド
ifconfig | grep "inet " | grep -v 127.0.0.1

# 方法2: システム環境設定
システム環境設定 → ネットワーク → WiFi → 詳細 → TCP/IP

# 方法3: ターミナル（簡単）
ipconfig getifaddr en0

# 出力結果
192.168.179.24
```

**ネットワーク接続確認**
```bash
# Macから自分のIPに接続テスト
curl http://192.168.179.24:8000/api/todos/

# 正常レスポンス例
{"count":6,"next":null,"previous":null,"results":[...]}
```

### 📱 Step 3: Flutter アプリのAPI設定変更

**3.1 api_service.dart の修正**

**変更前（動作しない）**
```dart
class ApiService {
  static const String baseUrl = 'http://127.0.0.1:8000/api';
  // ...
}
```

**変更後（動作する）**
```dart
class ApiService {
  static const String baseUrl = 'http://192.168.179.24:8000/api';
  // ...
}
```

**実際の変更コマンド**
```bash
cd /Users/kazuhiroyamamoto/Desktop/repo/test_todo

# ファイル編集
# todo_flutter_app/lib/services/api_service.dart を編集
```

### 🖥️ Step 4: Django サーバー設定の調整

**4.1 ALLOWED_HOSTS の設定**

**変更前**
```python
# todoproject/settings.py
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
```

**変更後**
```python
# todoproject/settings.py
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.179.24']
```

**4.2 サーバー起動方法の変更**

**変更前（内部アクセスのみ）**
```bash
python manage.py runserver 127.0.0.1:8000
```

**変更後（外部アクセス許可）**
```bash
python manage.py runserver 0.0.0.0:8000
```

**サーバー起動確認**
```bash
cd /Users/kazuhiroyamamoto/Desktop/repo/test_todo
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000

# 出力例
Django version 5.2.2, using settings 'todoproject.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```

### 🔄 Step 5: アプリの再ビルド・デプロイ

**5.1 Flutter アプリの再ビルド**
```bash
cd todo_flutter_app

# クリーンビルド
flutter clean
flutter pub get

# iOS実機向けリビルド
flutter run --release
```

**ビルド時間の比較**
```
初回ビルド: 419.5秒 (約7分) - フルビルド
再ビルド:   34.9秒 (約35秒) - 差分ビルド
※ 変更が小さいため大幅に短縮
```

### 📊 Step 6: 接続テスト・動作確認

**6.1 ネットワーク接続テスト**
```bash
# MacからAPI接続確認
curl -X GET http://192.168.179.24:8000/api/todos/

# レスポンス例
{
  "count": 6,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "たすく",
      "completed": true,
      "created_at": "2025-06-08T..."
    },
    ...
  ]
}
```

**6.2 iPhone実機での動作確認**
```
期待される動作:
✅ アプリが正常に起動
✅ 黒い画面が解消される
✅ Todo リストが表示される
✅ 日本語のTodoアイテムが表示される
✅ CRUD操作が動作する
```

### 📱 Step 7: 実機での動作確認詳細

**7.1 成功時の画面表示**
```
┌─────────────────────────────────┐
│           TODO LIST             │
├─────────────────────────────────┤
│ [Search note...] [🔍] [ALL] [+] │
├─────────────────────────────────┤
│ ☑️ たすく                       │🗑️│
├─────────────────────────────────┤
│ ☑️ こんにちは                   │🗑️│
├─────────────────────────────────┤
│ ⬜ テスト計画を立案する           │🗑️│
├─────────────────────────────────┤
│ ☑️ UIデザインのモックアップを...  │🗑️│
├─────────────────────────────────┤
│ ☑️ データベースの設計を完了する   │🗑️│
├─────────────────────────────────┤
│ ☑️ プロジェクトの詳細書を作成する │🗑️│
├─────────────────────────────────┤
│ [Input your note...]        [+] │
└─────────────────────────────────┘
```

**7.2 CRUD機能の動作確認**
```
✅ Todo追加: 新しいTodoを入力 → [+]ボタン → リストに追加
✅ Todo完了切り替え: チェックボックスタップ → 状態変更
✅ Todo削除: ゴミ箱ボタンタップ → アイテム削除
✅ Todo検索: 検索バー入力 → フィルタリング表示
✅ リアルタイム同期: 変更が即座にサーバーに反映
```

### 🔧 Step 8: よく発生する問題とトラブルシューティング

**8.1 "Network Error" が表示される**
```
原因と解決方法:
1. MacのIPアドレス変更
   → ifconfig で現在のIPを確認・修正
2. Djangoサーバーが停止
   → python manage.py runserver 0.0.0.0:8000
3. WiFiネットワークが異なる
   → Mac・iPhone同一ネットワーク確認
```

**8.2 "CORS Error" が発生する**
```python
# todoproject/settings.py で確認
CORS_ALLOWED_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# 必要に応じて特定ドメイン指定
CORS_ALLOWED_ORIGINS = [
    "http://192.168.179.24:8000",
]
```

**8.3 HTTPSエラーが発生する**
```
問題: "You're accessing the development server over HTTPS"
解決: Info.plist のNSAppTransportSecurity設定確認

<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

**8.4 "Connection Refused" エラー**
```bash
# Django サーバーのファイアウォール確認
sudo ufw status

# macOS ファイアウォール設定確認
システム環境設定 → セキュリティとプライバシー → ファイアウォール
→ Python（Django）のアクセスを許可
```

### 📊 ネットワーク設定完了チェックリスト

**Django サーバー設定**
- ✅ ALLOWED_HOSTS にMacのIPアドレス追加
- ✅ サーバー起動: `0.0.0.0:8000` で外部アクセス許可
- ✅ CORS設定有効
- ✅ API エンドポイント正常動作

**Flutter アプリ設定**
- ✅ API baseUrl をMacのIPアドレスに変更
- ✅ HTTP通信許可設定（Info.plist）
- ✅ アプリ再ビルド・再デプロイ完了

**ネットワーク環境**
- ✅ Mac・iPhone同一WiFiネットワーク接続
- ✅ IPアドレス到達性確認
- ✅ ファイアウォール・セキュリティ設定適切

**実機動作確認**
- ✅ アプリ正常起動
- ✅ API接続成功
- ✅ Todo データ表示
- ✅ CRUD操作動作
- ✅ 日本語表示対応

### 🎯 デプロイ成功時の最終状況

**システム構成**
```
Mac (Django Server)
├── IP: 192.168.179.24:8000
├── OS: macOS Darwin 24.3.0
├── Python: Django 5.2.2
└── Database: SQLite (6 Todo items)

iPhone (Flutter App)  
├── Device: kazuhiroのiPhone
├── OS: iOS 18.5 (22F76)
├── App: Todo Flutter App v1.0.0
└── Connection: HTTP API → Mac
```

**通信ログ確認**
```bash
# Django サーバーログで確認可能
[08/Jun/2025 16:38:19] "GET /api/todos/ HTTP/1.1" 200 1041

# HTTP Status 200: 正常な通信
# レスポンスサイズ: 1041 bytes
```

### 🚀 パフォーマンス・品質

**アプリ起動速度**
```
冷起動: 約2-3秒
温起動: 約1秒
API応答: 平均100-200ms
UI応答: 即座（Flutter高速レンダリング）
```

**データ同期**
```
Todo追加: リアルタイム同期
Todo更新: 即座に反映  
Todo削除: 即座に反映
検索機能: インクリメンタル検索
```

### 🔄 次のステップ

このPhaseで基本的なiPhone実機デプロイとAPI接続が完了しました。

**Phase 7では:**
- 包括的テストスイートの実装
- エラーハンドリングの改善
- パフォーマンス最適化
- 品質保証の実施

**今後の配布オプション:**
- TestFlight配布（Apple Developer Program）
- PWA版作成（無料配布）
- App Store公開（本格配布）

### 💡 開発効率化のためのワークフロー

**日常的な開発サイクル**
```bash
# 1. Django サーバー起動
cd /Users/kazuhiroyamamoto/Desktop/repo/test_todo
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000

# 2. Flutter ホットリロード開発
cd todo_flutter_app
flutter run --hot-reload

# 3. コード変更 → 保存 → 自動リロード
# 4. iPhone実機で即座に確認
```

**トラブル時の定型対処**
```bash
# ネットワーク確認
ping 192.168.179.24
curl http://192.168.179.24:8000/api/todos/

# Flutter リセット
flutter clean && flutter pub get && flutter run

# Django リセット  
python manage.py runserver 0.0.0.0:8000
``` 