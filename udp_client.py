import socket
from struct import *

server_ip = '192.168.1.32'
server_port = 1234

message_type = b'DATA'
light = 100.25
temperature = 25.03
humidity = 3250.75
client_name_length = b'6'
client_name = b'Client'

fmt = '4sfffc' + str(int(client_name_length)) + 's'
message = pack(fmt, message_type, light, temperature, humidity, client_name_length, client_name)
print(message)
unpacked = unpack(fmt, message)
print(unpacked)

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.sendto(message, (server_ip, server_port))
