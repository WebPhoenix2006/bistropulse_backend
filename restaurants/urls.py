from django.urls import path
from .views import (
    RestaurantListCreateView,
    RestaurantRetrieveUpdateDestroyView,
    FoodCategoryListCreateView,
    FoodListCreateView,
    ExtraListCreateView,
    RestaurantFoodListCreateView,
    RiderListCreateView,
    RiderRetrieveUpdateDestroyView,
)
from orders.views import OrderListCreateView

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
        "<str:restaurant_id>/riders/",
        RiderListCreateView.as_view(),
        name="restaurant-riders",
    ),
    # Restaurant-specific Orders
    path(
        "<str:restaurant_id>/orders/",
        OrderListCreateView.as_view(),
        name="restaurant-orders",
    ),
    
    # Food Categories
    path(
        "food-categories/", FoodCategoryListCreateView.as_view(), name="food-categories"
    ),
    # Foods (global and restaurant-specific)
    path("foods/", FoodListCreateView.as_view(), name="foods"),
    path(
        "<str:restaurant_id>/foods/",
        RestaurantFoodListCreateView.as_view(),
        name="restaurant-foods",
    ),
    # Extras
    path("extras/", ExtraListCreateView.as_view(), name="extras"),
    path(
    "<str:restaurant_id>/riders/<str:rider_code>/",
    RiderRetrieveUpdateDestroyView.as_view(),
    name="restaurant-rider-detail",
),
]
