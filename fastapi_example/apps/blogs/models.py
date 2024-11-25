from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Blog(Model):
    # Defining `id` field is optional, it will be defined automatically
    # if you haven't done it yourself
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True, null=True)

    # Defining ``__str__`` is also optional, but gives you pretty
    # represent of model in debugger and interpreter

    class Meta:
        ordering = ['id', '-created_at', '-updated_at']
        app_label = 'blogs'

    def __str__(self):
        return self.name
