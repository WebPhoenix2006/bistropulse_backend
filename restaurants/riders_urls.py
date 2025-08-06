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
    path("<str:rider_code>/", RiderRetrieveUpdateDestroyView.as_view(), name="rider-detail"),

    # Rider's assigned orders (aka deliveries)
    path("<str:rider_code>/deliveries/", RiderOrderListView.as_view(), name="rider-deliveries"),

    # Other stuff
    path("<str:rider_code>/toggle-active/", toggle_rider_active_status, name="rider-toggle-active"),
    path("<str:rider_code>/shifts/start/", StartRiderShiftView.as_view(), name="start-rider-shift"),
    path("shifts/<int:pk>/end/", EndRiderShiftView.as_view(), name="end-rider-shift"),
    path("shifts/", RiderShiftListView.as_view(), name="rider-shifts"),
]
