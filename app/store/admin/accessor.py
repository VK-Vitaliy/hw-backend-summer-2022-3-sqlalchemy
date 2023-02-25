import asyncio
import typing
from hashlib import sha256
from typing import Optional

from sqlalchemy import select

from app.admin.models import AdminModel
from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def get_by_email(self, email: str) -> Optional[AdminModel]:
        query = select(AdminModel).where(AdminModel.email == email)
        async with self.app.database.session() as session:
            answer = await session.execute(query)
            result = answer.first()
            if result:
                return result[0]
            return None

    async def create_admin(self, email: str, password: str) -> AdminModel:
        admin = AdminModel(
            email=email,
            password=str(sha256(password.encode("utf-8")).hexdigest()),
        )
        existed_admin = await self.get_by_email(email)
        if not existed_admin:
            async with self.app.database.session() as session:
                session.add(admin)
                await session.commit()
        return admin

    async def connect(self, app: "Application"):
        await self.create_admin(
            email=self.app.config.admin.email,
            password=self.app.config.admin.password,
        )
