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
    ShiftTypeListCreateView,
    RiderShiftListView,
    StartRiderShiftView,
    EndRiderShiftView,
    toggle_rider_active_status,
)

urlpatterns = [
    # Restaurants
    path("", RestaurantListCreateView.as_view(), name="restaurant-list-create"),
    path(
        "<str:pk>/",
        RestaurantRetrieveUpdateDestroyView.as_view(),
        name="restaurant-detail",
    ),
    # Riders (global and by restaurant)
    path("riders/", RiderListCreateView.as_view(), name="rider-list-create"),
    path(
        "restaurants/<int:restaurant_id>/riders/",
        RiderListCreateView.as_view(),
        name="restaurant-riders",
    ),
    path(
        "riders/<int:pk>/",
        RiderRetrieveUpdateDestroyView.as_view(),
        name="rider-detail",
    ),
    path(
        "riders/<int:pk>/toggle-active/",
        toggle_rider_active_status,
        name="rider-toggle-active",
    ),
    # Foods
    path(
        "food-categories/", FoodCategoryListCreateView.as_view(), name="food-categories"
    ),
    path("foods/", FoodListCreateView.as_view(), name="foods"),
    path(
        "<str:restaurant_id>/foods/",
        RestaurantFoodListCreateView.as_view(),
        name="restaurant-foods",
    ),
    # Extras
    path("extras/", ExtraListCreateView.as_view(), name="extras"),
    # Shifts
    path("shifts/types/", ShiftTypeListCreateView.as_view(), name="shift-types"),
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
]
