from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source="sender.id")  # 👈 important

    class Meta:
        model = Message
        fields = "__all__"
