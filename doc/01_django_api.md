# Django REST API 実装ガイド

## 🚀 Django REST Framework による API設計・実装

### 📋 API概要

**実装されたREST API仕様**
```
Base URL: http://192.168.179.24:8000/api/
Content-Type: application/json
Authentication: None (開発版)
CORS: 有効
Pagination: ページネーション対応 (PAGE_SIZE: 10)
```

### 🛠️ 技術スタック

**使用ライブラリ**
```python
Django==5.2.2
djangorestframework==3.15.2
django-cors-headers==4.4.0
```

**主要コンポーネント**
- **ViewSets**: APIビューロジック
- **Serializers**: JSON シリアライゼーション
- **Pagination**: ページネーション
- **CORS**: クロスオリジン設定

### 📊 API エンドポイント一覧

#### Todo CRUD API

| Method | Endpoint | 説明 | レスポンス |
|--------|----------|------|------------|
| `GET` | `/api/todos/` | Todo一覧取得 | ページネーション付きリスト |
| `POST` | `/api/todos/` | Todo作成 | 作成されたTodo |
| `GET` | `/api/todos/{id}/` | Todo詳細取得 | 単一Todo |
| `PUT` | `/api/todos/{id}/` | Todo更新 | 更新されたTodo |
| `DELETE` | `/api/todos/{id}/` | Todo削除 | 204 No Content |
| `OPTIONS` | `/api/todos/` | CORS プリフライト | 200 OK |

### 🔧 Step 1: Django REST Framework 設定

**1.1 settings.py の設定**

```python
# todoproject/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',        # Django REST Framework
    'corsheaders',          # CORS対応
    'todo',                 # Todo アプリ
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS (最上部)
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# REST Framework 設定
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

# CORS 設定
CORS_ALLOWED_ALL_ORIGINS = True  # 開発環境用
CORS_ALLOW_CREDENTIALS = True

# 本番環境では以下のように特定ドメインを指定
# CORS_ALLOWED_ORIGINS = [
#     "https://your-frontend-domain.com",
#     "http://192.168.179.24:8000",
# ]

# 外部アクセス許可
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.179.24']
```

### 📝 Step 2: データモデルの確認

**2.1 Todo モデル (todo/models.py)**

```python
from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']  # 新しいもの順
```

**データベース構造**
```sql
CREATE TABLE todo_todo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL
);
```

### 🔄 Step 3: シリアライザーの実装

**3.1 todo/serializers.py の作成**

```python
from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    """
    Todo モデル用シリアライザー
    JSON <-> Django モデル の変換を担当
    """
    
    class Meta:
        model = Todo
        fields = ['id', 'title', 'completed', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_title(self, value):
        """
        タイトルのカスタムバリデーション
        """
        if not value or not value.strip():
            raise serializers.ValidationError("タイトルは必須です")
        
        if len(value.strip()) > 200:
            raise serializers.ValidationError("タイトルは200文字以内で入力してください")
            
        return value.strip()
    
    def create(self, validated_data):
        """
        Todo作成時のカスタムロジック
        """
        return Todo.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Todo更新時のカスタムロジック
        """
        instance.title = validated_data.get('title', instance.title)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.save()
        return instance
```

### 🎯 Step 4: APIビューの実装

**4.1 todo/api_views.py の作成**

