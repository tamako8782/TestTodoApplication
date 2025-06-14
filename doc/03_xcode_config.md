# Xcode設定・ビルド・実機デプロイガイド

## 🍎 Phase 4 & 5: Xcode設定からiPhone実機デプロイまで

### 🔧 前提条件

**必要な環境**
- macOS (Darwin 24.3.0以降)
- Xcode 15+ インストール済み
- Apple ID（開発者アカウント）
- iPhone実機（iOS 12以降）
- Lightning/USB-Cケーブル

**Flutter環境確認**
```bash
# 現在の作業ディレクトリ
cd /Users/kazuhiroyamamoto/Desktop/repo/test_todo/todo_flutter_app

# Flutter環境・接続デバイス確認
flutter doctor -v
flutter devices
```

### 📱 Step 1: iOS実機の準備

**iPhone側設定**
1. **設定 → 一般 → 情報 → デベロッパ**: デベロッパーアプリをタップ
2. **設定 → プライバシーとセキュリティ → デベロッパーモード**: 有効化
3. **信頼設定**: 後でXcodeビルド後に設定

**Mac側でデバイス認識確認**
```bash
# デバイス確認
flutter devices

# 出力例
iPhone • 00008110-001234567890123E • ios • iOS 18.5 22F76
```

### 🔨 Step 2: Xcodeプロジェクトを開く

```bash
# Xcodeワークスペースを開く（重要: .xcodeprojではなく.xcworkspace）
open ios/Runner.xcworkspace
```

**Xcodeで開くべきファイル**
```
todo_flutter_app/ios/Runner.xcworkspace  ← これを開く
```

### ⚙️ Step 3: Xcode での基本設定

**3.1 プロジェクト設定確認**
```
Navigator → Runner プロジェクト選択
→ TARGETS: Runner を選択
→ General タブ
```

**重要な設定項目**
```
Display Name: Todo Flutter App
Bundle Identifier: com.example.todoFlutterApp  # 一意である必要
Version: 1.0.0
Build: 1

Deployment Info:
├── iOS Deployment Target: 12.0以降推奨
├── Device Orientation: Portrait, Landscape Left, Landscape Right
└── Status Bar Style: Default
```

**3.2 Signing & Capabilities設定**
```
Signing & Capabilities タブ
├── Automatically manage signing: ✅ 有効
├── Team: [あなたのApple ID] を選択
├── Provisioning Profile: Xcode Managed Profile
└── Bundle Identifier: 一意のIDに変更（例: com.yourname.todoapp）
```

**Apple IDがない場合の対処**
```
Xcode → Preferences → Accounts → [+] → Add Apple ID
無料のApple IDでも実機テストは可能（7日間の制限あり）
```

### 🏗️ Step 4: ビルド設定の調整

**4.1 Build Settings確認**
```
Build Settings タブ → All & Combined表示

重要な設定:
├── iOS Deployment Target: 12.0
├── Valid Architectures: arm64
├── Enable Bitcode: No
└── Swift Language Version: Swift 5以降
```

**4.2 Info.plist設定確認**
```
Info.plist ファイル確認:
ios/Runner/Info.plist

重要な設定:
├── CFBundleDisplayName: Todo Flutter App
├── CFBundleIdentifier: $(PRODUCT_BUNDLE_IDENTIFIER)
├── CFBundleVersion: $(FLUTTER_BUILD_NUMBER)
├── CFBundleShortVersionString: $(FLUTTER_BUILD_NAME)
└── NSAppTransportSecurity: 
    └── NSAllowsArbitraryLoads: YES  # HTTP通信許可
```

### 📱 Step 5: デバイス選択・初回ビルド

**5.1 ターゲットデバイス選択**
```
Xcode上部のスキーム選択部分:
[Runner] > [Your iPhone Name] を選択

※ シミュレーターではなく実機を選択
```

**5.2 初回ビルド実行**
```bash
# Flutterからのビルド（推奨）
flutter run --release

# または Xcode からのビルド
Xcode: Product → Run (⌘+R)
```

**初回ビルド時の設定**
```
ビルド時間: 初回 10-15分程度
生成される要素:
├── iOS App Bundle (.app)
├── Provisioning Profile
├── Code Signing Certificate
└── Debug Symbols
```

### 🔐 Step 6: 証明書・信頼設定

