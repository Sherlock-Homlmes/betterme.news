from pydantic import BaseModel


class getSelfResponse(BaseModel):
    pass


class getDiscordAuthResponse(BaseModel):
    token: str


class getOauthLinkResponse(BaseModel):
    discord_link: str
