from sqlalchemy.ext.asyncio import AsyncSession

from app.cores.database import Base
from app.repositories.database_repository import DatabaseRepository


def get_repository(
    model: type[Base],
    session: AsyncSession,
) -> DatabaseRepository:
    return DatabaseRepository(model, session)
