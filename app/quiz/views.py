
from collections import Counter

from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound, HTTPBadRequest
from aiohttp_apispec import request_schema, response_schema, querystring_schema

from app.quiz.models import Answer
from app.quiz.schemes import (
    ThemeSchema, ThemeListSchema, QuestionSchema, ThemeIdSchema, ListQuestionSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(AuthRequiredMixin, View):
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema)
    async def post(self):
        title = self.data["title"]
        existing_theme = await self.store.quizzes.get_theme_by_title(title)
        if existing_theme:
            raise HTTPConflict(reason="theme exists")
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    @response_schema(ThemeListSchema)
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        return json_response(data=ThemeListSchema().dump({"themes": themes}))


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        data = self.request['data']

        if len(data['answers']) <= 1:
            raise HTTPBadRequest

        count_answer = Counter(val['is_correct'] for val in data['answers'] if val['is_correct'])
        if not count_answer or count_answer[True] > 1:
            raise HTTPBadRequest

        theme = await self.store.quizzes.get_theme_by_id(data['theme_id'])
        if not theme:
            raise HTTPNotFound

        question_title = await self.store.quizzes.get_question_by_title(data["title"])
        if question_title:
            raise HTTPConflict

        answers = self.data['answers']
        question = await self.store.quizzes.create_question(
            title=data['title'],
            theme_id=data['theme_id'],
            answers=[Answer(
                title=answer["title"],
                is_correct=answer["is_correct"]
            ) for answer in answers],
        )

        return json_response(data=QuestionSchema().dump(question))


class QuestionListView(AuthRequiredMixin, View):
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema)
    async def get(self):
        theme_id = self.request["querystring"].get('theme_id')
        questions = await self.store.quizzes.list_questions(theme_id=theme_id)
        resp = {"questions": questions}
        return json_response(data=ListQuestionSchema().dump(resp))
