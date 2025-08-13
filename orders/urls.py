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
    # GET all orders & POST new ones (admin/manager only)
    path("orders/", OrderListCreateView.as_view(), name="order-list-create"),
    # GET, PUT, PATCH, DELETE a specific order (admin/manager/rider)
    path(
        "orders/<str:order_id>/",
        OrderRetrieveUpdateDestroyView.as_view(),
        name="order-detail",
    ),
    # GET/PUT/PATCH/DELETE a specific order by order_id for a restaurant
    path(
        "restaurants/<str:restaurant_id>/orders/<str:order_id>/",
        RestaurantOrderRetrieveUpdateDestroyView.as_view(),
        name="restaurant-order-detail",
    ),
    # GET all orders assigned to a specific rider (admin/manager)
    path(
        "riders/<int:rider_id>/deliveries/",
        RiderOrderListView.as_view(),
        name="rider-deliveries",
    ),
    # POST new order for a specific rider (manager only)
    path(
        "restaurants/<str:restaurant_id>/riders/<str:rider_id>/deliveries/",
        RiderOrderCreateView.as_view(),
        name="rider-order-create",
    ),
    # GET, PUT, PATCH, DELETE a specific order for a specific rider (admin/manager)
    path(
        "riders/<str:rider_id>/deliveries/<int:pk>/",
        RiderOrderRetrieveUpdateDestroyView.as_view(),
        name="rider-order-detail",
    ),
]
