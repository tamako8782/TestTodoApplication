# トラブルシューティング・よくある問題と解決方法

## 🚨 開発過程で発生した主要な問題と解決法

### 📱 1. iPhone実機デプロイ関連

#### 1.1 問題: アプリが黒い画面で固まる

**症状**
```
✅ Xcodeでビルド成功
✅ iPhone実機にインストール成功
❌ アプリ起動後、黒い画面で何も表示されない
❌ "Dart VM Service was not discovered after 60 seconds"
```

**根本原因**
```
Flutter アプリが localhost (127.0.0.1) にアクセスしようとしているが、
iPhoneからはMacの localhost にアクセスできない
```

**解決方法**
```bash
# 1. MacのIPアドレスを確認
ifconfig | grep "inet " | grep -v 127.0.0.1
# または
ipconfig getifaddr en0

# 2. Flutter app の API設定を変更
# api_service.dart
static const String baseUrl = 'http://192.168.179.24:8000/api';

# 3. Django ALLOWED_HOSTS を更新
# settings.py
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.179.24']

# 4. Django サーバーを外部アクセス許可で起動
python manage.py runserver 0.0.0.0:8000
```

#### 1.2 問題: "Untrusted Developer" エラー

**症状**
```
アプリをタップすると
「信頼されていないデベロッパ」エラー
アプリが起動しない
```

**解決方法**
```
iPhone設定:
設定 → 一般 → VPNとデバイス管理
→ デベロッパApp → [あなたのApple ID]
→ "信頼" をタップ
```

#### 1.3 問題: Xcodeでビルドエラー

**症状**
```
No Provisioning Profile found
Code signing error
Bundle Identifier conflicts
```

**解決方法**
```
1. Bundle Identifier を一意のものに変更
   com.example.todoFlutterApp → com.yourname.todoapp

2. Apple ID でサインイン確認
   Xcode → Preferences → Accounts

3. Automatically manage signing を有効化

4. Clean Build
   Xcode: Product → Clean Build Folder (⌘+Shift+K)
```

### 🌐 2. ネットワーク・API接続関連

#### 2.1 問題: CORS エラー

**症状**
```
Browser Console:
Access to XMLHttpRequest blocked by CORS policy
```

**解決方法**
```python
# settings.py
CORS_ALLOWED_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# 特定オリジンのみ許可する場合
CORS_ALLOWED_ORIGINS = [
    "http://192.168.179.24:8000",
]
```

#### 2.2 問題: "Connection Refused" エラー

**症状**
```
Network Error: Connection refused
API calls failing
```

**解決方法チェックリスト**
```bash
# 1. Django サーバー起動確認
python manage.py runserver 0.0.0.0:8000

# 2. ファイアウォール設定確認
# macOS
システム環境設定 → セキュリティとプライバシー → ファイアウォール

# 3. ネットワーク到達性確認
ping 192.168.179.24
curl http://192.168.179.24:8000/api/todos/

# 4. Mac・iPhone同一ネットワーク確認
WiFi設定で同じSSIDに接続
```

#### 2.3 問題: HTTPSエラー

**症状**
```
Django Log:
"You're accessing the development server over HTTPS, but it only supports HTTP"
```

**解決方法**
```xml
<!-- ios/Runner/Info.plist -->
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

### 🧪 3. テスト関連

#### 3.1 問題: URLリバースエラー

**症状**
```python
NoReverseMatch: Reverse for 'todo:api_todos' not found
```

**原因**
```
URL namespace の不整合
todo:api_todos vs api:todos
```

**解決方法**
```python
# URL設定確認
# todoproject/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls', namespace='todo')),
    path('api/', include('todo.api_urls', namespace='api')),  # ここを確認
]

# テストコード修正
# 修正前
url = reverse('todo:api_todos')
# 修正後
url = reverse('api:todos')
```

#### 3.2 問題: ページネーションテストエラー

**症状**
```python
AssertionError: 2 != 10
Expected len(response.data) == 10, got 2
```

**原因**
```
DRF ページネーションレスポンス構造の理解不足
response.data が直接リストではなく辞書構造
```

**解決方法**
```python
# 修正前
self.assertEqual(len(response.data), 10)

# 修正後
self.assertIn('count', response.data)
self.assertIn('results', response.data)
self.assertEqual(len(response.data['results']), 10)
```

### 🔧 4. Flutter関連

#### 4.1 問題: pub get エラー

**症状**
```
flutter pub get
Package dependencies error
Version conflicts
```

**解決方法**
```bash
# 1. キャッシュクリア
flutter clean
rm pubspec.lock

# 2. 依存関係再取得
flutter pub get

# 3. 依存関係の競合解決
flutter pub deps
flutter pub upgrade
```

#### 4.2 問題: iOS Podfile エラー

**症状**
```
CocoaPods error
Flutter.framework not found
```

**解決方法**
```bash
cd ios
rm -rf Pods/ Podfile.lock
cd ..
flutter clean
flutter pub get
cd ios
pod install
```

#### 4.3 問題: Hot Reload が動作しない

**症状**
```
ホットリロードが反応しない
変更が反映されない
```

**解決方法**
```bash
# 1. Flutter Doctor で環境確認
flutter doctor -v

# 2. デバイス接続確認
flutter devices

