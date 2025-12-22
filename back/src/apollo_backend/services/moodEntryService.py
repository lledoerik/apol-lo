from sqlalchemy.orm import Session
from typing import Optional
from collections import defaultdict

from ..models.dao.moodEntryDAO import MoodEntryDAO
from ..models.dto.moodEntryDTO import MoodEntryCreateDTO, MoodEntryUpdateDTO


class MoodEntryServiceResult:
    """Resultat d'operacions del servei."""
    def __init__(self, success: bool, message: str, data=None):
        self.success = success
        self.message = message
        self.data = data


class MoodEntryService:
    """Servei per gestionar les entrades del diari."""

    @staticmethod
    def create_entry(db: Session, user_id: int, dto: MoodEntryCreateDTO) -> MoodEntryServiceResult:
        """Crea una nova entrada."""
        try:
            entry = MoodEntryDAO.create(
                db=db,
                user_id=user_id,
                text=dto.text,
                mood=dto.mood,
                date=dto.date,
                time=dto.time
            )
            return MoodEntryServiceResult(
                success=True,
                message="Entrada creada correctament",
                data=entry
            )
        except Exception as e:
            return MoodEntryServiceResult(
                success=False,
                message=f"Error creant entrada: {str(e)}"
            )

    @staticmethod
    def get_entry(db: Session, user_id: int, entry_id: int) -> MoodEntryServiceResult:
        """Obté una entrada verificant que pertany a l'usuari."""
        entry = MoodEntryDAO.get_by_id_and_user(db, entry_id, user_id)
        if not entry:
            return MoodEntryServiceResult(
                success=False,
                message="Entrada no trobada"
            )
        return MoodEntryServiceResult(
            success=True,
            message="Entrada trobada",
            data=entry
        )

    @staticmethod
    def get_all_entries(db: Session, user_id: int, limit: int = 100, offset: int = 0) -> MoodEntryServiceResult:
        """Obté totes les entrades de l'usuari agrupades per dia."""
        entries = MoodEntryDAO.get_all_by_user(db, user_id, limit, offset)

        # Agrupar per dia
        grouped = defaultdict(list)
        for entry in entries:
            grouped[entry.date].append({
                "id": entry.id,
                "text": entry.text,
                "mood": entry.mood,
                "date": entry.date,
                "time": entry.time,
                "created_at": entry.created_at.isoformat() if entry.created_at else None
            })

        return MoodEntryServiceResult(
            success=True,
            message=f"{len(entries)} entrades trobades",
            data=dict(grouped)
        )

    @staticmethod
    def get_entries_by_date(db: Session, user_id: int, date: str) -> MoodEntryServiceResult:
        """Obté les entrades d'un dia específic."""
        entries = MoodEntryDAO.get_by_user_and_date(db, user_id, date)
        return MoodEntryServiceResult(
            success=True,
            message=f"{len(entries)} entrades trobades",
            data=[{
                "id": e.id,
                "text": e.text,
                "mood": e.mood,
                "date": e.date,
                "time": e.time,
                "created_at": e.created_at.isoformat() if e.created_at else None
            } for e in entries]
        )

    @staticmethod
    def update_entry(db: Session, user_id: int, entry_id: int, dto: MoodEntryUpdateDTO) -> MoodEntryServiceResult:
        """Actualitza una entrada."""
        entry = MoodEntryDAO.get_by_id_and_user(db, entry_id, user_id)
        if not entry:
            return MoodEntryServiceResult(
                success=False,
                message="Entrada no trobada o no tens permís"
            )

        try:
            updated = MoodEntryDAO.update(db, entry, dto.text, dto.mood)
            return MoodEntryServiceResult(
                success=True,
                message="Entrada actualitzada",
                data=updated
            )
        except Exception as e:
            return MoodEntryServiceResult(
                success=False,
                message=f"Error actualitzant: {str(e)}"
            )

    @staticmethod
    def delete_entry(db: Session, user_id: int, entry_id: int) -> MoodEntryServiceResult:
        """Elimina una entrada."""
        entry = MoodEntryDAO.get_by_id_and_user(db, entry_id, user_id)
        if not entry:
            return MoodEntryServiceResult(
                success=False,
                message="Entrada no trobada o no tens permís"
            )

        try:
            MoodEntryDAO.delete(db, entry)
            return MoodEntryServiceResult(
                success=True,
                message="Entrada eliminada"
            )
        except Exception as e:
            return MoodEntryServiceResult(
                success=False,
                message=f"Error eliminant: {str(e)}"
            )

    @staticmethod
    def get_stats(db: Session, user_id: int) -> MoodEntryServiceResult:
        """Obté estadístiques de l'usuari."""
        entries = MoodEntryDAO.get_all_by_user(db, user_id, limit=1000)
        unique_dates = MoodEntryDAO.get_unique_dates_by_user(db, user_id)

        if not entries:
            return MoodEntryServiceResult(
                success=True,
                message="Sense entrades",
                data={
                    "total": 0,
                    "days": 0,
                    "average": 0,
                    "streak": 0
                }
            )

        # Calcular mitjana
        total_mood = sum(e.mood for e in entries)
        average = round(total_mood / len(entries), 1)

        # Calcular ratxa (dies consecutius)
        from datetime import datetime, timedelta
        streak = 0
        today = datetime.now().date()

        for i in range(len(unique_dates)):
            expected_date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            if expected_date in unique_dates:
                streak += 1
            else:
                break

        return MoodEntryServiceResult(
            success=True,
            message="Estadístiques calculades",
            data={
                "total": len(entries),
                "days": len(unique_dates),
                "average": average,
                "streak": streak
            }
        )
