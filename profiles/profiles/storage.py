
import json
from pathlib import Path

class Storage:

    async def create(self, user, incoming):
        raise NotImplementedError

    async def read(self, user):
        raise NotImplementedError

    async def update(self, user, incoming):
        raise NotImplementedError

    async def delete(self, user):
        raise NotImplementedError

class MongoStorage(Storage):

    def __init__(self, db, collection_name):
        self.db = db
        self.collection = self.db[collection_name]

    async def create(self, user, incoming):
        document = await self.collection.find_one_and_replace(
            {"_id": user},
            {"_id": user, "image": incoming["image"]},
            upsert=True
        )
        return dict(updated=1) if document else dict(created=1)

    async def read(self, user):
        document = await self.collection.find_one(
            {"_id": user},
            {"_id": False}
        )
        return document

    async def update(self, user, incoming):
        return await self.create(user, incoming)

    async def delete(self, user):
        result = await self.collection.delete_one(
            {"_id": user}
        )
        return dict(deleted=1) if result.deleted_count == 1 else None

class FileStorage(Storage):

    def __init__(self, template="/data/{user[0]}/{user}.json"):
        self.template = template

    def doc_path(self, user):
        return Path(self.template.format(user=user))

    async def create(self, user, incoming):
        doc_path = self.doc_path(user)
        exists = doc_path.is_file()
        doc_path.parent.mkdir(parents=True, exist_ok=True)
        with open(doc_path, "w") as stream:
            json.dump({"image": incoming["image"]}, stream)
        return dict(updated=1) if exists else dict(created=1)

    async def read(self, user):
        doc_path = self.doc_path(user)
        try:
            with open(doc_path, "r") as stream:
                return json.load(stream)
        except:
            return None

    async def update(self, user, incoming):
        return await self.create(user, incoming)

    async def delete(self, user):
        doc_path = self.doc_path(user)
        try:
            doc_path.unlink()
            return dict(deleted=1)
        except:
            return None
