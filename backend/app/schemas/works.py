from pydantic import BaseModel
from typing import Optional
from datetime import date

class BaseWork(BaseModel):
    date: date
    title: str
    description: str
    type: str
    image: str
    author_photo: str

class Work(BaseWork):
    id: int

class WorkPreview(BaseModel):
    id: int
    image: str