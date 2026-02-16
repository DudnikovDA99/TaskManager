from django.contrib import admin

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")


admin.site.register(Task, TaskAdmin)

# Register your models here.
