# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Connected to test WebSocket!"}))

    async def disconnect(self, close_code):
        print("Disconnected test socket")

    async def receive(self, text_data):
        await self.send(text_data=json.dumps({"echo": text_data}))
