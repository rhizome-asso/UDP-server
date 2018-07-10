import socket
from struct import *

server_ip = '192.168.1.32'
server_port = 1234

message = b'DATA\x03\xf3\x03\x96D\xf3\x03\xafD\xdc\xb6\xc4Dd\xd4\xf5AP\xf6\x8bC\tsunflower'

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.sendto(message, (server_ip, server_port))
