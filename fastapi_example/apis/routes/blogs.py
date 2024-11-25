from fastapi import APIRouter
from apps.blogs.models import Blog
from fastapi.params import Query
from tortoise.query_utils import QueryModifier
from apps import blogs
from apps.blogs.schema import Blog_Pydantic_List, Blog_Pydantic

blogs_router = APIRouter()


@blogs_router.get("/search/{last_page}", response_model=Blog_Pydantic_List)
async def search_blogs(name: str = Query(None, description="Blog Name"),
                       page: int = Query(default=1, description="last_page")):
    _offset = (page - 1) * 10
    blogs = await Blog.all().offset(_offset).limit(10)
    return blogs


@blogs_router.post("/posts", response_model=Blog_Pydantic)
async def create_post(blog: Blog_Pydantic):
    new_post = await Blog.create(**blog)
    return new_post
