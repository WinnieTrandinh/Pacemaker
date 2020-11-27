#!/usr/bin/env python
# coding: utf-8

# In[48]:

# libraries
import tkinter as tk
import random
#import matplotlib.pyplot as plt

# stores information from text files
class User:
    def __init__(self, name, password, AOO, VOO, AAI, VVI, DOO, DOOR, DDDR):
        # FIELDS
        self.name = name
        self.password = password
        self.AOO = AOO
        self.VOO = VOO
        self.AAI = AAI
        self.VVI = VVI
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
user_list = []
user_id = 0
pacemakerNumber = [1234,5453,6789,5809,2354,1765,3490,5692,3745,6890]
default_AOO = [1000, 1000, 10]
default_VOO = [1000, 1000, 10]
default_AAI = [400, 3500]
default_VVI = [400, 3500]
default_DOO = [500, 1.0, 20, 8, 500]
default_DOOR = [300]
default_DDDR = [300]

# stores textfile info in User class object
with open("pacemaker_users.txt") as i:
    names = i.readlines()
    names = [x.strip() for x in names]

with open("pacemaker_passwords.txt") as i:
    password_list = i.readlines()
    password_list = [x.strip() for x in password_list]

with open("pacemaker_AOO.txt") as i:
    AOO_list = i.readlines()

    for i in range(0, len(AOO_list)):
        AOO_list[i] = list(AOO_list[i].split(", "))

with open("pacemaker_VOO.txt") as i:
    VOO_list = i.readlines()

    for i in range(0, len(VOO_list)):
        VOO_list[i] = list(VOO_list[i].split(", "))

with open("pacemaker_AAI.txt") as i:
    AAI_list = i.readlines()

    for i in range(0, len(AAI_list)):
        AAI_list[i] = list(AAI_list[i].split(", "))

with open("pacemaker_VVI.txt") as i:
    VVI_list = i.readlines()

    for i in range(0, len(VVI_list)):
        VVI_list[i] = list(VVI_list[i].split(", "))

with open("pacemaker_DOO.txt") as i:
    DOO_list = i.readlines()

    for i in range(0, len(DOO_list)):
        DOO_list[i] = list(DOO_list[i].split(", "))

with open("pacemaker_DOOR.txt") as i:
    DOOR_list = i.readlines()
    
    for i in range(0, len(DOOR_list)):
        DOOR_list[i] = list(DOOR_list[i].split())

with open("pacemaker_DDDR.txt") as i:
    DDDR_list = i.readlines()
    
    for i in range(0, len(DDDR_list)):
        DDDR_list[i] = list(DDDR_list[i].split())

for i in range(0, len(names)):
    user_list.append(User(names[i], password_list[i], AOO_list[i], VOO_list[i], AAI_list[i], VVI_list[i], DOO_list[i], DOOR_list[i], DDDR_list[i]))

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
        user_list.append(User(name.get(), confirmPassword.get()))
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

        root.after(250, signupWindow.destroy())

