from django.urls import path
from .views import (
    # ─── Restaurant & Food ──────────────────────────────
    RestaurantListCreateView,
    RestaurantRetrieveUpdateDestroyView,
    FoodCategoryListCreateView,
    FoodListCreateView,
    ExtraListCreateView,
    RestaurantFoodListCreateView,
    # ─── Rider & Shifts ────────────────────────────────
    RiderListCreateView,
    RiderRetrieveUpdateDestroyView,
    ShiftTypeListCreateView,
    RiderShiftListView,
    StartRiderShiftView,
    EndRiderShiftView,
    toggle_rider_active_status,
    RestaurantRiderListView,  # <-- added import
)

urlpatterns = [
    # ─── RESTAURANTS ───────────────────────────────────
    path("", RestaurantListCreateView.as_view(), name="restaurant-list-create"),
    path(
        "<str:pk>/",
        RestaurantRetrieveUpdateDestroyView.as_view(),
        name="restaurant-detail",
    ),
    path(
        "<str:restaurant_id>/riders/",  # <-- new route
        RestaurantRiderListView.as_view(),
        name="restaurant-riders",
    ),
    # ─── FOOD ──────────────────────────────────────────
    path(
        "food-categories/", FoodCategoryListCreateView.as_view(), name="food-categories"
    ),
    path("foods/", FoodListCreateView.as_view(), name="foods"),
    path("extras/", ExtraListCreateView.as_view(), name="extras"),
    path(
        "<str:restaurant_id>/foods/",
        RestaurantFoodListCreateView.as_view(),
        name="restaurant-foods",
    ),
    # ─── RIDERS ────────────────────────────────────────
    path("riders/", RiderListCreateView.as_view(), name="rider-list-create"),
    path(
        "riders/<int:pk>/",
        RiderRetrieveUpdateDestroyView.as_view(),
        name="rider-detail",
    ),
    # ─── SHIFT TYPES ───────────────────────────────────
    path("shifts/types/", ShiftTypeListCreateView.as_view(), name="shift-types"),
    # ─── RIDER SHIFTS ──────────────────────────────────
    path(
        "riders/<int:rider_id>/shifts/start/",
        StartRiderShiftView.as_view(),
        name="start-rider-shift",
    ),
    path(
        "riders/shifts/<int:pk>/end/",
        EndRiderShiftView.as_view(),
        name="end-rider-shift",
    ),
    path("riders/shifts/", RiderShiftListView.as_view(), name="rider-shifts"),
    path(
        "riders/<int:pk>/toggle-active/",
        toggle_rider_active_status,
        name="rider-toggle-active",
    ),
]
