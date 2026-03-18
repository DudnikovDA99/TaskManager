from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    startDate = serializers.DateTimeField(source="start_date")
    endDate = serializers.DateTimeField(source="end_date")
    priority = serializers.CharField(source="get_priority_display", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "priority",
            "is_completed",
            "startDate",
            "endDate",
        ]
