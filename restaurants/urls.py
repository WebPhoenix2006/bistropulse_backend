from django.urls import path
from .views import (
    RestaurantCategoryFoodCreateView,
    RestaurantListCreateView,
    RestaurantRetrieveUpdateDestroyView,
    FoodCategoryListCreateView,
    FoodListCreateView,
    ExtraListCreateView,
    RestaurantFoodListCreateView,
    RiderListCreateView,
    RiderRetrieveUpdateDestroyView,
)
from orders.views import (
    OrderListCreateView,
    RestaurantOrderRetrieveUpdateDestroyView,
    RiderOrderCreateView,
)

urlpatterns = [
    # Restaurants
    path("", RestaurantListCreateView.as_view(), name="restaurant-list-create"),
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
    path(
        "<str:restaurant_id>/orders/<str:order_id>/",
        RestaurantOrderRetrieveUpdateDestroyView.as_view(),
        name="restaurant-order-detail",
    ),
    path(
        "<str:restaurant_id>/riders/<str:rider_id>/deliveries/",
        RiderOrderCreateView.as_view(),
        name="create-rider-order",
    ),
    # Food Categories
    path(
        "<str:restaurant_id>food-categories/", FoodCategoryListCreateView.as_view(), name="food-categories"
    ),
    # Foods (global and restaurant-specific)
    path("foods/", FoodListCreateView.as_view(), name="foods"),
    path(
        "<str:restaurant_id>/foods/",
        RestaurantFoodListCreateView.as_view(),
        name="restaurant-foods",
    ),
    path(
        "<str:restaurant_id>/category-food/",
        RestaurantCategoryFoodCreateView.as_view(),
        name="restaurant-category-food-create",
    ),
    # Extras
    path("extras/", ExtraListCreateView.as_view(), name="extras"),
    path(
        "<str:restaurant_id>/riders/<str:rider_code>/",
        RiderRetrieveUpdateDestroyView.as_view(),
        name="restaurant-rider-detail",
    ),
    path(
        "<str:pk>/",
        RestaurantRetrieveUpdateDestroyView.as_view(),
        name="restaurant-detail",
    ),
]
