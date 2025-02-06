import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_URL = "mongodb://localhost:27017"  # Replace with your actual MongoDB URL
DATABASE_NAME = "mindful_db"

class MongoDB:
    def __init__(self):
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

    async def get_notes(self):
        """
        Retrieve all notes.
        """
        return await self.db.notes.find().to_list(length=100)

db = MongoDB()

