from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.career_path import CareerPath
from pydantic import BaseModel

router = APIRouter()


class CareerPathOut(BaseModel):
    id: int
    name: str
    description: str | None = None


@router.get("/", response_model=list[CareerPathOut])
def list_career_paths(db: Session = Depends(get_db)):
    stmt = select(CareerPath).order_by(CareerPath.id)
    items = db.execute(stmt).scalars().all()
    return [
        CareerPathOut(id=cp.id, name=cp.name, description=cp.description)
        for cp in items
    ]