# libraries
from fastapi import APIRouter

# local
from core.models import Users

router = APIRouter(
    tags=["users"],
)


@router.post("/users", status_code=204)
async def create_user():
    user = Users(
        email="khoitm@gmail.com",
        discord_id=23434,
        name="khoi",
        avatar="http://aadf.com",
    )
    await user.insert()
