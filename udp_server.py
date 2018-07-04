import socket
from struct import *
from collections import namedtuple

server_ip = '192.168.1.32'
server_port = 1234

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((server_ip, server_port))

Sensors = namedtuple('Sensors', 'message_type light temperature humidity client_name_length client_name')

while True:
    raw_data, addr = serverSock.recvfrom(500)
    print(raw_data)
    
    fmt_1 = '4sfffB'
    data = Sensors._make(unpack(fmt_1, raw_data[:17]) + (b'',))
    
    l = int(data.client_name_length)
    fmt_2 = '<' + str(l) + 's'
    client_name = unpack(fmt_2, raw_data[17:])[0]
    data = data._replace(client_name=client_name)
    print(data)
    