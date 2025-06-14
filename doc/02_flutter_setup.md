# Flutter環境構築・アプリ開発ガイド

## 📱 Phase 2: Flutter アプリ開発プロセス

### 🔍 前提条件確認

**既存のDjangoバックエンド状況**
```bash
# Django プロジェクト構成確認
test_todo/
├── todoproject/
│   ├── settings.py    # CORS設定含む
│   └── urls.py        # API URLルーティング
├── todo/
│   ├── models.py      # Todo モデル
│   ├── views.py       # HTML ビュー
│   ├── api_views.py   # REST API ビュー
│   └── serializers.py # DRF シリアライザー
└── manage.py

# 利用可能なAPI エンドポイント
GET  /api/todos/              # Todo一覧取得（ページネーション対応）
POST /api/todos/              # Todo作成
GET  /api/todos/{id}/         # Todo詳細取得
PUT  /api/todos/{id}/         # Todo更新
DELETE /api/todos/{id}/       # Todo削除
```

**Django設定の重要ポイント**
```python
# todoproject/settings.py
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.179.24']  # 後でネットワーク対応
CORS_ALLOWED_ALL_ORIGINS = True  # CORS設定
CORS_ALLOW_CREDENTIALS = True

# REST Framework設定
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

### 🚀 Step 1: Flutter プロジェクト作成

```bash
# 作業ディレクトリで実行
cd /Users/kazuhiroyamamoto/Desktop/repo/test_todo

# Flutter プロジェクト作成
flutter create todo_flutter_app
cd todo_flutter_app

# プロジェクト構造確認
tree -L 3
```

**生成された基本構造**
```
todo_flutter_app/
├── lib/
│   └── main.dart              # エントリーポイント
├── ios/                       # iOS固有設定
│   ├── Runner.xcodeproj/      # Xcodeプロジェクト
│   └── Runner/
│       ├── Info.plist         # アプリ情報
│       └── Assets.xcassets/   # アイコン・画像
├── android/                   # Android固有設定
├── pubspec.yaml              # 依存関係管理
└── test/                     # テストディレクトリ
```

### 📦 Step 2: 依存関係の設定

**pubspec.yaml の編集**
```yaml
name: todo_flutter_app
description: "A new Flutter project."
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: ^3.8.1

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.8
  
  # API通信用
  http: ^1.2.0
  
  # JSON シリアライゼーション
  json_serializable: ^6.8.0
  json_annotation: ^4.9.0
  
  # 状態管理
  provider: ^6.1.2
  
  # 国際化対応
  intl: ^0.19.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^5.0.0
  build_runner: ^2.4.13  # JSON code generation
```

**依存関係インストール**
```bash
flutter pub get
```

### 🏗️ Step 3: プロジェクト構造の構築

**lib/ ディレクトリ構成**
```
lib/
├── main.dart                 # アプリエントリーポイント
├── models/
│   └── todo.dart            # Todo データモデル
├── services/
│   └── api_service.dart     # API通信サービス
├── screens/
│   └── todo_list_screen.dart # メイン画面
└── widgets/
    └── todo_item.dart       # Todo表示コンポーネント
```

### 📝 Step 4: データモデルの実装

**models/todo.dart**
```dart
import 'package:json_annotation/json_annotation.dart';

part 'todo.g.dart';

@JsonSerializable()
class Todo {
  final int id;
  final String title;
  final bool completed;
  final DateTime createdAt;

  Todo({
    required this.id,
    required this.title,
    required this.completed,
    required this.createdAt,
  });

  factory Todo.fromJson(Map<String, dynamic> json) => _$TodoFromJson(json);
  Map<String, dynamic> toJson() => _$TodoToJson(this);
}

@JsonSerializable()
class TodoResponse {
  final int count;
  final String? next;
  final String? previous;
  final List<Todo> results;

  TodoResponse({
    required this.count,
    this.next,
    this.previous,
    required this.results,
  });

