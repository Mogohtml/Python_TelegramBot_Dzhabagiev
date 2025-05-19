from dataclasses import dataclass
from typing import Optional


from app.core.repositories.users import UserRepository

@dataclass
class UserService:
    repository: UserRepository

    async def create_user(self, user_id: int, last_name: str, first_name: str, email: str,
                                    password: Optional[str] = None, patronymic: Optional[str] = None) -> None:
        patronymic = patronymic or ''
        await self.repository.create_user_if_not_exists(user_id, last_name, first_name, email, password, patronymic)

    async def read_user(self, user_id: int) -> Optional[dict]:
        return await self.repository.read_user(user_id)

    async def edit_user(self, user_id: int, last_name: Optional[str] = None, first_name: Optional[str] = None, patronymic: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None) -> None:
        await self.repository.edit_user(user_id, last_name, first_name, patronymic, email, password)

    async def delete_user(self, user_id: int) -> Optional[dict]:
        return await self.repository.delete_user(user_id)


