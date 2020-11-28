import serial
from struct import *
ser=serial.Serial("COM4",115200, timeout = 2)
#ser.port='COM4'
# print("name: ", ser.name)
# print("is open: ", ser.is_open)
# print("serial: ", ser)

# endian = little
# defaults to @ which uses native endian
#   native of windows OS is little
#   FRDM board set to little endian in model config
# < will be first char in format string

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


# string format:
#   DCM -> pacemaker:
#       used to update one of the param in the pacemaker or start sending egram info
#       [   x   ]   [     x     ]   [  xxxx  ]   [  x  ]
#       startByte   paramSelector   paramValue   endByte
#         uint8         uint8         single      uint8
#       startByte = 34 -> update param
#       startByte = 85 -> start to send egram info
#           middle four bytes padding
#       endByte = 42
#       format string -> BBfB

#   pacemaker -> DCM:
#       used to send egram info to DCM or tell DCM whether message received or not
#       [   x   ]   [ xxxx ]   [  xxxx ]   [  x  ]   [  xxxx  ]   [   x  ]   [  x  ]
#       startByte     time     atrSignal   atrPace   ventSignal   ventPace   endByte
#         uint8      single      single     uint8      single       uint8     uint8
#       startByte = 22 -> send egram info
#       startByte = 66 -> received message successfully
#           middle 10 bytes padding
#       startByte = 101 -> request DCM to resend previous message
#           middle 10 bytes padding
#       endByte = 42
#       format string -> BffBfBB

# Note: when receiving string, check with startByte and endByte
#       if not valid:
#           DCM receiver -> have DCM ignore that message from pacemaker
#           pacemaker receiver -> send request signal to DCM to resend previous message

# Note: explicitly typecast variables into desired type before sending and after receiving


# paramSelector:
#   general
#   1 -> LRL
#   2 -> atrium amp
#   3 -> atrium pulse width
#   4 -> ventricle amp
#   5 -> ventricle pulse width

#   inhibit
#   6 -> hysteresis interval
#   7 -> RP
#   8 -> atrium sensitivity
#   9 -> ventricle sensitivity

#   rate adaptive
#   10 -> MSR
#   11 -> activity threshold
#   12 -> response factor
#   13 -> reaction time
#   14 -> recovery time
#   15 -> rate adaptive on

#   dual pacing
#   16 -> AV delay

#   operating modes
#   17 -> sensed
#   18 -> response
#   19 -> paced



messageS = pack('<BBfB', 34, 16, 300, 42)
print("messageS:     ", messageS)
print("num bytes: ", ser.write(messageS) )

# messageR_Raw = ser.read(10)
# print("messageR_Raw: ", messageR_Raw)
# messageR = unpack('@HHfH', messageR_Raw);
# print("messageR:     ", messageR);
# for m in messageR:
#     print(m, end=' ')

ser.close()
#print(ser.is_open)