  factory TodoResponse.fromJson(Map<String, dynamic> json) => 
      _$TodoResponseFromJson(json);
  Map<String, dynamic> toJson() => _$TodoResponseToJson(this);
}
```

**JSON code generation実行**
```bash
flutter packages pub run build_runner build
```

### 🌐 Step 5: API サービスの実装

**services/api_service.dart**
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/todo.dart';

class ApiService {
  // 重要: 後でネットワーク設定により変更
  static const String baseUrl = 'http://127.0.0.1:8000/api';
  
  // Todo一覧取得（ページネーション対応）
  Future<TodoResponse> getTodos({int page = 1, String? search}) async {
    try {
      final queryParams = <String, String>{
        'page': page.toString(),
      };
      
      if (search != null && search.isNotEmpty) {
        queryParams['search'] = search;
      }
      
      final uri = Uri.parse('$baseUrl/todos/').replace(
        queryParameters: queryParams,
      );
      
      final response = await http.get(
        uri,
        headers: {'Content-Type': 'application/json'},
      );
      
      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body);
        return TodoResponse.fromJson(jsonData);
      } else {
        throw Exception('Failed to load todos: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }
  
  // Todo作成
  Future<Todo> createTodo(String title) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/todos/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'title': title}),
      );
      
      if (response.statusCode == 201) {
        return Todo.fromJson(json.decode(response.body));
      } else {
        throw Exception('Failed to create todo: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }
  
  // Todo更新（完了状態切り替え）
  Future<Todo> updateTodo(int id, {String? title, bool? completed}) async {
    try {
      final Map<String, dynamic> data = {};
      if (title != null) data['title'] = title;
      if (completed != null) data['completed'] = completed;
      
      final response = await http.put(
        Uri.parse('$baseUrl/todos/$id/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(data),
      );
      
      if (response.statusCode == 200) {
        return Todo.fromJson(json.decode(response.body));
      } else {
        throw Exception('Failed to update todo: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }
  
  // Todo削除
  Future<void> deleteTodo(int id) async {
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/todos/$id/'),
        headers: {'Content-Type': 'application/json'},
      );
      
      if (response.statusCode != 204) {
        throw Exception('Failed to delete todo: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }
}
```

### 🎨 Step 6: UI コンポーネントの実装

**widgets/todo_item.dart**
```dart
import 'package:flutter/material.dart';
import '../models/todo.dart';

class TodoItem extends StatelessWidget {
  final Todo todo;
  final VoidCallback onToggle;
  final VoidCallback onDelete;

  const TodoItem({
    Key? key,
    required this.todo,
    required this.onToggle,
    required this.onDelete,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 4.0, horizontal: 16.0),
      padding: const EdgeInsets.all(16.0),
      decoration: BoxDecoration(
        color: Colors.grey[900],
        borderRadius: BorderRadius.circular(8.0),
        border: Border.all(color: Colors.indigo, width: 1.0),
      ),
      child: Row(
        children: [
          // チェックボックス
          GestureDetector(
            onTap: onToggle,
            child: Container(
              width: 24,
              height: 24,
              decoration: BoxDecoration(
                color: todo.completed ? Colors.indigo : Colors.transparent,
                borderRadius: BorderRadius.circular(4),
                border: Border.all(color: Colors.indigo, width: 2),
              ),
              child: todo.completed
                  ? const Icon(Icons.check, color: Colors.white, size: 16)
                  : null,
            ),
          ),
          const SizedBox(width: 16),
          
          // Todo テキスト
          Expanded(
            child: Text(
              todo.title,
              style: TextStyle(
                color: todo.completed ? Colors.white54 : Colors.white,
                fontSize: 18,
                fontWeight: FontWeight.w500,
                decoration: todo.completed 
                    ? TextDecoration.lineThrough 
                    : TextDecoration.none,
              ),
            ),
          ),
          
          // 削除ボタン
          GestureDetector(
            onTap: onDelete,
            child: Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: Colors.red[700],
                borderRadius: BorderRadius.circular(4),
              ),
              child: const Icon(
                Icons.delete,
                color: Colors.white,
                size: 20,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
```

### 🖥️ Step 7: メイン画面の実装

