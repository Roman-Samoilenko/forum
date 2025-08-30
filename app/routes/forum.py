from fastapi import APIRouter, Request, Form, Depends, HTTPException, UploadFile, File
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from bson.binary import Binary
from ..database import topics_collection
from ..models import Topic
from ..utils import get_current_user
from ..graph import find_related_topics, update_graph_connections
import base64
from starlette.responses import Response

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/forum")

@router.get("", response_class=HTMLResponse)
async def forum_home(request: Request, current_user: str = Depends(get_current_user)):
    topics = await topics_collection.find().sort("created_at", -1).limit(20).to_list(length=20)
    for topic in topics:
        topic["_id"] = str(topic["_id"])
        # Преобразуем медиа для отображения в списке тоже
        if topic.get("media"):
            if isinstance(topic["media"], (bytes, Binary)):
                topic["media"] = base64.b64encode(topic["media"]).decode("utf-8")
            # Если уже строка - оставляем как есть
    return templates.TemplateResponse("forum_home.html", {"request": request, "topics": topics, "current_user": current_user})

@router.get("/media/{topic_id}")
async def serve_media(topic_id: str):
    """Отдает медиафайл по ID топика"""
    topic = await topics_collection.find_one({"_id": ObjectId(topic_id)})
    
    if not topic or not topic.get("media"):
        raise HTTPException(status_code=404, detail="Медиафайл не найден")
    
    media_data = topic["media"]
    media_type = topic.get("media_type", "image/jpeg")
    
    # Обрабатываем разные форматы данных
    if isinstance(media_data, str):
        # Если base64
        media_bytes = base64.b64decode(media_data)
    elif isinstance(media_data, Binary):
        # Если MongoDB Binary
        media_bytes = bytes(media_data)  
    else:
        # Если уже bytes
        media_bytes = media_data
    
    return Response(
        content=media_bytes,
        media_type=media_type,
        headers={"Cache-Control": "max-age=3600"}  # Кэш на час
    )

# И измените существующий view_topic роут:
@router.get("/topic/{topic_id}", response_class=HTMLResponse)
async def view_topic(request: Request, topic_id: str, current_user: str = Depends(get_current_user)):
    topic = await topics_collection.find_one({"_id": ObjectId(topic_id)})
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Убираем конвертацию в base64 - больше не нужна!
    # if topic.get("media") and isinstance(topic["media"], (bytes, Binary)):
    #     topic["media"] = base64.b64encode(topic["media"]).decode("utf-8")
    
    # Просто добавляем флаг наличия медиа
    topic["has_media"] = bool(topic.get("media"))
    
    related_topics = await find_related_topics(topic_id)
    topic["_id"] = str(topic["_id"])
    
    return templates.TemplateResponse(
        "topic_detail.html",
        {
            "request": request,
            "topic": topic, 
            "related_topics": related_topics,
            "current_user": current_user,
        }
    )

@router.get("/new-topic", response_class=HTMLResponse)
async def new_topic_form(request: Request, current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse("new_topic.html", {"request": request, "current_user": current_user})

@router.post("/new-topic")
async def create_topic(
    request: Request, 
    title: str = Form(...), 
    content: str = Form(""),  # Пустая строка по умолчанию вместо None
    media: UploadFile = File(None),  # Сделали необязательным
    tags: str = Form(""), 
    links: str = Form(""), 
    current_user: str = Depends(get_current_user)
):
    tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    links_list = [link.strip() for link in links.split(",") if link.strip()]
    
    media_data = None
    media_type = None
    
    # Улучшенная проверка загруженного файла
    if media and media.filename and media.size > 0:
        try:
            media_bytes = await media.read()
            if media_bytes:  # Дополнительная проверка на пустые данные
                media_data = Binary(media_bytes)
                media_type = media.content_type
        except Exception as e:
            # Логируем ошибку, но не прерываем создание топика
            print(f"Ошибка при обработке медиа: {e}")
    
    topic = Topic(
        title=title,
        author=current_user,
        content=content,
        media=media_data,
        media_type=media_type,
        tags=tags_list,
        links=links_list
    )
    
    topic_dict = topic.to_dict()
    result = await topics_collection.insert_one(topic_dict)
    await update_graph_connections(topic_dict)
    
    return RedirectResponse(f"/forum/topic/{result.inserted_id}", status_code=303)