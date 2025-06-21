from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ForeignKey

from calendar_bot.events.models import Event


# Создайте модель пользователя в Django для хранения информации
# о пользователе: его идентификатор Telegram, имя и события в календаре.
class User(AbstractUser):
    patronymic = models.CharField(max_length=255, blank=True, null=True)
    event = ForeignKey(Event, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']