def chooseDisplay(username, password):
    incorrectPassLabel = tk.Label(root, bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
 
    for i in range(0, len(user_list)):
        flag = 0

        if (user_list[i].name == username and user_list[i].password == password):
            incorrectPassLabel = tk.Label(root, text = "Welcome!", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
            flag = 1
            # ********************************************* window demo ***********************************************************
            menu1(tk.Toplevel(root,  height = 0, width = 0, bg = '#FFB6C1'), i)

            break

        if(username == user_list[i].name and password != user_list[i].password and flag == 0):
            incorrectPassLabel = tk.Label(root, text = "Incorrect Username or Password!", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
            flag = 1
        if(username != user_list[i].name and flag == 0):
            incorrectPassLabel = tk.Label(root, text = "Incorrect Username or Password!", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
            flag = 1

def menu1(window, i):

    pacingModeWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    pacingModeWindow.title("Mode Menu")
    pacingModeWindow.resizable(0, 0)
    pacingModeWindow.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, (root.winfo_screenwidth()/2) - (WIDTH/2), (root.winfo_screenheight()/2) - (HEIGHT/2)))

    window.destroy()

    pacingLabel = tk.Label(pacingModeWindow, text = "Pacing Modes", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 75, width = 500, height = 50)
    pacemakerLabel = tk.Label(pacingModeWindow, text = "Pacemaker " + str(pacemakerNumber[i]) +  " Connected", bg = '#00FF00', font = ("Comic Sans MS", 10)).place(x = 550, y = 650, width = 200, height = 50)

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

    nextButton = tk.Button(pacingModeWindow, text = "->", font = ("Comic Sans MS", 15), command = lambda: menu2(pacingModeWindow, i))
    nextButton.place(x = 750, y = 20, width = 30, height = 50)

def menu2(window, i):
    pacingModeWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    pacingModeWindow.title("Mode Menu")
    pacingModeWindow.resizable(0, 0)
    pacingModeWindow.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, (root.winfo_screenwidth()/2) - (WIDTH/2), (root.winfo_screenheight()/2) - (HEIGHT/2)))

    window.destroy()

    pacingLabel = tk.Label(pacingModeWindow, text = "Pacing Modes", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 75, width = 500, height = 50)
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

    nextButton = tk.Button(pacingModeWindow, text = "->", font = ("Comic Sans MS", 15), command = lambda: menu3(pacingModeWindow, i))
    nextButton.place(x = 750, y = 20, width = 30, height = 50)

    prevButton = tk.Button(pacingModeWindow, text = "<-", font = ("Comic Sans MS", 15), command = lambda: menu1(pacingModeWindow, i))
    prevButton.place(x = 50, y = 20, width = 30, height = 50)

def menu3(window, i):
    pacingModeWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    pacingModeWindow.title("Mode Menu")
    pacingModeWindow.resizable(0, 0)
    pacingModeWindow.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, (root.winfo_screenwidth()/2) - (WIDTH/2), (root.winfo_screenheight()/2) - (HEIGHT/2)))

    window.destroy()

    pacingLabel = tk.Label(pacingModeWindow, text = "Pacing Modes", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 75, width = 500, height = 50)
    pacemakerLabel = tk.Label(pacingModeWindow, text = "Pacemaker " + str(pacemakerNumber[i]) +  " Connected", bg = '#00FF00', font = ("Comic Sans MS", 10)).place(x = 550, y = 650, width = 200, height = 50)

    AOOButton = tk.Button(pacingModeWindow, text="DDDR", font=("Comic Sans MS", 15),command = lambda:dataValuesDDDR(pacingModeWindow, "DDDR", "no"))
    AOOButton.place(x = 250, y = 175, width = 300, height = 50) 

    prevButton = tk.Button(pacingModeWindow, text = "<-", font = ("Comic Sans MS", 15), command = lambda: menu2(pacingModeWindow, i))
    prevButton.place(x = 50, y = 20, width = 30, height = 50)
    
