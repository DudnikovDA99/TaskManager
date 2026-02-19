from django.contrib import admin

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)

    exclude = ("created_by",)


admin.site.register(Task, TaskAdmin)

# Register your models here.
