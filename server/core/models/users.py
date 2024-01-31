# default
from enum import Enum
import datetime
from typing import List

# libraries
from beanie import Document
from pydantic import EmailStr


class UserRoleEnum(Enum):
    ADMIN = "admin"
    USER = "user"


class Users(Document):
    email: EmailStr
    discord_id: int
    name: str
    avatar_url: str
    roles: List[UserRoleEnum]
    last_logged_in_at: datetime.datetime

    class Settings:
        validate_on_save = True

    def get_info(self):
        # TODO: use pydantic

        return {
            "id": str(self.id),
            "discord_id": self.discord_id,
            "name": self.name,
            "email": self.email,
            "avatar_url": self.avatar_url,
            "roles": [role.value for role in self.roles],
        }
