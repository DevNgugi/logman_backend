import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import paramiko
import time
from asgiref.sync import sync_to_async 
from api.utils.crypt import cipher_suite

from api.models import Connection, Source
class LogConsumer(AsyncWebsocketConsumer):
    task = None
    data = None
    async def connect(self):
        self.socket_id = self.scope["url_route"]["kwargs"]["socket_id"]
        self.room_group_name = f"log_{self.socket_id}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        print('disconnecting')
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        if self.task:
            self.task.cancel()
            self.data = None
            try:
                await self.task
                print(self.task)
            except asyncio.CancelledError:
                print("Task was cancelled")

    async def send_message_every_second(self, source):
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            log_lines = []

            hostname = source.connection.ssh_host
            port = source.connection.ssh_port
            username = source.connection.ssh_user
            password = source.connection.ssh_pass
            command = (f'tail -f {source.file_path}')

            ssh.connect(hostname, port=port, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
            try:

                while not stdout.channel.exit_status_ready():
                    # Non-blocking read using recv_ready and recv
                    if stdout.channel.recv_ready():
                        
                        if not self.data:
                            self.data = stdout.channel.recv(2048)
                            message = (self.data.decode().strip()).splitlines()
                            for i, m in enumerate(message):
                                 await self.channel_layer.group_send(
                                self.room_group_name,
                                {"type": "chat.message", "message":  m}
                            )
                        else:
                            self.data = None        
                    
                    await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                print("was cancelled. Performing cleanup.")

            except Exception as e:
                    print(f"An error occurred while reading log: {e}")
                    ssh.close() 

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        source_id = text_data_json["source"]
        # get object with specifi id
        source = await self.get_source_object(source_id)
        # decode password
        print(vars(source.connection))

        source.connection.ssh_pass = await self.decode_password(source.connection.ssh_pass)
        # send logs
        self.data = None
        self.task = asyncio.create_task(self.send_message_every_second(source))




    async def get_source_object(self, source_id):
        try:
            # Asynchronous query to fetch Source object by id
            # connection = await sync_to_async (Source.objects.get)(id=source_id)
            source = await sync_to_async(Source.objects.select_related('connection').get)(id=source_id)
            # decode password
            return source
        
        except Connection.DoesNotExist:
            return None
    async def decode_password(self, encoded_pass):
        print('*************',encoded_pass)
        try:
            plain = (cipher_suite().decrypt(encoded_pass))
            return plain.decode()
        except Exception as e:
             pass
     
    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))