from django.db import models

from mailing.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок', default='Заголовок отсутствует')
    content = models.TextField(verbose_name='Текст', default='Текст отсутствует')
    preview = models.ImageField(upload_to='blog/preview/', verbose_name='Изображение', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    public_date = models.DateField(auto_now=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title
