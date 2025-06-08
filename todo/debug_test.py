from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Todo
import json


class DebugAPITest(APITestCase):
    """デバッグ用テスト"""
    
    def setUp(self):
        print(f"setUp開始時のTodo数: {Todo.objects.count()}")
        Todo.objects.all().delete()
        print(f"削除後のTodo数: {Todo.objects.count()}")
        
        self.todo1 = Todo.objects.create(title="API タスク1", completed=False)
        self.todo2 = Todo.objects.create(title="API タスク2", completed=True)
        print(f"作成後のTodo数: {Todo.objects.count()}")
        
        # 実際のデータを表示
        for todo in Todo.objects.all():
            print(f"Todo ID: {todo.id}, Title: {todo.title}")
    
    def test_debug_get_todo_list(self):
        """デバッグ用Todo一覧API取得のテスト"""
        print(f"テスト開始時のTodo数: {Todo.objects.count()}")
        
        url = '/api/todos/'
        response = self.client.get(url)
        print(f"API レスポンス状態: {response.status_code}")
        print(f"API レスポンスデータ数: {len(response.data)}")
        print(f"API レスポンス内容: {json.dumps(response.data, indent=2, ensure_ascii=False)}")
        
        self.assertEqual(response.status_code, 200)
        print(f"期待値: 2, 実際の値: {len(response.data)}") 