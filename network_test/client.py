import socket
from shared import *

client = socket.create_connection((host, port))  # Takes some time to set up. Checks both IPv4 and IPv6

while (message := input("message: ")) != "!q":
    client.send(message.encode())

client.close()