from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView

from calendar_bot.api.serialize import EventSerializer, BotStatisticsSerializer, AppointmentSerializer, UserSerializer
from calendar_bot.events.models import Event, BotStatistics, Appointment
from calendar_bot.users.models import User


# Create your views here.
class EventListCreateView(ListCreateAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

class EventRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

class BotStatisticsListView(ListAPIView):
    serializer_class = BotStatisticsSerializer
    queryset = BotStatistics.objects.all()

class AppointmentListCreateView(ListCreateAPIView):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

class AppointmentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

class UserListView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

