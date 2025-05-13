from dataclasses import dataclass

from typing import Optional
from app.core.repositories.events import EventRepository

@dataclass
class EventService:
    repository: EventRepository

    async def create_event(self, user_id: int, name: str, date: str, time: str, details: Optional[str] = None):
        await self.repository.create_event_if_not_exists(user_id, name, date, time, details)

    async def read_event(self, event_id: int, user_id: int):
        return await self.repository.read_event(event_id, user_id)

    async def edit_event(self, event_id: int, user_id: int, name: Optional[str]=None, date: Optional[str]=None, time: Optional[str]=None, details: Optional[str]=None):
        await self.repository.edit_event(event_id, user_id, name, date, time, details)

    async def delete_event(self, event_id: int, user_id: int):
        return await self.repository.delete_event(event_id, user_id)

    async def display_event_sorted(self, user_id: int, reverse: bool = False):
        return await self.repository.display_event(user_id, reverse)



