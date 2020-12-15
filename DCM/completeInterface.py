#!/usr/bin/env python
# coding: utf-8

# In[48]:

# LIBRARIES
import tkinter as tk
#import random
import matplotlib.pyplot as plt
#import numpy as np
from Serial import *
#from itertools import count
from matplotlib.animation import FuncAnimation
#import time

class User:
    def __init__(self, name, password, AOO, VOO, LRL, AAI, VVI, hys, RP, ROO, DOOR, DDDR):
        # FIELDS
        self.name = name
        self.password = password
        self.AOO = AOO
        self.VOO = VOO
        self.LRL = LRL
        self.AAI = AAI
        self.VVI = VVI
        self.hys = hys
        self.ROO = ROO
        self.DOOR = DOOR
        self.DDDR = DDDR
        self.RP = RP

# GLOBAL VARIABLES
global user_id
user_id = 0

global user_list
user_list = []

global pacemakerConnected
pacemakerConnected = True

global run
run = True

global close
serial = Serial("COM4") #serial

pacemakerNumber = [1234,5453,6789,5809,2354,1765,3490,5692,3745,6890]

# [atrium amp, atrium pulse width
defaultAOO = [[5.0], [10]]
# [ventricle amp, ventricle pulse width]
defaultVOO = [[5.0], [10]]
# [LRL]
defaultLRL = [[1000]]
# [hysteresis interval]
defaultHys = [[500]]
# [atrium sensitivity]
defaultAAI = [[3.5]]
# [ventricle sensitivity]
defaultVVI = [[3.5]]
# [MSR, activity threshold, reaction time, response factor, recovery factor]
defaultROO = [[500], [0.1], [5], [16], [8]]
# [AV delay]
defaultDOOR = [[100]]
# [PVARP]
defaultDDDR = [[300]]
# [RP]
defaultRP = [[400]]

def readFile(fileName):
    with open(fileName, "r") as i:
        data = i.read()

    out_list = []
    out = []
    elem = []
    num = ''

    for i in range(0, len(data)):
        try:
            if (data[i] == "." or isinstance(int(data[i]), int)):
                num += data[i]
                if (data[i+1] == ',' or data[i+1] == ']'):
                    try:
                        elem.append(int(num))
                    except ValueError:
                        elem.append(float(num))
                    num = ''
        except ValueError:
            try:
                if (data[i] == "]"):
                    if (len(elem) == 0):
                        out_list.append(list(out))
                        out.clear()
                    else:
                        out.append(list(elem))
                        elem.clear()
            except:
                pass

    return(out_list)

def signupWriteFile(fileName, defaultList):
    with open(fileName, "a") as file:
        file.write(str(defaultList) + "\n")

def changeParamWriteFile(fileName, modList):
    with open(fileName, "w") as file:
        for i in modList:
            file.write(str(i) + "\n")

# *****************************************  new classes ***************************************************
# parent class of all gComp (graphical component) classes, excluding the label
# also happens to be a button
class Button(tk.Tk):
    def __init__(self, window, textLabel, function):
        self.gComp = tk.Button(window, text=textLabel, font=("Comic Sans MS", 15), command=function)

    def place(self, xPos, yPos, width, height):
        self.gComp.place(x=xPos, y=yPos, width=width, height=height)

# label class
class Label(tk.Tk):
    def __init__(self, canvas, textLabel):
        self.gComp = tk.Label(canvas, text=textLabel, bg='#FFB6C1', font=('Comic Sans MS', 30))

    def place(self, xPos, yPos, width):
        self.gComp.place(x=xPos, y=yPos, width=width)
        self.gComp.bind('<Button-1>', self.hide)

    # call this to hide a label
    # to reshow a label, call place again
    def hide(self):
        self.gComp.place_forget()

# entry component inherits from Button
class Entry(Button):
    # different constructor needed though
    def __init__(self, canvas):
        self.gComp = tk.Entry(canvas, font=("Comic Sans MS", 20));
    # kind of stupid to have a wrapper function with the same name,
    # but I'm too lazy to change all the get() calls in the code
    # Probably better to do that though, and change this function
    # into getEntry() or something.
    def get(self):
        return self.gComp.get()

# same as above but inputs show as *
class PasswordEntry(Entry):
    def __init__(self, canvas):
        self.gComp = tk.Entry(canvas, font=("Comic Sans MS", 20), show="*")

# class for window creation
class Window(tk.Tk):
    def __init__(self, canvas, x, y, height, width, title):
        self.window = tk.Toplevel(canvas, height=height, width=width, bg='#FFB6C1')
        self.setPos(x, y)
        self.setTitle(title)
        self.title = title
    # this sets the position of the window when created
    def setPos(self, x, y):
        self.window.geometry("+%d+%d" % (x, y))

    def setTitle(self, title):
        self.window.title(title)

    def getTitle(self):
        return self.title
    # returns the actual window object so that it can be used as a canvas for gComponents
    def getWindow(self):
        return self.window

# ****************************************************************************************************
# GLOBAL VARIABLES FOR WINDOWS
root = tk.Tk()
HEIGHT = 800
WIDTH = 800
canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
canvas.pack()

# SERIAL FUNCTIONS
def updateParam(selec, val):
    # serial
    global pacemakerConnected
    try:
        response = serial.updateParam(selec, val)
        if (response[0] == 0):
            pacemakerConnected = False
        else:
            pacemakerConnected = True
    except:
        pacemakerConnected = False
    return pacemakerConnected


