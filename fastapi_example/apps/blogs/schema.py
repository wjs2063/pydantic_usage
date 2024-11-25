from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from .models import Blog

Blog_Pydantic = pydantic_model_creator(Blog)
Blog_Pydantic_List = pydantic_queryset_creator(Blog)
