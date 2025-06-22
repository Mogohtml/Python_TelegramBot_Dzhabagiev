from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from events.models import Event, Appointment


class EventInLine(admin.TabularInline):
    model = Event
    extra = 1

class AppointmentInLine(admin.TabularInline):
    model = Appointment
    extra = 1

class CustomUserAdmin(UserAdmin):
    inlines = (EventInLine, AppointmentInLine)
    list_display = ('id', 'first_name', 'last_name', 'email')
    list_filter = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'email')

if not admin.site.is_registered(User):
    admin.site.register(User, CustomUserAdmin)
else:
    admin.site.unregister(User)
    admin.site.register(User, CustomUserAdmin)