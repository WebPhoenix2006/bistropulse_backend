from django.urls import path
from .views import (
    RiderListCreateView,
    RiderRetrieveUpdateDestroyView,
    toggle_rider_active_status,
    StartRiderShiftView,
    EndRiderShiftView,
    RiderShiftListView,
)
from orders.views import RiderOrderListView

urlpatterns = [
    path("", RiderListCreateView.as_view(), name="rider-list-create"),
    path("<int:pk>/", RiderRetrieveUpdateDestroyView.as_view(), name="rider-detail"),

    # Rider's assigned orders (aka deliveries)
    path("<int:rider_id>/deliveries/", RiderOrderListView.as_view(), name="rider-deliveries"),

    # Other stuff
    path("<int:pk>/toggle-active/", toggle_rider_active_status, name="rider-toggle-active"),
    path("<int:rider_id>/shifts/start/", StartRiderShiftView.as_view(), name="start-rider-shift"),
    path("shifts/<int:pk>/end/", EndRiderShiftView.as_view(), name="end-rider-shift"),
    path("shifts/", RiderShiftListView.as_view(), name="rider-shifts"),
]
