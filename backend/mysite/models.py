from django.db import models


class Post(models.Model):
    title = models.CharField('Название статьи', max_length=32)
    text = models.TextField(verbose_name='Текст статьи')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

