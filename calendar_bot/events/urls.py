from django.urls import include, path

from calendar_bot.events.views import ExportEventsView

urlpatterns = [
    path('export-events/<int:user_id>/<str:format>/', ExportEventsView.as_view(), name='export-events'),
]