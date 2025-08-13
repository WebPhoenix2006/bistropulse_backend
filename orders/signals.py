# orders/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Order
from .serilalizers import OrderSerializer

@receiver(post_save, sender=Order)
def order_saved(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()

    # 1. Broadcast to order-specific group
    async_to_sync(channel_layer.group_send)(
        f"order_{instance.id}",
        {
            "type": "send_order_update",
            "data": {
                "event": "created" if created else "updated",
                **OrderSerializer(instance).data
            }
        }
    )

    # 2. Broadcast to restaurant dashboard group
    async_to_sync(channel_layer.group_send)(
        f"restaurant_{instance.restaurant.id}",
        {
            "type": "send_order_update",
            "data": {
                "event": "created" if created else "updated",
                **OrderSerializer(instance).data
            }
        }
    )

@receiver(post_delete, sender=Order)
def order_deleted(sender, instance, **kwargs):
    channel_layer = get_channel_layer()

    # Order group
    async_to_sync(channel_layer.group_send)(
        f"order_{instance.id}",
        {
            "type": "send_order_update",
            "data": {
                "event": "deleted",
                "order_id": instance.id
            }
        }
    )

    # Restaurant group
    async_to_sync(channel_layer.group_send)(
        f"restaurant_{instance.restaurant.id}",
        {
            "type": "send_order_update",
            "data": {
                "event": "deleted",
                "order_id": instance.id
            }
        }
    )
