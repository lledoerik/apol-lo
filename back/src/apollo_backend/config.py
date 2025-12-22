from datetime import timedelta
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database URL (Render/PostgreSQL en producció, MySQL en local)
    DATABASE_URL: str | None = None

    # MySQL pieces (per desenvolupament local)
    mysql_user: str | None = None
    mysql_password: str | None = None
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_db: str | None = None

    # Frontend URL per CORS
    FRONTEND_URL: str = "http://localhost:5173"

    class Config:
        extra = "ignore"
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_database_url(self) -> str:
        # Si tenim DATABASE_URL directa (Render/producció), usar-la
        if self.DATABASE_URL:
            return self.DATABASE_URL
        # Sinó, construir URL MySQL per desenvolupament local
        if self.mysql_user and self.mysql_password and self.mysql_db:
            return (
                f"mysql+mysqlconnector://{self.mysql_user}:"
                f"{self.mysql_password}@{self.mysql_host}:"
                f"{self.mysql_port}/{self.mysql_db}"
            )
        raise ValueError("No database configuration found. Set DATABASE_URL or mysql_* variables.")

    @property
    def access_token_expires(self) -> timedelta:
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
