from core.conf import app

# from core.event_handler import *
# from core.routes import api_router

# # include all api routers
# app.include_router(api_router)


@app.get("/api/")
def main_router():
    return {"status": "alive"}
