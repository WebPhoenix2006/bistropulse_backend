from django.urls import path
from .views import (
    OrderListCreateView,
    OrderRetrieveUpdateDestroyView,
    RestaurantOrderRetrieveUpdateDestroyView,
    RiderOrderListView,
    RiderOrderCreateView,
    RiderOrderRetrieveUpdateDestroyView,
)

urlpatterns = [
    # ----------------------------
    # Orders (general)
    # ----------------------------
    path("orders/", OrderListCreateView.as_view(), name="order-list-create"),
    path(
        "orders/<str:order_id>/",
        OrderRetrieveUpdateDestroyView.as_view(),
        name="order-detail",
    ),
    # ----------------------------
    # Orders for a specific restaurant (by restaurant_id and order_id)
    # ----------------------------
    path(
        "restaurants/<str:restaurant_id>/orders/<str:order_id>/",
        RestaurantOrderRetrieveUpdateDestroyView.as_view(),
        name="restaurant-order-detail",
    ),
    # ----------------------------
    # Rider-specific orders
    # ----------------------------
    path(
        "riders/<int:rider_id>/deliveries/",
        RiderOrderListView.as_view(),
        name="rider-deliveries",
    ),
    path(
        "restaurants/<str:restaurant_id>/riders/<str:rider_id>/deliveries/",
        RiderOrderCreateView.as_view(),
        name="rider-order-create",
    ),
    path(
        "riders/<str:rider_id>/deliveries/<int:pk>/",
        RiderOrderRetrieveUpdateDestroyView.as_view(),
        name="rider-order-detail",
    ),
]
