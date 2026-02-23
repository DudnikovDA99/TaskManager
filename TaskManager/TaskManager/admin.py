from django.contrib import admin
from .models import Task, Subtask
from django.utils.html import format_html
from django.urls import reverse


class SubtaskInline(admin.TabularInline):
    model = Subtask
    extra = 1
    can_delete = False
    readonly_fields = ["edit_link",]


    def get_fields(self, request, obj=None):
        fields = [
            "edit_link",
        ]
        if obj is not None:
            fields.append("is_completed")
        return fields

    def edit_link(self, obj):
        """Возвращает ссылку на редактирование подзадачи с её названием."""
        if obj.pk:  # для уже существующих объектов
            # Формируем URL для изменения объекта Subtask
            url = reverse(
                f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change",
                args=[obj.pk],
            )
            return format_html('<a href="{}">{}</a>', url, obj.name)
        return "—"  # для новых, ещё не сохранённых записей

    edit_link.short_description = " "  # Заголовок колонки


class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at", "is_completed")

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)

    exclude = ("created_by",)
    inlines = [SubtaskInline]


@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    list_display = ("name", "is_completed")
    exclude = ("order", "task")


admin.site.register(Task, TaskAdmin)
# Register your models here.
