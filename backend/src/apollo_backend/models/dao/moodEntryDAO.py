from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional

from ..entities.moodEntryEntity import MoodEntry


class MoodEntryDAO:
    """Data Access Object per MoodEntry."""

    @staticmethod
    def create(db: Session, user_id: int, text: str, mood: int, date: str, time: str) -> MoodEntry:
        """Crea una nova entrada."""
        entry = MoodEntry(
            user_id=user_id,
            text=text,
            mood=mood,
            date=date,
            time=time
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    @staticmethod
    def get_by_id(db: Session, entry_id: int) -> Optional[MoodEntry]:
        """Obté una entrada per ID."""
        return db.query(MoodEntry).filter(MoodEntry.id == entry_id).first()

    @staticmethod
    def get_by_id_and_user(db: Session, entry_id: int, user_id: int) -> Optional[MoodEntry]:
        """Obté una entrada per ID verificant que pertany a l'usuari."""
        return db.query(MoodEntry).filter(
            MoodEntry.id == entry_id,
            MoodEntry.user_id == user_id
        ).first()

    @staticmethod
    def get_all_by_user(db: Session, user_id: int, limit: int = 100, offset: int = 0) -> list[MoodEntry]:
        """Obté totes les entrades d'un usuari ordenades per data i hora."""
        return db.query(MoodEntry).filter(
            MoodEntry.user_id == user_id
        ).order_by(
            desc(MoodEntry.date),
            desc(MoodEntry.time)
        ).offset(offset).limit(limit).all()

    @staticmethod
    def get_by_user_and_date(db: Session, user_id: int, date: str) -> list[MoodEntry]:
        """Obté les entrades d'un usuari per un dia específic."""
        return db.query(MoodEntry).filter(
            MoodEntry.user_id == user_id,
            MoodEntry.date == date
        ).order_by(MoodEntry.time).all()

    @staticmethod
    def get_by_user_and_date_range(
        db: Session, user_id: int, start_date: str, end_date: str
    ) -> list[MoodEntry]:
        """Obté les entrades d'un usuari en un rang de dates."""
        return db.query(MoodEntry).filter(
            MoodEntry.user_id == user_id,
            MoodEntry.date >= start_date,
            MoodEntry.date <= end_date
        ).order_by(
            desc(MoodEntry.date),
            desc(MoodEntry.time)
        ).all()

    @staticmethod
    def update(db: Session, entry: MoodEntry, text: Optional[str] = None, mood: Optional[int] = None) -> MoodEntry:
        """Actualitza una entrada."""
        if text is not None:
            entry.text = text
        if mood is not None:
            entry.mood = mood
        db.commit()
        db.refresh(entry)
        return entry

    @staticmethod
    def delete(db: Session, entry: MoodEntry) -> None:
        """Elimina una entrada."""
        db.delete(entry)
        db.commit()

    @staticmethod
    def count_by_user(db: Session, user_id: int) -> int:
        """Compta el total d'entrades d'un usuari."""
        return db.query(MoodEntry).filter(MoodEntry.user_id == user_id).count()

    @staticmethod
    def get_unique_dates_by_user(db: Session, user_id: int) -> list[str]:
        """Obté les dates úniques amb entrades per un usuari."""
        results = db.query(MoodEntry.date).filter(
            MoodEntry.user_id == user_id
        ).distinct().order_by(desc(MoodEntry.date)).all()
        return [r[0] for r in results]
