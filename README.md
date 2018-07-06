# UDP-server

A simple UDP based log server for sensor devices. The server listens on a predefined port for incoming messages and stores them in files.

## UDP message format

A simple, fixed-length message format is expected. Fields should appear in the order listed below and occupy a predefined length in number of bytes. The `client name` field is a character string, which is terminated by NULL (\0) and with a length given by the `client name length` field.

* `message type`  
  type: `char[]`  
  size: 4 Bytes  
  A message type name. For now we only support `DATA` messages.
* `light`  
  type: `float`  
  size: 4 Bytes  
  A floating point value representing light intensity as measured by a photodiode (or other photo sensor) and interpreted by the client.
* `temperature`  
  type: `float`  
  size: 4 Bytes  
  A floating point value representing temperature as measured by a thermistor (or other temperature sensor) and interpreted by the client.
* `humidity`  
  type: `float`  
  size: 4 Bytes  
  A floating point value representing humidity or soil moisture as measured by a sensor and interpreted by the client.  
* `client name length`  
  type: `char`  
  size: 1 Byte  
  Defines the length of the client name character string
* `client name`  
  type: `char[]`  
  size: variable  
  The name of the client sending the message, is at most 255 characters long. The `client name length` field defines its length.

The client name is set to be the last field to allow for easy data unpacking.

## Data processing

When the message buffer is read from the socket, the first 4 bytes are unpacked, then the type field is checked and the appropriate processing method is called. The next 13 bytes are unpacked into the respective fields and Python types. Then the character string representing the name is read up to the advertised name length. The message receipt time is recorded.

Finally, the collected data is written in CSV string format into a file with name being the client name. If the file does not exist yet, it is created and the CSV header row is first written. Each received and decoded message is appended as an additional CSV row into the file.