**6.1 開発者証明書の信頼設定（iPhone側）**
```
初回インストール後、iPhoneで:
設定 → 一般 → VPNとデバイス管理
→ デベロッパApp → [あなたのApple ID]
→ "[Apple ID] を信頼" をタップ
→ 信頼 をタップ
```

**6.2 信頼設定完了の確認**
```
ホーム画面にアプリアイコンが表示される
アプリをタップして起動確認
```

### 🚀 Step 7: アプリの動作確認

**7.1 アプリ起動テスト**
```
期待される動作:
✅ アプリが起動する
✅ スプラッシュ画面が表示される
✅ メイン画面（Todo リスト）が表示される

この時点では API接続エラーが発生する可能性があります
（Phase 6で解決）
```

**7.2 基本機能テスト**
```
UI要素の確認:
✅ "TODO LIST" タイトル表示
✅ 検索バー表示
✅ "ALL" フィルター表示
✅ 新規Todo入力エリア表示
✅ "+" 追加ボタン表示

※ API通信は後で設定
```

### 🔧 Step 8: よくある問題とトラブルシューティング

**8.1 ビルドエラー: "No Provisioning Profile"**
```
解決方法:
1. Bundle Identifier を一意のものに変更
2. Apple ID でサインイン確認
3. "Automatically manage signing" を有効化
4. Clean Build Folder (⌘+Shift+K)
```

**8.2 ビルドエラー: "Flutter.framework not found"**
```bash
解決方法:
cd ios
rm -rf Pods/ Podfile.lock
cd ..
flutter clean
flutter pub get
cd ios
pod install
```

**8.3 実機で起動しない: "Untrusted Developer"**
```
解決方法:
iPhone: 設定 → 一般 → VPNとデバイス管理
→ 開発者を信頼する設定を実行
```

**8.4 "Could not launch" エラー**
```
解決方法:
1. iPhone再起動
2. Xcodeでクリーンビルド
3. ケーブル接続確認
4. iOS Deployment Target確認
```

### 🏃‍♂️ Step 9: リリースビルドの作成

**9.1 リリースモードでのビルド**
```bash
# リリースビルド作成
flutter build ios --release

# または Xcode Archive
Xcode: Product → Archive
```

**9.2 Archive の確認**
```
Xcode → Window → Organizer
→ Archives タブ
→ 作成されたアーカイブを確認
```

### 📊 Xcode設定フェーズ完了チェックリスト

**開発環境設定**
- ✅ Xcode プロジェクト正常オープン
- ✅ Apple ID アカウント設定完了
- ✅ Bundle Identifier 設定完了
- ✅ Signing & Capabilities 設定完了

**ビルド・実機テスト**
- ✅ 初回ビルド成功
- ✅ iPhone実機認識
- ✅ アプリインストール成功
- ✅ 開発者信頼設定完了
- ✅ アプリ起動確認

**設定ファイル**
- ✅ Info.plist 設定適切
- ✅ Build Settings 適切
- ✅ HTTP通信許可設定

### 🎯 実機デプロイ成功時の状況

**デバイス情報**
```
デバイス名: kazuhiroのiPhone
iOS バージョン: iOS 18.5 (22F76)
接続状態: USB接続
開発者モード: 有効
```

**アプリ情報**
```
アプリ名: Todo Flutter App
Bundle ID: com.example.todoFlutterApp
バージョン: 1.0.0 (1)
サイズ: 約 50-80MB
```

**ビルド結果**
```
初回ビルド時間: 419.5秒 (約7分)
2回目以降: 34.9秒 (高速)
※ 差分ビルドにより大幅短縮
```

### 🔄 次のステップ予告

Phase 6では、iPhoneアプリからDjangoサーバーへの接続設定を行います。

**予想される課題:**
1. ネットワーク接続エラー (localhost → IP変更)
2. CORS設定調整
3. HTTP通信許可設定
4. ファイアウォール・セキュリティ設定

これらの問題解決により、完全に動作するTodoアプリが完成します。

### 💡 開発効率向上のTips

**Xcodeショートカット**
```
⌘+R: ビルド・実行
⌘+Shift+K: クリーンビルド
⌘+B: ビルドのみ
⌘+.: ビルド停止
```

**Flutter便利コマンド**
```bash
flutter logs                    # ログ確認
flutter run --hot-reload       # ホットリロード有効
flutter run --release          # リリースモード
flutter clean && flutter run   # クリーンビルド
``` 