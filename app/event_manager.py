from app.infra.postgres.db import Database


class Calendar:
    def __init__(self, database: Database):
        self.database = database

    async def create_event(self, event_name, event_date, event_time, event_details):
        insert_query = """
            INSERT INTO events (name, date, time, details)
            VALUES ($1, $2, $3, $4)
            RETURNING id;
        """
        async with self.database.connection as conn:
            event_id = await conn.fetchval(insert_query, event_name, event_date, event_time, event_details)
            return event_id

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

    async def display_event_sorted(self):
        return await self.display_event(reverse=True)
