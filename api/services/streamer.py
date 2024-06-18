import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import paramiko

async def send_message_every_second():
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
            while True:
                if stdout.channel.recv_ready():
                    line = stdout.readline()
                    if line:
                        message = line.strip()
                        print(message)
               
                await asyncio.sleep(0.1)

        except Exception as e:
                print(f"An error occurred while reading log: {e}")
                ssh.close()

if __name__ =='__main__':
     asyncio.run(send_message_every_second())