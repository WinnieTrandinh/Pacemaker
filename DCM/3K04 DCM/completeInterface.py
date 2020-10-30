#!/usr/bin/env python
# coding: utf-8

# In[48]:


import tkinter as tk
import random
import time

class User: 
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.AOO = [1000, 1000, 10]
        self.VOO = [1000, 1000, 10]
        self.AII = [1000, 1000, 10, 400, 300, 0]
        self.VII = [1000, 1000, 10, 400, 300, 0]

    def change_name(self, new_name):
        self.name = new_name
    
    def change_password(self, new_password):
        self.password = new_password
    
    

user_list = []
user_id = 0
pacemakerNumber = [1234,5453,6789,5809,2354,1765,3490,5692,3745,6890]

with open("pacemaker_users.txt") as i:
    names = i.readlines()
    names = [x.strip() for x in names]

with open("pacemaker_passwords.txt") as i:
    password_list = i.readlines()
    password_list = [x.strip() for x in password_list]

for i in range(len(names)):
    user_list.append(User(names[i], password_list[i]))

for i in range(len(user_list)):
    print(user_list[i].name + "   " + user_list[i].password)


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
    # this sets the position of the window when created
    def setPos(self, x, y):
        self.window.geometry("+%d+%d" % (x, y))

    def setTitle(self, title):
        self.window.title(title)
    # returns the actual window object so that it can be used as a canvas for gComponents
    def getWindow(self):
        return self.window

# ****************************************************************************************************


root = tk.Tk()
root.title('Login/Signup')


HEIGHT = 800
WIDTH = 800
canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
canvas.pack()


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

def quit(window):
        window.destroy()

def signup():

    if(len(user_list) < 10):
        signupWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
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
        
       
            
        signupButton2 = tk.Button(signupWindow, text="Sign Up", font=("Comic Sans MS", 15), command = lambda:signup2(signupWindow,nameEntry2,passwordEntry2,confirmPasswordEntry))
        signupButton2.place(x = 350, y = 675, width = 100, height = 50)
    elif(len(user_list) >= 10):
        maxUsersLabel = tk.Label(root, text = "Max Users Reached!", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)

