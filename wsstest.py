import os
import django

# ==== Setup Django ====
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# ===== CONFIG =====
order_id = "BO2453938"  # Change to an existing order's ID
data = {
    "event": "manual_test",
    "message": "Hello from Render service 🚀"
}

# ===== SEND =====
channel_layer = get_channel_layer()
async_to_sync(channel_layer.group_send)(
    f"order_{order_id}",
    {
        "type": "send_order_update",
        "data": data
    }
)

print(f"Sent update to order_{order_id} group ✅")
