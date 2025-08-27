from fastapi import Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from ..database import topics_collection
from ..utils import get_current_user
templates = Jinja2Templates(directory="app/templates")


from fastapi import APIRouter
router = APIRouter(prefix="/forum")

@router.get("/forum/author/{author_name}", response_class=HTMLResponse)
async def author_topics(
    request: Request, 
    author_name: str, 
    current_user: str = Depends(get_current_user)
):
    """Все темы автора - граф-связь по автору"""
    
    topics = await topics_collection.find({"author": author_name}).sort("created_at", -1).to_list(length=50)
    
    for topic in topics:
        topic["_id"] = str(topic["_id"])
    
    return templates.TemplateResponse("author_topics.html", {
        "request": request,
        "topics": topics,
        "author_name": author_name,
        "current_user": current_user
    })