from beanie import Document
from pydantic import EmailStr


class Users(Document):
    email: EmailStr
    discord_id: int
    name: str
    avatar: str

    class Settings:
        validate_on_save = True
