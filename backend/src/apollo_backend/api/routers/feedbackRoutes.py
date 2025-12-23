from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from ...database import get_db
from ...services.feedbackService import FeedbackService
from ...models.dto.feedbackDTO import FeedbackRequestDTO
from ..deps import get_current_user_or_none
from ...models.entities.userEntity import User

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/", response_model=dict)
async def save_feedback(
    request: FeedbackRequestDTO,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_or_none)
):
    """
    Guarda el feedback de l'usuari (confirmació o correcció del sentiment detectat).
    Aquesta informació s'usa per millorar el model de ML.
    """
    try:
        # Obtenir user_id del token JWT si està autenticat
        user_id = current_user.id if current_user else None

        result = FeedbackService.save_feedback(db, request, user_id)

        return {
            "success": True,
            "status_code": 200,
            "message": result.message,
            "data": {
                "id": result.id,
                "was_corrected": result.was_corrected,
            },
        }

    except Exception as e:
        return {
            "success": False,
            "status_code": 500,
            "message": "Error guardant feedback",
            "errors": str(e),
        }


@router.get("/stats", response_model=dict)
async def get_feedback_stats(db: Session = Depends(get_db)):
    """
    Retorna estadístiques del feedback recollit.
    Útil per veure quina precisió té el model.
    """
    try:
        stats = FeedbackService.get_stats(db)

        return {
            "success": True,
            "status_code": 200,
            "data": stats,
        }

    except Exception as e:
        return {
            "success": False,
            "status_code": 500,
            "message": "Error obtenint estadístiques",
            "errors": str(e),
        }


@router.get("/export", response_model=dict)
async def export_training_data(db: Session = Depends(get_db)):
    """
    Exporta les dades de feedback en format per re-entrenar el model.
    """
    try:
        data = FeedbackService.get_training_data(db)

        return {
            "success": True,
            "status_code": 200,
            "data": data,
            "count": len(data),
        }

    except Exception as e:
        return {
            "success": False,
            "status_code": 500,
            "message": "Error exportant dades",
            "errors": str(e),
        }
