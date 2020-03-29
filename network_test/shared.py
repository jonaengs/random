import socket


def get_local_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("192.168.1.1", 8000))  # router address. Must connect to external device or IP will be set to 'localhost'
    local_ip = s.getsockname()[0]  # getsockname() returns (<socket_ip>, <socket_port>)
    return local_ip


host = get_local_ip_address()
port = 8000
msg_size = 2048  # maximum packet size in bits? Must be a power of 2
