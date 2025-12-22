from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from ...database import get_db
from ...services.moodEntryService import MoodEntryService
from ...models.dto.moodEntryDTO import MoodEntryCreateDTO, MoodEntryUpdateDTO
from ..deps import get_current_user
from ...models.entities.userEntity import User

router = APIRouter(prefix="/entries", tags=["Mood Entries"])


@router.post("/", response_model=dict)
async def create_entry(
    request: MoodEntryCreateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crea una nova entrada al diari."""
    result = MoodEntryService.create_entry(db, current_user.id, request)

    if not result.success:
        return {
            "success": False,
            "status_code": 400,
            "message": result.message
        }

    return {
        "success": True,
        "status_code": 201,
        "message": result.message,
        "data": {
            "id": result.data.id,
            "text": result.data.text,
            "mood": result.data.mood,
            "date": result.data.date,
            "time": result.data.time
        }
    }


@router.get("/", response_model=dict)
async def get_all_entries(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obté totes les entrades de l'usuari agrupades per dia."""
    result = MoodEntryService.get_all_entries(db, current_user.id, limit, offset)

    return {
        "success": True,
        "status_code": 200,
        "message": result.message,
        "data": result.data
    }


@router.get("/date/{date}", response_model=dict)
async def get_entries_by_date(
    date: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obté les entrades d'un dia específic."""
    result = MoodEntryService.get_entries_by_date(db, current_user.id, date)

    return {
        "success": True,
        "status_code": 200,
        "message": result.message,
        "data": result.data
    }


@router.get("/stats", response_model=dict)
async def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obté estadístiques de l'usuari."""
    try:
        result = MoodEntryService.get_stats(db, current_user.id)

        return {
            "success": True,
            "status_code": 200,
            "data": result.data
        }
    except Exception as e:
        return {
            "success": False,
            "status_code": 500,
            "message": "Error obtenint estadístiques",
            "errors": str(e)
        }


@router.get("/{entry_id}", response_model=dict)
async def get_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obté una entrada específica."""
    result = MoodEntryService.get_entry(db, current_user.id, entry_id)

    if not result.success:
        return {
            "success": False,
            "status_code": 404,
            "message": result.message
        }

    return {
        "success": True,
        "status_code": 200,
        "data": {
            "id": result.data.id,
            "text": result.data.text,
            "mood": result.data.mood,
            "date": result.data.date,
            "time": result.data.time
        }
    }


@router.put("/{entry_id}", response_model=dict)
async def update_entry(
    entry_id: int,
    request: MoodEntryUpdateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualitza una entrada."""
    result = MoodEntryService.update_entry(db, current_user.id, entry_id, request)

    if not result.success:
        return {
            "success": False,
            "status_code": 404,
            "message": result.message
        }

    return {
        "success": True,
        "status_code": 200,
        "message": result.message,
        "data": {
            "id": result.data.id,
            "text": result.data.text,
            "mood": result.data.mood
        }
    }


@router.delete("/{entry_id}", response_model=dict)
async def delete_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Elimina una entrada."""
    result = MoodEntryService.delete_entry(db, current_user.id, entry_id)

    if not result.success:
        return {
            "success": False,
            "status_code": 404,
            "message": result.message
        }

    return {
        "success": True,
        "status_code": 200,
        "message": result.message
    }
