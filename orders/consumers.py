# orders/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer

class OrderTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f"order_{self.order_id}"

        # Join group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Client sends message (optional)
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"Received from client: {data}")

    # Server sends message to client
    async def send_order_update(self, event):
        await self.send(text_data=json.dumps(event['data']))


class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            "message": "WebSocket connected successfully!"
        }))

    def disconnect(self, close_code):
        print("Disconnected with code:", close_code)

    def receive(self, text_data):
        print("Received from frontend:", text_data)
        self.send(text_data=json.dumps({
            "echo": text_data
        }))
        
class OrderTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f"order_{self.order_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        print("Client sent:", text_data)

    async def send_order_update(self, event):
        await self.send(text_data=json.dumps(event['data']))
