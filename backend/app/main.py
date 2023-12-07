from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.database import Base 

from config.database import engine

from routers import events


app = FastAPI(
    title = "College Portfolio API",
    docs_url = "/documentation",
    redoc_url = None
)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(events.router)