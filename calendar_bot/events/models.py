from django.db import models
from django.conf import settings

from users.models import User


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    details = models.TextField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    is_public = models.BooleanField(default=False)

class BotStatistics(models.Model):
    date = models.DateField(auto_now_add=True)
    user_count = models.PositiveIntegerField(default=0)
    event_count = models.PositiveIntegerField(default=0)
    edited_events = models.PositiveIntegerField(default=0)
    canceled_events = models.PositiveIntegerField(default=0)

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    details = models.TextField(blank=True)
    status = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.user.first_name} - {self.event.name} - {self.date} - {self.time}"