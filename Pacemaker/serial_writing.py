# #########################  Serial use #######################################

# *************************  endianness  **************************************
# endian = little
# defaults to @ which uses native endian
#   native of windows OS is little
#   FRDM board set to little endian in model config
# < will be first char in format string to use little endian

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


# *************************  string format  ***********************************
#   DCM -> pacemaker:
#       used to update one of the param in the pacemaker or request egram info
#       [   x   ]   [     x     ]   [  xxxx  ]   [  x  ]
#       startByte   paramSelector   paramValue   endByte
#         uint8         uint8         single      uint8
#       startByte = 34 -> update param
#           see below for paramSelector legend
#       startByte = 85 -> request egram info
#           middle five bytes padding
#       endByte = 42
#       format string -> BBfB

#   pacemaker -> DCM:
#       used to send egram info to DCM or tell DCM whether message received or not
#       [   x   ]   [ xxxx ]   [  xxxx ]   [  x  ]   [  xxxx  ]   [   x  ]   [  x  ]
#       startByte     time     atrSignal   atrPace   ventSignal   ventPace   endByte
#         uint8      single      single     uint8      single       uint8     uint8
#       startByte = 22 -> sent egram info
#       startByte = 66 -> received message successfully
#           middle 14 bytes padding
#       startByte = 101 -> faulty message
#           middle 14 bytes padding
#       endByte = 42
#       format string -> BffBfBB

# Note: when receiving string, check with startByte and endByte
#       if not valid:
#           DCM receiver -> have DCM ignore that message from pacemaker
#           pacemaker receiver -> send faulty message indicator

# Note: explicitly typecast variables into desired type before sending and after receiving


# **************************  paramSelector  **********************************
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
#   17 -> sensed (1 = atrium, 2 = ventricle, 3 = both)
#   18 -> response (1 = no response, 2 = inhibit, 3 = DDD)
#   19 -> paced (1 = atrium, 2 = ventricle, 3 = both)


# ************************** operating modes **********************************
# The following parameters must be set to switch to a new mode

# AOO -> sensed = 1 or 2
#        response = 1
#        paced = 1
#        rateAdaptiveOn = 0
# VOO -> sensed = 1 or 2
#        response = 1
#        paced = 2
#        rateAdaptiveOn = 0
# AAI -> sensed = 1
#        response = 2
#        paced = 1
#        rateAdaptiveOn = 0
# VVI -> sensed = 2
#        response = 2
#        paced = 2
#        rateAdaptiveOn = 0
# DOO -> sensed = 3
#        response = 1
#        paced = 1
#        rateAdaptiveOn = 0

# if rate adaptive (ex. AOOR), set rateAdaptiveOn = 1



# ************************  Initialize port  **********************************
import serial
from struct import *
# COM port should be the one that shows as J-Link under device manager
# should be called at beginning of program; probably at login
ser=serial.Serial("COM4",115200, timeout = 2)

# ****************************  Use  ******************************************
# convert data into bytearray using pack(<format string>, <value1>, ..., <valueN> )
# see DCM -> pacemaker above for serial packet format
# use one of the two below:

# for changing parameter
messageS = pack('<BBfB', 34, 18, 2, 42)
# for getting egram data
# messageS = pack('<BBfB', 85, 0, 0, 42)

# write to serial
ser.write(messageS)

# read response from pacemaker
messageR_Raw = ser.read(16)

# check if response valid
try:
    messageR = unpack('<BffBfBB', messageR_Raw);
except:
    # no response received
    # should signify the pacemaker being disconnected
    print("connection lost")
    messageR = [0, 0, 0, 0, 0, 0, 0]

# response from pacemaker signifies that previous message was not in the proper format
# probably due to bytes getting dropped
if (messageR[0] == 101):
    # should prompt the user to redo the action
    # this case will probably never occur so don't spend too much time on this
    print("message not properly received, please try again")

# debugging purposes
print(messageR)

# **************************  closure  ****************************************
# should close the port at end of program if possible
# will automatically close if program closes
ser.close()

# ***************************  notes  *****************************************
# - for use, everything in 'use' section should be included for any serial communication
# - when displaying egram, should continuously send request for egram within DCM
#       - pacemaker will not send info unless request message received




# *****************  debugging purposes  ********************************
# import serial
# from struct import *
# ser=serial.Serial("COM4",115200, timeout = 2)
# #ser.port='COM4'
# # print("name: ", ser.name)
# # print("is open: ", ser.is_open)
# # print("serial: ", ser)

# messageS = pack('<BBfB', 34, 16, 300, 42)
#
# # print("messageS:     ", messageS)
# # print("num bytes: ", ser.write(messageS) )
#
# messageR_Raw = ser.read(16)
# try:
#     messageR = unpack('<BffBfBB', messageR_Raw);
# except:
#     print("connection lost")
#     messageR = [0, 0, 0, 0, 0, 0, 0]
# if (messageR[0] == 101):
#     print("message not properly received, please try again")

# # messageR = unpack('<BffBfBB', messageR_Raw);
# # print("messageR_Raw: ", messageR_Raw)
# print("messageR:     ", messageR);
# # for m in messageR:
# #     print(m, end=' ')
