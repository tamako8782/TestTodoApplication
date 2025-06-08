from django.db import models
from django.utils import timezone

class Todo(models.Model):
    title = models.CharField(max_length=200, verbose_name="タイトル")
    completed = models.BooleanField(default=False, verbose_name="完了")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Todo"
        verbose_name_plural = "Todos"

    def __str__(self):
        return self.title
