from django.urls import path
from calendar_bot.api.views import BotStatisticsListView, EventListCreateView, EventRetrieveUpdateDestroyView, \
    AppointmentRetrieveUpdateDestroyAPIView, AppointmentListCreateView

urlpatterns = [
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventRetrieveUpdateDestroyView.as_view(), name='event-retrieve-update-destroy'),
    path('statistics/', BotStatisticsListView.as_view(), name='bot-statistics-list'),
    path('appointments/', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('appointments/<int:pk>/', AppointmentRetrieveUpdateDestroyAPIView.as_view(),
         name='appointment-retrieve-update-destroy'),

]