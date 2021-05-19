
import os

from jupyterhub.services.auth import HubAuthenticated
from tornado import escape, httpclient, web

from rest import BaseHandler

class admin_or_user:

    def __init__(self, error):
        self.error = error

    def __call__(self, func):
        async def _func(obj, user):
            current_user = obj.get_current_user()
            if current_user.get("admin", False) or current_user["name"] == user:
                document = await func(obj, user)
                obj.write_or_error(document, self.error)
            else:
                raise web.HTTPError(403)
        return _func

class ProfileHandler(BaseHandler):

    def initialize(self):
        self.storage = self.settings["storage"]
        self.images_api_url = self.settings["images_api_url"]

class HubProfileHandler(ProfileHandler):

    async def get(self, user):
        token = self.request.headers.get('Authorization')
        if token == os.environ["HUB_PROFILES_TOKEN"]:
            document = await self.storage.read(user)
            self.write_or_error(document, 404)
        else:
            raise web.HTTPError(403)

class UserProfileHandler(HubAuthenticated, ProfileHandler):

    allow_admin = True

    @admin_or_user(422)
    @web.authenticated
    async def put(self, user):
        incoming = await self._validate_incoming(user)
        if incoming:
            document = await self.storage.create(user, incoming)
        else:
            document = None
        return document

    async def _validate_incoming(self, user):
        incoming = escape.json_decode(self.request.body)
        if type(incoming) is not dict:
            return None
        if "image" not in incoming:
            return None
        if len(incoming) != 1:
            return None
        image_exists = await self._image_exists(user, incoming["image"])
        if not image_exists:
            return None
        return incoming

    async def _image_exists(self, user, image):
        client = httpclient.AsyncHTTPClient()
        try:
            response = await client.fetch(f"{self.images_api_url}user/{user}",
                headers={"Authorization": f"token {self.hub_auth.api_token}"})
        except Exception as e:
            print("Error: %s" % e)
            return False
        else:
            doc = escape.json_decode(response.body)
            return image in doc["images"]

    @admin_or_user(404)
    @web.authenticated
    async def get(self, user):
        return await self.storage.read(user)

    @admin_or_user(404)
    @web.authenticated
    async def delete(self, user):
        return await self.storage.delete(user)
