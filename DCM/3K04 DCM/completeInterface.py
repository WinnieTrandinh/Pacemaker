#!/usr/bin/env python
# coding: utf-8

# In[48]:

# libraries
import tkinter as tk
import random
import matplotlib.pyplot as plt
import numpy as np
from Serial import *
from itertools import count
from matplotlib.animation import FuncAnimation
import time



# stores information from text files
class User:
    def __init__(self, name, password, AOO, VOO, LRL, AAI, VVI, hys, DOO, DOOR, DDDR):
        # FIELDS
        self.name = name
        self.password = password
        self.AOO = AOO
        self.VOO = VOO
        self.LRL = LRL
        self.AAI = AAI
        self.VVI = VVI
        self.hys = hys
        self.DOO = DOO
        self.DOOR = DOOR
        self.DDDR = DDDR

    # MODIFIERS
    def change_name(self, new_name):
        self.name = new_name

    def change_password(self, new_password):
        self.password = new_password

    def change_AOO(self, new_AOO):
        self.AOO = new_AOO

    def change_VOO(self, new_VOO):
        self.VOO = new_VOO

    def change_AAI(self, new_AAI):
        self.AOO = new_AAI

    def change_VVI(self, new_VVI):
        self.VVI = new_VVI

# global variables
user_id = 0
user_list = []
pacemakerNumber = [1234,5453,6789,5809,2354,1765,3490,5692,3745,6890]
default_AOO = [1000,10]
default_VOO = [1000, 10]
default_LRL = [1000]
default_hys = [4000]
default_AAI = [400, 0.5]
default_VVI = [3.5]
default_DOO = [500, 0.1 , 20, 8, 500]
default_DOOR = [300]
default_DDDR = [300]

global pacemakerConnected
pacemakerConnected = True

global run
run = True
serial = Serial("COM4")

# stores textfile info in User class object
with open("pacemaker_users.txt") as i:
    names = i.readlines()
    names = [x.strip() for x in names]

with open("pacemaker_passwords.txt") as i:
    password_list = i.readlines()
    password_list = [x.strip() for x in password_list]

def read_file(fileName):
    out = []

    with open(fileName) as i:
        out = i.readlines()

    for i in range(0, len(out)):
        out [i] = list(out[i].split(", "))

    return out


    if (response[0] == 0):
        connectOrNot = False

# debugging
for i in user_list:
    print(i.name + i.password)

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

# global variables to run tkinter objects
root = tk.Tk()
HEIGHT = 800
WIDTH = 800
canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
canvas.pack()

def connection(selec, val):
    response = serial.updateParam(selec, val)
    if (response[0] == 0):
        pacemakerConnected = False

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
        user_list.append(User(name.get(), confirmPassword.get(), default_AOO, default_VOO, default_LRL, default_AAI, default_VVI, default_hys, default_DOO, default_DOOR, default_DDDR))
        f = open("pacemaker_users.txt", "a")
        f.write(name.get() + "\n")
        f.close

        f = open("pacemaker_passwords.txt", "a")
        f.write(confirmPassword.get() + "\n")
        f.close

        with open('pacemaker_AOO.txt', 'a') as f:
            for i in range(0, len(default_AOO)):
                if (i == (len(default_AOO) - 1)):
                    f.write("%s" % default_AOO[i])
                else:
                    f.write("%s, " % default_AOO[i])
            f.write("\n")

        with open('pacemaker_VOO.txt', 'a') as f:
            for i in range(0, len(default_VOO)):
                if (i == (len(default_VOO) - 1)):
                    f.write("%s" % default_VOO[i])
                else:
                    f.write("%s, " % default_VOO[i])
            f.write("\n")

        with open('pacemaker_AAI.txt', 'a') as f:
            for i in range(0, len(default_AAI)):
                if (i == (len(default_AAI) - 1)):
                    f.write("%s" % default_AAI[i])
                else:
                    f.write("%s, " % default_AAI[i])

            f.write("\n")

        with open('pacemaker_VVI.txt', 'a') as f:
            for i in range(0, len(default_VVI)):
                if (i == (len(default_VVI) - 1)):
                    f.write("%s" % default_VVI[i])
                else:
                    f.write("%s, " % default_VVI[i])

            f.write("\n")

        with open('pacemaker_DOO.txt', 'a') as f:
            for i in range(0, len(default_DOO)):
                if (i == (len(default_DOO) - 1)):
                    f.write("%s" % default_DOO[i])
                else:
                    f.write("%s, " % default_DOO[i])
            f.write("\n")

        with open('pacemaker_DOOR.txt', 'a') as f:
            for i in range(0, len(default_DOOR)):
                if (i == (len(default_DOOR) - 1)):
                    f.write("%s" % default_DOOR[i])
                else:
                    f.write("%s, " % default_DOOR[i])
                f.write("\n")

            with open('pacemaker_DDDR.txt', 'a') as f:
                for i in range(0, len(default_DDDR)):
                    if (i == (len(default_DDDR) - 1)):
                        f.write("%s" % default_DDDR[i])
                    else:
                        f.write("%s, " % default_DDDR[i])
                f.write("\n")

            with open('pacemaker_hys.txt', 'a') as f:
                for i in range(0, len(default_hys)):
                    if (i == (len(default_hys) - 1)):
                        f.write("%s" % default_hys[i])
                    else:
                        f.write("%s, " % default_hys[i])
                f.write("\n")

            with open('pacemaker_LRL.txt', 'a') as f:
                for i in range(0, len(default_LRL)):
                    if (i == (len(default_LRL) - 1)):
                        f.write("%s" % default_LRL[i])
                    else:
                        f.write("%s, " % default_LRL[i])
                f.write("\n")

        root.after(250, signupWindow.destroy())

