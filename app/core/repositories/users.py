from dataclasses import dataclass

from typing import Optional

from app.infra.postgres.db import Database

@dataclass
class UserRepository:
    database: Database

    async def create_user_if_not_exists(self, user_id: int, last_name: str, first_name: str, email: str,
                                        password: Optional[str] = None, patronymic: Optional[str] = None) -> None:
        patronymic = patronymic or ''
        create_user_query = """
                            INSERT INTO users (id, last_name, first_name, patronymic, email, password)
                            VALUES ($1, $2, $3, $4, $5, $6)
                            """
        print(
            f"Inserting user with id: {user_id}, last_name: {last_name}, first_name: {first_name}, patronymic: {patronymic}, email: {email}, password: {password}")

        async with self.database.connection() as conn:
            await conn.execute(create_user_query, user_id, last_name, first_name, patronymic, email, password)


    async def read_user(self, user_id: int) -> Optional[dict]:
        get_user_query = """
        SELECT * FROM users WHERE user_id = $1;"""

        async with self.database.connection() as conn:
            user = await conn.fetchrow(get_user_query, user_id)
            if user:
                return {
                    "user_id": user["user_id"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "patronymic": user["patronymic"],
                    "email": user["email"],
                    "password": user["password"]
                }
            return None


    async def edit_user(self, user_id: int, last_name: Optional[str] = None, first_name: Optional[str] = None, patronymic: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None) -> None:
        update_user_query = """
        UPDATE users
        SET last_name = COALESCE($2, last_name),
            first_name = COALESCE($3, first_name),
            patronymic = COALESCE($4, patronymic),
            email = COALESCE($5, email),
            password = COALESCE($6, password),
        WHERE user_id = $1;
        """
        async with self.database.connection() as conn:
            await conn.execute(update_user_query, user_id, last_name, first_name, patronymic, email, password)


    async def delete_user(self, user_id: int) -> Optional[dict]:
        delete_user_query = """
        DELETE FROM users WHERE user_id = $1 RETURNING *;"""
        async with self.database.connection() as conn:
            deleted_user = await conn.fetchrow(delete_user_query, user_id)
            if deleted_user:
                return {
                    "user_id": deleted_user['user_id'],
                    "last_name": deleted_user['last_name'],
                    "first_name": deleted_user['first_name'],
                    "patronymic":  deleted_user['patronymic'],
                    "email":  deleted_user['email'],
                    "password": deleted_user['password']
            }
            return None