# 3. 完全リビルド
flutter clean
flutter run --hot-reload
```

### 📊 5. Django設定関連

#### 5.1 問題: "That port is already in use"

**症状**
```bash
python manage.py runserver 127.0.0.1:8000
Error: That port is already in use.
```

**解決方法**
```bash
# 1. ポート使用プロセス確認
lsof -ti:8000

# 2. プロセス終了
kill -9 $(lsof -ti:8000)

# 3. 別ポート使用
python manage.py runserver 0.0.0.0:8001
```

#### 5.2 問題: Static Files 404エラー

**症状**
```
Static files not found
CSS/JS loading fails
```

**解決方法**
```python
# settings.py
import os

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# 静的ファイル収集
python manage.py collectstatic
```

#### 5.3 問題: Migration エラー

**症状**
```
No migrations to apply
Migration conflicts
```

**解決方法**
```bash
# 1. Migration状態確認
python manage.py showmigrations

# 2. Migration作成
python manage.py makemigrations

# 3. Migration適用
python manage.py migrate

# 4. 強制リセット（開発環境のみ）
rm -rf todo/migrations/
python manage.py makemigrations todo
python manage.py migrate
```

### 🎯 6. パフォーマンス関連

#### 6.1 問題: ビルド時間が遅い

**症状**
```
初回ビルド: 7分以上
開発効率が悪い
```

**解決方法**
```bash
# 1. インクリメンタルビルド活用
flutter run --hot-reload  # 変更時は数秒

# 2. 不要な依存関係除去
# pubspec.yaml の見直し

# 3. iOS Simulator 使用（実機より高速）
flutter run  # シミュレーター選択

# 4. リリースビルドは必要時のみ
flutter run --debug     # 開発時（高速）
flutter run --release   # テスト時（最適化）
```

#### 6.2 問題: API応答が遅い

**症状**
```
Todo読み込みに時間がかかる
UIが固まる
```

**解決方法**
```python
# 1. データベースクエリ最適化
# N+1問題回避
todos = Todo.objects.select_related().all()

# 2. ページネーション適切設定
REST_FRAMEWORK = {
    'PAGE_SIZE': 10,  # 適切なサイズ
}

# 3. インデックス追加
class Todo(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
```

### 🔧 7. よく使うデバッグコマンド

#### 7.1 Flutter デバッグ
```bash
# デバイス・環境確認
flutter doctor -v
flutter devices

# ログ確認
flutter logs
flutter run --verbose

# クリーンビルド
flutter clean && flutter pub get && flutter run

# パフォーマンス分析
flutter run --profile
```

#### 7.2 Django デバッグ
```bash
# 開発サーバー詳細ログ
python manage.py runserver --verbosity=2

# データベース確認
python manage.py dbshell
python manage.py shell

# システムチェック
python manage.py check
python manage.py check --deploy
```

#### 7.3 ネットワークデバッグ
```bash
# IP・ネットワーク確認
ifconfig
ipconfig getifaddr en0
ping 192.168.179.24

# API接続確認
curl -X GET http://192.168.179.24:8000/api/todos/
curl -X POST http://192.168.179.24:8000/api/todos/ \
  -H "Content-Type: application/json" \
  -d '{"title":"curl test"}'
```

### 📋 8. 問題対処フローチャート

#### 8.1 アプリが起動しない場合
```
1. Xcodeビルドエラー？
   Yes → 証明書・Bundle ID 確認
   No → 2へ

2. アプリインストール済み？
   No → 実機認識・信頼設定確認
   Yes → 3へ

3. 黒い画面で固まる？
   Yes → ネットワーク・API設定確認
   No → ログ確認・詳細調査
```

#### 8.2 API接続エラーの場合
```
1. Django サーバー起動中？
   No → python manage.py runserver 0.0.0.0:8000
   Yes → 2へ

2. 同一ネットワーク？
   No → WiFi設定確認
   Yes → 3へ

3. CORS設定適切？
   No → settings.py 確認
   Yes → 4へ

4. IP アドレス正しい？
   No → ifconfig で確認・修正
   Yes → ファイアウォール・セキュリティ確認
```

### 💡 9. 予防策・ベストプラクティス

#### 9.1 環境管理
```bash
# .env ファイルで環境変数管理
API_BASE_URL=http://192.168.179.24:8000/api
DEBUG=True

# requirements.txt でバージョン固定
Django==5.2.2
djangorestframework==3.15.2
```

#### 9.2 設定管理
```python
# settings/local.py, settings/production.py で環境分離
# git で .env, local.py は除外
```

#### 9.3 テスト習慣
```bash
# 変更前後でのテスト実行
python manage.py test
flutter test

# デプロイ前チェック
python manage.py check --deploy
flutter build ios --release
```

### 🔄 10. 継続的改善

#### 10.1 定期確認項目
```
□ 依存関係の更新確認
□ セキュリティパッチ適用
□ パフォーマンス監視
□ エラーログ確認
□ テストカバレッジ維持
```

#### 10.2 学習リソース
```
- Flutter 公式ドキュメント
- Django 公式ドキュメント  
- Apple Developer Documentation
- Stack Overflow / GitHub Issues
- 開発コミュニティ参加
```

このトラブルシューティングガイドを活用することで、同様の問題に迅速に対処し、スムーズな開発を継続できます。 