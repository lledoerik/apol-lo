from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ...database import Base


class MoodEntry(Base):
    """Entitat per guardar les entrades del diari emocional."""

    __tablename__ = "mood_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    text = Column(Text, nullable=False)
    mood = Column(Integer, nullable=False)  # 1-5
    date = Column(String(10), nullable=False, index=True)  # YYYY-MM-DD
    time = Column(String(5), nullable=False)  # HH:MM
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relació amb User
    user = relationship("User", back_populates="mood_entries")
