from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGODB_URL, DB_NAME
from pymongo import TEXT

client = AsyncIOMotorClient(MONGODB_URL)
db = client[DB_NAME]

theme_collection = db.theme
users_collection = db.users
tags_collection = db.tags

theme_collection.create_index([
    ('title', TEXT),
    ('author', TEXT),
    ('tags', TEXT),
    ('links', TEXT)
], name='theme_search_index')


users_collection.create_index([
    ('username', TEXT)
], name='user_search_index')


tags_collection.create_index([
    ('name', TEXT)
], name='tags_search_index')