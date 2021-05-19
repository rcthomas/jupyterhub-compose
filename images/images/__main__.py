
import argparse
import os

from tornado import ioloop, web

from rest import DefaultHandler

from .api import APIShifterImageHandler

def main():

    args = parse_arguments()

    settings = dict(
        default_handler_class=DefaultHandler,
        serve_traceback=args.serve_traceback,
    )

    return web.Application([
        args.handler_rule(args)
    ], **settings)

def api_handler_rule(args):
    return (
        args.service_prefix + r"user/(.+)", APIShifterImageHandler,
        dict(
            shifter_api_token=args.shifter_api_token,
            shifter_api_host=args.shifter_api_host,
        )
    )

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--service-prefix",
        default=os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "/services/images/"))
    parser.add_argument("--serve-traceback",
        action="store_true")
    subparsers = parser.add_subparsers()

    api_parser = subparsers.add_parser("api")
    api_parser.add_argument("--shifter-api-token",
        default=os.environ.get("SHIFTER_API_TOKEN"))
    api_parser.add_argument("--shifter-api-host",
        default=os.environ.get("SHIFTER_API_HOST"))
    api_parser.set_defaults(handler_rule=api_handler_rule)

    return parser.parse_args()

if __name__ == "__main__":
    app = main()
    app.listen(8888)
    ioloop.IOLoop.current().start()
