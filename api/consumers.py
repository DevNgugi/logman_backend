import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import paramiko
import time
class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.socket_id = self.scope["url_route"]["kwargs"]["socket_id"]
        self.room_group_name = f"log_{self.socket_id}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        asyncio.create_task(self.send_message_every_second())

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def send_message_every_second(self):
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            log_lines = []

            hostname = '165.90.23.196'
            port = 8044
            username = 'pngugi'
            password = 'C0nn4cT140'
            command = ('tail -f /var/log/county/ug_county.out.log')
            ssh.connect(hostname, port=port, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
            try:

                while not stdout.channel.exit_status_ready():
                    # Non-blocking read using recv_ready and recv
                    if stdout.channel.recv_ready():
                        data = stdout.channel.recv(2048)
                        if data:
                            message = (data.decode().strip()).splitlines()
                            for i, m in enumerate(message):
                                 await self.channel_layer.group_send(
                                self.room_group_name,
                                {"type": "chat.message", "message":  m}
                            )
                            # await self.channel_layer.group_send(
                            #     self.room_group_name,
                            #     {"type": "chat.message", "message":  message}
                            # )
                    
                    await asyncio.sleep(0.1)

            except Exception as e:
                    print(f"An error occurred while reading log: {e}")
                    ssh.close()

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        message = text_data_json["message"]

     
    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))