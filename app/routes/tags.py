from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from ..database import topics_collection
from ..utils import get_current_user

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/forum")

@router.get("/tag/{tag_name}", response_class=HTMLResponse)
async def tag_topics(request: Request, tag_name: str, current_user: str = Depends(get_current_user)):
    topics = await topics_collection.find({"tags": tag_name}).sort("created_at", -1).to_list(length=50)
    for topic in topics:
        topic["_id"] = str(topic["_id"])
    return templates.TemplateResponse("tag_topics.html", {"request": request, "topics": topics, "tag_name": tag_name, "current_user": current_user})
