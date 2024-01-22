from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {
    'blank': True,
    'null': True,
}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    is_active = models.BooleanField(default=True, verbose_name='Активность')
    code = models.CharField(max_length=12, verbose_name='Код', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        permissions = [
            ('set_is_active', 'Может блокировать пользователя')
        ]