def changeParameter(i, new_value, window, mode, title, label):
    if (mode == "AOO"):
        user_list[user_id].AOO[i] = new_value.get()
        with open("pacemaker_AOO.txt", "r") as file:
            info = file.readlines()

        for i in range(0, len(user_list[user_id].AOO)):
            info[user_id] = info[user_id] + (str(user_list[user_id].AOO[i]))
            
            if (i != (len(user_list[user_id].AOO) - 1)):
                info[user_id] = info[user_id] + ", "

        with open('pacemaker_AOO.txt', 'w') as f:
            f.writelines(info)

        dataValuesAOO(window, title, "no")

    elif (mode == "VOO"):
        user_list[user_id].VOO[i] = new_value.get()
        
        with open("pacemaker_VOO.txt", "r") as file:
            info = file.readlines()

        info[user_id] = ', '.join(user_list[user_id].VOO) + "\n"

        with open("pacemaker_VOO.txt", "w") as file:
            file.writelines(info)

        dataValuesVOO(window, title, "no")
        
    elif (mode == "AAI"):
        user_list[user_id].AAI[i] = new_value.get()
        
        with open("pacemaker_AAI.txt", "r") as file:
            info = file.readlines()

        info[user_id] = ', '.join(user_list[user_id].AAI) + "\n"

        with open("pacemaker_AAI.txt", "w") as file:
            file.writelines(info)
        
        dataValuesAAI2(window, title, "no")

    elif (mode == "VVI"):
        user_list[user_id].VVI[i] = new_value.get()

        with open("pacemaker_VVI.txt", "r") as file:
            info = file.readlines()

        info[user_id] = ', '.join(user_list[user_id].VVI) + "\n"

        with open("pacemaker_VVI.txt", "w") as file:
            file.writelines(info)

        dataValuesVVI2(window, title, "no")
        
    elif (mode == "DOO"):
        user_list[user_id].DOO[i] = new_value.get()

        with open("pacemaker_DOO.txt", "r") as file:
            info = file.readlines()

        info[user_id] = ', '.join(user_list[user_id].DOO) + "\n"

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

        info[user_id] = ''.join(user_list[user_id].DOOR) + "\n"

        with open("pacemaker_DOOR.txt", "w") as file:
            file.writelines(info)
        
        dataValuesDOOR2(window, title, "no")
    
    elif (mode == "DDDR"):
        user_list[user_id].DDDR[i] = new_value.get()

        with open("pacemaker_DDDR.txt", "r") as file:
            info = file.readlines()

        info[user_id] = ''.join(user_list[user_id].DDDR) + "\n"

        with open("pacemaker_DDDR.txt", "w") as file:
            file.writelines(info)
        
        dataValuesDDDR2(window, title, "no")

    window.destroy()

def checkParameter(min, max, i, new_value, window, x_in, y_in, mode, title, label):
    try:
        if (mode == "DOO" and i == 1):
            if (float(new_value.get()) > max or float(new_value.get()) < min):
                invalidEntry = tk.Label(window, text = "Out of Range",bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x = x_in + 320, y = y_in)
            else:
                changeParameter(i, new_value, window, mode, title, label)
                print(mode)

        else:
            if (int(new_value.get()) > max or int(new_value.get()) < min):
                invalidEntry = tk.Label(window, text = "Out of Range",bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x = x_in + 320, y = y_in)
            else:
                changeParameter(i, new_value, window, mode, title, label)
    except ValueError:
        invalidEntry = tk.Label(window, text = "Invalid Entry",bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x = x_in + 320, y = y_in)

def graph(window):
    #This part goes in the chooseDisplay function where the other buttons are
    atrGraphButton = tk.Button(window, text="Atrium Graph", font=("Comic Sans MS", 15),command = lambda:atrGraph())
    atrGraphButton.place(x = 830, y = 325, width = 300, height = 50)
                
    venGraphButton = tk.Button(window, text="Ventricle Graph", font=("Comic Sans MS", 15),command = lambda:venGraph())
    venGraphButton.place(x = 830, y = 425, width = 300, height = 50)

    dualGraphButton = tk.Button(window, text="Display Both Graphs", font=("Comic Sans MS", 15),command = lambda:dualGraph())
    dualGraphButton.place(x = 830, y = 525, width = 300, height = 50)

def atrGraph(): 
    atrValues = np.random.normal(200000, 25000, 5000)
    plt.hist(atrValues, 50)
    plt.show()

def venGraph(): 
    venValues = np.random.normal(200000, 25000, 5000)
    plt.hist(venValues, 50)
    plt.show()

def dualGraph(): 
    atrValues = np.random.normal(200000, 25000, 5000)
    venValues = np.random.normal(200000, 25000, 5000)
    plt.hist(atrValues, 50)
    plt.hist(venValues, 50)
    plt.show()

