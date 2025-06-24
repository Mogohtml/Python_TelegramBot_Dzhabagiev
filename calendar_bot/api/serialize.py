from rest_framework import serializers

from calendar_bot.events.models import Event, BotStatistics, Appointment
from calendar_bot.events.views import User


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'date', 'time', 'details', 'user', 'is_public']


class BotStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotStatistics
        fields = ['date', 'user_count', 'event_count', 'edited_events', 'canceled_events']

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['user', 'evemt', 'date', 'time', 'details', 'status']

# User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'patronymic', 'email', 'password']

