# orders/routing.py
from django.urls import re_path, path
from . import consumers  # OrderTrackingConsumer
from chat import consumers as chat_consumers  # Your TestConsumer

websocket_urlpatterns = [
    # Main order tracking WebSocket
    re_path(r'ws/orders/(?P<order_id>\w+)/$', consumers.OrderTrackingConsumer.as_asgi()),

    # Test WebSocket route (from your old backend.routing)
    path("ws/test/", consumers.TestConsumer.as_asgi()),  # Temporary test route
]
