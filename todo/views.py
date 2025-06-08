from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from .models import Todo

# Create your views here.

class TodoListView(ListView):
    model = Todo
    template_name = 'todo/todo_list.html'
    context_object_name = 'todos'
    
    def get_queryset(self):
        search_query = self.request.GET.get('search')
        if search_query:
            return Todo.objects.filter(title__icontains=search_query)
        return Todo.objects.all()

class AddTodoView(CreateView):
    model = Todo
    fields = ['title']
    template_name = 'todo/add_todo.html'
    success_url = reverse_lazy('todo:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Todoが正常に追加されました！')
        return super().form_valid(form)

def toggle_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.completed = not todo.completed
    todo.save()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'completed': todo.completed})
    
    return redirect('todo:list')

def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.delete()
    messages.success(request, 'Todoが削除されました。')
    return redirect('todo:list')
