from dataclasses import dataclass

from typing import Optional
from app.infra.postgres.db import Database


@dataclass
class EventRepository:
    database: Database

    async def create_event_if_not_exists(self, id: int, name: str, date: str, time: str, details: Optional[str] = None) -> None:
        create_event_query = """
        INSERT INTO events (id, name, date, time, details)
        VALUES ($1, $2, $3, $4, $5) 
        ON CONFLICT (id) DO NOTHING"""

        async with self.database.connection() as conn:
            await conn.execute(create_event_query, id, name, date, time, details)


    async def read_event(self, event_id):
        sql_query = "SELECT * FROM events WHERE id = $1"
        async with self.database.connection as conn:
            event = await conn.fetchrow(sql_query, event_id)
            if event:
                return {
                    "id": event["id"],
                    "name": event["name"],
                    "date": event["date"],
                    "time": event["time"],
                    "details": event["details"]
                }
            raise ValueError("Такого события нет! Пожалуйста, введите корректный номер события.")

    async def edit_event(self, event_id, name=None, date=None, time=None, details=None):
        update_query = """
            UPDATE events 
            SET name = COALESCE($1, name), 
                date = COALESCE($2, date), 
                time = COALESCE($3, time), 
                details = COALESCE($4, details)
            WHERE id = $5;
        """
        async with self.database.connection as conn:
            await conn.execute(update_query, name, date, time, details, event_id)


    async def delete_event(self, event_id):
        delete_query = "DELETE FROM events WHERE id = $1 RETURNING *;"
        async with self.database.connection as conn:
            deleted_event = await conn.fetchrow(delete_query, event_id)
            if deleted_event:
                return {
                "id": deleted_event["id"],
                "name": deleted_event["name"],
                "date": deleted_event["date"],
                "time": deleted_event["time"],
                "details": deleted_event["details"]
                }
            raise ValueError("Такого события нет! Пожалуйста введите корректный номер события")

    async def display_event(self, reverse=False):
        order_by = "ASC" if not reverse else "DESC"
        display_query = f"SELECT * FROM events ORDER BY date {order_by}"
        async with self.database.connection as conn:
            events = await conn.fetch(display_query)
        return [
        {
            "id": event["id"],
            "name": event["name"],
            "date": event["date"],
            "time": event["time"],
            "details": event["details"]
        } for event in events
        ]




