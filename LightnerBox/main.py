from fastapi import FastAPI
from contextlib import asynccontextmanager
from LightnerBox.auth import routes as auth_routes
from LightnerBox.auth import routes as protected_routes
from . import models, database
from LightnerBox.auth import routes as card_crud
# from typing import AsyncGenerator


models.Base.metadata.create_all(bind=database.engine)


# Lifecycle event
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App starting up")
    yield
    print("App shutting down")


# FastAPI application
app = FastAPI(lifespan=lifespan)

# insert routes
app.include_router(auth_routes.router)
app.include_router(protected_routes.router)

app.include_router(card_crud.router)
