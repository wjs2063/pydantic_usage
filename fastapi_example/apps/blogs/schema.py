from pydantic import BaseModel
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from .models import Blog
from datetime import datetime

Blog_Pydantic = pydantic_model_creator(Blog)
Blog_Pydantic_List = pydantic_queryset_creator(Blog)


class InputBlog(BaseModel):
    name: str
    title: str
    content: str
