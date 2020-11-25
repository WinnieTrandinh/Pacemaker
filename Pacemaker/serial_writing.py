import serial
from struct import *
ser=serial.Serial("COM4",115200, timeout = 2)
#ser.port='COM4'
# print("name: ", ser.name)
# print("is open: ", ser.is_open)
# print("serial: ", ser)

# first byte = 22
# second byte = 34 for echo, 85 for set param

# endian = little
# defaults to @ which uses native endian
#   native of windows OS is little
#   FRDM board set to little endian in model config
# @ will be first char in format string

# byte format string
# x = pad byte (no value)
# c = char
# b = int8
# B = uint8
# ? = boolean
# h = int16
# H = uint16
# i = int32
# I = uint32
# f = single (float) - 32 bits
# d = double (float) - 64 bits
# note: value in brackets represent python's representation
# format = 'xxxxxxxx' where x can be any of the above format chars


messageS = pack('@HHfH', 152, 2, 3.55, 1)
print("messageS:     ", messageS)
print("num bytes: ", ser.write(messageS) )
#print("num bytes: ", ser.write([22, 85, 0,1,1,1,1,1,1,55]))

messageR_Raw = ser.read(10)
print("messageR_Raw: ", messageR_Raw)
messageR = unpack('@HHfH', messageR_Raw);
print("messageR:     ", messageR);
#print("unpacked: ", unpack('message', b'\x01\x02\x03\x04\x05\x06\x07\x08\t\n') )
# for m in messageR:
#     print(m, end=' ')

ser.close()
#print(ser.is_open)
