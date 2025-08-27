from datetime import datetime
from typing import List

class Topic:
    def __init__(self, title: str, author: str, content: str = "", tags: List[str] = None, links: List[str] = None):
        self.title = title
        self.author = author
        self.content = content
        self.tags = tags or []
        self.links = links or []
        self.created_at = datetime.utcnow()
        
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "content": self.content,
            "tags": self.tags,
            "links": self.links,
            "created_at": self.created_at
        }
