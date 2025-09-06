from bson import ObjectId
from .database import theme_collection, users_collection, tags_collection

async def find_related_topics(topic_id: str) -> dict:
    topic = await theme_collection.find_one({"_id": ObjectId(topic_id)})
    if not topic:
        return {}
    
    related = {"by_author": [], "by_tags": [], "by_links": []}
    
    related["by_author"] = await theme_collection.find(
        {"author": topic["author"], "_id": {"$ne": ObjectId(topic_id)}}
    ).limit(5).to_list(length=5)
    
    if topic.get("tags"):
        related["by_tags"] = await theme_collection.find(
            {"tags": {"$in": topic["tags"]}, "_id": {"$ne": ObjectId(topic_id)}}
        ).limit(5).to_list(length=5)
    
    if topic.get("links"):
        related["by_links"] = await theme_collection.find(
            {"$text": {"$search": " ".join(topic["links"])}, "_id": {"$ne": ObjectId(topic_id)}}
        ).limit(5).to_list(length=5)
    
    return related


async def update_graph_connections(topic_dict: dict):
    await users_collection.update_one(
        {"username": topic_dict["author"]},
        {"$setOnInsert": {"username": topic_dict["author"], "topics_count": 0}},
        upsert=True
    )
    
    await users_collection.update_one(
        {"username": topic_dict["author"]},
        {"$inc": {"topics_count": 1}}
    )
    
    for tag in topic_dict.get("tags", []):
        await tags_collection.update_one(
            {"name": tag},
            {"$setOnInsert": {"name": tag, "usage_count": 0}},
            upsert=True
        )
        await tags_collection.update_one(
            {"name": tag},
            {"$inc": {"usage_count": 1}}
        )
