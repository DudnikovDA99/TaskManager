from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    class Priority(models.IntegerChoices):
        MAIN_QUEST = 1, "Main_quest"
        SIDE_QUEST = 2, "Routine"
        DAILY = 3, "Daily"
        GRIND = 4, "Grind"

    priority = models.IntegerField(
        choices=Priority.choices,
        default=Priority.SIDE_QUEST,
    )
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
