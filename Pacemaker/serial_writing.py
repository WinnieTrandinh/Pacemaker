import serial
ser=serial.Serial("COM4",115200)
#ser.port='COM4'
print(ser.name)
print(ser.is_open)
print(ser)
ser.write([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,])





ser.close()
print(ser.is_open)