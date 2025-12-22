from sqlalchemy.orm import Session
from ..entities.feedbackEntity import SentimentFeedback
from ..dto.feedbackDTO import FeedbackRequestDTO


class FeedbackDAO:
    @staticmethod
    def create(db: Session, dto: FeedbackRequestDTO, user_id: int = None) -> SentimentFeedback:
        """Guarda un nou feedback a la BD"""
        was_corrected = 1 if dto.predicted_mood != dto.corrected_mood else 0

        feedback = SentimentFeedback(
            user_id=user_id,
            text=dto.text,
            predicted_label=dto.predicted_label,
            predicted_prob_neg=dto.predicted_probabilities.get("0", 0),
            predicted_prob_neu=dto.predicted_probabilities.get("1", 0),
            predicted_prob_pos=dto.predicted_probabilities.get("2", 0),
            predicted_mood=dto.predicted_mood,
            corrected_mood=dto.corrected_mood,
            was_corrected=was_corrected,
        )

        db.add(feedback)
        db.commit()
        db.refresh(feedback)
        return feedback

    @staticmethod
    def get_all_corrections(db: Session):
        """Retorna tots els feedbacks on l'usuari va corregir la predicció"""
        return db.query(SentimentFeedback).filter(
            SentimentFeedback.was_corrected == 1
        ).all()

    @staticmethod
    def get_all(db: Session):
        """Retorna tots els feedbacks"""
        return db.query(SentimentFeedback).all()

    @staticmethod
    def export_for_training(db: Session) -> list[dict]:
        """
        Exporta les dades en format per re-entrenar el model.
        Retorna llista de {text, sentiment} on sentiment és basat en corrected_mood.
        """
        feedbacks = db.query(SentimentFeedback).all()

        training_data = []
        for fb in feedbacks:
            # Convertir mood 1-5 a sentiment label
            if fb.corrected_mood <= 2:
                sentiment = "negative"
            elif fb.corrected_mood >= 4:
                sentiment = "positive"
            else:
                sentiment = "neutral"

            training_data.append({
                "text": fb.text,
                "sentiment": sentiment,
                "mood": fb.corrected_mood,
            })

        return training_data
