from django.db import models
from django.contrib.auth.models import AbstractUser


# Модель пользователя
class User(AbstractUser):
    is_verify = models.BooleanField(default=0)
    code = models.UUIDField(null=True)
