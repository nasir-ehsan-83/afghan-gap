from fastapi import FastAPI

from src.common.errors.handlers import init_error_handlers
from server.src.db import database
from server.src.modules.auth import routes as auth_routes
from server.src.modules.users import routes as users_routes
from server.src.modules.posts import routes as posts_routes
from server.src.modules.votes import routes as votes_routes

app = FastAPI()

@app.on_event("startup")
async def init_tables():
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)

# Activate the robust error handling system globally
init_error_handlers(app)

app.include_router(auth_routes.router)
app.include_router(users_routes.router)
app.include_router(posts_routes.router)
app.include_router(votes_routes.router)