```python
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import Todo
from .serializers import TodoSerializer

class TodoViewSet(viewsets.ModelViewSet):
    """
    Todo の CRUD操作を提供するViewSet
    
    利用可能なアクション:
    - list: GET /api/todos/
    - create: POST /api/todos/
    - retrieve: GET /api/todos/{id}/
    - update: PUT /api/todos/{id}/
    - partial_update: PATCH /api/todos/{id}/
    - destroy: DELETE /api/todos/{id}/
    """
    
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    
    def get_queryset(self):
        """
        検索クエリに基づいてQuerySetをフィルタリング
        """
        queryset = Todo.objects.all()
        search = self.request.query_params.get('search', None)
        
        if search is not None:
            queryset = queryset.filter(
                Q(title__icontains=search)
            )
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        Todo一覧取得 (ページネーション付き)
        
        Query Parameters:
        - search: タイトル検索
        - page: ページ番号
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        Todo作成
        
        Request Body:
        {
            "title": "新しいTodo"
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        todo = serializer.save()
        
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """
        Todo更新
        
        Request Body:
        {
            "title": "更新されたタイトル",
            "completed": true
        }
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        todo = serializer.save()
        
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Todo削除
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        """
        カスタムアクション: Todo完了状態の切り替え
        
        POST /api/todos/{id}/toggle/
        """
        todo = self.get_object()
        todo.completed = not todo.completed
        todo.save()
        
        serializer = self.get_serializer(todo)
        return Response(serializer.data)
```

### 🌐 Step 5: URL設定

**5.1 todo/api_urls.py の作成**

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import TodoViewSet

# DRF Router を使用した自動URL生成
router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todos')

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]

# 生成されるURL一覧:
# GET    /api/todos/          -> TodoViewSet.list
# POST   /api/todos/          -> TodoViewSet.create  
# GET    /api/todos/{id}/     -> TodoViewSet.retrieve
# PUT    /api/todos/{id}/     -> TodoViewSet.update
# PATCH  /api/todos/{id}/     -> TodoViewSet.partial_update
# DELETE /api/todos/{id}/     -> TodoViewSet.destroy
# POST   /api/todos/{id}/toggle/ -> TodoViewSet.toggle (カスタム)
```

**5.2 メインプロジェクトのURL設定 (todoproject/urls.py)**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls', namespace='todo')),    # HTML ビュー
    path('api/', include('todo.api_urls', namespace='api')),  # REST API
]
```

### 📊 Step 6: APIレスポンス例

**6.1 Todo一覧取得 (GET /api/todos/)**

```json
{
  "count": 6,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 6,
      "title": "プロジェクトの詳細書を作成する",
      "completed": true,
      "created_at": "2025-06-08T12:29:18.123456Z"
    },
    {
      "id": 5,
      "title": "データベースの設計を完了する", 
      "completed": true,
      "created_at": "2025-06-08T12:29:09.654321Z"
    },
    {
      "id": 4,
      "title": "UIデザインのモックアップを作成する",
      "completed": true,
      "created_at": "2025-06-08T12:28:15.987654Z"
    },
    {
      "id": 3,
      "title": "テスト計画を立案する",
      "completed": false,
      "created_at": "2025-06-08T10:15:30.456789Z"
    },
    {
      "id": 2,
      "title": "こんにちは",
      "completed": true,
      "created_at": "2025-06-08T09:45:22.123456Z"
    },
    {
      "id": 1,
      "title": "たすく",
      "completed": true,
      "created_at": "2025-06-08T09:30:15.789123Z"
    }
  ]
}
```

**6.2 Todo作成 (POST /api/todos/)**

**Request:**
```json
{
  "title": "新しいタスク"
}
```

**Response (201 Created):**
```json
{
  "id": 7,
  "title": "新しいタスク",
  "completed": false,
  "created_at": "2025-06-08T17:30:45.123456Z"
}
```

**6.3 Todo更新 (PUT /api/todos/7/)**

**Request:**
```json
{
  "title": "更新されたタスク",
  "completed": true
}
```

**Response (200 OK):**
```json
{
  "id": 7,
  "title": "更新されたタスク", 
  "completed": true,
  "created_at": "2025-06-08T17:30:45.123456Z"
}
```

**6.4 Todo削除 (DELETE /api/todos/7/)**

**Response (204 No Content):**
```
(空のレスポンス)
```

**6.5 検索機能 (GET /api/todos/?search=テスト)**

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 3,
      "title": "テスト計画を立案する",
      "completed": false,
      "created_at": "2025-06-08T10:15:30.456789Z"
    }
  ]
}
```

### 🔧 Step 7: APIテスト

**7.1 curl を使用した手動テスト**

```bash
# 一覧取得
curl -X GET http://192.168.179.24:8000/api/todos/

