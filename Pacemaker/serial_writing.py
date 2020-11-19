import serial
from struct import *
ser=serial.Serial("COM4",115200, timeout = 10)
#ser.port='COM4'
print("name: ", ser.name)
print("is open: ", ser.is_open)
print("serial: ", ser)

# first byte = 22
# second byte = 34 for echo, 85 for set param
print("num bytes: ", ser.write([22, 85, 0,1,1,1,1,1,1,1]))

message = ser.read(10);
print("message: ", message);
#print("unpacked: ", unpack('message', b'\x01\x02\x03\x04\x05\x06\x07\x08\t\n') )



ser.close()
print(ser.is_open)
