from hashlib import sha256

from aiohttp.web_exceptions import HTTPForbidden, HTTPBadRequest
from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session

from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response, error_json_response


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        email = self.data["email"]
        existed_admin = await self.store.admins.get_by_email(email)
        if not existed_admin:
            raise HTTPForbidden(reason="no admin with the email")

        password = self.data["password"]
        if not existed_admin.is_password_valid(password):
            raise HTTPForbidden(reason="invalid password")

        raw_admin = AdminSchema().dump(existed_admin)

        session = await new_session(request=self.request)
        session["admin"] = raw_admin

        return json_response(data={"id": existed_admin.id, "email": existed_admin.email})


class AdminCurrentView(AuthRequiredMixin, View):
    @response_schema(AdminSchema, 200)
    async def get(self):
        return json_response(AdminSchema().dump(self.request.admin))