def chooseDisplay(username, password):
    incorrectPassLabel = tk.Label(root, bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)

    for i in range(0, len(user_list)):
        flag = 0

        if (user_list[i].name == username and user_list[i].password == password):
            incorrectPassLabel = tk.Label(root, text = "Welcome!", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
            flag = 1
            # ********************************************* window demo ***********************************************************

            pacingModeWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
            pacingModeWindow.title("Mode Menu")
            pacingModeWindow.resizable(0, 0)
            pacingModeWindow.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, (root.winfo_screenwidth()/2) - (WIDTH/2), (root.winfo_screenheight()/2) - (HEIGHT/2)))
            menu1(pacingModeWindow)

            global user_id
            user_id = i

            break

        if(username == user_list[i].name and password != user_list[i].password and flag == 0):
            incorrectPassLabel = tk.Label(root, text = "Incorrect Username or Password!", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
            flag = 1
        if(username != user_list[i].name and flag == 0):
            incorrectPassLabel = tk.Label(root, text = "Incorrect Username or Password!", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
            flag = 1

def menu1(pacingModeWindow):
    for w in pacingModeWindow.winfo_children():
        w.destroy()

    pacingLabel = tk.Label(pacingModeWindow, text = "Pacing Modes", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 75, width = 500, height = 50)


    if(pacemakerConnected == 0):
        pacemakerLabel = tk.Label(pacingModeWindow, text = "Pacemaker " + str(pacemakerNumber[user_id]) +  " Connected", bg = '#FF0000', font = ("Comic Sans MS", 10)).place(x = 550, y = 650, width = 200, height = 50)
    elif(pacemakerConnected == 1):
        pacemakerLabel = tk.Label(pacingModeWindow, text = "Pacemaker " + str(pacemakerNumber[user_id]) +  " Connected", bg = '#00FF00', font = ("Comic Sans MS", 10)).place(x = 550, y = 650, width = 200, height = 50)

    AOOButton = tk.Button(pacingModeWindow, text="AOO", font=("Comic Sans MS", 15),command = lambda:dataValuesAOO(pacingModeWindow, "AOO", "no"))
    AOOButton.place(x = 250, y = 175, width = 300, height = 50)

    VOOButton = tk.Button(pacingModeWindow, text="VOO", font=("Comic Sans MS", 15),command = lambda:dataValuesVOO(pacingModeWindow, "VOO", "no"))
    VOOButton.place(x = 250, y = 300, width = 300, height = 50)

    AAIButton = tk.Button(pacingModeWindow, text="AAI", font=("Comic Sans MS", 15),command = lambda:dataValuesAAI1(pacingModeWindow, "AAI", "no"))
    AAIButton.place(x = 250, y = 425, width = 300, height = 50)

    VVIButton = tk.Button(pacingModeWindow, text="VVI", font=("Comic Sans MS", 15),command = lambda:dataValuesVVI1(pacingModeWindow, "VVI","no"))
    VVIButton.place(x = 250, y = 550, width = 300, height = 50)

    DOOButton = tk.Button(pacingModeWindow, text="DOO", font=("Comic Sans MS", 15),command = lambda:dataValuesDOO1(pacingModeWindow, "DOO", "no"))
    DOOButton.place(x = 250, y = 675, width = 300, height = 50)

    nextButton = tk.Button(pacingModeWindow, text = "->", font = ("Comic Sans MS", 15), command = lambda: menu2(pacingModeWindow))
    nextButton.place(x = 750, y = 20, width = 30, height = 50)

def menu2(pacingModeWindow):
    for w in pacingModeWindow.winfo_children():
        w.destroy()

    pacingLabel = tk.Label(pacingModeWindow, text = "Pacing Modes", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 75, width = 500, height = 50)
    if(pacemakerConnected == 0):
        pacemakerLabel = tk.Label(pacingModeWindow, text = "Pacemaker " + str(pacemakerNumber[i]) +  " Connected", bg = '#FF0000', font = ("Comic Sans MS", 10)).place(x = 550, y = 650, width = 200, height = 50)
    elif(pacemakerConnected == 1):
        pacemakerLabel = tk.Label(pacingModeWindow, text = "Pacemaker " + str(pacemakerNumber[i]) +  " Connected", bg = '#00FF00', font = ("Comic Sans MS", 10)).place(x = 550, y = 650, width = 200, height = 50)

    AOOButton = tk.Button(pacingModeWindow, text="AOOR", font=("Comic Sans MS", 15),command = lambda:dataValuesAOOR1(pacingModeWindow, "AOOR", "no"))
    AOOButton.place(x = 250, y = 175, width = 300, height = 50)

    VOOButton = tk.Button(pacingModeWindow, text="VOOR", font=("Comic Sans MS", 15),command = lambda:dataValuesVOOR1(pacingModeWindow, "VOOR", "no"))
    VOOButton.place(x = 250, y = 300, width = 300, height = 50)

    AAIButton = tk.Button(pacingModeWindow, text="AAIR", font=("Comic Sans MS", 15),command = lambda:dataValuesAAI1(pacingModeWindow, "AAIR", "no"))
    AAIButton.place(x = 250, y = 425, width = 300, height = 50)

    VVIButton = tk.Button(pacingModeWindow, text="VVIR", font=("Comic Sans MS", 15),command = lambda:dataValuesVVI1(pacingModeWindow, "VVIR", "no"))
    VVIButton.place(x = 250, y = 550, width = 300, height = 50)

    DOOButton = tk.Button(pacingModeWindow, text="DOOR", font=("Comic Sans MS", 15),command = lambda:dataValuesDOOR(pacingModeWindow, "DOOR", "no"))
    DOOButton.place(x = 250, y = 675, width = 300, height = 50)

    nextButton = tk.Button(pacingModeWindow, text = "->", font = ("Comic Sans MS", 15), command = lambda: menu3(pacingModeWindow))
    nextButton.place(x = 750, y = 20, width = 30, height = 50)

    prevButton = tk.Button(pacingModeWindow, text = "<-", font = ("Comic Sans MS", 15), command = lambda: menu1(pacingModeWindow))
    prevButton.place(x = 50, y = 20, width = 30, height = 50)

def menu3(pacingModeWindow):
    for w in pacingModeWindow.winfo_children():
        w.destroy()

    pacingLabel = tk.Label(pacingModeWindow, text = "Pacing Modes", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 75, width = 500, height = 50)
    if(pacemakerConnected == 0):
        pacemakerLabel = tk.Label(pacingModeWindow, text = "Pacemaker " + str(pacemakerNumber[i]) +  " Connected", bg = '#FF0000', font = ("Comic Sans MS", 10)).place(x = 550, y = 650, width = 200, height = 50)
    elif(pacemakerConnected == 1):
        pacemakerLabel = tk.Label(pacingModeWindow, text = "Pacemaker " + str(pacemakerNumber[i]) +  " Connected", bg = '#00FF00', font = ("Comic Sans MS", 10)).place(x = 550, y = 650, width = 200, height = 50)

    AOOButton = tk.Button(pacingModeWindow, text="DDDR", font=("Comic Sans MS", 15),command = lambda:dataValuesDDDR(pacingModeWindow, "DDDR", "no"))
    AOOButton.place(x = 250, y = 175, width = 300, height = 50)

    prevButton = tk.Button(pacingModeWindow, text = "<-", font = ("Comic Sans MS", 15), command = lambda: menu2(pacingModeWindow))
    prevButton.place(x = 50, y = 20, width = 30, height = 50)

def changeParameter(i, new_value, window, mode, title, label):
    if (mode == "AOO"):
        user_list[user_id].AOO[i] = new_value.get()

        with open("pacemaker_AOO.txt", "r") as file:
            info = file.readlines()

        info[user_id] = ''
        for i in range(0, len(user_list[user_id].AOO)):
            info[user_id] += str(user_list[user_id].AOO[i])
            if (i != len(user_list[user_id].AOO) - 1):
                info[user_id] += ", "

        info[user_id] += "\n"

        with open("pacemaker_AOO.txt", "w") as file:
            file.writelines(info)

        dataValuesAOO(window, title, "no")

    elif (mode == "VOO"):
        user_list[user_id].VOO[i] = new_value.get()

        with open("pacemaker_VOO.txt", "r") as file:
            info = file.readlines()

        info[user_id] = ''
        for i in range(0, len(user_list[user_id].VOO)):
            info[user_id] += str(user_list[user_id].VOO[i])
            if (i != len(user_list[user_id].VOO) - 1):
                info[user_id] += ", "

        info[user_id] += "\n"

        with open("pacemaker_VOO.txt", "w") as file:
            file.writelines(info)

        dataValuesVOO(window, title, "no")

    elif (mode == "LRL"):
        user_list[user_id].LRL[i] = new_value.get()

        with open("pacemaker_LRL.txt", "r") as file:
            info = file.readlines()

        info[user_id] = ''
        for i in range(0, len(user_list[user_id].LRL)):
            info[user_id] += str(user_list[user_id].LRL[i])
            if (i != len(user_list[user_id].LRL) - 1):
                info[user_id] += ", "

        info[user_id] += "\n"

        with open("pacemaker_LRL.txt", "w") as file:
            file.writelines(info)

        if (mode[0] == 'A'):
            dataValuesAOO(window, title, "no")
        elif (mode[0] == 'V'):
            dataValuesVOO(window, title, "no")

    elif (mode == "AAI"):
        user_list[user_id].AAI[i] = new_value.get()

        with open("pacemaker_AAI.txt", "r") as file:
            info = file.readlines()

        info[user_id] = ''
        for i in range(0, len(user_list[user_id].AAI)):
            info[user_id] += str(user_list[user_id].AAI[i])
            if (i != len(user_list[user_id].AAI) - 1):
                info[user_id] += ", "

        info[user_id] += "\n"

        with open("pacemaker_AAI.txt", "w") as file:
            file.writelines(info)

        dataValuesAAI2(window, title, "no")

    elif (mode == "VVI"):
        user_list[user_id].VVI[i] = new_value.get()

        with open("pacemaker_VVI.txt", "r") as file:
            info = file.readlines()

        info[user_id] = ''
        for i in range(0, len(user_list[user_id].VVI)):
            info[user_id] += str(user_list[user_id].VVI[i])
            if (i != len(user_list[user_id].VVI) - 1):
                info[user_id] += ", "

        info[user_id] += "\n"

        with open("pacemaker_VVI.txt", "w") as file:
            file.writelines(info)

        dataValuesVVI2(window, title, "no")

    elif (mode == "hys"):
        user_list[user_id].hys[i] = new_value.get()

        with open("pacemaker_hys.txt", "r") as file:
            info = file.readlines()

        info[user_id] = ''
        for i in range(0, len(user_list[user_id].hys)):
            info[user_id] += str(user_list[user_id].hys[i])
            if (i != len(user_list[user_id].hys) - 1):
                info[user_id] += ", "

        info[user_id] += "\n"

        with open("pacemaker_VVI.txt", "w") as file:
            file.writelines(info)

        if (mode[0] == 'A'):
            dataValuesAAI2(window, title, "no")
        elif (mode[0] == 'V'):
            dataValuesVVI2(window, mode, "no")

    elif (mode == "DOO"):
        user_list[user_id].DOO[i] = new_value.get()

        with open("pacemaker_DOO.txt", "r") as file:
            info = file.readlines()

        info[user_id] = ''
        for i in range(0, len(user_list[user_id].DOO)):
            info[user_id] += str(user_list[user_id].DOO[i])
            if (i != len(user_list[user_id].DOO) - 1):
                info[user_id] += ", "

        info[user_id] += "\n"

        with open("pacemaker_DOO.txt", "w") as file:
            file.writelines(info)

        if (i == 0 or i == 1 or i == 2):
            dataValuesDOO1(window, title, "no")
        elif (i == 3 or i == 4):
            dataValuesDOO2(window, title, "no")

    elif (mode == "DOOR"):
        user_list[user_id].DOOR[i] = new_value.get()

        with open("pacemaker_DOOR.txt", "r") as file:
            info = file.readlines()

        info[user_id] = ''
        for i in range(0, len(user_list[user_id].DOOR)):
            info[user_id] += str(user_list[user_id].DOOR[i])
            if (i != len(user_list[user_id].DOOR) - 1):
                info[user_id] += ", "

        info[user_id] += "\n"

        with open("pacemaker_DOOR.txt", "w") as file:
            file.writelines(info)

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
    try:
        if (mode == "DOO" and i == 1) or (mode == "VVI" and i == 0) or (mode == "AAI" and i == 1):
            if (float(new_value.get()) > max or float(new_value.get()) < min):
                invalidEntry = tk.Label(window, text = "Out of Range",bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x = x_in + 320, y = y_in)
            else:
                changeParameter(i, new_value, window, mode, title, label)
                serial.updateParam(paramNumber,new_value)
                print(mode)
        else:
            if (int(new_value.get()) > max or int(new_value.get()) < min):
                invalidEntry = tk.Label(window, text = "Out of Range",bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x = x_in + 320, y = y_in)
            else:
                changeParameter(i, new_value, window, mode, title, label)
                serial.updateParam(paramNumber,new_value)

    except ValueError:
        invalidEntry = tk.Label(window, text = "Invalid Entry",bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x = x_in + 320, y = y_in)

def graph(window):
    #This part goes in the chooseDisplay function where the other buttons are
    atrGraphButton = tk.Button(window, text="Atrium Graph", font=("Comic Sans MS", 15),command = lambda:atrGraph(window))
    atrGraphButton.place(x = 830, y = 325, width = 300, height = 50)

    venGraphButton = tk.Button(window, text="Ventricle Graph", font=("Comic Sans MS", 15),command = lambda:venGraph(window))
    venGraphButton.place(x = 830, y = 425, width = 300, height = 50)

    dualGraphButton = tk.Button(window, text="Display Both Graphs", font=("Comic Sans MS", 15),command = lambda:dualGraph(window))
    dualGraphButton.place(x = 830, y = 525, width = 300, height = 50)


def randValues(arr):
    i = 0
    while i < 8:
        i = i + 1
        arr.append(random.randint(0,1))

    # counter = 0
    # while counter < 10:
    #     counter = counter + 1
    #for i in range(7):
    # i = 0
    # i = i + 1
    # if(i == 0):
    #     # arr.append(85)
    #     arr.append(random.randint(0,1))
    # elif(i == 1):
    #     # arr.append(next(ind))
    #     arr.append(random.randint(0,1))
    # elif(i == 2):
    #     arr.append(random.randint(0,1))
    # elif(i == 3):
    #     # arr.append(1)
    #     arr.append(random.randint(0,1))
    # elif(i == 4):
    #     arr.append(random.randint(0,1))
    # elif(i == 5):
    #     # arr.append(1)
    #     arr.append(random.randint(0,1))
    # elif(i == 6):
    #     # arr.append(42)
    #     arr.append(random.randint(0,1))
    # if(i == 6):
    #     i = 0

def runFalse():
    global run
    run = False

def pulse(atrium, ventricle, window):
    maxSize = 200
    sampleRate = 0.0000001
    dataA = [ [0]*2 for size in range(0) ]
    dataV = [ [0]*2 for size in range(0) ]

    display = True

    run = True
    while(run):
        newData = serial.requestEgram()

        plt.cla()
        #plt.axis( [time[pointer-1]-(sampleRate*maxSize), time[pointer-1], 0, 5] )

        #print("newData: ", newData)
        if newData[0] == 0:
            display = False

        time = newData[1]

        if atrium:
            signal = newData[2]
            paced = newData[3]

            if paced:
                signal = (float)(user_list[user_id].AOO[0])/1000
            elif (signal < 2.2 or signal > 2.7):
                signal = 4.5
            else:
                signal = 0

            if len(dataA) < maxSize:
                dataA.append([time, signal])
            else:
                dataA.pop(0)
                dataA.append([time, signal])
            #print("data: ", data)

            timeA =  [x[0] for x in dataA ]
            signalA =  [y[1] for y in dataA]
            plt.plot(timeA, signalA, 'r', label="Atrium")
            plt.axis( [timeA[len(timeA)-1]-12, timeA[len(timeA)-1], 0, 5] )

        if ventricle:
            signal = newData[4]
            paced = newData[5]

            if paced:
                signal = (float)(user_list[user_id].VOO[0])/1000
            elif (signal < 2.2 or signal > 2.7):
                signal = 4.5
            else:
                signal = 0

            if len(dataV) < maxSize:
                dataV.append([time, signal])
            else:
                dataV.pop(0)
                dataV.append([time, signal])
            #print("data: ", data)

            timeV =  [x[0] for x in dataV ]
            signalV =  [y[1] for y in dataV]
            plt.plot(timeV, signalV, 'b', label="Ventricle")
            plt.axis( [timeV[len(timeV)-1]-12, timeV[len(timeV)-1], 0, 5] )

        plt.legend(loc="upper left")
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude (V)')
        plt.gcf().axes[0].xaxis.get_major_formatter().set_scientific(False)
        plt.pause(sampleRate)

        quitButton = tk.Button(window, text="Quit", font=("Comic Sans MS", 15), command = runFalse())
        quitButton.place(x = 830, y = 525, width = 300, height = 50) 
    plt.show()



def atrGraph(window):
    atrAni = FuncAnimation(plt.gcf(),pulse(1,0, window), interval = 100)


def venGraph(window):
    venAni = FuncAnimation(plt.gcf(),pulse(0,1, window), interval = 100)


def dualGraph(window):
    dualAni = FuncAnimation(plt.gcf(),pulse(1,1, window), interval = 100)


# MODES
def LRL(window, title):
    # Lower Rate
    lowerRateLabel = tk.Label(window, text = "Lower Rate Limit: " + str(user_list[user_id].LRL[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=50)
    LRRangeLabel =  tk.Label(window, text = "(Range: 343 - 2000 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=85)

    lowerRateEntry = tk.Entry(window, font=("Comic Sans MS", 20))
    lowerRateEntry.place(x = 50, y = 140, width = 500, height = 50)

    lowerRateChangeButton = tk.Button(window, text="Change", font=("Comic Sans MS", 15), command = lambda:checkParameter(343, 2000, 0, lowerRateEntry, window, 50, 215, "LRL", title, lowerRateLabel))
    lowerRateChangeButton.place(x = 50, y = 215, width = 300, height = 50)

def hys(window, title):
    #hysteris
    hysLabel = tk.Label(window, text = "Hystersis: " + str(user_list[user_id].hys[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=50)
    hysRangeLabel =  tk.Label(window, text = "(Range: 343 - 2000 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=85)

    hysRateEntry = tk.Entry(window, font=("Comic Sans MS", 20))
    hysRateEntry.place(x = 50, y = 140, width = 500, height = 50)

    hysRateChangeButton = tk.Button(window, text="Change", font=("Comic Sans MS", 15), command = lambda:checkParameter(343, 2000, 0, hysRateEntry, window, 50, 215, "hys", title, hysLabel))
    hysRateChangeButton.place(x = 50, y = 215, width = 300, height = 50)

def dataValuesAOO(oldWin, title, delCom):
    AOOWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    AOOWindow.title(title)

    graph(AOOWindow)

    if (delCom == "yes"):
        oldWin.destroy()

    print(user_id)
    print(user_list[user_id].AOO)

    connection(17,3)
    connection(18,1)
    connection(19,1)
    connection(15,0)

    # Lower Rate
    LRL(AOOWindow, title) # Lower Rate Limit

    # Atrial Amplitude
    amplitudeLabel = tk.Label(AOOWindow, text = "Atrial Amplitude: " + str(user_list[user_id].AOO[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=325)
    amplitudeRangeLabel =  tk.Label(AOOWindow, text = "(Range: 500-5000mV)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=360)

    amplitudeEntry = tk.Entry(AOOWindow, font=("Comic Sans MS", 20))
    amplitudeEntry.place(x = 50, y = 400, width = 500, height = 50)

    amplitudeChangeButton = tk.Button(AOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(500, 5000, 1, amplitudeEntry, AOOWindow, 50, 475, "AOO", title, amplitudeLabel, 2))
    amplitudeChangeButton.place(x = 50, y = 475, width = 300, height = 50)

    # Atrial Pulse Width
    pWLabel = tk.Label(AOOWindow, text = "Atrial Pulse Width: " + str(user_list[user_id].AOO[1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=600)
    pWLabel =  tk.Label(AOOWindow, text = "(Range: 1-30ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=635)

    pWEntry = tk.Entry(AOOWindow, font=("Comic Sans MS", 20))
    pWEntry.place(x = 50, y = 675, width = 500, height = 50)

    pwEntryChangeButton = tk.Button(AOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(1, 30, 2, pWEntry, AOOWindow, 50, 750, "AOO", title, pWLabel, 3))
    pwEntryChangeButton.place(x = 50, y = 750, width = 300, height = 50)

    # Switch Button for AAI Window
    if (title == "DOOR"):
        switchButton = tk.Button(AOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesVOO(AOOWindow, title, "yes"))
        switchButton.place(x = 1100, y = 800, width = 300, height = 50)
    elif (title == "AOOR"):
        switchButton = tk.Button(AOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO1(AOOWindow, title, "yes"))
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

    connection(17,3)
    connection(18,1)
    connection(19,2)
    connection(15,0)

    '''
    lowerRateLabel = tk.Label(VOOWindow, text = "Ventrical Lower Rate: " + str(user_list[user_id].VOO[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=50)
    LRRangeLabel =  tk.Label(VOOWindow, text = "(Range: 343 - 2000 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=85)

    lowerRateEntry_1 = tk.Entry(VOOWindow, font=("Comic Sans MS", 20))
    lowerRateEntry_1.place(x = 50, y = 140, width = 500, height = 50)

    lowerRateChangeButton = tk.Button(VOOWindow, text="Change", font=("Comic Sans MS", 15), command = lambda:checkParameter(343, 2000, 0, lowerRateEntry_1, VOOWindow, 50, 215, "VOO", title, lowerRateLabel,1))
    lowerRateChangeButton.place(x = 50, y = 215, width = 300, height = 50)
    '''

    # Lower Rate Limit
    LRL(VOOWindow, title)

    # Ventricle Amplitude
    amplitudeLabel = tk.Label(VOOWindow, text = "Ventricle Amplitude: " + str(user_list[user_id].VOO[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=325)
    amplitudeRangeLabel =  tk.Label(VOOWindow, text = "(Range: 500-5000mV)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=360)

    amplitudeEntry = tk.Entry(VOOWindow, font=("Comic Sans MS", 20))
    amplitudeEntry.place(x = 50, y = 400, width = 500, height = 50)

    amplitudeChangeButton = tk.Button(VOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(500, 5000, 1, amplitudeEntry, VOOWindow, 50, 475, "VOO", title, amplitudeLabel,4))
    amplitudeChangeButton.place(x = 50, y = 475, width = 300, height = 50)

    # Ventricle Pulse Width
    pWLabel = tk.Label(VOOWindow, text = "Ventricle Pulse Width: " + str(user_list[user_id].VOO[2]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=600)
    pWLabel =  tk.Label(VOOWindow, text = "(Range: 1-30ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=635)

    pWEntry = tk.Entry(VOOWindow, font=("Comic Sans MS", 20))
    pWEntry.place(x = 50, y = 675, width = 500, height = 50)

    pwEntryChangeButton = tk.Button(VOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(1, 30, 2, pWEntry, VOOWindow, 50, 750, "VOO", title, pWLabel, 5))
    pwEntryChangeButton.place(x = 50, y = 750, width = 300, height = 50)

    # Switch Button for AAI Window
    if (title == "VOOR"):
        nextButton = tk.Button(VOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO1(VOOWindow, title, "yes"))
        nextButton.place(x = 1100, y = 800, width = 300, height = 50)
    elif (title == "DOOR"):
        nextButton = tk.Button(VOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO1(VOOWindow, title, "yes"))
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

def dataValuesAAI1(oldWin, title, delCom):
    AAIWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    AAIWindow.title(title)

    if (delCom == "yes"):
        oldWin.destroy()

    dataValuesAOO(AAIWindow, title, "yes")
    connection(17,1)
    connection(18,2)
    connection(19,1)
    connection(15,0)

def dataValuesAAI2(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    AAIWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    AAIWindow.title(title)

    graph(AAIWindow)

    connection(17,1)
    connection(18,2)
    connection(19,1)
    connection(15,0)

    hys(AAIWindow, title)

    # ARP
    ARPLabel = tk.Label(AAIWindow, text = "ARP: " + str(user_list[user_id].AAI[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=325)
    ARPLabel =  tk.Label(AAIWindow, text = "(Range: 150-500 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=360)

    ARPEntry = tk.Entry(AAIWindow, font=("Comic Sans MS", 20))
    ARPEntry.place(x = 50, y = 400, width = 500, height = 50)

    ARPEntryChangeButton_2 = tk.Button(AAIWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(150, 500, 0, ARPEntry, AAIWindow, 50, 475, "AAI", title, ARPLabel))
    ARPEntryChangeButton_2.place(x = 50, y = 475, width = 300, height = 50)

    ARPEntryChangeButton_2 = tk.Button(AAIWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(150, 500, 0, ARPEntry, AAIWindow, 50, 350, "AAI", title, ARPLabel, 7))
    ARPEntryChangeButton_2.place(x = 50, y = 350, width = 300, height = 50)

    # ASensitivity
    A_sensLabel = tk.Label(AAIWindow, text = "Atrial Sensitivity: " + str(user_list[user_id].AAI[1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=600)
    A_sensLabel =  tk.Label(AAIWindow, text = "(Range: 3 - 5 V)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=635)

    A_sensEntry = tk.Entry(AAIWindow, font=("Comic Sans MS", 20))
    A_sensEntry.place(x = 50, y = 675, width = 500, height = 50)

    A_sensEntryChangeButton_2 = tk.Button(AAIWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(3000, 5000, 1, A_sensEntry, AAIWindow, 50, 635, "AAI", title, A_sensLabel,8))
    A_sensEntryChangeButton_2.place(x = 50, y = 635, width = 300, height = 50)

    # goes to previous window
    if (title == 'AAIR'):
        nextButton = tk.Button(AAIWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO1(AAIWindow, title, "yes"))
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

    connection(17,2)
    connection(18,2)
    connection(19,2)
    connection(15,0)

def dataValuesVVI2(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    VVIWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    VVIWindow.title(title)

    hys(VVIWindow, title)
    graph(VVIWindow)

    connection(17,2)
    connection(18,2)
    connection(19,2)
    connection(15,0)

    '''
    # VRP
    VRPLabel = tk.Label(VVIWindow, text = "VRP: " + str(user_list[user_id].VVI[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=200)
    VRPLabel =  tk.Label(VVIWindow, text = "(Range: 150-500 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=235)

    VRPEntry = tk.Entry(VVIWindow, font=("Comic Sans MS", 20))
    VRPEntry.place(x = 50, y = 275, width = 500, height = 50)

    VRPEntryChangeButton_2 = tk.Button(VVIWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(150, 500, 0, VRPEntry, VVIWindow, 50, 350, "VVI", title, VRPLabel,7))
    VRPEntryChangeButton_2.place(x = 50, y = 350, width = 300, height = 50)
    '''

    # VSensitivity
    V_sensLabel = tk.Label(VVIWindow, text = "Ventricle Sensitivity: " + str(user_list[user_id].VVI[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=300)
    V_sensLabel =  tk.Label(VVIWindow, text = "(Range: 3-5 V)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=335)

    V_sensEntry = tk.Entry(VVIWindow, font=("Comic Sans MS", 20))
    V_sensEntry.place(x = 50, y = 375, width = 500, height = 50)

    V_sensEntryChangeButton_2 = tk.Button(VVIWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(3000, 5000, 1, V_sensEntry, VVIWindow, 50, 635, "VVI", title, V_sensLabel,9))
    V_sensEntryChangeButton_2.place(x = 50, y = 635, width = 300, height = 50)

    if (title == "VVIR" or title == "DDDR"):
        nextButton = tk.Button(VVIWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO1(VVIWindow, title, "yes"))
        nextButton.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton = tk.Button(VVIWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesVVI1(VVIWindow, title, "yes"))
        prevButton.place(x = 775, y = 800, width = 300, height = 50)
        prevButton.place(x = 775, y = 800, width = 300, height = 50)
    else:
        switchButton2 = tk.Button(VVIWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesVVI1(VVIWindow, title, "yes"))
        switchButton2.place(x = 1100, y = 800, width = 300, height = 50)

def dataValuesDOO1(oldWin, title, delCom):
    DOOWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    DOOWindow.title(title)

    graph(DOOWindow)

    if (delCom == "yes"):
        oldWin.destroy()

    connection(17,3)
    connection(18,1)
    connection(19,1)
    connection(15,0)

    # Maximum Sensor Rate Limit
    maxSenLabel= tk.Label(DOOWindow, text = "Maximum Sensor Rate Limit: " + str(user_list[user_id].DOO[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=50)
    RangeLabel =  tk.Label(DOOWindow, text = "(Range: 343 - 1200 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=85)

    maxSenEntry = tk.Entry(DOOWindow, font=("Comic Sans MS", 20))
    maxSenEntry.place(x = 50, y = 140, width = 500, height = 50)

    maxSenChangeButton = tk.Button(DOOWindow, text="Change", font=("Comic Sans MS", 15), command = lambda:checkParameter(343, 1200, 0, maxSenEntry, DOOWindow, 50, 215, "DOO", title, maxSenLabel,10))
    maxSenChangeButton.place(x = 50, y = 215, width = 300, height = 50)

    # Activity Threshold
    actLabel = tk.Label(DOOWindow, text = "Activity Threshold: " + str(user_list[user_id].DOO[1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=325)
    actRangeLabel =  tk.Label(DOOWindow, text = "(Range: 0.05 - 1.5 g)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=360)

    actEntry = tk.Entry(DOOWindow, font=("Comic Sans MS", 20))
    actEntry.place(x = 50, y = 400, width = 500, height = 50)

    actChangeButton = tk.Button(DOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(0.05, 1.5, 1, actEntry, DOOWindow, 50, 475, "DOO", title, actLabel,11))
    actChangeButton.place(x = 50, y = 475, width = 300, height = 50)

    # Reaction Time
    reactLabel = tk.Label(DOOWindow, text = "Reaction Time: " + str(user_list[user_id].DOO[2]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=600)
    reactLabel =  tk.Label(DOOWindow, text = "(Range: 10 - 50s)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=635)

    reactEntry = tk.Entry(DOOWindow, font=("Comic Sans MS", 20))
    reactEntry.place(x = 50, y = 675, width = 500, height = 50)

    reactEntryChangeButton = tk.Button(DOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(1, 30, 2, reactEntry, DOOWindow, 50, 750, "DOO", title, reactLabel,13))
    reactEntryChangeButton.place(x = 50, y = 750, width = 300, height = 50)

    if (title == "AOOR"):
        nextButton2 = tk.Button(DOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO2(DOOWindow, title, "yes"))
        nextButton2.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton2 = tk.Button(DOOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesAOO(DOOWindow, title, "yes"))
        prevButton2.place(x = 775, y = 800, width = 300, height = 50)
    elif (title == "AAIR"):
        nextButton2 = tk.Button(DOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO2(DOOWindow, title, "yes"))
        nextButton2.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton2 = tk.Button(DOOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesAAI2(DOOWindow, title, "yes"))
        prevButton2.place(x = 775, y = 800, width = 300, height = 50)
    elif (title == "VVIR" or title == "DDDR"):
        nextButton2 = tk.Button(DOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO2(DOOWindow, title, "yes"))
        nextButton2.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton2 = tk.Button(DOOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesVVI2(DOOWindow, title, "yes"))
        prevButton2.place(x = 775, y = 800, width = 300, height = 50)
    elif (title == "VOOR" or title == "DOOR"):
        nextButton2 = tk.Button(DOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO2(DOOWindow, title, "yes"))
        nextButton2.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton2 = tk.Button(DOOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesVOO(DOOWindow, title, "yes"))
        prevButton2.place(x = 775, y = 800, width = 300, height = 50)

    # goes to next window
    switchButton2 = tk.Button(DOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO2(DOOWindow, title, "yes"))
    switchButton2.place(x = 1100, y = 800, width = 300, height = 50)

def dataValuesDOO2(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    DOOWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    DOOWindow.title(title)

    graph(DOOWindow)

    connection(17,3)
    connection(18,1)
    connection(19,1)
    connection(15,0)

    # response
    responseLabel = tk.Label(DOOWindow, text = "Response Factor: " + str(user_list[user_id].DOO[3]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=200)
    responseLabel =  tk.Label(DOOWindow, text = "(Range: 1-16)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=235)

    responseEntry = tk.Entry(DOOWindow, font=("Comic Sans MS", 20))
    responseEntry.place(x = 50, y = 275, width = 500, height = 50)

    responseEntryChangeButton_2 = tk.Button(DOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(1, 16, 3, responseEntry, DOOWindow, 50, 350, "DOO", title, responseLabel,12))
    responseEntryChangeButton_2.place(x = 50, y = 350, width = 300, height = 50)

    # ASensitivity
    recovLabel = tk.Label(DOOWindow, text = "Recovery Time: " + str(user_list[user_id].DOO[4]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=475)
    recovLabel =  tk.Label(DOOWindow, text = "(Range: 120 - 960 s)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=510)

    recovEntry = tk.Entry(DOOWindow, font=("Comic Sans MS", 20))
    recovEntry.place(x = 50, y = 550, width = 500, height = 50)

    recovEntryChangeButton_2 = tk.Button(DOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(120, 960, 4, recovEntry, DOOWindow, 50, 635, "DOO", title, recovLabel,14))
    recovEntryChangeButton_2.place(x = 50, y = 635, width = 300, height = 50)

    # goes to previous window
    if (title == "DOOR"):
        nextButton = tk.Button(DOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOOR2(DOOWindow, title, "yes"))
        nextButton.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton = tk.Button(DOOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO1(DOOWindow, title, "yes"))
        prevButton.place(x = 775, y = 800, width = 300, height = 50)

    else:
        switchButton2 = tk.Button(DOOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO1(DOOWindow, title, "yes"))
        switchButton2.place(x = 1100, y = 800, width = 300, height = 50)

    '''
    elif (title == "DDDR"):
        nextButton = tk.Button(DOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDDDR2(DOOWindow, title, "yes"))
        nextButton.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton = tk.Button(DOOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO1(DOOWindow, title, "yes"))
        prevButton.place(x = 775, y = 800, width = 300, height = 50)
    '''

def dataValuesAOOR1(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    dataValuesAOO(tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1'), title, "yes")

    connection(17,3)
    connection(18,1)
    connection(19,1)
    connection(15,1)

def dataValuesVOOR1(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    dataValuesVOO(tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1'), title, "yes")

    connection(17,3)
    connection(18,1)
    connection(19,2)
    connection(15,1)

def dataValuesAAIR1(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    dataValuesAAI1(tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1'), title, "yes")

    connection(17,1)
    connection(18,2)
    connection(19,1)
    connection(15,1)

def dataValuesVVIR1(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    dataValuesVVI1(tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1'), title, "yes")

    connection(17,2)
    connection(18,2)
    connection(19,2)
    connection(15,1)

def dataValuesDOOR(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    dataValuesAOO(tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1'), title, "yes")

    connection(17,3)
    connection(18,1)
    connection(19,1)
    connection(15,1)

def dataValuesDOOR2(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    DOORWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    DOORWindow.title(title)

    graph(DOORWindow)

    connection(17,3)
    connection(18,1)
    connection(19,1)
    connection(15,1)

    responseLabel = tk.Label(DOORWindow, text = "Fixed Atrial Ventrical (AV) Delay: " + str(user_list[user_id].DOOR[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=200)
    responseLabel =  tk.Label(DOORWindow, text ="(Range: 70-300 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=235)

    responseEntry = tk.Entry(DOORWindow, font=("Comic Sans MS", 20))
    responseEntry.place(x = 50, y = 275, width = 500, height = 50)

    responseEntryChangeButton = tk.Button(DOORWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(70, 300, 0, responseEntry, DOORWindow, 50, 215, "DOOR", title, responseLabel,12))
    responseEntryChangeButton.place(x = 50, y = 350, width = 300, height = 50)

    switchButton2 = tk.Button(DOORWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO2(DOORWindow, title, "yes"))
    switchButton2.place(x = 1100, y = 800, width = 300, height = 50)

def dataValuesDDDR(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    dataValuesAAI1(tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1'), title, "yes")

    connection(17,3)
    connection(18,3)
    connection(19,3)
    connection(15,1)

def dataValuesDDDR2(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    DDDRWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    DDDRWindow.title(title)

    graph(DDDRWindow)

    connection(17,3)
    connection(18,3)
    connection(19,3)
    connection(15,1)

    responseLabel = tk.Label(DDDRWindow, text = "PVARP: " + str(user_list[user_id].DDDR[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=200)

    '''
    responseLabel = tk.Label(DDDRWindow, text = "PVARP: " + str(user_list[user_id].DDDR[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=200)
    responseLabel =  tk.Label(DDDRWindow, text ="(Range: 150 - 500 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=235)

    responseEntry = tk.Entry(DDDRWindow, font=("Comic Sans MS", 20))
    responseEntry.place(x = 50, y = 275, width = 500, height = 50)

    responseEntryChangeButton = tk.Button(DDDRWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(150, 500, 0, responseEntry, DDDRWindow, 50, 215, "DDDR", title, responseLabel,12))
    responseEntryChangeButton.place(x = 50, y = 350, width = 300, height = 50)

    switchButton2 = tk.Button(DDDRWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO2(DDDRWindow, title, "yes"))
    switchButton2.place(x = 1100, y = 800, width = 300, height = 50)
    '''

# main window
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
    AOO_list = read_file("pacemaker_AOO.txt")
    VOO_list = read_file("pacemaker_VOO.txt")
    LRL_list = read_file("pacemaker_LRL.txt")
    AAI_list = read_file("pacemaker_AAI.txt")
    VVI_list = read_file("pacemaker_VVI.txt")
    hys_list = read_file("pacemaker_hys.txt")
    DOO_list = read_file("pacemaker_DOO.txt")
    DOOR_list = read_file("pacemaker_DOOR.txt")
    DDDR_list = read_file("pacemaker_DDDR.txt")
    hys_list = read_file("pacemaker_hys.txt")

    global user_list
    user_list = []
    for i in range(0, len(names)):
        user_list.append(User(names[i], password_list[i], AOO_list[i], VOO_list[i], LRL_list[i], AAI_list[i], VVI_list[i], hys_list[i], DOO_list[i], DOOR_list[i], DDDR_list[i]))

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
