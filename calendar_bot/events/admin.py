from django.contrib import admin

from .models import Event, BotStatistics, Appointment

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'user')
    list_filter = ('date', 'user')
    list_search_fields = ('name', 'user__first_name', 'user__last_name')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'user')
    search_fields = ('user__first_name', 'user__last_name', 'event__name')

@admin.register(BotStatistics)
class BotStatisticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'user_count', 'event_count', 'edited_events', 'canceled_events')
    list_filters = ('date',)
    search_fields = ('date',)
