from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGODB_URL, DB_NAME
from pymongo import TEXT

client = AsyncIOMotorClient(MONGODB_URL)
db = client[DB_NAME]

topics_collection = db.theme
users_collection = db.users
tags_collection = db.tags
