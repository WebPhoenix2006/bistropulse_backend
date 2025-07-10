from django.urls import path
from .views import (
    RestaurantListCreateView,
    RestaurantRetrieveUpdateDestroyView,
    FoodCategoryListCreateView,
    FoodListCreateView,
    ExtraListCreateView,
)

urlpatterns = [
    path("", RestaurantListCreateView.as_view(), name="restaurant-list-create"),
    path(
        "food-categories/", FoodCategoryListCreateView.as_view(), name="food-categories"
    ),
    path("foods/", FoodListCreateView.as_view(), name="foods"),
    path("extras/", ExtraListCreateView.as_view(), name="extras"),
    path(
        "<str:pk>/",
        RestaurantRetrieveUpdateDestroyView.as_view(),
        name="restaurant-detail",
    ),  # ✅ fixed
]