# Todo作成
curl -X POST http://192.168.179.24:8000/api/todos/ \
  -H "Content-Type: application/json" \
  -d '{"title":"curl で作成したTodo"}'

# Todo更新  
curl -X PUT http://192.168.179.24:8000/api/todos/1/ \
  -H "Content-Type: application/json" \
  -d '{"title":"更新されたタイトル","completed":true}'

# Todo削除
curl -X DELETE http://192.168.179.24:8000/api/todos/1/

# 検索
curl -X GET "http://192.168.179.24:8000/api/todos/?search=テスト"
```

**7.2 Django テストコードでのAPI検証**

```python
# todo/tests.py (抜粋)

class TodoAPITest(APITestCase):
    def test_api_todo_list(self):
        """API Todo一覧取得のテスト"""
        url = reverse('api:todos-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
    
    def test_api_todo_create(self):
        """API Todo作成のテスト"""
        url = reverse('api:todos-list')
        data = {'title': 'API新規Todo'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'API新規Todo')
```

### 📈 Step 8: パフォーマンス最適化

**8.1 データベースクエリ最適化**

```python
class TodoViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        # select_related / prefetch_related の使用
        queryset = Todo.objects.select_related().all()
        
        # インデックスを活用した検索
        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(title__icontains=search)
        
        return queryset
```

**8.2 キャッシュの活用**

```python
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60 * 5), name='list')  # 5分キャッシュ
class TodoViewSet(viewsets.ModelViewSet):
    # ...
```

**8.3 ページネーション設定の調整**

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # パフォーマンスとUXのバランス
}
```

### 🔒 Step 9: セキュリティ考慮事項

**9.1 認証・認可 (将来の実装)**

```python
# settings.py (本番環境用)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

**9.2 入力値検証の強化**

```python
class TodoSerializer(serializers.ModelSerializer):
    def validate_title(self, value):
        # HTMLタグの除去
        import bleach
        value = bleach.clean(value, tags=[], strip=True)
        
        # 最大長チェック
        if len(value) > 200:
            raise serializers.ValidationError("タイトルは200文字以内です")
            
        return value
```

**9.3 レート制限 (将来の実装)**

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

### 📊 API実装完了チェックリスト

**基本実装**
- ✅ Django REST Framework セットアップ
- ✅ Todo シリアライザー実装
- ✅ Todo ViewSet 実装 (CRUD)
- ✅ URL ルーティング設定
- ✅ ページネーション対応

**機能実装**
- ✅ 一覧取得・作成・更新・削除
- ✅ 検索機能 (title 部分一致)
- ✅ 日付ソート (新しいもの順)
- ✅ バリデーション (タイトル必須・文字数制限)
- ✅ エラーハンドリング

**設定・運用**
- ✅ CORS 設定 (Flutter アプリ対応)
- ✅ 外部アクセス許可設定
- ✅ JSON レスポンス形式
- ✅ 包括的テストスイート (7 API tests)
- ✅ 手動テスト用 curl コマンド

**ドキュメント**
- ✅ API仕様書
- ✅ エンドポイント一覧
- ✅ リクエスト・レスポンス例
- ✅ 実装詳細の記録

### 🚀 今後の改善案

**機能拡張**
- [ ] 認証・認可システム
- [ ] カテゴリ・タグ機能
- [ ] 期限設定・通知
- [ ] ファイル添付機能

**パフォーマンス**
- [ ] Redis キャッシュ
- [ ] データベースインデックス最適化
- [ ] API レスポンス圧縮
- [ ] CDN 配信

**運用・監視**
- [ ] API ログ監視
- [ ] パフォーマンス測定
- [ ] エラー率監視
- [ ] 利用統計取得

このDjango REST API実装により、FlutterアプリやWebフロントエンドから安全で高速なデータアクセスが可能になりました。 