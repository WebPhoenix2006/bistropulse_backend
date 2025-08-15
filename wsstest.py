import os
import django
import time
import random
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")  # change if needed
django.setup()

ORDER_ID = "BO8604105"
GROUP_NAME = f"order_{ORDER_ID}"
statuses = ["pending", "confirmed", "preparing", "picked up", "on the way", "delivered"]

channel_layer = get_channel_layer()
print(f"Sending live updates for order {ORDER_ID}...")

try:
    while True:
        status = random.choice(statuses)
        timestamp = datetime.utcnow().isoformat()

        async_to_sync(channel_layer.group_send)(
            GROUP_NAME,
            {
                "type": "send_order_update",
                "data": {"status": status, "timestamp": timestamp}
            }
        )

        print(f"Sent update: {status} at {timestamp}")
        time.sleep(5)

except KeyboardInterrupt:
    print("\n Stopped live updates")
