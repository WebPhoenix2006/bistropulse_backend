# orders/routing.py
from django.urls import re_path, path
from . import consumers  # OrderTrackingConsumer
from chat import consumers as chat_consumers  # Your TestConsumer

websocket_urlpatterns = [
    re_path(r"ws/orders/(?P<order_id>\d+)/$", consumers.OrderTrackingConsumer.as_asgi()),
    re_path(r"ws/restaurant/(?P<restaurant_id>\d+)/$", consumers.RestaurantOrdersConsumer.as_asgi()),
]
