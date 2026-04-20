from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.career_path import CareerPath

router = APIRouter()

class CareerPathUpdateIn(BaseModel):
    career_path_id: int

@router.patch("/me/career-path")
def update_my_career_path(
    payload: CareerPathUpdateIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cp = db.get(CareerPath, payload.career_path_id)
    if not cp:
        raise HTTPException(status_code=404, detail="Career path not found")

    current_user.career_path_id = payload.career_path_id
    db.commit()

    return {"ok": True, "career_path_id": current_user.career_path_id}