def signup2(signupWindow, name, password, confirmPassword):
    flag = 1

    if(password.get() != confirmPassword.get()):
        incorrectPassLabel = tk.Label(signupWindow, text = "Not The Same Password!", font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
        flag = 0
    for i in user_list:
        if(name.get() in i.name):
            userExistsLabel = tk.Label(signupWindow, text = "User already exists!", bg = '#FFB6C1',font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
            flag = 0
    if(flag == 1) : 
        user_list.append(User(name.get(), confirmPassword.get()))
        f = open("pacemaker_users.txt", "a")
        f.write(name.get() + "\n")
        f.close
        f = open("pacemaker_passwords.txt", "a")
        f.write(confirmPassword.get() + "\n")
        f.close
        #root.after(1000, userDoesNotExistLabel = tk.Label(signupWindow, text = "Thank you!", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
        root.after(250, signupWindow.destroy())
        #uSureButton = tk.Button(signupWindow, text="Confirm", font=("Comic Sans MS", 15), command = lambda:quit(signupWindow))
        #uSureButton.place(x = 500, y = 675, width = 100, height = 50)
        



def chooseDisplay(username, password):
    incorrectPassLabel = tk.Label(root, bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
    num =0
    flag = 0
    for i in user_list:  #loops through all names within the user list 
        if(username == i.name and password == i.password):
            flag = 1
            incorrectPassLabel = tk.Label(root, text = "Welcome!", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)   

        
            
            # ********************************************* window demo ***********************************************************
            pacingModeWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
            pacingModeWindow.title("Pacing Modes")

            pacingLabel = tk.Label(pacingModeWindow, text = "Pacing Modes", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 75, width = 500, height = 50)

            pacemakerLabel = tk.Label(pacingModeWindow, text = "Pacemaker " + str(pacemakerNumber[num]) +  " Connected", bg = '#00FF00', font = ("Comic Sans MS", 10)).place(x = 550, y = 650, width = 200, height = 50)


            AOOButton = tk.Button(pacingModeWindow, text="AOO", font=("Comic Sans MS", 15),command = lambda:dataValuesAOO())
            AOOButton.place(x = 250, y = 175, width = 300, height = 50)

            VOOButton = tk.Button(pacingModeWindow, text="VOO", font=("Comic Sans MS", 15),command = lambda:dataValuesVOO())
            VOOButton.place(x = 250, y = 300, width = 300, height = 50)

            AIIButton = tk.Button(pacingModeWindow, text="AII", font=("Comic Sans MS", 15),command = lambda:dataValuesAII())
            AIIButton.place(x = 250, y = 425, width = 300, height = 50)

            VVIButton = tk.Button(pacingModeWindow, text="VVI", font=("Comic Sans MS", 15),command = lambda:dataValuesVVI())
            VVIButton.place(x = 250, y = 550, width = 300, height = 50)
            # ***********************************************************************************************************************************************
        if(username == i.name and password != i.password and flag == 0):
            incorrectPassLabel = tk.Label(root, text = "Incorrect Username or Password!", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
            flag = 1
        if(username != i.name and flag == 0):
            incorrectPassLabel = tk.Label(root, text = "Incorrect Username or Password!", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
            flag = 1
        num = num + 1

def changeParameter(i, new_value, window, mode):
    if (mode == "AOO"):
        user_list[user_id].AOO[i] = new_value.get()
    elif (mode == "VOO"):
        user_list[user_id].VOO[i] = new_value.get()
    elif (mode == "AII"):
        user_list[user_id].AII[i] = new_value.get()
    elif (mode == "VII"):
        user_list[user_id].VII[i] = new_value.get()

    window.destroy()


def lowerRate(mode):
    lowerRateWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    lowerRateWindow.title("Lower Rate Limit")

    lowerRateEntry = tk.Entry(lowerRateWindow, font=("Comic Sans MS", 20))
    lowerRateEntry.place(x = 150, y = 350, width = 500, height = 50)


    if (mode == "AOO"):
        lowerRateLabel1 = tk.Label(lowerRateWindow,text= ("Lower Rate Limit: " + str(user_list[user_id].AOO[0])) , bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=225,y=210)
    elif (mode == "VOO"):
        lowerRateLabel1 = tk.Label(lowerRateWindow,text= ("Lower Rate Limit: " + str(user_list[user_id].VOO[0])) , bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=225,y=210)
    elif (mode == "AII"):
        lowerRateLabel1 = tk.Label(lowerRateWindow,text= ("Lower Rate Limit: " + str(user_list[user_id].AII[0])) , bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=225,y=210)
    elif (mode == "VII"):
        lowerRateLabel1 = tk.Label(lowerRateWindow,text= ("Lower Rate Limit: " + str(user_list[user_id].VII[0])) , bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=225,y=210)
    
    userLowerRateLabel = tk.Label(lowerRateWindow,text="Range: 343-2000ms" , bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=225,y=260)

    enterButton1 = tk.Button(lowerRateWindow, text="Enter", font=("Comic Sans MS", 15), command = lambda: changeParameter(0, lowerRateEntry, lowerRateWindow, mode))
    enterButton1.place(x = 250, y = 475, width = 300, height = 50)

    closeButton1 = tk.Button(lowerRateWindow, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(lowerRateWindow))
    closeButton1.place(x = 250, y = 575, width = 300, height = 50)
def upperRate():
    upperRateWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    upperRateWindow.title("Upper Rate Limit")

    upperRateEntry = tk.Entry(upperRateWindow, font=("Comic Sans MS", 20))
    upperRateEntry.place(x = 150, y = 350, width = 500, height = 50)
    
    upperRateLabel1 = tk.Label(upperRateWindow,text="Upper Rate Limit: ", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=225,y=260)



    enterButton2 = tk.Button(upperRateWindow, text="Enter", font=("Comic Sans MS", 15))
    enterButton2.place(x = 250, y = 475, width = 300, height = 50)

    closeButton2 = tk.Button(upperRateWindow, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(upperRateWindow))
    closeButton2.place(x = 250, y = 575, width = 300, height = 50)

def amplitude(mode):
    amplitudeWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    amplitudeWindow.title("Atrial Amplitude")

    amplitudeEntry = tk.Entry(amplitudeWindow, font=("Comic Sans MS", 20))
    amplitudeEntry.place(x = 150, y = 350, width = 500, height = 50)

    if (mode == "AOO"):
        amplitudeLabel1 = tk.Label(amplitudeWindow,text="Atrial Amplitude: " + str(user_list[user_id].AOO[1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=225,y=220)
    elif (mode == "AII"):
        amplitudeLabel1 = tk.Label(amplitudeWindow,text="Atrial Amplitude: " + str(user_list[user_id].AII[1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=225,y=220)
    
    userAmplitudeLabel1 = tk.Label(amplitudeWindow,text="Range: 500-5000ms", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=225,y=260)
    enterButton3 = tk.Button(amplitudeWindow, text="Enter", font=("Comic Sans MS", 15), command = lambda:changeParameter(1, amplitudeEntry, amplitudeWindow, mode))
    enterButton3.place(x = 250, y = 475, width = 300, height = 50)

    closeButton3 = tk.Button(amplitudeWindow, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(amplitudeWindow))
    closeButton3.place(x = 250, y = 575, width = 300, height = 50)


def pulseWidth(mode):
    pulseWidthWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    pulseWidthWindow.title("Atrial Pulse Width")

    pulseWidthEntry = tk.Entry(pulseWidthWindow, font=("Comic Sans MS", 20))
    pulseWidthEntry.place(x = 150, y = 350, width = 500, height = 50)

    if (mode == "AOO"):
        userPulseWidthLabel1 = tk.Label(pulseWidthWindow,text="Atrial Pulse Width: " + str(user_list[user_id].AOO[2]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=200,y=220)
    elif (mode == "AII"):
        userPulseWidthLabel1 = tk.Label(pulseWidthWindow,text="Atrial Pulse Width: " + str(user_list[user_id].AII[2]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=200,y=220)
    
    pulseWidthLabel1 = tk.Label(pulseWidthWindow,text="Range: 1-30ms", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=200,y=260)

    enterButton4 = tk.Button(pulseWidthWindow, text="Enter", font=("Comic Sans MS", 15), command = lambda: (changeParameter(2, pulseWidthEntry, pulseWidthWindow, mode)))
    enterButton4.place(x = 250, y = 475, width = 300, height = 50)

    closeButton4 = tk.Button(pulseWidthWindow, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(pulseWidthWindow))
    closeButton4.place(x = 250, y = 575, width = 300, height = 50)


def ventricularAmp(mode):
    ventricularAmpWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    ventricularAmpWindow.title("Ventricular Amplitude")

    ventricularAmpEntry = tk.Entry(ventricularAmpWindow, font=("Comic Sans MS", 20))
    ventricularAmpEntry.place(x = 150, y = 350, width = 500, height = 50)

    if (mode == "VOO"):
        userVentricularAmpLabel1 = tk.Label(ventricularAmpWindow,text="Ventricular Amplitude: " + str(user_list[user_id].VOO[1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=175,y=220)
    elif (mode == "VII"):
        userVentricularAmpLabel1 = tk.Label(ventricularAmpWindow,text="Ventricular Amplitude: " + str(user_list[user_id].VII[1]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=175,y=220)
    
    ventricularAmpLabel1 = tk.Label(ventricularAmpWindow,text="Range: 500-5000ms", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=175,y=260)

    enterButton5 = tk.Button(ventricularAmpWindow, text="Enter", font=("Comic Sans MS", 15), command = lambda: changeParameter(1, ventricularAmpEntry, ventricularAmpWindow, mode))
    enterButton5.place(x = 250, y = 475, width = 300, height = 50)

    closeButton5 = tk.Button(ventricularAmpWindow, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(ventricularAmpWindow))
    closeButton5.place(x = 250, y = 575, width = 300, height = 50)



def ventricularPulse(mode):
    ventricularPulseWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    ventricularPulseWindow.title("Ventricular Pulse Width")

    ventricularPulseEntry = tk.Entry(ventricularPulseWindow, font=("Comic Sans MS", 20))
    ventricularPulseEntry.place(x = 150, y = 350, width = 500, height = 50)

    if (mode == "VOO"):
        userVentricularAmpLabel1 = tk.Label(ventricularPulseWindow,text="Ventricular Pulse Width: " + str(user_list[user_id].VOO[2]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=175,y=220)
    elif (mode == "VII"):
        userVentricularAmpLabel1 = tk.Label(ventricularPulseWindow,text="Ventricular Pulse Width: " + str(user_list[user_id].VII[2]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=175,y=220)
    
    ventricularPulseLabel1 = tk.Label(ventricularPulseWindow,text="Ventricular Pulse Width: 1-30ms", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=175,y=260)

    enterButton6 = tk.Button(ventricularPulseWindow, text="Enter", font=("Comic Sans MS", 15), command = lambda: changeParameter(2, ventricularPulseEntry, ventricularPulseWindow, mode))
    enterButton6.place(x = 250, y = 475, width = 300, height = 50)

    closeButton6 = tk.Button(ventricularPulseWindow, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(ventricularPulseWindow))
    closeButton6.place(x = 250, y = 575, width = 300, height = 50)


def VRP(mode):
    VRPWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    VRPWindow.title("VRP")

    VRPEntry = tk.Entry(VRPWindow, font=("Comic Sans MS", 20))
    VRPEntry.place(x = 150, y = 350, width = 500, height = 50)

    userVRPLabel1 = tk.Label(VRPWindow,text="VRP: " + str(user_list[user_id].VII[3]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=300,y=260)
    VRPLabel1 = tk.Label(VRPWindow,text="VRP: 150-500ms", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=300,y=220)

    enterButton7 = tk.Button(VRPWindow, text="Enter", font=("Comic Sans MS", 15), command = lambda: changeParameter(3, VRPEntry, VRPWindow, mode))
    enterButton7.place(x = 250, y = 475, width = 300, height = 50)

    closeButton7 = tk.Button(VRPWindow, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(VRPWindow))
    closeButton7.place(x = 250, y = 575, width = 300, height = 50)


def ARP(mode):
    ARPWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    ARPWindow.title("ARP")  

    ARPEntry = tk.Entry(ARPWindow, font=("Comic Sans MS", 20))
    ARPEntry.place(x = 150, y = 350, width = 500, height = 50)


    userARPLabel1 = tk.Label(ARPWindow,text="ARP: " + str(user_list[user_id].AII[3]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=300,y=260)
    ARPLabel1 = tk.Label(ARPWindow,text="Range: 150-500ms", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=300,y=220)


    enterButton8 = tk.Button(ARPWindow, text="Enter", font=("Comic Sans MS", 15), command = lambda: changeParameter(3, ARPEntry, ARPWindow, mode))
    enterButton8.place(x = 250, y = 475, width = 300, height = 50)

    closeButton8 = tk.Button(ARPWindow, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(ARPWindow))
    closeButton8.place(x = 250, y = 575, width = 300, height = 50)
     
def hysteresis(mode):
    hysteresisWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    hysteresisWindow.title("Hysteresis")  

    hysteresisEntry = tk.Entry(hysteresisWindow, font=("Comic Sans MS", 20))
    hysteresisEntry.place(x = 150, y = 350, width = 500, height = 50)

    if (mode == "AII"):
        userHysteresisLabel1 = tk.Label(hysteresisWindow,text="Hysteresis Interval: " + str(user_list[user_id].AII[4]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=200,y=260)
    elif (mode == "VII"):
        userHysteresisLabel1 = tk.Label(hysteresisWindow,text="Hysteresis Interval: " + str(user_list[user_id].VII[4]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=200,y=260)
    
    hysteresisLabel1 = tk.Label(hysteresisWindow,text="Hysteresis Interval: 200-500ms", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=200,y=220)


    enterButton9 = tk.Button(hysteresisWindow, text="Enter", font=("Comic Sans MS", 15), command = lambda:changeParameter(4, hysteresisEntry, hysteresisWindow, mode))
    enterButton9.place(x = 250, y = 475, width = 300, height = 50)

    closeButton9 = tk.Button(hysteresisWindow, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(hysteresisWindow))
    closeButton9.place(x = 250, y = 575, width = 300, height = 50)

def aSensitivity(mode):
    aSensitivityWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    aSensitivityWindow.title("Atrium Sensitivity")  

    aSensitivityEntry = tk.Entry(aSensitivityWindow, font=("Comic Sans MS", 20))
    aSensitivityEntry.place(x = 150, y = 350, width = 500, height = 50)

    userASensitivityLabel = tk.Label(aSensitivityWindow,text="Atrium Sensitivity: " + str(user_list[user_id].AII[5]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=200,y=220)
    aSensitivityLabel = tk.Label(aSensitivityWindow,text="Range: 0/1", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=200,y=260)


    enterButton10 = tk.Button(aSensitivityWindow, text="Enter", font=("Comic Sans MS", 15), command= lambda:changeParameter(5, aSensitivityEntry, aSensitivityWindow, mode))
    enterButton10.place(x = 250, y = 475, width = 300, height = 50)

    closeButton10 = tk.Button(aSensitivityWindow, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(aSensitivityWindow))
    closeButton10.place(x = 250, y = 575, width = 300, height = 50)

def vSensitivity(mode):
    vSensitivityWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    vSensitivityWindow.title("Ventricle Sensitivity")  

    vSensitivityEntry = tk.Entry(vSensitivityWindow, font=("Comic Sans MS", 20))
    vSensitivityEntry.place(x = 150, y = 350, width = 500, height = 50)


    userASensitivityLabel = tk.Label(vSensitivityWindow,text="Ventricle Sensitivity: " + str(user_list[user_id].VII[5]), bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=200,y=220)
    vSensitivityLabel = tk.Label(vSensitivityWindow,text="Range: 0/1", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=200,y=260)


    enterButton11 = tk.Button(vSensitivityWindow, text="Enter", font=("Comic Sans MS", 15), command = lambda: changeParameter(5, vSensitivityEntry, vSensitivityWindow, mode))
    enterButton11.place(x = 250, y = 475, width = 300, height = 50)

    closeButton11 = tk.Button(vSensitivityWindow, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(vSensitivityWindow))
    closeButton11.place(x = 250, y = 575, width = 300, height = 50)



# MODES
def dataValuesAOO():
    loginWindow1 = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    loginWindow1.title("Logged In")

    lowerRateButton = tk.Button(loginWindow1, text="Lower Rate Limit", font=("Comic Sans MS", 15),command = lambda:lowerRate("AOO"))
    lowerRateButton.place(x = 250, y = 25, width = 300, height = 50)

    amplitudeButton = tk.Button(loginWindow1, text="Atrial Amplitude", font=("Comic Sans MS", 15),command = lambda:amplitude("AOO"))
    amplitudeButton.place(x = 250, y = 125, width = 300, height = 50)

    pulseWidthButton = tk.Button(loginWindow1, text="Atrial Pulse Width", font=("Comic Sans MS", 15),command = lambda:pulseWidth("AOO"))
    pulseWidthButton.place(x = 250, y = 225, width = 300, height = 50)

    closeButton12 = tk.Button(loginWindow1, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(loginWindow1))
    closeButton12.place(x = 250, y = 625, width = 300, height = 50)

def dataValuesVOO():
    loginWindow2 = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    loginWindow2.title("Logged In")

    lowerRateButton = tk.Button(loginWindow2, text="Lower Rate Limit", font=("Comic Sans MS", 15),command = lambda:lowerRate("VOO"))
    lowerRateButton.place(x = 250, y = 25, width = 300, height = 50)

    ventricularAmpButton = tk.Button(loginWindow2, text="Ventricular Amplitude", font=("Comic Sans MS", 15),command = lambda:ventricularAmp("VOO"))
    ventricularAmpButton.place(x = 250, y = 125, width = 300, height = 50)

    ventricularPulseButton = tk.Button(loginWindow2, text="Ventricular Pulse Width", font=("Comic Sans MS", 15),command = lambda:ventricularPulse("VOO"))
    ventricularPulseButton.place(x = 250, y = 225, width = 300, height = 50)

    closeButton13 = tk.Button(loginWindow2, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(loginWindow2))
    closeButton13.place(x = 250, y = 625, width = 300, height = 50)

def dataValuesAII():
    loginWindow3 = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    loginWindow3.title("Logged In")

    lowerRateButton = tk.Button(loginWindow3, text="Lower Rate Limit", font=("Comic Sans MS", 15),command = lambda:lowerRate("AII"))
    lowerRateButton.place(x = 250, y = 25, width = 300, height = 50)

    amplitudeButton = tk.Button(loginWindow3, text="Atrial Amplitude", font=("Comic Sans MS", 15),command = lambda:amplitude("AII"))
    amplitudeButton.place(x = 250, y = 125, width = 300, height = 50)

    pulseWidthButton = tk.Button(loginWindow3, text="Atrial Pulse Width", font=("Comic Sans MS", 15),command = lambda:pulseWidth("AII"))
    pulseWidthButton.place(x = 250, y = 225, width = 300, height = 50)

    ARPButton = tk.Button(loginWindow3, text="ARP", font=("Comic Sans MS", 15),command = lambda:ARP("AII"))
    ARPButton.place(x = 250, y = 325, width = 300, height = 50)

    hysteresisButton = tk.Button(loginWindow3, text="Hysteresis Interval", font=("Comic Sans MS", 15),command = lambda:hysteresis("AII"))
    hysteresisButton.place(x = 250, y = 425, width = 300, height = 50)

    aSensitivityButton = tk.Button(loginWindow3, text="Atrium Sensitivity", font=("Comic Sans MS", 15),command = lambda:aSensitivity("AII"))
    aSensitivityButton.place(x = 250, y = 525, width = 300, height = 50)

    closeButton14 = tk.Button(loginWindow3, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(loginWindow3))
    closeButton14.place(x = 250, y = 625, width = 300, height = 50)

def dataValuesVVI():
    loginWindow4 = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    loginWindow4.title("Logged In")

    lowerRateButton = tk.Button(loginWindow4, text="Lower Rate Limit", font=("Comic Sans MS", 15),command = lambda:lowerRate("VII"))
    lowerRateButton.place(x = 250, y = 25, width = 300, height = 50)


    ventricularAmpButton = tk.Button(loginWindow4, text="Ventricular Amplitude", font=("Comic Sans MS", 15),command = lambda:ventricularAmp("VII"))
    ventricularAmpButton.place(x = 250, y = 125, width = 300, height = 50)

    ventricularPulseButton = tk.Button(loginWindow4, text="Ventricular Pulse Width", font=("Comic Sans MS", 15),command = lambda:ventricularPulse("VII"))
    ventricularPulseButton.place(x = 250, y = 225, width = 300, height = 50)


    VRPButton = tk.Button(loginWindow4, text="VRP", font=("Comic Sans MS", 15),command = lambda:VRP("VII"))
    VRPButton.place(x = 250, y = 325, width = 300, height = 50)

    hysteresisButton = tk.Button(loginWindow4, text="Hysteresis Interval", font=("Comic Sans MS", 15),command = lambda:hysteresis("VII"))
    hysteresisButton.place(x = 250, y = 425, width = 300, height = 50)

    vSensitivityButton = tk.Button(loginWindow4, text="Ventricle Sensitivity", font=("Comic Sans MS", 15),command = lambda:vSensitivity("VII"))
    vSensitivityButton.place(x = 250, y = 525, width = 300, height = 50)

    closeButton15 = tk.Button(loginWindow4, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(loginWindow4))
    closeButton15.place(x = 250, y = 625, width = 300, height = 50)
        

	           
loginButton = tk.Button(root, text="Login", font=("Comic Sans MS", 15), command = lambda: chooseDisplay(nameEntry.get(), passwordEntry.get()))
loginButton.place(x = 350, y = 600, width = 100, height = 50)

signupButton = tk.Button(root, text="Sign Up", font=("Comic Sans MS", 15), command = lambda: signup())
signupButton.place(x = 350, y = 675, width = 100, height = 50)


                

root.mainloop()


# In[ ]:
