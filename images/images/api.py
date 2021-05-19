
from aiocache import cached
from aiocache.serializers import NullSerializer
from jupyterhub.services.auth import HubAuthenticated
from tornado import escape, httpclient, web

from rest import BaseHandler


def key_builder(func, self, user):
    return user


class ShifterImageHandler(HubAuthenticated, BaseHandler):

    allow_admin = True

    @web.authenticated
    async def get(self, user):
        current_user = self.get_current_user()
        if current_user.get("admin", False) or current_user["name"] == user:
            images = await self._get(user)
            self.write_dict({"images": images})
        else:
            raise web.HTTPError(403)

    async def _get(self, user):
        raise NotImplementedError


class APIShifterImageHandler(ShifterImageHandler):

    def initialize(self, shifter_api_token, shifter_api_host):
        self.shifter_api_token = shifter_api_token
        self.shifter_api_host = shifter_api_host

    @cached(60, key_builder=key_builder, serializer=NullSerializer())
    async def _get(self, user):
        client = httpclient.AsyncHTTPClient()
        try:
            response = await client.fetch(f"{self.shifter_api_host}/list/{user}",
                headers={"Authorization": self.shifter_api_token})
        except Exception as e:
            print("Error: %s" % e)
            return False
        else:
            doc = escape.json_decode(response.body)
            images = list()
            for entry in doc.get("images", []):
                env = entry.get("ENV", [])
                if env and "NERSC_JUPYTER_IMAGE=YES" in env:
                    images += entry.get("tag", [])
            return images
