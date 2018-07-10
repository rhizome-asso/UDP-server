import socket
import os.path
import csv
import yaml
import numpy as np
from struct import *
from collections import namedtuple
from datetime import datetime


def decode_data(raw_data, time):
    # Decode temperature, humidity, number of light sensors, and client name length
    fmt_1 = 'ffBB'
    data = Sensors._make(('DATA',) + unpack(fmt_1, raw_data[:10]) + ([],b'',time))
    print(data)
    
    # Decode the values of the light sensors
    n = data.num_lights
    light_array = np.zeros(n)
    for i in range(n):
        print(raw_data[10:14])
        light_array[i] = unpack('f', raw_data[10+i*4:10+i*4+4])[0]
    data = data._replace(lights = light_array)
    
    # Decode the client name
    l = data.client_name_length
    fmt_2 = '<' + str(l) + 's'
    client_name = (unpack(fmt_2, raw_data[n*4+10:])[0]).decode('utf-8')
    data = data._replace(client_name=client_name)
    return data


def write_csv(data):
    # File directory as specified in the configuration file
    file_name = str(config['data_dir']) + str(data.client_name) + '.csv'
    # If the file exists, append the data
    if os.path.isfile(file_name):
        with open(file_name, 'a') as file:
            file_writer = csv.writer(file, delimiter=',')
            file_writer.writerow(data)
    # If the file doesn't exist, generate it with the data
    else:
        with open(file_name, 'w') as file:
            file_writer = csv.writer(file, delimiter=',')
            file_writer.writerow(Sensors._fields)
            file_writer.writerow(data)


# Read the data from the configuration file in yaml format
with open('config.yml', 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

server_ip = '0.0.0.0'
server_port = config['UDP_port']

# Start the server
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((server_ip, server_port))

# Initialization of the Sensors object to store all data
Sensors = namedtuple('Sensors', ['message_type',
                                 'temperature',
                                 'humidity',
                                 'num_lights',
                                 'client_name_length',
                                 'lights',
                                 'client_name','time'])

# Receive messages on the server
while True:
    raw_data, addr = serverSock.recvfrom(500)
    # Save the time the message was received
    st = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    
    # Decode the message type
    msgtype_fmt = '4s'
    msgtype = (unpack(msgtype_fmt, raw_data[:4])[0]).decode('utf-8')
    if msgtype == 'DATA':
        # Decode the message of type DATA
        data = decode_data(raw_data[4:], st)
        print(data)
        write_csv(data)
    else:
        print('%s message type unknown' %msgtype)