**screens/todo_list_screen.dart**
```dart
import 'package:flutter/material.dart';
import '../models/todo.dart';
import '../services/api_service.dart';
import '../widgets/todo_item.dart';

class TodoListScreen extends StatefulWidget {
  @override
  _TodoListScreenState createState() => _TodoListScreenState();
}

class _TodoListScreenState extends State<TodoListScreen> {
  final ApiService _apiService = ApiService();
  final TextEditingController _searchController = TextEditingController();
  final TextEditingController _newTodoController = TextEditingController();
  
  List<Todo> _todos = [];
  bool _isLoading = false;
  String _searchQuery = '';
  String _errorMessage = '';

  @override
  void initState() {
    super.initState();
    _loadTodos();
  }

  Future<void> _loadTodos() async {
    setState(() {
      _isLoading = true;
      _errorMessage = '';
    });
    
    try {
      final response = await _apiService.getTodos(
        search: _searchQuery.isNotEmpty ? _searchQuery : null,
      );
      setState(() {
        _todos = response.results;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'エラー: $e';
        _isLoading = false;
      });
    }
  }

  Future<void> _addTodo() async {
    if (_newTodoController.text.trim().isEmpty) return;
    
    try {
      await _apiService.createTodo(_newTodoController.text.trim());
      _newTodoController.clear();
      _loadTodos();
    } catch (e) {
      _showErrorSnackBar('Todo追加に失敗しました: $e');
    }
  }

  Future<void> _toggleTodo(Todo todo) async {
    try {
      await _apiService.updateTodo(todo.id, completed: !todo.completed);
      _loadTodos();
    } catch (e) {
      _showErrorSnackBar('更新に失敗しました: $e');
    }
  }

  Future<void> _deleteTodo(Todo todo) async {
    try {
      await _apiService.deleteTodo(todo.id);
      _loadTodos();
    } catch (e) {
      _showErrorSnackBar('削除に失敗しました: $e');
    }
  }

  void _showErrorSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), backgroundColor: Colors.red),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[800],
      appBar: AppBar(
        title: const Text(
          'TODO LIST',
          style: TextStyle(
            color: Colors.white,
            fontSize: 24,
            fontWeight: FontWeight.w500,
          ),
        ),
        backgroundColor: Colors.grey[800],
        elevation: 0,
      ),
      body: Column(
        children: [
          // 検索バー & フィルター
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              children: [
                Expanded(
                  child: Container(
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.white, width: 1),
                    ),
                    child: TextField(
                      controller: _searchController,
                      style: const TextStyle(color: Colors.white),
                      decoration: const InputDecoration(
                        hintText: 'Search note...',
                        hintStyle: TextStyle(color: Colors.grey),
                        border: InputBorder.none,
                        contentPadding: EdgeInsets.all(16),
                        suffixIcon: Icon(Icons.search, color: Colors.white),
                      ),
                      onChanged: (value) {
                        setState(() {
                          _searchQuery = value;
                        });
                        _loadTodos();
                      },
                    ),
                  ),
                ),
                const SizedBox(width: 16),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                  decoration: BoxDecoration(
                    color: Colors.indigo,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Text(
                    'ALL',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 16,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
              ],
            ),
          ),
          
          // Todo リスト
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : _errorMessage.isNotEmpty
                    ? Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text(
                              _errorMessage,
                              style: const TextStyle(color: Colors.red),
                              textAlign: TextAlign.center,
                            ),
                            const SizedBox(height: 16),
                            ElevatedButton(
                              onPressed: _loadTodos,
                              child: const Text('再試行'),
                            ),
                          ],
                        ),
                      )
                    : ListView.builder(
                        itemCount: _todos.length,
                        itemBuilder: (context, index) {
                          final todo = _todos[index];
                          return TodoItem(
                            todo: todo,
                            onToggle: () => _toggleTodo(todo),
                            onDelete: () => _deleteTodo(todo),
                          );
                        },
                      ),
          ),
        ],
      ),
      
      // 新規Todo追加エリア
      bottomNavigationBar: Container(
        padding: const EdgeInsets.all(16),
        color: Colors.grey[800],
        child: SafeArea(
          child: Row(
            children: [
              Expanded(
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.white, width: 1),
                  ),
                  child: TextField(
                    controller: _newTodoController,
                    style: const TextStyle(color: Colors.white),
                    decoration: const InputDecoration(
                      hintText: 'Input your note...',
                      hintStyle: TextStyle(color: Colors.grey),
                      border: InputBorder.none,
                      contentPadding: EdgeInsets.all(16),
                    ),
                    onSubmitted: (_) => _addTodo(),
                  ),
                ),
              ),
              const SizedBox(width: 16),
              GestureDetector(
                onTap: _addTodo,
                child: Container(
                  padding: const EdgeInsets.all(16),
                  decoration: const BoxDecoration(
                    color: Colors.indigo,
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(
                    Icons.add,
                    color: Colors.white,
                    size: 24,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _searchController.dispose();
    _newTodoController.dispose();
    super.dispose();
  }
}
```

### 🚀 Step 8: アプリケーションエントリーポイント

**main.dart**
```dart
import 'package:flutter/material.dart';
import 'screens/todo_list_screen.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Todo Flutter App',
      theme: ThemeData(
        primarySwatch: Colors.indigo,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: TodoListScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}
```

### ⚡ Step 9: 初期テスト実行

```bash
# iOS シミュレーターでテスト
flutter run

# エラーが発生した場合のデバッグ
flutter doctor        # 環境確認
flutter clean          # クリーンビルド
flutter pub get        # 依存関係再取得
```

### 🔧 Step 10: 重要な設定ファイル確認

**ios/Runner/Info.plist の重要設定**
```xml
<key>CFBundleDisplayName</key>
<string>Todo Flutter App</string>

<!-- ネットワーク通信許可（後でHTTP通信で必要） -->
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

### 📊 Phase 2 完了チェックリスト

- ✅ Flutter プロジェクト作成完了
- ✅ 必要な依存関係インストール
- ✅ プロジェクト構造構築
- ✅ データモデル実装（JSON対応）
- ✅ API サービス実装（CRUD操作）
- ✅ UI コンポーネント実装（Material Design）
- ✅ メイン画面実装（検索・フィルター対応）
- ✅ エラーハンドリング実装
- ✅ iOS シミュレーターでの動作確認

### 🔄 次のステップ

Phase 3では、実際のDjangoサーバーとの統合テストを行い、API接続の動作確認を実施します。

**予想される課題:**
1. CORS設定の調整
2. ネットワーク通信エラーの対処
3. JSON レスポンス形式の調整
4. エラーハンドリングの改善

これらは次のフェーズで詳細に対応していきます。 