# MODES
def dataValuesAOO(oldWin, title, delCom):
    AOOWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    AOOWindow.title(title)

    graph(AOOWindow)

    if (delCom == "yes"):
        oldWin.destroy()

    # Lower Rate
    lowerRateLabel = tk.Label(AOOWindow, text = "Atrial Lower Rate: " + str(user_list[user_id].AOO[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=50)
    LRRangeLabel =  tk.Label(AOOWindow, text = "(Range: 343 - 2000 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=85)

    lowerRateEntry_1 = tk.Entry(AOOWindow, font=("Comic Sans MS", 20))
    lowerRateEntry_1.place(x = 50, y = 140, width = 500, height = 50)

    lowerRateChangeButton = tk.Button(AOOWindow, text="Change", font=("Comic Sans MS", 15), command = lambda:checkParameter(343, 2000, 0, lowerRateEntry_1, AOOWindow, 50, 215, "AOO", title, lowerRateLabel))
    lowerRateChangeButton.place(x = 50, y = 215, width = 300, height = 50)

    # Atrial Amplitude
    amplitudeLabel = tk.Label(AOOWindow, text = "Atrial Amplitude: " + str(user_list[user_id].AOO[1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=325)
    amplitudeRangeLabel =  tk.Label(AOOWindow, text = "(Range: 500-5000mV)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=360)

    amplitudeEntry = tk.Entry(AOOWindow, font=("Comic Sans MS", 20))
    amplitudeEntry.place(x = 50, y = 400, width = 500, height = 50)

    amplitudeChangeButton = tk.Button(AOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(500, 5000, 1, amplitudeEntry, AOOWindow, 50, 475, "AOO", title, amplitudeLabel))
    amplitudeChangeButton.place(x = 50, y = 475, width = 300, height = 50)

    # Atrial Pulse Width
    pWLabel = tk.Label(AOOWindow, text = "Atrial Pulse Width: " + str(user_list[user_id].AOO[2]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=600)
    pWLabel =  tk.Label(AOOWindow, text = "(Range: 1-30ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=635)

    pWEntry = tk.Entry(AOOWindow, font=("Comic Sans MS", 20))
    pWEntry.place(x = 50, y = 675, width = 500, height = 50)

    pwEntryChangeButton = tk.Button(AOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(1, 30, 2, pWEntry, AOOWindow, 50, 750, "AOO", title, pWLabel))
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

    lowerRateLabel = tk.Label(VOOWindow, text = "Ventrical Lower Rate: " + str(user_list[user_id].VOO[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=50)
    LRRangeLabel =  tk.Label(VOOWindow, text = "(Range: 343 - 2000 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=85)

    lowerRateEntry_1 = tk.Entry(VOOWindow, font=("Comic Sans MS", 20))
    lowerRateEntry_1.place(x = 50, y = 140, width = 500, height = 50)

    lowerRateChangeButton = tk.Button(VOOWindow, text="Change", font=("Comic Sans MS", 15), command = lambda:checkParameter(343, 2000, 0, lowerRateEntry_1, VOOWindow, 50, 215, "VOO", title, lowerRateLabel))
    lowerRateChangeButton.place(x = 50, y = 215, width = 300, height = 50)

    # Atrial Amplitude
    amplitudeLabel = tk.Label(VOOWindow, text = "Ventrical Amplitude: " + str(user_list[user_id].VOO[1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=325)
    amplitudeRangeLabel =  tk.Label(VOOWindow, text = "(Range: 500-5000mV)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=360)

    amplitudeEntry = tk.Entry(VOOWindow, font=("Comic Sans MS", 20))
    amplitudeEntry.place(x = 50, y = 400, width = 500, height = 50)

    amplitudeChangeButton = tk.Button(VOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(500, 5000, 1, amplitudeEntry, VOOWindow, 50, 475, "VOO", title, amplitudeLabel))
    amplitudeChangeButton.place(x = 50, y = 475, width = 300, height = 50)

    # Atrial Pulse Width
    pWLabel = tk.Label(VOOWindow, text = "Ventrical Pulse Width: " + str(user_list[user_id].VOO[2]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=600)
    pWLabel =  tk.Label(VOOWindow, text = "(Range: 1-30ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=635)

    pWEntry = tk.Entry(VOOWindow, font=("Comic Sans MS", 20))
    pWEntry.place(x = 50, y = 675, width = 500, height = 50)

    pwEntryChangeButton = tk.Button(VOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(1, 30, 2, pWEntry, VOOWindow, 50, 750, "VOO", title, pWLabel))
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

def dataValuesAAI2(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    AAIWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    AAIWindow.title(title)

    graph(AAIWindow)

    # ARP
    ARPLabel = tk.Label(AAIWindow, text = "ARP: " + str(user_list[user_id].AAI[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=200)
    ARPLabel =  tk.Label(AAIWindow, text = "(Range: 150-500 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=235)

    ARPEntry = tk.Entry(AAIWindow, font=("Comic Sans MS", 20))
    ARPEntry.place(x = 50, y = 275, width = 500, height = 50)

    ARPEntryChangeButton_2 = tk.Button(AAIWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(150, 500, 0, ARPEntry, AAIWindow, 50, 350, "AAI", title, ARPLabel))
    ARPEntryChangeButton_2.place(x = 50, y = 350, width = 300, height = 50)
    
    # ASensitivity
    A_sensLabel = tk.Label(AAIWindow, text = "Atrical Sensitivity: " + str(user_list[user_id].AAI[1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=475)
    A_sensLabel =  tk.Label(AAIWindow, text = "(Range: 3000-5000 mV)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=510)

    A_sensEntry = tk.Entry(AAIWindow, font=("Comic Sans MS", 20))
    A_sensEntry.place(x = 50, y = 550, width = 500, height = 50)

    A_sensEntryChangeButton_2 = tk.Button(AAIWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(3000, 5000, 1, A_sensEntry, AAIWindow, 50, 635, "AAI", title, A_sensLabel))
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

def dataValuesVVI2(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    VVIWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    VVIWindow.title(title)

    graph(VVIWindow)

    # VRP
    VRPLabel = tk.Label(VVIWindow, text = "VRP: " + str(user_list[user_id].VVI[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=200)
    VRPLabel =  tk.Label(VVIWindow, text = "(Range: 150-500 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=235)

    VRPEntry = tk.Entry(VVIWindow, font=("Comic Sans MS", 20))
    VRPEntry.place(x = 50, y = 275, width = 500, height = 50)

    VRPEntryChangeButton_2 = tk.Button(VVIWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(150, 500, 0, VRPEntry, VVIWindow, 50, 350, "VVI", title, VRPLabel))
    VRPEntryChangeButton_2.place(x = 50, y = 350, width = 300, height = 50)
    
    # ASensitivity
    V_sensLabel = tk.Label(VVIWindow, text = "Ventrical Sensitivity: " + str(user_list[user_id].VVI[1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=475)
    V_sensLabel =  tk.Label(VVIWindow, text = "(Range: 3000-5000 mV)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=510)

    V_sensEntry = tk.Entry(VVIWindow, font=("Comic Sans MS", 20))
    V_sensEntry.place(x = 50, y = 550, width = 500, height = 50)

    V_sensEntryChangeButton_2 = tk.Button(VVIWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(3000, 5000, 1, V_sensEntry, VVIWindow, 50, 635, "VVI", title, V_sensLabel))
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
    
    # Maximum Sensor Rate Limit
    maxSenLabel= tk.Label(DOOWindow, text = "Maximum Sensor Rate Limit: " + str(user_list[user_id].DOO[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=50)
    RangeLabel =  tk.Label(DOOWindow, text = "(Range: 343 - 1200 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=85)
    
    maxSenEntry = tk.Entry(DOOWindow, font=("Comic Sans MS", 20))
    maxSenEntry.place(x = 50, y = 140, width = 500, height = 50)

    maxSenChangeButton = tk.Button(DOOWindow, text="Change", font=("Comic Sans MS", 15), command = lambda:checkParameter(343, 1200, 0, maxSenEntry, DOOWindow, 50, 215, "DOO", title, maxSenLabel))
    maxSenChangeButton.place(x = 50, y = 215, width = 300, height = 50)

    # Activity Threshold
    actLabel = tk.Label(DOOWindow, text = "Activity Threshold: " + str(user_list[user_id].DOO[1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=325)
    actRangeLabel =  tk.Label(DOOWindow, text = "(Range: 0.05 - 1.5 activity)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=360)

    actEntry = tk.Entry(DOOWindow, font=("Comic Sans MS", 20))
    actEntry.place(x = 50, y = 400, width = 500, height = 50)

    actChangeButton = tk.Button(DOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(0.05, 1.5, 1, actEntry, DOOWindow, 50, 475, "DOO", title, actLabel))
    actChangeButton.place(x = 50, y = 475, width = 300, height = 50)

    # Reaction Time
    reactLabel = tk.Label(DOOWindow, text = "Reaction Time: " + str(user_list[user_id].DOO[2]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=600)
    reactLabel =  tk.Label(DOOWindow, text = "(Range: 10 - 50s)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=635)

    reactEntry = tk.Entry(DOOWindow, font=("Comic Sans MS", 20))
    reactEntry.place(x = 50, y = 675, width = 500, height = 50)

    reactEntryChangeButton = tk.Button(DOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(1, 30, 2, reactEntry, DOOWindow, 50, 750, "DOO", title, reactLabel))
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

    # response
    responseLabel = tk.Label(DOOWindow, text = "Response Factor: " + str(user_list[user_id].DOO[3]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=200)
    responseLabel =  tk.Label(DOOWindow, text = "(Range: 1-16)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=235)

    responseEntry = tk.Entry(DOOWindow, font=("Comic Sans MS", 20))
    responseEntry.place(x = 50, y = 275, width = 500, height = 50)

    responseEntryChangeButton_2 = tk.Button(DOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(1, 16, 3, responseEntry, DOOWindow, 50, 350, "DOO", title, responseLabel))
    responseEntryChangeButton_2.place(x = 50, y = 350, width = 300, height = 50)
    
    # ASensitivity
    recovLabel = tk.Label(DOOWindow, text = "Recovery Time: " + str(user_list[user_id].DOO[4]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=475)
    recovLabel =  tk.Label(DOOWindow, text = "(Range: 120 - 960 s)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=510)

    recovEntry = tk.Entry(DOOWindow, font=("Comic Sans MS", 20))
    recovEntry.place(x = 50, y = 550, width = 500, height = 50)

    recovEntryChangeButton_2 = tk.Button(DOOWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(120, 960, 4, recovEntry, DOOWindow, 50, 635, "DOO", title, recovLabel))
    recovEntryChangeButton_2.place(x = 50, y = 635, width = 300, height = 50)

    # goes to previous window
    if (title == "DOOR"):
        nextButton = tk.Button(DOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOOR2(DOOWindow, title, "yes"))
        nextButton.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton = tk.Button(DOOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO1(DOOWindow, title, "yes"))
        prevButton.place(x = 775, y = 800, width = 300, height = 50)
    elif (title == "DDDR"):
        nextButton = tk.Button(DOOWindow, text = "Next Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDDDR2(DOOWindow, title, "yes"))
        nextButton.place(x = 1100, y = 800, width = 300, height = 50)

        prevButton = tk.Button(DOOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO1(DOOWindow, title, "yes"))
        prevButton.place(x = 775, y = 800, width = 300, height = 50)
    else:
        switchButton2 = tk.Button(DOOWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO1(DOOWindow, title, "yes"))
        switchButton2.place(x = 1100, y = 800, width = 300, height = 50)

def dataValuesAOOR1(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()
    
    dataValuesAOO(tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1'), title, "yes")

def dataValuesVOOR1(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()
    
    dataValuesVOO(tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1'), title, "yes")

def dataValuesAAIR1(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()
    
    dataValuesAAI1(tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1'), title, "yes")

def dataValuesVVIR1(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()
    
    dataValuesVVI1(tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1'), title, "yes")

def dataValuesDOOR(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()
    
    dataValuesAOO(tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1'), title, "yes")

def dataValuesDOOR2(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    DOORWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    DOORWindow.title(title)

    graph(DOORWindow)

    responseLabel = tk.Label(DOORWindow, text = "Fixed Atrial Ventrical (AV) Delay: " + str(user_list[user_id].DOOR[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=200)
    responseLabel =  tk.Label(DOORWindow, text ="(Range: 70-300 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=235)

    responseEntry = tk.Entry(DOORWindow, font=("Comic Sans MS", 20))
    responseEntry.place(x = 50, y = 275, width = 500, height = 50)

    responseEntryChangeButton = tk.Button(DOORWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(70, 300, 0, responseEntry, DOORWindow, 50, 215, "DOOR", title, responseLabel))
    responseEntryChangeButton.place(x = 50, y = 350, width = 300, height = 50)

    switchButton2 = tk.Button(DOORWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO2(DOORWindow, title, "yes"))
    switchButton2.place(x = 1100, y = 800, width = 300, height = 50)

def dataValuesDDDR(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()
    
    dataValuesAAI1(tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1'), title, "yes")

def dataValuesDDDR2(oldWin, title, delCom):
    if (delCom == "yes"):
        oldWin.destroy()

    DDDRWindow = tk.Toplevel(root,  height = root.winfo_screenheight(), width = root.winfo_screenwidth(), bg = '#FFB6C1')
    DDDRWindow.title(title)

    graph(DDDRWindow)

    responseLabel = tk.Label(DDDRWindow, text = "RVARP: " + str(user_list[user_id].DDDR[0]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=50,y=200)
    responseLabel =  tk.Label(DDDRWindow, text ="(Range: 150 - 500 ms)", bg='#FFB6C1',font = ("Comic Sans MS", 12)).place(x=50,y=235)

    responseEntry = tk.Entry(DDDRWindow, font=("Comic Sans MS", 20))
    responseEntry.place(x = 50, y = 275, width = 500, height = 50)

    responseEntryChangeButton = tk.Button(DDDRWindow, text = "Change", font = ("Comic Sans MS", 15), command = lambda:checkParameter(150, 500, 0, responseEntry, DDDRWindow, 50, 215, "DDDR", title, responseLabel))
    responseEntryChangeButton.place(x = 50, y = 350, width = 300, height = 50)

    switchButton2 = tk.Button(DDDRWindow, text = "Previous Page", font = ("Comic Sans MS", 15), command = lambda: dataValuesDOO2(DDDRWindow, title, "yes"))
    switchButton2.place(x = 1100, y = 800, width = 300, height = 50)

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
    root.bind('<Return>', print("hi"))
    
    loginButton = tk.Button(root, text="Login", font=("Comic Sans MS", 15), command = lambda: chooseDisplay(nameEntry.get(), passwordEntry.get()))
    loginButton.place(x = 350, y = 600, width = 100, height = 50)

    signupButton = tk.Button(root, text="Sign Up", font=("Comic Sans MS", 15), command = lambda: signup())
    signupButton.place(x = 350, y = 675, width = 100, height = 50)

    root.mainloop()

main() # runs program
      # %%