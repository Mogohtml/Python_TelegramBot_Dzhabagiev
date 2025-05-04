from dataclasses import dataclass

from app.core.users.repositories import UserRepository

@dataclass
class UserService:
    repository: UserRepository

    async def register_visitor(self, user_id: int) -> None:
        await self.repository.create_user_if_not_exists(user_id)

