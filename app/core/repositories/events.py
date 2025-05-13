from dataclasses import dataclass

from typing import Optional
from app.infra.postgres.db import Database



@dataclass
class EventRepository:
    database: Database

    async def create_event_if_not_exists(self, user_id: int, name: str, date: str, time: str, details: Optional[str] = None) -> None:
        details = details or ''
        create_event_query = f"""
        INSERT INTO events (name, date, time, details, user_id)
        VALUES ($1, $2, $3, $4, $5) 
        """

        async with self.database.connection() as conn:
            await conn.execute(create_event_query, name, date, time, details or '', user_id)


    async def read_event(self, event_id: int, user_id: int) -> Optional[dict]:
        sql_query = "SELECT * FROM events WHERE id = $1 AND user_id = $2"
        async with self.database.connection() as conn:
            event = await conn.fetchrow(sql_query, event_id, user_id)
            if event:
                return {
                    "id": event["id"],
                    "name": event["name"],
                    "date": event["date"],
                    "time": event["time"],
                    "details": event["details"],
                    "user_id": event["user_id"],
                }
            raise ValueError("Такого события нет! Пожалуйста, введите корректный номер события.")

    async def edit_event(self, event_id: int, user_id: int, name: Optional[str]=None, date: Optional[str]=None, time: Optional[str]=None, details:Optional[str]=None) -> None:
        update_query = """
            UPDATE events 
            SET name = COALESCE($3, name), 
                date = COALESCE($4, date), 
                time = COALESCE($5, time), 
                details = COALESCE($6, details)
            WHERE id = $1 AND user_id = $2;
        """
        async with self.database.connection() as conn:
            await conn.execute(update_query, event_id, user_id, name, date, time, details)


    async def delete_event(self, event_id: int, user_id: int) -> Optional[dict]:
        delete_query = "DELETE FROM events WHERE id = $1 AND user_id = $2 RETURNING *;"
        async with self.database.connection() as conn:
            deleted_event = await conn.fetchrow(delete_query, event_id, user_id)
            if deleted_event:
                return {
                "id": deleted_event["id"],
                "name": deleted_event["name"],
                "date": deleted_event["date"],
                "time": deleted_event["time"],
                "details": deleted_event["details"]
                }
            raise ValueError("Такого события нет! Пожалуйста введите корректный номер события")

    async def display_event(self, user_id: int, reverse: bool=False) -> Optional[list]:
        order_by = "ASC" if not reverse else "DESC"
        display_query = f"SELECT * FROM events WHERE user_id = $1 ORDER BY date {order_by}"
        async with self.database.connection() as conn:
            events = await conn.fetch(display_query, user_id)
        return [
        {
            "id": event["id"],
            "name": event["name"],
            "date": event["date"],
            "time": event["time"],
            "details": event["details"]
        } for event in events
        ]




