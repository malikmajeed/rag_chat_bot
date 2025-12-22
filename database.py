import os
import motor.motor_asyncio
from datetime import datetime
import uuid
from dotenv import load_dotenv

load_dotenv()

class DatabaseHandler:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_uri)
        self.db = self.client["rag_chatbot"]
        self.chat_collection = self.db["chat_history"]

    async def save_message(self, user_id, message, sender):
        """Save a single message to MongoDB."""
        chat_document = {
            "user_id": user_id,
            "message": message,
            "sender": sender,
            "timestamp": datetime.utcnow()
        }
        await self.chat_collection.insert_one(chat_document)

    async def get_recent_history(self, user_id, limit=10):
        """Retrieve the last N messages for a user."""
        cursor = self.chat_collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
        history = await cursor.to_list(length=limit)
        # Reverse to get chronological order [oldest to newest]
        return history[::-1]

    async def clear_history(self, user_id):
        """Clear chat history for a user."""
        await self.chat_collection.delete_many({"user_id": user_id})
