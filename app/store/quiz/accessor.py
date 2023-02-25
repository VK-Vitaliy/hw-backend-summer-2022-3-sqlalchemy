from sqlalchemy import select

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Answer,
    Question,
    Theme, ThemeModel, QuestionModel, AnswerModel,
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme = ThemeModel(title=title)
        async with self.app.database.session() as session:
            session.add(theme)
            await session.commit()
        return Theme(id=theme.id, title=theme.title)

    async def get_theme_by_title(self, title: str) -> Theme | None:
        query = select(ThemeModel).where(ThemeModel.title == title)
        async with self.app.database.session() as session:
            answer = await session.execute(query)
            result = answer.first()[0]
            if result:
                return Theme(id=result.id, title=result.title)
            return None

    async def get_theme_by_id(self, id_: int) -> Theme | None:
        query = select(ThemeModel).where(ThemeModel.id == id_)
        async with self.app.database.session() as session:
            answer = await session.execute(query)
            result = answer.first()[0]
            if result:
                return Theme(id=result.id, title=result.title)
            return None

    async def list_themes(self) -> list[Theme]:
        list_themes = []
        query = select(ThemeModel)
        async with self.app.database.session() as session:
            answer = await session.execute(query)
            results = answer.scalars().all()
            for res in results:
                list_themes.append(Theme(id=res.id, title=res.title))
        return list_themes

    async def create_answers(self, question_id: int, answers: list[Answer]) -> list[Answer]:
        raise NotImplemented

    async def create_question(self, title: str, theme_id: int, answers: list[Answer]) -> Question:
        question = QuestionModel(title=title, theme_id=theme_id)
        existed_question = await self.get_question_by_title(title)
        if not existed_question:
            async with self.app.database.session() as session:
                session.add(question)
                await session.commit()
        await self.create_answers(answers=answers, question_id=question.id)
        return question

    async def get_question_by_title(self, title: str) -> Question | None:
        query = select(QuestionModel).where(QuestionModel.title == title)
        async with self.app.database.session() as session:
            answer = await session.execute(query)
            result = answer.first()[0]
            if result:
                return Question(
                    id=result.id,
                    title=title,
                    theme_id=result.theme_id,
                    answers=[
                        Answer(
                            title=a.title,
                            is_correct=a.is_correct,
                        )
                        for a in result.answers
                    ],
                )
            return None

    async def list_questions(self, theme_id: int | None = None) -> list[Question]:
        list_questions = []
        query_question_models = select(QuestionModel) if not theme_id else select(QuestionModel).where(
            QuestionModel.theme_id == theme_id)
        query_answer_models = select(AnswerModel)
        async with self.app.database.session() as session:

            question_models = await session.execute(query_question_models)
            question_models_results = question_models.scalars().all()
            answer_models = await session.execute(query_answer_models)
            answer_models_results = answer_models.scalars().all()

            for res in question_models_results:
                list_questions.append(
                    Question(
                        id=res.id,
                        title=res.title,
                        theme_id=res.theme_id,
                        answers=[Answer(title=ans.title, is_correct=ans.is_correct)
                                 for ans in answer_models_results if ans.question_id == res.id]))
        if theme_id is None:
            return list_questions
