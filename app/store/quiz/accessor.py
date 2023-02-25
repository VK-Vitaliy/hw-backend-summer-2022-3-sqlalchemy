from sqlalchemy import select

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Answer,
    Question,
    Theme, ThemeModel,
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme = ThemeModel(title=title)
        existed_theme = await self.get_theme_by_title(title)
        if not existed_theme:
            async with self.app.database.session() as session:
                session.add(theme)
                await session.commit()
        return theme


    async def get_theme_by_title(self, title: str) -> Theme | None:
        query = select(ThemeModel).where(ThemeModel.title == title)
        async with self.app.database.session() as session:
            answer = await session.execute(query)
            result = answer.first()
            if result:
                return result[0]
            return None

    async def get_theme_by_id(self, id_: int) -> Theme | None:
        raise NotImplemented

    async def list_themes(self) -> list[Theme]:
        raise NotImplemented

    async def create_answers(
            self, question_id: int, answers: list[Answer]
    ) -> list[Answer]:
        raise NotImplemented

    async def create_question(
            self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        raise NotImplemented

    async def get_question_by_title(self, title: str) -> Question | None:
        raise NotImplemented

    async def list_questions(self, theme_id: int | None = None) -> list[Question]:
        raise NotImplemented
