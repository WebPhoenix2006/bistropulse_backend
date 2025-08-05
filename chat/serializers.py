from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source="sender.id")  # 👈 important
    # timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")


    class Meta:
        model = Message
        fields = "__all__"
