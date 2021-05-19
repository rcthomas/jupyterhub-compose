
import json
import traceback

from tornado import escape, web

class BaseHandler(web.RequestHandler):

    def write_or_error(self, document, status_code):
        if document:
            self.write_dict(document)
        else:
            raise web.HTTPError(status_code)

    def write_error(self, status_code, **kwargs):
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
        else:
            self.write_dict(status_code=status_code, reason=self._reason)
        self.finish()

    def write_dict(self, *args, **kwargs):
        if args:
            if len(args) == 1 and type(args[0]) is dict:
                self.write_json(args[0])
            else:
                raise ValueError
        else:
            self.write_json(kwargs)

    def write_json(self, document):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(escape.utf8(json.dumps(document)))

class DefaultHandler(BaseHandler):

    async def prepare(self):
        raise web.HTTPError(404)
