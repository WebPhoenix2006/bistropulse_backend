from django.urls import path
from .views import (
    OrderListCreateView,
    RestaurantListCreateView,
    RestaurantRetrieveUpdateDestroyView,
    FoodCategoryListCreateView,
    FoodListCreateView,
    ExtraListCreateView,
    RestaurantFoodListCreateView,
    RiderListCreateView,
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
        "restaurants/<str:restaurant_id>/riders/",
        RiderListCreateView.as_view(),
        name="restaurant-riders",
    ),
    # ✅ Restaurant-specific Orders
    path(
        "<str:restaurant_id>/orders/",
        OrderListCreateView.as_view(),
        name="restaurant-orders",
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
