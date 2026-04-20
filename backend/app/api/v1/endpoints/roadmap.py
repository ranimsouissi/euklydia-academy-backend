from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.learning_path import LearningPathOut
from app.services.learning_path_service import build_learning_path

router = APIRouter()


@router.get("", response_model=LearningPathOut)
def get_roadmap(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.career_path_id:
        raise HTTPException(status_code=400, detail="Select career path first")

    return build_learning_path(
        db=db,
        user_id=current_user.id,
        career_path_id=current_user.career_path_id,
    )