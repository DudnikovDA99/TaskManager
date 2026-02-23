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
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    is_completed = models.BooleanField(default=False)
    order = models.PositiveBigIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pk:  # новый объект
            max_order = Subtask.objects.filter(task=self.task).aggregate(
                models.Max("order")
            )["order__max"]
            self.order = (max_order or 0) + 1
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"subtask {self.order}"
