from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from src.config import Settings


def get_engine(settings: Settings) -> Engine:
    connect_args = {
        "connect_timeout": settings.query_timeout_seconds,
        "ssl": {"ssl": {}},
    }

    connection_url = (
        f"mysql+pymysql://{settings.db_user}:{settings.db_password}"
        f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
        f"?charset=utf8mb4"
    )

    engine = create_engine(
        connection_url,
        pool_pre_ping=True,
        pool_recycle=1800,
        pool_size=5,
        max_overflow=10,
        future=True,
        connect_args=connect_args,
    )
    return engine
