from django.urls import path
from .views import RestaurantListCreateView, RestaurantDetailView

urlpatterns = [
    path('', RestaurantListCreateView.as_view(), name='restaurant-list'),
]
