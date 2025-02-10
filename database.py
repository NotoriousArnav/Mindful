import motor.motor_asyncio
from bson.objectid import ObjectId
import os
from schemas import *

MONGO_URL = os.getenv("MONGODB_URL" ,"mongodb://localhost:27017")  # Replace with your actual MongoDB URL
DATABASE_NAME = os.getenv("MONGO_DB_NAME","mindful_db")

class MongoDB:
    def __init__(self, MONGO_URL=MONGO_URL, DATABASE_NAME=DATABASE_NAME):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
        self.db = self.client[DATABASE_NAME]

    async def get_user(self, **kwargs):
        """
        Retrieve a user by ObjectId, username or email from the database.
        """
        user = await self.db.users.find_one(kwargs)
        return user

    async def insert_user(self, user_data: dict):
        """
        Insert a new user document into the database.
        """
        result = await self.db.users.insert_one(user_data)
        return str(result.inserted_id)

    async def get_notes(self, **kwargs):
        """
        Retrieve all notes.
        """
        result = await self.db.notes.find(kwargs).to_list(length=None)
        return [NoteFetch(**note) for note in result]

    async def get_note_by_id(self, note_id: str, **kwargs):
        """
        Retrieve a note by ObjectId from the database.
        """
        if not ObjectId.is_valid(note_id):
            __import__('pprint').pprint(note_id)
            return None
        note = await self.db.notes.find_one({"_id": ObjectId(note_id), **kwargs})
        if not note:
            return None
        _id = note['_id']
        note = NoteFetch(**note)
        note._id = str(_id)
        return note

    async def insert_note(self, note_data: Note):
        """
        Insert a new note document into the database.
        """
        note_data = note_data.model_dump()
        result = await self.db.notes.insert_one(note_data)
        return str(result.inserted_id)

    async def update_note(self, note_id: str, note_data: Note):
        """
        Update a note document in the database.
        """
        note_data = note_data.model_dump()
        await self.db.notes.update_one({"_id": ObjectId(note_id)}, {"$set": note_data})
        return await self.get_note_by_id(note_id)

    async def delete_note(self, note_id: str):
        """
        Delete a note document from the database.
        """
        return await self.db.notes.delete_one({"_id": ObjectId(note_id)})

    async def get_collections(self, **kwargs):
        return await self.db.collections.find(kwargs).to_list(length=None)

    async def get_collection_by_id(self, collection_id: str, **kwargs):
        if not ObjectId.is_valid(collection_id):
            __import__('pprint').pprint(collection_id)
            return None
        collection = await self.db.collections.find_one({"_id": ObjectId(collection_id), **kwargs})
        _id = collection['_id']
        collection = NoteCollectionCreate(**collection)
        if collection:
            collection._id = str(_id)
        return collection

    async def insert_collection(self, collection_data: NoteCollectionCreate):
        collection_data = collection_data.model_dump()
        result = await self.db.collections.insert_one(collection_data)
        return str(result.inserted_id)

    async def update_collection(self, collection_id: str, collection_data: NoteCollectionCreate):
        collection_data = collection_data.model_dump()
        await self.db.collections.update_one({"_id": ObjectId(collection_id)}, {"$set": collection_data})
        return await self.get_collection_by_id(collection_id)

    async def delete_collection(self, collection_id: str):
        return await self.db.collections.delete_one({"_id": ObjectId(collection_id)})

db = MongoDB()

