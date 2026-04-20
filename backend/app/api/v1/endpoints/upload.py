import os
import uuid
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()

UPLOAD_DIR = "app/static/uploads"
ALLOWED_TYPES = {"image/png", "image/jpeg", "image/webp", "video/mp4"}
MAX_SIZE_MB = 50


@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Type de fichier non supporté : {file.content_type}. Formats acceptés : PNG, JPEG, WEBP, MP4."
        )

    contents = await file.read()

    if len(contents) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"Fichier trop volumineux. Maximum : {MAX_SIZE_MB}MB."
        )

    ext = file.filename.split(".")[-1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    with open(filepath, "wb") as f:
        f.write(contents)

    return {
        "url": f"/static/uploads/{filename}",
        "filename": filename,
        "original_name": file.filename,
        "content_type": file.content_type,
        "size_kb": round(len(contents) / 1024, 1),
    }