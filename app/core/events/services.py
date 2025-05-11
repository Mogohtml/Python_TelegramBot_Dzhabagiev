from dataclasses import dataclass

from typing import Optional
from app.core.events.repositories import EventRepository

@dataclass
class EventService:
    repository: EventRepository

    async def create_event(self, user_id: int, name: str, date: str, time: str, details: Optional[str] = None):
        await self.repository.create_event_if_not_exists(id, user_id, name, date, time, details)

    async def read_event(self, id: int, user_id: int):
        return await self.repository.read_event(id, user_id)

    async def edit_event(self, user_id: int, id: int, name: Optional[str]=None, date: Optional[str]=None, time: Optional[str]=None, details: Optional[str]=None):
        await self.repository.edit_event(user_id, id, name, date, time, details)

    async def delete_event(self, id: int, user_id: int):
        return await self.repository.delete_event(id, user_id)

    async def display_event(self, user_id: int):
        return await self.repository.display_event(user_id)

    async def display_event_sorted(self, user_id: int, reverse=False):
        return await self.repository.display_event(user_id, reverse)



