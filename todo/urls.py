from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.TodoListView.as_view(), name='list'),
    path('add/', views.AddTodoView.as_view(), name='add'),
    path('toggle/<int:todo_id>/', views.toggle_todo, name='toggle'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete'),
] 