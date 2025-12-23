from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import make_url
from ..config import settings

DATABASE_URL = settings.get_database_url()

# Parse DSN
url = make_url(DATABASE_URL)

# Detectar si és PostgreSQL (Render) o MySQL (local)
is_postgres = url.drivername.startswith("postgresql")


def ensure_database():
    """Crear base de dades si no existeix (només MySQL local)"""
    if is_postgres:
        # PostgreSQL a Render ja té la BD creada
        return

    # Build server URL WITHOUT database (només MySQL)
    server_url = (
        f"{url.drivername}://{url.username}:{url.password}@{url.host}:{url.port}/"
    )
    server_engine = create_engine(server_url, isolation_level="AUTOCOMMIT")

    db_name = url.database
    with server_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}`"))


# Create DB before regular engine is made (només MySQL)
ensure_database()

# Now the real engine WITH the database
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
