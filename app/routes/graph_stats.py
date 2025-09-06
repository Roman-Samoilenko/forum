from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from ..database import theme_collection, users_collection, tags_collection
from ..utils import get_current_user

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/forum")

@router.get("/graph-stats", response_class=HTMLResponse)
async def graph_stats(request: Request, current_user: str = Depends(get_current_user)):
    
    top_authors = await users_collection.find().sort("topics_count", -1).limit(10).to_list(length=10)
    top_tags = await tags_collection.find().sort("usage_count", -1).limit(10).to_list(length=10)
    total_topics = await theme_collection.count_documents({})
    total_users = await users_collection.count_documents({})
    total_tags = await tags_collection.count_documents({})

    return templates.TemplateResponse("graph_stats.html", {
        "request": request,
        "top_authors": top_authors,
        "top_tags": top_tags,
        "total_topics": total_topics,
        "total_users": total_users,
        "total_tags": total_tags,
        "current_user": current_user
    })
