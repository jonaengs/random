import socket
from shared import *

server = socket.create_server((host, port))
server.listen(1)
connection, address = server.accept()
print(connection, address)

while True:
    message = connection.recv(msg_size)  # message max length?
    print("\n" + str(message))  # message is bytes object
    if not message:
        break
