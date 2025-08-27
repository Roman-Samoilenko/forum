from fastapi import FastAPI
from .routes import forum, authors, tags, graph_stats

app = FastAPI()

app.include_router(forum.router)
app.include_router(authors.router)
app.include_router(tags.router)
app.include_router(graph_stats.router)
