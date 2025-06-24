from io import StringIO

from django.http import HttpRequest
from django.http import HttpResponse, JsonResponse

from django.views import View
from django.contrib.auth import get_user_model

from .models import Appointment, Event

import json
import csv


User = get_user_model()

class ExportEventsView(View):
    def get(self, request, user_id, format):
        user = User.objects.get(id=user_id)
        events = Event.objects.filter(user=user)

        if format == 'json':
            return self.export_to_json(events)
        elif format == 'csv':
            return self.export_to_csv(events)
        else:
            return HttpResponse("Unsupported format", status=400)

    def export_to_json(self, events):
        events_data = [
            {
                "id": events.id,
                "name": events.name,
                "date": events.date,
                "time": events.time,
                "details": events.details,
            }
            for events in events
        ]
        return JsonResponse(events_data, safe=False)

    def export_to_csv(self, events):
        # Создание буфера
        output = StringIO()
        writer = csv.writer(output)

        writer.writerow(["ID", "Name", "Date", "Time", "Details"])

        for event in events:
            writer.writerow([event.id, event.name, event.date, event.time, event.details])

        # Создаем HttpResponse с типом содержимого text/csv
        response = HttpResponse(output.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="events.csv"'
        return response
