from .models import User
from ..events.models import Event


# Реализуйте метод для получения событий пользователя
# из базы данных на основе его идентификатора Telegram.

def get_events_by_user_id(user_id):
    events = Event.objects.filter(user_id=user_id)
    return events


