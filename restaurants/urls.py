from django.urls import path
from .views import (
    ExtraListCreateView,
    FoodCategoryListCreateView,
    FoodListCreateView,
    RestaurantListCreateView,
)

urlpatterns = [
    path("", RestaurantListCreateView.as_view(), name="restaurant-list"),
    path(
        "food-categories/", FoodCategoryListCreateView.as_view(), name="food-categories"
    ),
    path("extras/", ExtraListCreateView.as_view(), name="extras"),
    path("foods/", FoodListCreateView.as_view(), name="foods"),
]
