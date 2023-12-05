from fastapi import (
    APIRouter, 
    HTTPException, 
    status, 
    Depends)

from ..config.db import get_database

from ..models import Works as WorksModel

from ..schemas import BaseWork, Work, WorkPreview

from sqlalchemy.orm import Session
from sqlalchemy import select, insert

from typing import List

router = APIRouter(
    prefix="/api/works",
    tags=["Works"]
)

@router.get("/", response_description="List of all works", response_model=List[WorkPreview], status_code=status.HTTP_200_OK)
def get_all_works(db: Session=Depends(get_database)):

    stmt = select(WorksModel.id, WorksModel.image)
    # print(stmt)
    works = database.execute(stmt).fetchall()

    if works == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nothing found"
        )

    return works


@router.get("/id/{id}", response_description="Get work by id", response_model=Work, status_code=status.HTTP_200_OK)
def get_work_by_id(id: int, db: Session=Depends(get_database)):

    stmt = select(WorksModel).where(WorksModel.id == id).limit(1)
    work = database.execute(stmt).scalar()

    if work is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nothing found"
        )

    return work


@router.post("/", response_description="Create new work", response_model=Work, status_code=status.HTTP_201_CREATED)
def create_work(work: BaseWork, database: Session=Depends(get_database)):

    try:
        new_work = database.execute(
            insert(WorksModel).returning(WorksModel), 
            [{**work.model_dump()}]
        ).scalar()

    except:
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Не удалось добавить новую работу"
        )
    
    else:
        database.commit()
        return new_work