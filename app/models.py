from datetime import datetime
from typing import List, Optional, Union
from bson.binary import Binary

class Topic:
    def __init__(
        self, 
        title: str, 
        author: str, 
        content: str = "", 
        media: Union[Binary, bytes, None] = None,
        media_type: Optional[str] = None, 
        tags: List[str] = None, 
        links: List[str] = None
    ):
        self.title = title
        self.author = author
        self.content = content
        self.media = media
        self.media_type = media_type
        self.tags = tags or []
        self.links = links or []
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "content": self.content,
            "media": self.media,
            "media_type": self.media_type,
            "tags": self.tags,
            "links": self.links,
            "created_at": self.created_at,
        }