from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Restaurant
from .serializers import RestaurantSerializer

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.none()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Restaurant.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)