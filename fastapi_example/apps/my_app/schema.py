from pydantic import BaseModel
from .models import Tournament
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

Tournament_Pydantic = pydantic_model_creator(Tournament, name="Tournament", exclude_readonly=True)
Tournament_PydanticList = pydantic_queryset_creator(Tournament,name="TournamentList")
