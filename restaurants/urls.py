from django.urls import path
from .views import (
    RestaurantListCreateView,
    RestaurantRetrieveUpdateDestroyView,
    FoodCategoryListCreateView,
    FoodListCreateView,
    ExtraListCreateView,
    RestaurantFoodListCreateView,
    RiderListCreateView,  # For restaurant-specific rider creation/list
)

urlpatterns = [
    # Restaurants
    path("", RestaurantListCreateView.as_view(), name="restaurant-list-create"),
    path(
        "<str:pk>/",
        RestaurantRetrieveUpdateDestroyView.as_view(),
        name="restaurant-detail",
    ),
    # Restaurant-specific Riders
    path(
        "restaurants/<int:restaurant_id>/riders/",
        RiderListCreateView.as_view(),
        name="restaurant-riders",
    ),
    # Food categories
    path(
        "food-categories/", FoodCategoryListCreateView.as_view(), name="food-categories"
    ),
    # Foods (global and per restaurant)
    path("foods/", FoodListCreateView.as_view(), name="foods"),
    path(
        "<str:restaurant_id>/foods/",
        RestaurantFoodListCreateView.as_view(),
        name="restaurant-foods",
    ),
    # Extras
    path("extras/", ExtraListCreateView.as_view(), name="extras"),
]
