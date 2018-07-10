import socket
import os.path
import csv
import yaml
import numpy as np
from struct import *
from collections import namedtuple
from datetime import datetime


def decode_data(raw_data, time):
    fmt_1 = 'B'
    num_lights = unpack(fmt_1, raw_data[:1])[0]
    fmt_2 = 'f'
    light_array = np.zeros(num_lights)
    for i in range(num_lights):
        light_array[i] = unpack(fmt_2, raw_data[i*4+1:i*4+5])[0]
    fmt_3 = 'ffB'
    data = Sensors._make(('DATA',light_array) + unpack(fmt_3, raw_data[num_lights*4+1:num_lights*4+10]) + (b'',time))
    
    l = int(data.client_name_length)
    fmt_4 = '<' + str(l) + 's'
    client_name = (unpack(fmt_4, raw_data[num_lights*4+10:])[0]).decode('utf-8')
    data = data._replace(client_name=client_name)
    return data


def write_csv(data):
    file_name = str(config['data_dir']) + str(data.client_name) + '.csv'
    if os.path.isfile(file_name):
        with open(file_name, 'a') as file:
            file_writer = csv.writer(file, delimiter=',')
            file_writer.writerow(data)
    else:
        with open(file_name, 'w') as file:
            file_writer = csv.writer(file, delimiter=',')
            file_writer.writerow(Sensors._fields)
            file_writer.writerow(data)



with open('config.yml', 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

server_ip = '0.0.0.0'
server_port = config['UDP_port']

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((server_ip, server_port))

Sensors = namedtuple('Sensors', ['message_type',
                                 'light',
                                 'temperature',
                                 'humidity',
                                 'client_name_length',
                                 'client_name','time'])

while True:
    raw_data, addr = serverSock.recvfrom(500)
    print(raw_data)
    st = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    print(st)
    
    msgtype_fmt = '4s'
    msgtype = (unpack(msgtype_fmt, raw_data[:4])[0]).decode('utf-8')
    if msgtype == 'DATA':
        data = decode_data(raw_data[4:], st)
        print(data)
        write_csv(data)
    else:
        print('%s message type unknown' %msgtype)