# SIGN UP FUNCTIONS
def signup():
    if(len(user_list) < 10):
        signupWindow = tk.Toplevel(root, height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
        signupWindow.resizable(0,0)
        signupWindow.title("Sign up")

        nameLabel2 = tk.Label(signupWindow,text="Enter Name:", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=150,y=200)

        nameEntry2 = tk.Entry(signupWindow, font=("Comic Sans MS", 20))
        nameEntry2.place(x = 150, y = 240, width = 500, height = 50)

        passwordLabel2 = tk.Label(signupWindow,text="Enter Password:", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=150,y=340)

        passwordEntry2 = tk.Entry(signupWindow, font=("Comic Sans MS", 20), show = "*")
        passwordEntry2.place(x = 150, y = 380, width = 500, height = 50)

        confirmPasswordLabel = tk.Label(signupWindow,text="Confirm Password:", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=150,y=480)

        confirmPasswordEntry = tk.Entry(signupWindow, font=("Comic Sans MS", 20), show = "*")
        confirmPasswordEntry.place(x = 150, y = 520, width = 500, height = 50)

        signupButton2 = tk.Button(signupWindow, text="Sign Up", font=("Comic Sans MS", 15), command = lambda:signupCheck(signupWindow,nameEntry2,passwordEntry2,confirmPasswordEntry))
        signupButton2.place(x = 350, y = 675, width = 100, height = 50)

    elif(len(user_list) >= 10):
        maxUsersLabel = tk.Label(root, text = "Max Users Reached!", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)

def signupCheck(signupWindow, name, password, confirmPassword):
    if (any(x.name == name.get() for x in user_list)):
        userExistsLabel = tk.Label(signupWindow, text = "User already exists!", bg = '#FFB6C1',font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
    elif (name.get() == "" or password.get() == "" or confirmPassword.get() == ""):
        incorrectPassLabel = tk.Label(signupWindow, text = "Empty Field(s)", font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
    elif(password.get() != confirmPassword.get()):
        incorrectPassLabel = tk.Label(signupWindow, text = "Password Doesn't Match", font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
    else:
        user_list.append(User(name.get(), confirmPassword.get(), defaultAOO, defaultVOO, defaultLRL, defaultAAI, defaultVVI, defaultHys, defaultRP, defaultROO, defaultDOOR, defaultDDDR))

        f = open("pacemaker_users.txt", "a")
        f.write(name.get() + "\n")
        f.close

        f = open("pacemaker_passwords.txt", "a")
        f.write(confirmPassword.get() + "\n")
        f.close

        signupWriteFile("pacemakerAOO.txt", defaultAOO)
        signupWriteFile("pacemakerVOO.txt", defaultVOO)
        signupWriteFile("pacemakerAAI.txt", defaultAAI)
        signupWriteFile("pacemakerVVI.txt", defaultVVI)
        signupWriteFile("pacemakerROO.txt", defaultROO)
        signupWriteFile("pacemakerDOOR.txt", defaultDOOR)
        signupWriteFile("pacemakerDDDR.txt", defaultDDDR)
        signupWriteFile("pacemakerHys.txt", defaultHys)
        signupWriteFile("pacemakerRP.txt", defaultRP)
        signupWriteFile("pacemakerLRL.txt", defaultLRL)

        root.after(250, signupWindow.destroy())

def chooseDisplay(username, password):
    incorrectPassLabel = tk.Label(root, bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)

    for i in range(0, len(user_list)):
        flag = 0

        if (user_list[i].name == username and user_list[i].password == password):
            incorrectPassLabel = tk.Label(root, text = "Welcome!", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
            flag = 1
            # ********************************************* window demo ***********************************************************
            global user_id
            user_id = i

            pacingModeWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
            pacingModeWindow.title("Mode Menu")
            pacingModeWindow.resizable(0, 0)
            pacingModeWindow.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, (root.winfo_screenwidth()/2) - (WIDTH/2), (root.winfo_screenheight()/2) - (HEIGHT/2)))
            menu1(pacingModeWindow)

            break

        if(username == user_list[i].name and password != user_list[i].password and flag == 0):
            incorrectPassLabel = tk.Label(root, text = "Incorrect Username or Password!", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
            flag = 1
        if(username != user_list[i].name and flag == 0):
            incorrectPassLabel = tk.Label(root, text = "Incorrect Username or Password!", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
            flag = 1

# PARAMETER MODIFIER FUNCTIONS
def changeParameter(i, new_value, window, mode, title, label):
    if (mode == "AOO"):
        user_list[user_id].AOO[i].append(new_value.get())

        info = readFile("pacemakerAOO.txt")
        try:
            info[user_id][i].append(int(user_list[user_id].AOO[i][-1]))
        except ValueError:
            info[user_id][i].append(float(user_list[user_id].AOO[i][-1]))
        changeParamWriteFile("pacemakerAOO.txt", info)

        dataValuesAOO(window, title, "no")

    elif (mode == "VOO"):
        user_list[user_id].VOO[i].append(new_value.get())

        info = readFile("pacemakerVOO.txt")
        try:
            info[user_id][i].append(int(user_list[user_id].VOO[i][-1]))
        except ValueError:
            info[user_id][i].append(float(user_list[user_id].VOO[i][-1]))
        changeParamWriteFile("pacemakerVOO.txt", info)

        dataValuesVOO(window, title, "no")

    elif (mode[0:3] == "LRL"):
        user_list[user_id].LRL[i].append(new_value.get())

        info = readFile("pacemakerLRL.txt")
        info[user_id][i].append(int(user_list[user_id].LRL[i][-1]))
        changeParamWriteFile("pacemakerLRL.txt", info)

        #dataValuesAOO(window, title, "no")

        if (mode[3] == 'A'):
            dataValuesAOO(window, title, "no")
        elif (mode[3] == 'V'):
            dataValuesVOO(window, title, "no")

    elif (mode == "AAI"):
        user_list[user_id].AAI[i].append(new_value.get())

        info = readFile("pacemakerAAI.txt")
        info[user_id][i].append(float(user_list[user_id].AAI[i][-1]))
        changeParamWriteFile("pacemakerAAI.txt", info)

        dataValuesAAI2(window, title, "no")

    elif (mode == "VVI"):
        user_list[user_id].VVI[i].append(new_value.get())

        info = readFile("pacemakerVVI.txt")
        info[user_id][i].append(float(user_list[user_id].VVI[i][-1]))
        changeParamWriteFile("pacemakerVVI.txt", info)

        dataValuesVVI2(window, title, "no")

    elif (mode == "hys"):
        user_list[user_id].hys[i].append(new_value.get())

        info = readFile("pacemakerHys.txt")
        info[user_id][i].append(int(user_list[user_id].hys[i][-1]))
        changeParamWriteFile("pacemakerHys.txt", info)

        if (title[0] == 'A'):
            dataValuesAAI2(window, title, "no")
        elif (title[0] == 'V'):
            dataValuesVVI2(window, mode, "no")

    elif (mode == "RP"):
        user_list[user_id].RP[i].append(new_value.get())

        info = readFile("pacemakerRP.txt")
        info[user_id][i].append(int(user_list[user_id].RP[i][-1]))
        changeParamWriteFile("pacemakerRP.txt", info)

        if (title[0] == 'A'):
            dataValuesAAI2(window, title, "no")
        elif (title[0] == 'V'):
            dataValuesVVI2(window, title, "no")

    elif (mode == "ROO"):
        user_list[user_id].ROO[i].append(new_value.get())

        info = readFile("pacemakerROO.txt")
        try:
            info[user_id][i].append(int(user_list[user_id].ROO[i][-1]))
        except ValueError:
            info[user_id][i].append(float(user_list[user_id].ROO[i][-1]))

        changeParamWriteFile("pacemakerROO.txt", info)

        if (i == 0 or i == 1 or i == 2):
            dataValuesROO1(window, title, "no")
        elif (i == 3 or i == 4):
            dataValuesROO2(window, title, "no")

    elif (mode[0:3] == "DOO"):
        user_list[user_id].DOOR[i].append(new_value.get())

        info = readFile("pacemakerDOOR.txt")
        info[user_id][i].append(int(user_list[user_id].DOOR[i][-1]))
        changeParamWriteFile("pacemakerDOOR.txt", info)

        dataValuesDOOR2(window, title, "no")

    elif (mode == "DDDR"):
        user_list[user_id].DDDR[i] = new_value.get()

        with open("pacemaker_DDDR.txt", "r") as file:
            info = file.readlines()

        info[user_id] = ''
        for i in range(0, len(user_list[user_id].DDDR)):
            info[user_id] += str(user_list[user_id].DDDR[i])
            if (i != len(user_list[user_id].DDDR) - 1):
                info[user_id] += ", "

        info[user_id] += "\n"

        with open("pacemaker_DDDR.txt", "w") as file:
            file.writelines(info)

        dataValuesDDDR2(window, title, "no")

    window.destroy()

def checkParameter(min, max, i, new_value, window, x_in, y_in, mode, title, label, paramNumber):
    global close
    try:
        if (mode == "ROO" and i == 1) or (mode == "VVI" and i == 0) or (mode == "AAI" and i == 0) or (mode == "VVI" and i == 0) or (mode == "AOO" and i == 0) or (mode == "VOO" and i == 0):
            if (float(new_value.get()) > max or float(new_value.get()) < min):
                invalidEntry = tk.Label(window, text = "Out of Range",bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x = x_in + 320, y = y_in)
            else:
                # serial
                connected = updateParam(paramNumber, float(new_value.get() ) )
                if (connected):
                    changeParameter(i, new_value, window, mode, title, label)
                else:
                    #global close
                    if ((connected == True and close == "green") or (connected == False and close == "red")):
                        invalidEntry = tk.Label(window, text = "Disconnected",bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x = x_in + 320, y = y_in)
                    else:
                        if (mode == "AOO"):
                            dataValuesAOO(window, title, "yes")
                        elif (mode == "VOO"):
                            dataValuesAOO(window, title, "yes")
                        elif (mode[0:3] == "LRL"):
                            if (mode[3] == 'A'):
                                dataValuesAOO(window, title, "yes")
                            elif (mode[3] == 'V'):
                                dataValuesVOO(window, title, "yes")
                        elif (mode == "AAI"):
                            user_list[user_id].AAI[i].append(new_value.get())
                        elif (mode == "VVI"):
                            dataValuesVVI2(window, title, "yes")
                        elif (mode == "hys"):
                            if (title[0] == 'A'):
                                dataValuesAAI2(window, title, "yes")
                            elif (title[0] == 'V'):
                                dataValuesVVI2(window, mode, "yes")
                        elif (mode == "RP"):
                            if (title[0] == 'A'):
                                dataValuesAAI2(window, title, "yes")
                            elif (title[0] == 'V'):
                                dataValuesVVI2(window, title, "yes")
                        elif (mode == "ROO"):
                            if (i == 0 or i == 1 or i == 2):
                                dataValuesROO1(window, title, "yes")
                            elif (i == 3 or i == 4):
                                dataValuesROO2(window, title, "yes")
                        elif (mode == "DOOR"):
                            dataValuesDOOR2(window, title, "yes")
        else:
            if (int(new_value.get()) > max or int(new_value.get()) < min):
                invalidEntry = tk.Label(window, text = "Out of Range",bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x = x_in + 320, y = y_in)
            else:
                # serial
                connected = updateParam(paramNumber, float(new_value.get() ) )
                if (connected):
                    changeParameter(i, new_value, window, mode, title, label)
                else:
                    if ((connected == True and close == "green") or (connected == False and close == "red")):
                        invalidEntry = tk.Label(window, text = "Disconnected",bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x = x_in + 320, y = y_in)
                    else:
                        if (mode == "AOO"):
                            dataValuesAOO(window, title, "yes")
                        elif (mode == "VOO"):
                            dataValuesAOO(window, title, "yes")
                        elif (mode[0:3] == "LRL"):
                            if (mode[3] == 'A'):
                                dataValuesAOO(window, title, "yes")
                            elif (mode[3] == 'V'):
                                dataValuesVOO(window, title, "yes")
                        elif (mode == "AAI"):
                            user_list[user_id].AAI[i].append(new_value.get())
                        elif (mode == "VVI"):
                            dataValuesVVI2(window, title, "yes")
                        elif (mode == "hys"):
                            if (title[0] == 'A'):
                                dataValuesAAI2(window, title, "yes")
                            elif (title[0] == 'V'):
                                dataValuesVVI2(window, mode, "yes")
                        elif (mode == "RP"):
                            if (title[0] == 'A'):
                                dataValuesAAI2(window, title, "yes")
                            elif (title[0] == 'V'):
                                dataValuesVVI2(window, title, "yes")
                        elif (mode == "ROO"):
                            if (i == 0 or i == 1 or i == 2):
                                dataValuesROO1(window, title, "yes")
                            elif (i == 3 or i == 4):
                                dataValuesROO2(window, title, "yes")
                        elif (mode == "DOOR"):
                            dataValuesDOOR2(window, title, "yes")

    except ValueError:
        invalidEntry = tk.Label(window, text = "Invalid Entry",bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x = x_in + 320, y = y_in)

# MENU FUNCTIONS
def menu1(pacingModeWindow):
    for w in pacingModeWindow.winfo_children():
        w.destroy()

    pacingLabel = tk.Label(pacingModeWindow, text = "Pacing Modes", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 75, width = 500, height = 50)

    if(pacemakerConnected == False):
        pacemakerLabel = tk.Label(pacingModeWindow, text = "Pacemaker " + str(pacemakerNumber[user_id]) +  " Disconnected", bg = '#FF0000', font = ("Comic Sans MS", 10)).place(x = 550, y = 650, width = 200, height = 50)
    elif(pacemakerConnected == True):
        pacemakerLabel = tk.Label(pacingModeWindow, text = "Pacemaker " + str(pacemakerNumber[user_id]) +  " Connected", bg = '#00FF00', font = ("Comic Sans MS", 10)).place(x = 550, y = 650, width = 200, height = 50)

    AOOButton = tk.Button(pacingModeWindow, text="AOO", font=("Comic Sans MS", 15),command = lambda:dataValuesAOO(pacingModeWindow, "AOO", "no"))
    AOOButton.place(x = 250, y = 175, width = 300, height = 50)

    VOOButton = tk.Button(pacingModeWindow, text="VOO", font=("Comic Sans MS", 15),command = lambda:dataValuesVOO(pacingModeWindow, "VOO", "no"))
    VOOButton.place(x = 250, y = 300, width = 300, height = 50)

    AAIButton = tk.Button(pacingModeWindow, text="AAI", font=("Comic Sans MS", 15),command = lambda:dataValuesAAI1(pacingModeWindow, "AAI", "no"))
    AAIButton.place(x = 250, y = 425, width = 300, height = 50)

    VVIButton = tk.Button(pacingModeWindow, text="VVI", font=("Comic Sans MS", 15),command = lambda:dataValuesVVI1(pacingModeWindow, "VVI","no"))
    VVIButton.place(x = 250, y = 550, width = 300, height = 50)

    DOOButton = tk.Button(pacingModeWindow, text="DOO", font=("Comic Sans MS", 15),command = lambda:dataValuesDOO(pacingModeWindow, "DOO", "no"))
    DOOButton.place(x = 250, y = 675, width = 300, height = 50)

    nextButton = tk.Button(pacingModeWindow, text = "->", font = ("Comic Sans MS", 15), command = lambda: menu2(pacingModeWindow))
    nextButton.place(x = 750, y = 20, width = 30, height = 50)

def menu2(pacingModeWindow):
    for w in pacingModeWindow.winfo_children():
        w.destroy()

    pacingLabel = tk.Label(pacingModeWindow, text = "Pacing Modes", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 75, width = 500, height = 50)
    if(pacemakerConnected == False):
        pacemakerLabel = tk.Label(pacingModeWindow, text = "Pacemaker " + str(pacemakerNumber[user_id]) +  " Disconnected", bg = '#FF0000', font = ("Comic Sans MS", 10)).place(x = 550, y = 650, width = 200, height = 50)
    elif(pacemakerConnected == 1):
        pacemakerLabel = tk.Label(pacingModeWindow, text = "Pacemaker " + str(pacemakerNumber[user_id]) +  " Connected", bg = '#00FF00', font = ("Comic Sans MS", 10)).place(x = 550, y = 650, width = 200, height = 50)

    AOOButton = tk.Button(pacingModeWindow, text="AOOR", font=("Comic Sans MS", 15),command = lambda:dataValuesAOOR1(pacingModeWindow, "AOOR", "no"))
    AOOButton.place(x = 250, y = 175, width = 300, height = 50)

    VOOButton = tk.Button(pacingModeWindow, text="VOOR", font=("Comic Sans MS", 15),command = lambda:dataValuesVOOR1(pacingModeWindow, "VOOR", "no"))
    VOOButton.place(x = 250, y = 300, width = 300, height = 50)

    AAIButton = tk.Button(pacingModeWindow, text="AAIR", font=("Comic Sans MS", 15),command = lambda:dataValuesAAI1(pacingModeWindow, "AAIR", "no"))
    AAIButton.place(x = 250, y = 425, width = 300, height = 50)

    VVIButton = tk.Button(pacingModeWindow, text="VVIR", font=("Comic Sans MS", 15),command = lambda:dataValuesVVI1(pacingModeWindow, "VVIR", "no"))
    VVIButton.place(x = 250, y = 550, width = 300, height = 50)

    ROOButton = tk.Button(pacingModeWindow, text="DOOR", font=("Comic Sans MS", 15),command = lambda:dataValuesDOOR(pacingModeWindow, "DOOR", "no"))
    ROOButton.place(x = 250, y = 675, width = 300, height = 50)

    nextButton = tk.Button(pacingModeWindow, text = "->", font = ("Comic Sans MS", 15), command = lambda: menu3(pacingModeWindow))
    nextButton.place(x = 750, y = 20, width = 30, height = 50)

    prevButton = tk.Button(pacingModeWindow, text = "<-", font = ("Comic Sans MS", 15), command = lambda: menu1(pacingModeWindow))
    prevButton.place(x = 50, y = 20, width = 30, height = 50)

def menu3(pacingModeWindow):
    for w in pacingModeWindow.winfo_children():
        w.destroy()

    pacingLabel = tk.Label(pacingModeWindow, text = "Pacing Modes", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 75, width = 500, height = 50)
    if(pacemakerConnected == False):
        pacemakerLabel = tk.Label(pacingModeWindow, text = "Pacemaker " + str(pacemakerNumber[user_id]) +  " Disconnected", bg = '#FF0000', font = ("Comic Sans MS", 10)).place(x = 550, y = 650, width = 200, height = 50)
    elif(pacemakerConnected == True):
        pacemakerLabel = tk.Label(pacingModeWindow, text = "Pacemaker " + str(pacemakerNumber[user_id]) +  " Connected", bg = '#00FF00', font = ("Comic Sans MS", 10)).place(x = 550, y = 650, width = 200, height = 50)

    AOOButton = tk.Button(pacingModeWindow, text="DDDR", font=("Comic Sans MS", 15),command = lambda:dataValuesDDDR(pacingModeWindow, "DDDR", "no"))
    AOOButton.place(x = 250, y = 175, width = 300, height = 50)

    prevButton = tk.Button(pacingModeWindow, text = "<-", font = ("Comic Sans MS", 15), command = lambda: menu2(pacingModeWindow))
    prevButton.place(x = 50, y = 20, width = 30, height = 50)

# GRAPH FUNCTIONS
def connectionCheck(window):
    global close

    if(pacemakerConnected == False):
        pacemakerLabel = tk.Label(window, text = "Pacemaker " + str(pacemakerNumber[user_id]) +  " Disconnected", bg = '#FF0000', font = ("Comic Sans MS", 10)).place(x = 1200, y = 40, width = 200, height = 50)
        close = "red"
    elif(pacemakerConnected == True):
        pacemakerLabel = tk.Label(window, text = "Pacemaker " + str(pacemakerNumber[user_id]) +  " Connected", bg = '#00FF00', font = ("Comic Sans MS", 10)).place(x = 1200, y = 40, width = 200, height = 50)
        close = "green"

def deactivate():
    # window.destroy()
    global run
    run = False
    plt.close()

def graph(window):
    #This part goes in the chooseDisplay function where the other buttons are
    atrGraphButton = tk.Button(window, text="Atrium Graph", font=("Comic Sans MS", 15),command = lambda:atrGraph(window))
    atrGraphButton.place(x = 830, y = 325, width = 300, height = 50)

    venGraphButton = tk.Button(window, text="Ventricle Graph", font=("Comic Sans MS", 15),command = lambda:venGraph(window))
    venGraphButton.place(x = 830, y = 425, width = 300, height = 50)

    dualGraphButton = tk.Button(window, text="Display Both Graphs", font=("Comic Sans MS", 15),command = lambda:dualGraph(window))
    dualGraphButton.place(x = 830, y = 525, width = 300, height = 50)

    quitButton = tk.Button(window, text="Quit Graph", font=("Comic Sans MS", 15), command = lambda:deactivate())
    quitButton.place(x = 830, y = 625, width = 300, height = 50)

def pulse(atrium, ventricle, window):
    maxSize = 200
    sampleRate = 0.0000001

    dataA = [ [0]*2 for size in range(0) ]
    dataV = [ [0]*2 for size in range(0) ]

    asLabel = [ [0]*2 for size in range(0) ]
    apLabel = [ [0]*2 for size in range(0) ]

    vsLabel = [ [0]*2 for size in range(0) ]
    vpLabel = [ [0]*2 for size in range(0) ]

    global run
    run = True

    while(run):
        newData = serial.requestEgram()

        plt.cla()
        #plt.axis( [time[pointer-1]-(sampleRate*maxSize), time[pointer-1], 0, 5] )

        #print("newData: ", newData)
        if newData[0] == 0:
            global pacemakerConnected
            pacemakerConnected = False;

        time = newData[1]

        if atrium:
            signal = newData[2]
            paced = newData[3]

            if paced:
                signal = float(user_list[user_id].AOO[0][-1])
                apLabel.append([time, signal+0.25])
            elif (signal < 2.2 or signal > 2.7):
                signal = 4.5
                asLabel.append([time, signal+0.25])
            else:
                signal = 0

            if len(dataA) < maxSize:
                dataA.append([time, signal])
            else:
                dataA.pop(0)
                dataA.append([time, signal])
            #print("data: ", data)

            for i in range(len(asLabel)-1):
                if asLabel[i][0] < dataA[len(dataA)-1][0]-12:
                    asLabel.pop(0)
                else:
                    break
            for i in range(len(apLabel)-1):
                if apLabel[i][0] < dataA[len(dataA)-1][0]-12:
                    apLabel.pop(0)
                else:
                    break

            timeA =  [x[0] for x in dataA ]
            signalA =  [y[1] for y in dataA]

            timeAS =  [x[0] for x in asLabel]
            signalAS =  [y[1] for y in asLabel]

            timeAP =  [x[0] for x in apLabel]
            signalAP =  [y[1] for y in apLabel]


            plt.plot(timeA, signalA, 'r', label="Atrium")
            for i in range(len(signalAS) ):
                plt.text(timeAS[i], signalAS[i], 'AS', horizontalalignment='center')
            for i in range(len(signalAP) ):
                plt.text(timeAP[i], signalAP[i], 'AP', horizontalalignment='center')
            plt.axis( [timeA[len(timeA)-1]-12, timeA[len(timeA)-1], 0, 6] )

        if ventricle:
            signal = newData[4]
            paced = newData[5]

            if paced:
                signal = float(user_list[user_id].VOO[0][-1])
                vpLabel.append([time, signal+0.25])
            elif (signal < 2.2 or signal > 2.7):
                signal = 4.5
                vsLabel.append([time, signal+0.25])
            else:
                signal = 0

            if len(dataV) < maxSize:
                dataV.append([time, signal])
            else:
                dataV.pop(0)
                dataV.append([time, signal])

            for i in range(len(vsLabel)-1):
                if vsLabel[i][0] < dataV[len(dataV)-1][0]-12:
                    vsLabel.pop(0)
                else:
                    break
            for i in range(len(vpLabel)-1):
                if vpLabel[i][0] < dataV[len(dataV)-1][0]-12:
                    vpLabel.pop(0)
                else:
                    break

            timeV =  [x[0] for x in dataV ]
            signalV =  [y[1] for y in dataV]

            timeVS =  [x[0] for x in vsLabel]
            signalVS =  [y[1] for y in vsLabel]

            timeVP =  [x[0] for x in vpLabel]
            signalVP =  [y[1] for y in vpLabel]

            plt.plot(timeV, signalV, 'b', label="Ventricle")
            for i in range(len(signalVS) ):
                plt.text(timeVS[i], signalVS[i], 'VS', horizontalalignment='center')
            for i in range(len(signalVP) ):
                plt.text(timeVP[i], signalVP[i], 'VP', horizontalalignment='center')
            plt.axis( [timeV[len(timeV)-1]-12, timeV[len(timeV)-1], 0, 6] )

        plt.legend(loc="upper left")
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude (V)')
        plt.gcf().axes[0].xaxis.get_major_formatter().set_scientific(False)
        plt.pause(sampleRate)

    plt.show()

def atrGraph(window):
    atrAni = FuncAnimation(plt.gcf(),pulse(1,0, window), interval = 100)

def venGraph(window):
    venAni = FuncAnimation(plt.gcf(),pulse(0,1, window), interval = 100)

def dualGraph(window):
    dualAni = FuncAnimation(plt.gcf(),pulse(1,1, window), interval = 100)

# MODES
def changeMode(title):
    if title[0:3] == "AOO":
        updateParam(17,1)
        updateParam(18,1)
        updateParam(19,1)
    elif title[0:3] == "VOO":
        updateParam(17,2)
        updateParam(18,1)
        updateParam(19,2)
    elif title[0:3] == "DOO":
        updateParam(17,3)
        updateParam(18,1)
        updateParam(19,3)
    elif title[0:3] == "AAI":
        updateParam(17,1)
        updateParam(18,2)
        updateParam(19,1)
    elif title[0:3] == "VVI":
        updateParam(17,2)
        updateParam(18,2)
        updateParam(19,2)
    elif title[0:3] == "DDD":
        updateParam(17,3)
        updateParam(18,3)
        updateParam(19,3)

    if title[-1] == "R":
        updateParam(15,1)
    else:
        updateParam(15,0)

def hys(window, title):
    #hysteris
    hysLabel = tk.Label(window, text = "Hystersis: " + str(user_list[user_id].hys[0][-1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=50)
    hysRangeLabel =  tk.Label(window, text = "(Range: 343 - 2000 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=85)

    hysRateEntry = tk.Entry(window, font=("Comic Sans MS", 20))
    hysRateEntry.place(x = 50, y = 140, width = 500, height = 50)

    hysRateChangeButton = tk.Button(window, text="Change", font=("Comic Sans MS", 15), command = lambda:checkParameter(343, 2000, 0, hysRateEntry, window, 50, 215, "hys", title, hysLabel, 6))
    hysRateChangeButton.place(x = 50, y = 215, width = 300, height = 50)

def LRL(window, title, mode):
    # Lower Rate
    lowerRateLabel = tk.Label(window, text = "Lower Rate Limit: " + str(user_list[user_id].LRL[0][-1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=50)
    LRRangeLabel =  tk.Label(window, text = "(Range: 343 - 2000 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=85)

    lowerRateEntry = tk.Entry(window, font=("Comic Sans MS", 20))
    lowerRateEntry.place(x = 50, y = 140, width = 500, height = 50)

    lowerRateChangeButton = tk.Button(window, text="Change", font=("Comic Sans MS", 15), command = lambda:checkParameter(343, 2000, 0, lowerRateEntry, window, 50, 215, "LRL" + mode, title, lowerRateLabel, 1))
    lowerRateChangeButton.place(x = 50, y = 215, width = 300, height = 50)

def RP(window, title):
    RPLabel = tk.Label(window, text = "Refractory Period (RP): " + str(user_list[user_id].RP[0][-1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=325)
    RPLabel =  tk.Label(window, text = "(Range: 150 - 500 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=360)

    RPEntry = tk.Entry(window, font=("Comic Sans MS", 20))
    RPEntry.place(x = 50, y = 400, width = 500, height = 50)

    RPButton = tk.Button(window, text="Change", font=("Comic Sans MS", 15), command = lambda:checkParameter(150, 500, 0, RPEntry, window, 50, 215, "RP", title, RPLabel, 7))
    RPButton.place(x = 50, y = 475, width = 300, height = 50)

def dataValuesAOO(oldWin, title, delCom):
    AOOWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    AOOWindow.title(title)

    graph(AOOWindow)

    if (delCom == "yes"):
        oldWin.destroy()

    # serial
    changeMode(title)
    # updateParam(17,3)
    # updateParam(18,1)
    # updateParam(19,1)
    # updateParam(15,0)
    connectionCheck(AOOWindow)

    # Lower Rate
    LRL(AOOWindow, title, "A") # Lower Rate Limit

    # Atrial Amplitude
    amplitudeLabel = tk.Label(AOOWindow, text = "Atrial Amplitude: " + str(user_list[user_id].AOO[0][-1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=325)
    amplitudeRangeLabel =  tk.Label(AOOWindow, text = "(Range: 0.5-5.0V)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=360)

    amplitudeEntry = tk.Entry(AOOWindow, font=("Comic Sans MS", 20))
    amplitudeEntry.place(x = 50, y = 400, width = 500, height = 50)

    amplitudeChangeButton = tk.Button(AOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(0.5, 5, 0, amplitudeEntry, AOOWindow, 50, 475, "AOO", title, amplitudeLabel, 2))
    amplitudeChangeButton.place(x = 50, y = 475, width = 300, height = 50)

    # Atrial Pulse Width
    pWLabel = tk.Label(AOOWindow, text = "Atrial Pulse Width: " + str(user_list[user_id].AOO[1][-1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=600)
    pWLabel =  tk.Label(AOOWindow, text = "(Range: 1-30ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=635)

    pWEntry = tk.Entry(AOOWindow, font=("Comic Sans MS", 20))
    pWEntry.place(x = 50, y = 675, width = 500, height = 50)

    pwEntryChangeButton = tk.Button(AOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(1, 30, 1, pWEntry, AOOWindow, 50, 750, "AOO", title, pWLabel, 3))
    pwEntryChangeButton.place(x = 50, y = 750, width = 300, height = 50)

    # Switch Button for AAI Window
    if (title == "DOOR"):
        switchButton = tk.Button(AOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesVOO(AOOWindow, title, "yes"))
        switchButton.place(x = 1100, y = 800, width = 300, height = 50)
    elif (title == "AOOR"):
        switchButton = tk.Button(AOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesROO1(AOOWindow, title, "yes"))
        switchButton.place(x = 1100, y = 800, width = 300, height = 50)
    elif (title == "DOO"):
        switchButton = tk.Button(AOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesVOO(AOOWindow, title, "yes"))
        switchButton.place(x = 1100, y = 800, width = 300, height = 50)
    elif (title == "AAI" or title == "AAIR" or title == "DDDR"):
        switchButton = tk.Button(AOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesAAI2(AOOWindow, title, "yes"))
        switchButton.place(x = 1100, y = 800, width = 300, height = 50)

def dataValuesVOO(oldWin, title, delCom):
    VOOWindow = tk.Toplevel(root, height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    VOOWindow.title(title)

    graph(VOOWindow)

    if (delCom == "yes"):
        oldWin.destroy()

    #serial
    changeMode(title)
    # updateParam(17,2)
    # updateParam(18,1)
    # updateParam(19,2)
    # updateParam(15,0)
    connectionCheck(VOOWindow)

    # Lower Rate Limit
    LRL(VOOWindow, title, "V")

    # Ventricle Amplitude
    amplitudeLabel = tk.Label(VOOWindow, text = "Ventricle Amplitude: " + str(user_list[user_id].VOO[0][-1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=325)
    amplitudeRangeLabel =  tk.Label(VOOWindow, text = "(Range: 0.5-5.0V)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=360)

    amplitudeEntry = tk.Entry(VOOWindow, font=("Comic Sans MS", 20))
    amplitudeEntry.place(x = 50, y = 400, width = 500, height = 50)

    amplitudeChangeButton = tk.Button(VOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(0.5, 5, 0, amplitudeEntry, VOOWindow, 50, 475, "VOO", title, amplitudeLabel,4))
    amplitudeChangeButton.place(x = 50, y = 475, width = 300, height = 50)

    # Ventricle Pulse Width
    pWLabel = tk.Label(VOOWindow, text = "Ventricle Pulse Width: " + str(user_list[user_id].VOO[1][-1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=600)
    pWLabel =  tk.Label(VOOWindow, text = "(Range: 1-30ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=635)

    pWEntry = tk.Entry(VOOWindow, font=("Comic Sans MS", 20))
    pWEntry.place(x = 50, y = 675, width = 500, height = 50)

    pwEntryChangeButton = tk.Button(VOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(1, 30, 1, pWEntry, VOOWindow, 50, 750, "VOO", title, pWLabel, 5))
    pwEntryChangeButton.place(x = 50, y = 750, width = 300, height = 50)

    # Switch Button for AAI Window
    if (title == "VOOR"):
        nextButton = tk.Button(VOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesROO1(VOOWindow, title, "yes"))
        nextButton.place(x = 1100, y = 800, width = 300, height = 50)
    elif (title == "DOOR"):
        nextButton = tk.Button(VOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesROO1(VOOWindow, title, "yes"))
        nextButton.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton = tk.Button(VOOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesAOO(VOOWindow, title, "yes"))
        prevButton.place(x = 775, y = 800, width = 300, height = 50)
    elif (title == "DDDR"):
        nextButton = tk.Button(VOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesVVI2(VOOWindow, title, "yes"))
        nextButton.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton = tk.Button(VOOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesAAI2(VOOWindow, title, "yes"))
        prevButton.place(x = 775, y = 800, width = 300, height = 50)
    elif (title == "VVI" or title == "VVIR"):
        switchButton = tk.Button(VOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesVVI2(VOOWindow, title, "yes"))
        switchButton.place(x = 1100, y = 800, width = 300, height = 50)
    elif (title == "DOO"):
        nextButton = tk.Button(VOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOOR2(VOOWindow, title, "yes"))
        nextButton.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton = tk.Button(VOOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesAOO(VOOWindow, title, "yes"))
        prevButton.place(x = 775, y = 800, width = 300, height = 50)

def dataValuesAAI1(oldWin, title, delCom):
    AAIWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    AAIWindow.title(title)

    if (delCom == "yes"):
        oldWin.destroy()

    dataValuesAOO(AAIWindow, title, "yes")

    #serial
    changeMode(title)
    # updateParam(17,1)
    # updateParam(18,2)
    # updateParam(19,1)
    # updateParam(15,0)

def dataValuesAAI2(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    AAIWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    AAIWindow.title(title)

    graph(AAIWindow)

    #serial
    changeMode(title)
    # updateParam(17,1)
    # updateParam(18,2)
    # updateParam(19,1)
    # updateParam(15,0)
    connectionCheck(AAIWindow)

    hys(AAIWindow, title)
    RP(AAIWindow, title)

    # ARP
    '''
    ARPLabel = tk.Label(AAIWindow, text = "ARP: " + str(user_list[user_id].AAI[0][-1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=325)
    ARPLabel =  tk.Label(AAIWindow, text = "(Range: 150-500 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=360)

    ARPEntry = tk.Entry(AAIWindow, font=("Comic Sans MS", 20))
    ARPEntry.place(x = 50, y = 400, width = 500, height = 50)

    ARPEntryChangeButton_2 = tk.Button(AAIWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(150, 500, 0, ARPEntry, AAIWindow, 50, 475, "AAI", title, ARPLabel, 7))
    ARPEntryChangeButton_2.place(x = 50, y = 475, width = 300, height = 50)
    '''

    # ASensitivity
    A_sensLabel = tk.Label(AAIWindow, text = "Atrial Sensitivity: " + str(user_list[user_id].AAI[0][-1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=600)
    A_sensLabel =  tk.Label(AAIWindow, text = "(Range: 3.0 - 5.0 V)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=635)

    A_sensEntry = tk.Entry(AAIWindow, font=("Comic Sans MS", 20))
    A_sensEntry.place(x = 50, y = 675, width = 500, height = 50)

    A_sensEntryChangeButton_2 = tk.Button(AAIWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(3, 5, 0, A_sensEntry, AAIWindow, 50, 750, "AAI", title, A_sensLabel,8))
    A_sensEntryChangeButton_2.place(x = 50, y = 750, width = 300, height = 50)

    # goes to previous window
    if (title == 'AAIR'):
        nextButton = tk.Button(AAIWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesROO1(AAIWindow, title, "yes"))
        nextButton.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton = tk.Button(AAIWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesAAI1(AAIWindow, title, "yes"))
        prevButton.place(x = 775, y = 800, width = 300, height = 50)
    elif (title == "DDDR"):
        nextButton = tk.Button(AAIWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesVVI1(AAIWindow, title, "yes"))
        nextButton.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton = tk.Button(AAIWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesAAI1(AAIWindow, title, "yes"))
        prevButton.place(x = 775, y = 800, width = 300, height = 50)
    else:
        switchButton2 = tk.Button(AAIWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesAAI1(AAIWindow, title, "yes"))
        switchButton2.place(x = 1100, y = 800, width = 300, height = 50)

def dataValuesVVI1(oldWin, title, delCom):
    VVIWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    VVIWindow.title(title)

    if (delCom == "yes"):
        oldWin.destroy()

    dataValuesVOO(VVIWindow, title, "yes")
    # serial
    changeMode(title)
    # updateParam(17,2)
    # updateParam(18,2)
    # updateParam(19,2)
    # updateParam(15,0)

def dataValuesVVI2(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    VVIWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    VVIWindow.title(title)

    hys(VVIWindow, title)
    RP(VVIWindow, title)
    graph(VVIWindow)
    #serial
    changeMode(title)
    # updateParam(17,2)
    # updateParam(18,2)
    # updateParam(19,2)
    # updateParam(15,0)
    connectionCheck(VVIWindow)

    # VRP
    '''
    VRPLabel = tk.Label(VVIWindow, text = "VRP: " + str(user_list[user_id].VVI[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=200)
    VRPLabel =  tk.Label(VVIWindow, text = "(Range: 150-500 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=235)

    VRPEntry = tk.Entry(VVIWindow, font=("Comic Sans MS", 20))
    VRPEntry.place(x = 50, y = 275, width = 500, height = 50)

    VRPEntryChangeButton_2 = tk.Button(VVIWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(150, 500, 0, VRPEntry, VVIWindow, 50, 350, "VVI", title, VRPLabel,7))
    VRPEntryChangeButton_2.place(x = 50, y = 350, width = 300, height = 50)
    '''

    # VSensitivity
    V_sensLabel = tk.Label(VVIWindow, text = "Ventricle Sensitivity: " + str(user_list[user_id].VVI[0][-1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=600)
    V_sensLabel =  tk.Label(VVIWindow, text = "(Range: 3.0-5.0 V)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=635)

    V_sensEntry = tk.Entry(VVIWindow, font=("Comic Sans MS", 20))
    V_sensEntry.place(x = 50, y = 675, width = 500, height = 50)

    V_sensEntryChangeButton_2 = tk.Button(VVIWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(3, 5, 0, V_sensEntry, VVIWindow, 50, 750, "VVI", title, V_sensLabel,9))
    V_sensEntryChangeButton_2.place(x = 50, y = 750, width = 300, height = 50)

    if (title == "VVIR" or title == "DDDR"):
        nextButton = tk.Button(VVIWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesROO1(VVIWindow, title, "yes"))
        nextButton.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton = tk.Button(VVIWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesVVI1(VVIWindow, title, "yes"))
        prevButton.place(x = 775, y = 800, width = 300, height = 50)
        prevButton.place(x = 775, y = 800, width = 300, height = 50)
    else:
        switchButton2 = tk.Button(VVIWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesVVI1(VVIWindow, title, "yes"))
        switchButton2.place(x = 1100, y = 800, width = 300, height = 50)

def dataValuesDOO(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    dataValuesAOO(tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1'), title, "yes")

    # serial
    changeMode(title)
    # updateParam(17,2)
    # updateParam(18,2)
    # updateParam(19,2)
    # updateParam(15,0)

def dataValuesROO1(oldWin, title, delCom):
    ROOWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    ROOWindow.title(title)

    graph(ROOWindow)

    if (delCom == "yes"):
        oldWin.destroy()
    # serial
    changeMode(title)
    # updateParam(17,3)
    # updateParam(18,1)
    # updateParam(19,3)
    # updateParam(15,0)
    connectionCheck(ROOWindow)

    # Maximum Sensor Rate Limit
    maxSenLabel= tk.Label(ROOWindow, text = "Maximum Sensor Rate Limit: " + str(user_list[user_id].ROO[0][-1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=50)
    RangeLabel =  tk.Label(ROOWindow, text = "(Range: 343 - 1200 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=85)

    maxSenEntry = tk.Entry(ROOWindow, font=("Comic Sans MS", 20))
    maxSenEntry.place(x = 50, y = 140, width = 500, height = 50)

    maxSenChangeButton = tk.Button(ROOWindow, text="Change", font=("Comic Sans MS", 15), command = lambda:checkParameter(343, 1200, 0, maxSenEntry, ROOWindow, 50, 215, "ROO", title, maxSenLabel,10))
    maxSenChangeButton.place(x = 50, y = 215, width = 300, height = 50)

    # Activity Threshold
    actLabel = tk.Label(ROOWindow, text = "Activity Threshold: " + str(user_list[user_id].ROO[1][-1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=325)
    actRangeLabel =  tk.Label(ROOWindow, text = "(Range: 0.05 - 1.5 g)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=360)

    actEntry = tk.Entry(ROOWindow, font=("Comic Sans MS", 20))
    actEntry.place(x = 50, y = 400, width = 500, height = 50)

    actChangeButton = tk.Button(ROOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(0.05, 1.5, 1, actEntry, ROOWindow, 50, 475, "ROO", title, actLabel,11))
    actChangeButton.place(x = 50, y = 475, width = 300, height = 50)

    # Reaction Time
    reactLabel = tk.Label(ROOWindow, text = "Reaction Time: " + str(user_list[user_id].ROO[2][-1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=600)
    reactLabel =  tk.Label(ROOWindow, text = "(Range: 10 - 50s)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=635)

    reactEntry = tk.Entry(ROOWindow, font=("Comic Sans MS", 20))
    reactEntry.place(x = 50, y = 675, width = 500, height = 50)

    reactEntryChangeButton = tk.Button(ROOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(1, 30, 2, reactEntry, ROOWindow, 50, 750, "ROO", title, reactLabel,13))
    reactEntryChangeButton.place(x = 50, y = 750, width = 300, height = 50)

    if (title == "AOOR"):
        nextButton2 = tk.Button(ROOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesROO2(ROOWindow, title, "yes"))
        nextButton2.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton2 = tk.Button(ROOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesAOO(ROOWindow, title, "yes"))
        prevButton2.place(x = 775, y = 800, width = 300, height = 50)
    elif (title == "AAIR"):
        nextButton2 = tk.Button(ROOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesROO2(ROOWindow, title, "yes"))
        nextButton2.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton2 = tk.Button(ROOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesAAI2(ROOWindow, title, "yes"))
        prevButton2.place(x = 775, y = 800, width = 300, height = 50)
    elif (title == "VVIR" or title == "DDDR"):
        nextButton2 = tk.Button(ROOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesROO2(ROOWindow, title, "yes"))
        nextButton2.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton2 = tk.Button(ROOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesVVI2(ROOWindow, title, "yes"))
        prevButton2.place(x = 775, y = 800, width = 300, height = 50)
    elif (title == "VOOR" or title == "DOOR" or title == "DDDR"):
        nextButton2 = tk.Button(ROOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesROO2(ROOWindow, title, "yes"))
        nextButton2.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton2 = tk.Button(ROOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesVOO(ROOWindow, title, "yes"))
        prevButton2.place(x = 775, y = 800, width = 300, height = 50)

    # goes to next window
    switchButton2 = tk.Button(ROOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesROO2(ROOWindow, title, "yes"))
    switchButton2.place(x = 1100, y = 800, width = 300, height = 50)

def dataValuesROO2(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    ROOWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    ROOWindow.title(title)

    graph(ROOWindow)
    # serial
    changeMode(title)
    # updateParam(17,3)
    # updateParam(18,1)
    # updateParam(19,3)
    # updateParam(15,0)
    connectionCheck(ROOWindow)

    # response
    responseLabel = tk.Label(ROOWindow, text = "Response Factor: " + str(user_list[user_id].ROO[3][-1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=200)
    responseLabel =  tk.Label(ROOWindow, text = "(Range: 1-16)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=235)

    responseEntry = tk.Entry(ROOWindow, font=("Comic Sans MS", 20))
    responseEntry.place(x = 50, y = 275, width = 500, height = 50)

    responseEntryChangeButton_2 = tk.Button(ROOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(1, 16, 3, responseEntry, ROOWindow, 50, 350, "ROO", title, responseLabel,12))
    responseEntryChangeButton_2.place(x = 50, y = 350, width = 300, height = 50)

    # ASensitivity
    recovLabel = tk.Label(ROOWindow, text = "Recovery Time: " + str(user_list[user_id].ROO[4][-1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=475)
    recovLabel =  tk.Label(ROOWindow, text = "(Range: 120 - 960 s)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=510)

    recovEntry = tk.Entry(ROOWindow, font=("Comic Sans MS", 20))
    recovEntry.place(x = 50, y = 550, width = 500, height = 50)

    recovEntryChangeButton_2 = tk.Button(ROOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(120, 960, 4, recovEntry, ROOWindow, 50, 635, "ROO", title, recovLabel,14))
    recovEntryChangeButton_2.place(x = 50, y = 635, width = 300, height = 50)

    # goes to previous window
    if (title == "DOOR" or title == "DDDR"):
        nextButton = tk.Button(ROOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOOR2(ROOWindow, title, "yes"))
        nextButton.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton = tk.Button(ROOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesROO1(ROOWindow, title, "yes"))
        prevButton.place(x = 775, y = 800, width = 300, height = 50)

    else:
        switchButton2 = tk.Button(ROOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesROO1(ROOWindow, title, "yes"))
        switchButton2.place(x = 1100, y = 800, width = 300, height = 50)

    '''
    elif (title == "DDDR"):
        nextButton = tk.Button(ROOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDDDR2(ROOWindow, title, "yes"))
        nextButton.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton = tk.Button(ROOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesROO1(ROOWindow, title, "yes"))
        prevButton.place(x = 775, y = 800, width = 300, height = 50)
    '''

def dataValuesAOOR1(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    dataValuesAOO(tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1'), title, "yes")
    # serial
    changeMode(title)
    # updateParam(17,1)
    # updateParam(18,1)
    # updateParam(19,1)
    # updateParam(15,1)

def dataValuesVOOR1(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    dataValuesVOO(tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1'), title, "yes")

    # serial
    changeMode(title)
    # updateParam(17,2)
    # updateParam(18,1)
    # updateParam(19,2)
    # updateParam(15,1)

def dataValuesAAIR1(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    dataValuesAAI1(tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1'), title, "yes")

    # serial
    changeMode(title)
    # updateParam(17,1)
    # updateParam(18,2)
    # updateParam(19,1)
    # updateParam(15,1)

def dataValuesVVIR1(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    dataValuesVVI1(tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1'), title, "yes")

    # serial
    changeMode(title)
    # updateParam(17,2)
    # updateParam(18,2)
    # updateParam(19,2)
    # updateParam(15,1)

def dataValuesDOOR(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    dataValuesAOO(tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1'), title, "yes")

    # serial
    changeMode(title)
    # updateParam(17,3)
    # updateParam(18,1)
    # updateParam(19,3)
    # updateParam(15,1)

def dataValuesDOOR2(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    DOORWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    DOORWindow.title(title)

    graph(DOORWindow)
    # serial
    changeMode(title)
    # updateParam(17,3)
    # updateParam(18,1)
    # updateParam(19,3)
    # updateParam(15,1)
    connectionCheck(DOORWindow)

    avLabel = tk.Label(DOORWindow, text = "Fixed Atrial Ventrical (AV) Delay: " + str(user_list[user_id].DOOR[0][-1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=200)
    avLabel =  tk.Label(DOORWindow, text ="(Range: 70-300 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=235)

    avEntry = tk.Entry(DOORWindow, font=("Comic Sans MS", 20))
    avEntry.place(x = 50, y = 275, width = 500, height = 50)

    avEntryChangeButton = tk.Button(DOORWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(70, 300, 0, avEntry, DOORWindow, 50, 350, "DOOR", title, avLabel,16))
    avEntryChangeButton.place(x = 50, y = 350, width = 300, height = 50)

    if title == "DOO":
        switchButton2 = tk.Button(DOORWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesVOO(DOORWindow, title, "yes"))
        switchButton2.place(x = 1100, y = 800, width = 300, height = 50)
    else:
        switchButton2 = tk.Button(DOORWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesROO2(DOORWindow, title, "yes"))
        switchButton2.place(x = 1100, y = 800, width = 300, height = 50)

def dataValuesDDDR(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    dataValuesAAI1(tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1'), title, "yes")
    # serial
    changeMode(title)
    # updateParam(17,3)
    # updateParam(18,3)
    # updateParam(19,3)
    # updateParam(15,1)

def dataValuesDDDR2(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    DDDRWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    DDDRWindow.title(title)

    graph(DDDRWindow)
    # serial
    changeMode(title)
    # updateParam(17,3)
    # updateParam(18,3)
    # updateParam(19,3)
    # updateParam(15,1)
    connectionCheck(DDDRWindow)

    responseLabel = tk.Label(DDDRWindow, text = "PVARP: " + str(user_list[user_id].DDDR[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=200)

    '''
    responseLabel = tk.Label(DDDRWindow, text = "PVARP: " + str(user_list[user_id].DDDR[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=200)
    responseLabel =  tk.Label(DDDRWindow, text ="(Range: 150 - 500 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=235)

    responseEntry = tk.Entry(DDDRWindow, font=("Comic Sans MS", 20))
    responseEntry.place(x = 50, y = 275, width = 500, height = 50)

    responseEntryChangeButton = tk.Button(DDDRWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(150, 500, 0, responseEntry, DDDRWindow, 50, 215, "DDDR", title, responseLabel,12))
    responseEntryChangeButton.place(x = 50, y = 350, width = 300, height = 50)

    switchButton2 = tk.Button(DDDRWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesROO2(DDDRWindow, title, "yes"))
    switchButton2.place(x = 1100, y = 800, width = 300, height = 50)
    '''

# MAIN WINDOW
def main():
    # objects of tkinter class
    root.resizable(0, 0)
    root.title('Login/Signup')
    root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, (root.winfo_screenwidth()/2) - (WIDTH/2), (root.winfo_screenheight()/2) - (HEIGHT/2)))

    background_image = tk.PhotoImage(file='Heart.png')
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # ************************* label demo ************************************
    fooLabel = Label(root, "foo")
    fooLabel.place(100, 50, 200)
    fooLabel.hide()
    # *************************************************************************
    #connect()
    # ************************* read files ************************************

    # stores textfile info in User class object
    with open("pacemaker_users.txt") as i:
        names = i.readlines()
        names = [x.strip() for x in names]

    with open("pacemaker_passwords.txt") as i:
        password_list = i.readlines()
        password_list = [x.strip() for x in password_list]

    AOO_list = readFile("pacemakerAOO.txt")
    VOO_list = readFile("pacemakerVOO.txt")
    LRL_list = readFile("pacemakerLRL.txt")
    AAI_list = readFile("pacemakerAAI.txt")
    VVI_list = readFile("pacemakerVVI.txt")
    hys_list = readFile("pacemakerHys.txt")
    ROO_list = readFile("pacemakerROO.txt")
    DOOR_list = readFile("pacemakerDOOR.txt")
    DDDR_list = readFile("pacemakerDDDR.txt")
    hys_list = readFile("pacemakerHys.txt")
    RP_list = readFile("pacemakerRP.txt")

    global user_list
    user_list = []

    for i in range(0, len(names)):
        user_list.append(User(names[i], password_list[i], AOO_list[i], VOO_list[i], LRL_list[i], AAI_list[i], VVI_list[i], hys_list[i], RP_list[i], ROO_list[i], DOOR_list[i], DDDR_list[i]))

    # *************************************************************************

    welcomeLabel = tk.Label(root, text = "Welcome!", bg = '#FFB6C1', font = ("Comic Sans MS", 30))

    welcomeLabel.place(x= 300, y= 100, width = 200,)

    nameLabel = tk.Label(root,text="Enter Name:", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=150,y=260)

    # ******************* Entry demo ******************************************
    #nameEntry = tk.Entry(root, font=("Comic Sans MS", 20))
    #nameEntry.place(x = 150, y = 300, width = 500, height = 50)
    nameEntry = Entry(root)
    nameEntry.place(150, 300, 500, 50)
    # *************************************************************************

    passwordLabel = tk.Label(root,text="Enter Password:", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=150,y=460)

    # *************************** Password demo *******************************
    #passwordEntry = tk.Entry(root, font=("Comic Sans MS", 20), show = "*")
    #passwordEntry.place(x = 150, y = 500, width = 500, height = 50)
    passwordEntry = PasswordEntry(root)
    passwordEntry.place(150, 500, 500, 50)
    # *************************************************************************

    loginButton = tk.Button(root, text="Login", font=("Comic Sans MS", 15), command = lambda: chooseDisplay(nameEntry.get(), passwordEntry.get()))
    loginButton.place(x = 350, y = 600, width = 100, height = 50)

    signupButton = tk.Button(root, text="Sign Up", font=("Comic Sans MS", 15), command = lambda: signup())
    signupButton.place(x = 350, y = 675, width = 100, height = 50)

    root.mainloop()

main() # runs program
# %%
