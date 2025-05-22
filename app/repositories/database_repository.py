from datetime import datetime
from typing import Generic, Optional, TypeVar, Union

from sqlalchemy import BinaryExpression, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cores.database import Base

Model = TypeVar("Model", bound=Base)


class DatabaseRepository(Generic[Model]):
    """Repository for performing database queries."""

    def __init__(self, model: type[Model], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def create(self, instance: type[Model]) -> Model:
        # instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(self, pk: Union[str, int], update_data: dict) -> Optional[Model]:
        """Update record. If deleted_at is not null, clear it (restore)."""
        instance = await self.get(self.model.id == pk)
        if not instance:
            return None

        # If it's soft-deleted, restore it
        if instance.deleted_at is not None:
            instance.deleted_at = None

        for field, value in update_data.items():
            setattr(instance, field, value)

        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get(self, *expressions: BinaryExpression) -> Model | None:
        query = select(self.model).where(*expressions)
        result = await self.session.scalars(query)
        return result.first()

    async def filter(
        self,
        *expressions: BinaryExpression,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[Model]:
        query = select(self.model).where(self.model.deleted_at.is_(None))
        if expressions:
            query = query.where(*expressions)
        if skip is not None and limit is not None:
            query = query.offset(skip).limit(limit)
        result = await self.session.scalars(query)
        return result.all()

    async def count(self, *expressions: BinaryExpression) -> int:
        query = (
            select(func.count())
            .select_from(self.model)
            .where(self.model.deleted_at.is_(None))
        )
        if expressions:
            query = query.where(*expressions)
        result = await self.session.scalar(query)
        return result

    async def soft_delete(self, pk: Union[str, int]) -> bool:
        """Mark record as deleted by setting deleted_at to current time."""
        instance = await self.get(self.model.id == pk)
        if not instance:
            return False

        instance.deleted_at = datetime.now()
        self.session.add(instance)
        await self.session.commit()
        return True

    async def is_exist(self, *conditions: BinaryExpression) -> bool:
        result = await self.session.execute(select(self.model).where(*conditions))
        return result.scalar_one_or_none() is not None
