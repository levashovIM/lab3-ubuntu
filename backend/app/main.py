from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Нужен для разворачивания БД, 
# т.к. в нем хранится информация 
# о структуре всех таблиц
from .config.database import Base 

# Движок для подключения к БД
from .config.database import engine

# Подключаем роутеры
from .routers import works


app = FastAPI(
    title = "College Portfolio API",
    docs_url = "/documentation",
    redoc_url = None
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

origins = [
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаем в базе данных таблицы по моделям.
# Если таблицы уже есть, то ничего не произойдет.
Base.metadata.create_all(bind=engine)

# Добавляем подключенный роутер в объект app
app.include_router(works.router)