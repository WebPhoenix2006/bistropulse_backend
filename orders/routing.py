from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Orders WebSocket (alphanumeric order IDs)
    re_path(
        r"ws/orders/(?P<order_id>[\w\d]+)/$", consumers.OrderTrackingConsumer.as_asgi()
    ),
    # Restaurant WebSocket (alphanumeric restaurant IDs)
    re_path(
        r"ws/restaurant/(?P<restaurant_id>[\w\d]+)/$",
        consumers.RestaurantOrdersConsumer.as_asgi(),
    ),
]
