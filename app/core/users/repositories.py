from dataclasses import dataclass

from app.infra.postgres.db import Database


@dataclass
class UserRepository:
    database: Database

    async def create_user_if_not_exists(self, user_id: int, is_waiter: bool = False) -> None:
        async with self.database.connection as conn:
            await conn.execute("INSERT INTO users VALUES ($1, $2) ON CONFLICT DO NOTHING", user_id, is_waiter)
