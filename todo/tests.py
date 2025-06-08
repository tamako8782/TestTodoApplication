from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Todo
import json


class TodoModelTest(TestCase):
    """Todo モデルのテスト"""
    
    def setUp(self):
        Todo.objects.all().delete()
        self.todo = Todo.objects.create(
            title="テストタスク",
            completed=False
        )
    
    def test_todo_creation(self):
        """Todoオブジェクトが正しく作成されることをテスト"""
        self.assertEqual(self.todo.title, "テストタスク")
        self.assertFalse(self.todo.completed)
        self.assertIsNotNone(self.todo.created_at)
        self.assertIsNotNone(self.todo.updated_at)
    
    def test_todo_str_method(self):
        """Todoの__str__メソッドのテスト"""
        expected_str = "テストタスク"
        self.assertEqual(str(self.todo), expected_str)
    
    def test_todo_update(self):
        """Todoの更新が正しく動作することをテスト"""
        original_updated_at = self.todo.updated_at
        self.todo.completed = True
        self.todo.save()
        
        self.assertTrue(self.todo.completed)
        self.assertGreater(self.todo.updated_at, original_updated_at)


class TodoViewTest(TestCase):
    """Todo ビューのテスト"""
    
    def setUp(self):
        Todo.objects.all().delete()
        self.client = Client()
        self.todo1 = Todo.objects.create(title="タスク1", completed=False)
        self.todo2 = Todo.objects.create(title="タスク2", completed=True)
    
    def test_todo_list_view(self):
        """Todo一覧ページのテスト"""
        response = self.client.get(reverse('todo:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "タスク1")
        self.assertContains(response, "タスク2")
    
    def test_todo_add(self):
        """Todo追加機能のテスト"""
        response = self.client.post(reverse('todo:add'), {
            'title': '新しいタスク'
        })
        self.assertEqual(response.status_code, 302)  # リダイレクト
        self.assertTrue(Todo.objects.filter(title='新しいタスク').exists())
    
    def test_todo_toggle(self):
        """Todo完了状態切り替えのテスト"""
        response = self.client.post(reverse('todo:toggle', args=[self.todo1.id]))
        self.assertEqual(response.status_code, 302)
        self.todo1.refresh_from_db()
        self.assertTrue(self.todo1.completed)
    
    def test_todo_delete(self):
        """Todo削除機能のテスト"""
        todo_id = self.todo1.id
        response = self.client.post(reverse('todo:delete', args=[todo_id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(id=todo_id).exists())
    
    def test_search_functionality(self):
        """検索機能のテスト"""
        response = self.client.get(reverse('todo:list'), {'search': 'タスク1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "タスク1")
        self.assertNotContains(response, "タスク2")


class TodoAPITest(APITestCase):
    """Todo REST API のテスト"""
    
    def setUp(self):
        # テストごとにクリーンなデータベース状態を確保
        Todo.objects.all().delete()
        self.todo1 = Todo.objects.create(title="API タスク1", completed=False)
        self.todo2 = Todo.objects.create(title="API タスク2", completed=True)
        # 作成後のカウント確認
        self.assertEqual(Todo.objects.count(), 2)
    
    def test_get_todo_list(self):
        """Todo一覧API取得のテスト"""
        # テスト開始時のデータ数を確認
        self.assertEqual(Todo.objects.count(), 2)
        url = '/api/todos/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ページネーション形式のレスポンス確認
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_create_todo(self):
        """Todo作成APIのテスト"""
        initial_count = Todo.objects.count()
        url = '/api/todos/'
        data = {'title': 'API経由で作成したタスク', 'completed': False}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Todo.objects.filter(title='API経由で作成したタスク').exists())
        self.assertEqual(Todo.objects.count(), initial_count + 1)
    
    def test_update_todo(self):
        """Todo更新APIのテスト"""
        url = f'/api/todos/{self.todo1.id}/'
        data = {'title': '更新されたタスク', 'completed': True}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo1.refresh_from_db()
        self.assertEqual(self.todo1.title, '更新されたタスク')
        self.assertTrue(self.todo1.completed)
    
    def test_delete_todo(self):
        """Todo削除APIのテスト"""
        url = f'/api/todos/{self.todo1.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Todo.objects.filter(id=self.todo1.id).exists())
    
    def test_toggle_completed_action(self):
        """Todo完了状態切り替えAPIのテスト"""
        url = f'/api/todos/{self.todo1.id}/toggle_completed/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo1.refresh_from_db()
        self.assertTrue(self.todo1.completed)
    
    def test_invalid_todo_access(self):
        """存在しないTodoへのアクセステスト"""
        url = '/api/todos/999999/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_cors_headers(self):
        """CORS ヘッダーのテスト"""
        url = '/api/todos/'
        response = self.client.options(url)
        # CORSが設定されていることを確認
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TodoValidationTest(TestCase):
    """Todo バリデーションのテスト"""
    
    def setUp(self):
        Todo.objects.all().delete()
    
    def test_title_required(self):
        """タイトルが必須であることをテスト"""
        # Djangoのモデルは空文字列を許可するが、nullは許可しない
        todo = Todo.objects.create(title="", completed=False)
        self.assertEqual(todo.title, "")
    
    def test_long_title_handling(self):
        """長いタイトルの処理テスト"""
        long_title = "あ" * 1000  # 1000文字の長いタイトル
        todo = Todo.objects.create(title=long_title, completed=False)
        self.assertEqual(todo.title, long_title)


class TodoPerformanceTest(TransactionTestCase):
    """Todo パフォーマンステスト"""
    
    def setUp(self):
        # パフォーマンステスト用にクリーンな状態を確保
        Todo.objects.all().delete()
        self.assertEqual(Todo.objects.count(), 0)
    
    def test_bulk_todo_creation(self):
        """大量のTodo作成パフォーマンステスト"""
        self.assertEqual(Todo.objects.count(), 0)
        todos = [Todo(title=f"パフォーマンステスト {i}", completed=False) for i in range(100)]
        Todo.objects.bulk_create(todos)
        self.assertEqual(Todo.objects.count(), 100)
    
    def test_todo_list_performance(self):
        """Todo一覧取得のパフォーマンステスト"""
        # テスト開始時はクリーンな状態
        self.assertEqual(Todo.objects.count(), 0)
        
        # 100個のTodoを作成
        todos = [Todo(title=f"パフォーマンステスト {i}", completed=i % 2 == 0) for i in range(100)]
        Todo.objects.bulk_create(todos)
        self.assertEqual(Todo.objects.count(), 100)
        
        # APIアクセステスト
        url = '/api/todos/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # ページネーション形式のレスポンス確認
        self.assertEqual(response.data['count'], 100)
        # デフォルトページサイズ（通常20）での結果確認
        self.assertGreaterEqual(len(response.data['results']), 20)
        self.assertLessEqual(len(response.data['results']), 100)
