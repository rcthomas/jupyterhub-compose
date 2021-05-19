
import argparse
import os

from motor import motor_tornado
from tornado import ioloop, web

from rest import DefaultHandler

from .api import HubProfileHandler, UserProfileHandler
from .storage import FileStorage, MongoStorage

def main():

    args = parse_arguments()

    settings = dict(
        images_api_url=args.images_api_url,
        default_handler_class=DefaultHandler,
        serve_traceback=args.serve_traceback,
        storage=args.storage_factory(args)
    )

    return web.Application([
        (args.service_prefix + r"user/(.+)", UserProfileHandler),
        (args.service_prefix + r"hub/(.+)", HubProfileHandler),
    ], **settings)

def file_storage(args):
    template = os.path.join(args.storage_path, "{user[0]}/{user}.json")
    return FileStorage(template)

def mongo_storage(args):
    client = motor_tornado.MotorClient(args.mongodb_uri)
    if args.reset_database:
        client.drop_database(args.database_name)
    db = client[args.database_name]
    return MongoStorage(db, args.database_name)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--images-api-url",
        default=os.environ.get("IMAGES_API_URL", "http://proxy:8000/services/images/"))
    parser.add_argument("--service-prefix",
        default=os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "/services/profiles/"))
    parser.add_argument("--serve-traceback",
        action="store_true")
    subparsers = parser.add_subparsers()

    file_parser = subparsers.add_parser("file")
    file_parser.add_argument("--storage-path",
        default=os.environ.get("STORAGE_PATH", "/data"))
    file_parser.set_defaults(storage_factory=file_storage)

    mongodb_parser = subparsers.add_parser("mongodb")
    mongodb_parser.add_argument("--mongodb-uri",
        default=os.environ.get("MONGODB_URI", "mongodb://db:27017"))
    mongodb_parser.add_argument("--database-name",
        default=os.environ.get("MONGODB_DATABASE_NAME", "profiles"))
    mongodb_parser.add_argument("--reset-database",
        action="store_true")
    mongodb_parser.set_defaults(storage_factory=mongo_storage)

    return parser.parse_args()

if __name__ == "__main__":
    app = main()
    app.listen(8888)
    ioloop.IOLoop.current().start()
