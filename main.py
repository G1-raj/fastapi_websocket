from fastapi import FastAPI, WebSocket
from db.database import engine, Base
from routers import auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
