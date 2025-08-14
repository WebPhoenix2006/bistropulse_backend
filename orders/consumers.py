import json
from channels.generic.websocket import AsyncWebsocketConsumer


class OrderTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope["url_route"]["kwargs"]["order_id"]
        self.room_group_name = f"order_{self.order_id}"

        # Join order group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print(f"Client connected to order {self.order_id}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print(f"Client disconnected from order {self.order_id}")

    # Messages from frontend
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"Received from client for order {self.order_id}:", data)

        # Optional: echo ping/test messages back immediately
        if data.get("type") in ["ping", "test"]:
            await self.send(text_data=json.dumps({"echo": data}))

    # Messages from backend
    async def send_order_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))


class RestaurantOrdersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.restaurant_id = self.scope["url_route"]["kwargs"]["restaurant_id"]
        self.room_group_name = f"restaurant_{self.restaurant_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print(f"Client connected to restaurant {self.restaurant_id}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print(f"Client disconnected from restaurant {self.restaurant_id}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"Received from client for restaurant {self.restaurant_id}:", data)

        if data.get("type") in ["ping", "test"]:
            await self.send(text_data=json.dumps({"echo": data}))

    async def send_order_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))
