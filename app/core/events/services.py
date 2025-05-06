from dataclasses import dataclass

from typing import Optional
from app.core.events.repositories import EventRepository

@dataclass
class EventService:
    repository: EventRepository

    async def create_event(self, id: int, name: str, date: str, time: str, details: Optional[str] = None) -> None:
        await self.repository.create_event_if_not_exists(id, name, date, time, details)

    async def read_event(self, event_id: int) -> Optional[dict]:
        return await self.repository.read_event(event_id)

    async def edit_event(self, event_id: int, name: Optional[str]=None, date: Optional[str]=None, time: Optional[str]=None, details: Optional[str]=None) -> None:
        await self.repository.edit_event(event_id, name, date, time, details)

    async def delete_event(self, event_id) -> Optional[dict]:
        return await self.repository.delete_event(event_id)

    async def display_event(self, reverse=False) -> Optional[dict]:
        return await self.repository.display_event(reverse)



