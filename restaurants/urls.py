from django.urls import path
from .views import (
    RestaurantCategoryFoodCreateView,
    RestaurantListCreateView,
    RestaurantRetrieveUpdateDestroyView,
    FoodCategoryListCreateView,
    FoodListCreateView,
    ExtraListCreateView,
    RiderListCreateView,
    RiderRetrieveUpdateDestroyView,
    toggle_rider_active_status,
    ShiftTypeListCreateView,
    RiderShiftListView,
    StartRiderShiftView,
    EndRiderShiftView,
)
from orders.views import (
    OrderListCreateView,
    RestaurantOrderRetrieveUpdateDestroyView,
    RiderOrderCreateView,
)

urlpatterns = [
    # ---------------- RESTAURANTS ----------------
    path("", RestaurantListCreateView.as_view(), name="restaurant-list-create"),
    path(
        "<str:pk>/",
        RestaurantRetrieveUpdateDestroyView.as_view(),
        name="restaurant-detail",
    ),
    # ---------------- RIDERS ----------------
    path(
        "<str:restaurant_id>/riders/",
        RiderListCreateView.as_view(),
        name="restaurant-riders",
    ),
    path(
        "<str:restaurant_id>/riders/<str:rider_code>/",
        RiderRetrieveUpdateDestroyView.as_view(),
        name="restaurant-rider-detail",
    ),
    path(
        "riders/<int:pk>/toggle-active/",
        toggle_rider_active_status,
        name="toggle-rider-active",
    ),
    # ---------------- ORDERS ----------------
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
    # ---------------- FOOD CATEGORIES ----------------
    path(
        "<str:restaurant_id>/food-categories/",
        FoodCategoryListCreateView.as_view(),
        name="food-categories",
    ),
    # ---------------- FOODS ----------------
    path("foods/", FoodListCreateView.as_view(), name="foods"),
    path(
        "<str:restaurant_id>/foods/",
        FoodListCreateView.as_view(),
        name="restaurant-foods",
    ),
    # ---------------- CATEGORY + FOOD IN ONE ----------------
    path(
        "<str:restaurant_id>/category-food/",
        RestaurantCategoryFoodCreateView.as_view(),
        name="restaurant-category-food-create",
    ),
    # ---------------- EXTRAS ----------------
    path("extras/", ExtraListCreateView.as_view(), name="extras"),
    # ---------------- SHIFTS ----------------
    path("shift-types/", ShiftTypeListCreateView.as_view(), name="shift-types"),
    path("rider-shifts/", RiderShiftListView.as_view(), name="rider-shifts"),
    path(
        "rider/<int:rider_id>/start-shift/",
        StartRiderShiftView.as_view(),
        name="start-rider-shift",
    ),
    path(
        "rider-shift/<int:pk>/end/", EndRiderShiftView.as_view(), name="end-rider-shift"
    ),
]
