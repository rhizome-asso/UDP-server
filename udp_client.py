import socket
from struct import *

server_ip = '192.168.1.32'
server_port = 1234

message = b'DATAd\xd4\xf5AP\xf6\x8bC\x03\t\xdc\xb6\xc4D\xdc\xb6\xc4D\xdc\xb6\xc4Dsunflower'

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.sendto(message, (server_ip, server_port))
