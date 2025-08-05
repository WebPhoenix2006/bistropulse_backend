from django.urls import path
from .views import OrderListCreateView, RiderOrderListView

urlpatterns = [
    # GET all orders & POST new ones (admin/restaurant only)
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),

    # GET all orders assigned to a specific rider (admin view)
    # path('riders/<int:rider_id>/deliveries/', RiderOrderListView.as_view(), name='rider-deliveries'),
]
