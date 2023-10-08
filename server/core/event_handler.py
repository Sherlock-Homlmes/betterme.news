# libraries
import beanie

# local
from core.conf import app
from core.database.mongodb import client
from core.models import (
    Posts,
    PostTags,
    Tags,
    Users,
)


@app.on_event("startup")
async def startup():
    await beanie.init_beanie(
        database=client.betterme_news,
        document_models=[
            Posts,
            PostTags,
            Tags,
            Users,
        ],
    )

    print("Start up done")
