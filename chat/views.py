from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Message
from .serializers import MessageSerializer
from django.db.models import Q
import logging


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        other_user_id = self.request.query_params.get('user')

        if not other_user_id:
            return Message.objects.none()  # Avoid fetching everything accidentally

        # Combine sender/receiver filter with Q for cleaner logic
        queryset = Message.objects.filter(
            Q(sender=user, receiver_id=other_user_id) |
            Q(sender_id=other_user_id, receiver=user)
        ).order_by('timestamp')

        # Optional: Fetch only last message if `last=true` is passed
        if self.request.query_params.get('last') == 'true':
            return queryset.last() and [queryset.last()] or []

        return queryset

    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user)
        logging.info(f'Message saved at: {message.timestamp}')
