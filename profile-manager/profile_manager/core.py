
from jinja2 import Environment

from jupyterhub.services.auth import HubAuthenticated
from jupyterhub.utils import url_path_join

from tornado import ioloop, web

from jupyterhub_service_page.core import Service

class ServiceViewHandler(HubAuthenticated, web.RequestHandler):

    def initialize(self, loader):
        super().initialize()
        self.loader = loader
        self.env = Environment(loader=self.loader)
        self.template = self.env.get_template("index.html")

    @web.authenticated
    def get(self):
        user = self.get_current_user()
        prefix = self.hub_auth.hub_prefix
        logout_url = url_path_join(prefix, "logout")
        self.write(self.template.render(user=user, 
            static_url=self.static_url,
            login_url=self.hub_auth.login_url, 
            logout_url=logout_url,
            base_url=prefix,
            no_spawner_check=True))

class MyService(Service):

    def initialize(self, argv=None):
        super().initialize(argv)
        rules = [(self.service_prefix, ServiceViewHandler,
            {"loader": self.loader})]
        self.init_webapp(rules)

def main():
    app = MyService()
    app.initialize()
    app.start()
