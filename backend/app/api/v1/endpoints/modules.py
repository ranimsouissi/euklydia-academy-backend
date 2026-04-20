from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.module import Module
from app.models.user import User
from app.models.user_module_progress import UserModuleProgress
from app.schemas.module import ModuleRead

router = APIRouter()


@router.get("/", response_model=list[ModuleRead])
def read_modules(
    db: Session = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
) -> list[Module]:
    return (
        db.query(Module)
        .filter(Module.is_active.is_(True))
        .order_by(Module.display_order.asc(), Module.id.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{module_id}", response_model=ModuleRead)
def read_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Module:
    module = (
        db.query(Module)
        .filter(Module.id == module_id, Module.is_active.is_(True))
        .first()
    )
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    progress = (
        db.query(UserModuleProgress)
        .filter(
            UserModuleProgress.user_id == current_user.id,
            UserModuleProgress.module_id == module_id,
        )
        .first()
    )

    module.status = progress.status if progress else "not_started"
    module.progress_percent = progress.progress_percent if progress else 0

    return module


@router.post("/{module_id}/start")
def start_module(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    module = (
        db.query(Module)
        .filter(Module.id == module_id, Module.is_active.is_(True))
        .first()
    )
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    progress = (
        db.query(UserModuleProgress)
        .filter(
            UserModuleProgress.user_id == current_user.id,
            UserModuleProgress.module_id == module_id,
        )
        .first()
    )

    now = datetime.utcnow()

    if not progress:
        progress = UserModuleProgress(
            user_id=current_user.id,
            module_id=module_id,
            status="in_progress",
            started_at=now,
            progress_percent=0,  # ✅
        )
        db.add(progress)
    else:
        if progress.status != "completed":
            progress.status = "in_progress"
            if not progress.started_at:
                progress.started_at = now
            progress.updated_at = now
            # ✅ Ne pas écraser une progression existante

    db.commit()
    db.refresh(progress)

    return {
        "message": "Module started",
        "module_id": module_id,
        "status": progress.status,
        "progress_percent": progress.progress_percent,  # ✅
        "started_at": progress.started_at,
        "completed_at": progress.completed_at,
    }


@router.post("/{module_id}/complete")
def complete_module(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    module = (
        db.query(Module)
        .filter(Module.id == module_id, Module.is_active.is_(True))
        .first()
    )
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    progress = (
        db.query(UserModuleProgress)
        .filter(
            UserModuleProgress.user_id == current_user.id,
            UserModuleProgress.module_id == module_id,
        )
        .first()
    )

    now = datetime.utcnow()

    if not progress:
        progress = UserModuleProgress(
            user_id=current_user.id,
            module_id=module_id,
            status="completed",
            started_at=now,
            completed_at=now,
            progress_percent=100,  # ✅
        )
        db.add(progress)
    else:
        progress.status = "completed"
        progress.progress_percent = 100  # ✅
        if not progress.started_at:
            progress.started_at = now
        progress.completed_at = now
        progress.updated_at = now

    db.commit()
    db.refresh(progress)

    return {
        "message": "Module completed",
        "module_id": module_id,
        "status": progress.status,
        "progress_percent": progress.progress_percent,  # ✅
        "started_at": progress.started_at,
        "completed_at": progress.completed_at,
    }