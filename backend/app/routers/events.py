from fastapi import (
    APIRouter, 
    HTTPException, 
    status, 
    Depends)

from ..config.database import get_database

from ..models import Events as EventsModel

from ..schemas import BaseEvent, Event, EventPreview

from sqlalchemy.orm import Session
from sqlalchemy import select, insert

from typing import List

router = APIRouter(
    prefix="/api/events",
    tags=["Events"]
)

@router.get("/", response_description="List of all events", response_model=List[EventPreview], status_code=status.HTTP_200_OK)
def get_all_events(database: Session=Depends(get_database)):

    stmt = select(EventsModel.id, EventsModel.image)
    # print(stmt)
    events = database.execute(stmt).fetchall()

    if events == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nothing found"
        )

    return events


@router.get("/id/{id}", response_description="Get event by id", response_model=Event, status_code=status.HTTP_200_OK)
def get_event_by_id(id: int, database: Session=Depends(get_database)):

    stmt = select(EventsModel).where(EventsModel.id == id).limit(1)
    event = database.execute(stmt).scalar()

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nothing found"
        )

    return event


@router.post("/", response_description="Create new event", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event(event: BaseEvent, database: Session=Depends(get_database)):

    try:
        new_event = database.execute(
            insert(EventsModel).returning(EventsModel), 
            [{**event.model_dump()}]
        ).scalar()

    except:
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Can't make new event"
        )
    
    else:
        database.commit()
        return new_event

@router.get("/type/{type}", response_description="Get events by type", response_model=List[EventPreview], status_code=status.HTTP_200_OK)
def get_events_by_type(type: str, database: Session=Depends(get_database)):

    stmt = select(EventsModel).where(EventsModel.type == type)
    events = database.execte(stmt).fetchall()

    if events == []:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Looks like you've lost! Are you sure about that type {type}?"
        )
    return events