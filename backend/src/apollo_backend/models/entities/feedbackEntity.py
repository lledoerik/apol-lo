from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ...database import Base


class SentimentFeedback(Base):
    """
    Guarda les correccions dels usuaris per millorar el model.
    Quan l'usuari corregeix una predicció, guardem:
    - El text original
    - La predicció del model (label + probabilitats)
    - La correcció de l'usuari (mood 1-5)
    """
    __tablename__ = "sentiment_feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Text analitzat
    text = Column(String(1000), nullable=False)

    # Predicció original del model
    predicted_label = Column(String(20), nullable=False)  # negative/neutral/positive
    predicted_prob_neg = Column(Float, nullable=False)
    predicted_prob_neu = Column(Float, nullable=False)
    predicted_prob_pos = Column(Float, nullable=False)
    predicted_mood = Column(Integer, nullable=False)  # 1-5

    # Correcció de l'usuari
    corrected_mood = Column(Integer, nullable=False)  # 1-5
    was_corrected = Column(Integer, nullable=False, default=0)  # 1 si va canviar, 0 si va confirmar

    # Metadades
    created_at = Column(DateTime, server_default=func.now())

    # Relació amb User
    user = relationship("User", back_populates="feedbacks")
