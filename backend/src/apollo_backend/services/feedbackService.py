from sqlalchemy.orm import Session
from ..models.dao.feedbackDAO import FeedbackDAO
from ..models.dto.feedbackDTO import FeedbackRequestDTO, FeedbackResponseDTO


class FeedbackService:
    @staticmethod
    def save_feedback(db: Session, dto: FeedbackRequestDTO, user_id: int = None) -> FeedbackResponseDTO:
        """Guarda el feedback de l'usuari"""
        feedback = FeedbackDAO.create(db, dto, user_id)

        if feedback.was_corrected:
            message = "Gràcies per la correcció! Ajudarà a millorar el model."
        else:
            message = "Entrada guardada correctament."

        return FeedbackResponseDTO(
            id=feedback.id,
            was_corrected=bool(feedback.was_corrected),
            message=message,
        )

    @staticmethod
    def get_training_data(db: Session) -> list[dict]:
        """Retorna dades per re-entrenar el model"""
        return FeedbackDAO.export_for_training(db)

    @staticmethod
    def get_stats(db: Session) -> dict:
        """Retorna estadístiques del feedback"""
        all_feedbacks = FeedbackDAO.get_all(db)
        corrections = FeedbackDAO.get_all_corrections(db)

        total = len(all_feedbacks)
        corrected = len(corrections)
        accuracy = ((total - corrected) / total * 100) if total > 0 else 0

        return {
            "total_feedbacks": total,
            "corrections": corrected,
            "confirmations": total - corrected,
            "model_accuracy": round(accuracy, 1),
        }
