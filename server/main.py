from core.settings import app, settings

# from core.routes import api_router

# include all api routers
# app.include_router(api_router, prefix=)


@app.get("/api/")
def main_router():
    return {"status": "alive"}