from tortoise.models import Model
from tortoise import fields


class Tournament(Model):
    # Defining `id` field is optional, it will be defined automatically
    # if you haven't done it yourself
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)

    # Defining ``__str__`` is also optional, but gives you pretty
    # represent of model in debugger and interpreter

    class Meta:
        ordering = ['id', 'name']

    def __str__(self):
        return self.name


class Event(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    # References to other models are defined in format
    # "{app_name}.{model_name}" - where {app_name} is defined in tortoise config
    tournament = fields.ForeignKeyField('app.Tournament', related_name='events')
    participants = fields.ManyToManyField('app.Team', related_name='events', through='event_team')

    class Meta:
        ordering = ['id', 'name']

    def __str__(self):
        return self.name


class Team(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name
