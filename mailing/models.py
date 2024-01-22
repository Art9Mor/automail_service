from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {'blank': True, 'null': True}

STATUS_CHOICES = [
    ('Создана', 'Создана'),
    ('Запущена', 'Запущена'),
    ('Завершена', 'Завершена'),
]
INTERVAL_CHOICES = [
    ('Разово', 'Разово'),
    ('Ежедневно', 'Ежедневно'),
    ('Раз в неделю', 'Раз в неделю'),
    ('Раз в месяц', 'Раз в месяц'),
]


class Client(models.Model):
    name = models.CharField(max_length=200, verbose_name='ФИО', default='Инкогнито')
    email = models.EmailField(verbose_name='Почта', **NULLABLE)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Владелец клиента')

    def __str__(self):
        return f'{self.name}({self.owner})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    title = models.CharField(max_length=250, verbose_name='Тема письма', default='Привет!')
    content = models.TextField(verbose_name='Содержание',
                               default='Ты не знаешь, кто я, но я знаю тебя. Давай сыграем в игру...')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Автор')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование рассылки', default='Без названия')
    mail_to = models.ManyToManyField(Client, verbose_name='Кому')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', null=True)
    star_date = models.DateTimeField(default=timezone.now, verbose_name='Вреия начала рассылки')
    second_date = models.DateTimeField(default=timezone.now, verbose_name='Врея следующей рассылки')
    end_date = models.DateTimeField(default=timezone.now, verbose_name='Время окончания рассылки')
    interval = models.CharField(choices=INTERVAL_CHOICES, max_length=60, default='разовая',
                                verbose_name='Периодичность')
    status = models.CharField(choices=STATUS_CHOICES, max_length=60, help_text='Создана или Завершена',
                              verbose_name='Статус рассылки', default='В процессе')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='CСоздатель рассылки', null=True)
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    def __str__(self):
        return f'{self.name}(Кому: {self.mail_to}, Дата создания: {self.star_date}, Статус: {self.status})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('star_date',)

    permissions = [
        ('set_is_active', 'Может отключать рассылку')
    ]


class Logs(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка', null=True)
    last_mailing = models.DateTimeField(auto_now=True, verbose_name='Дата последней рассылки')
    status = models.CharField(**NULLABLE, max_length=60, verbose_name='Статус отправки')

    def __str__(self):
        return f'Отправлено: {self.last_mailing}/n Статус: {self.status}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
