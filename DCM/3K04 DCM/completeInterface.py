#!/usr/bin/env python
# coding: utf-8

# In[48]:


import tkinter as tk

with open("pacemaker_users.txt") as i:
    user_list = i.readlines()
    user_list = [x.strip() for x in user_list]

with open("pacemaker_passwords.txt") as i:
    password_list = i.readlines()
    password_list = [x.strip() for x in password_list]

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



def chooseDisplay(username, password):

    
    for i in range(len(user_list)):  #loops through all names within the user list 
        if(username == user_list[i] and password == password_list[i]):

            # ************************************************* window demo ***************************************************************
            #chooseDispWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
            #chooseDispWindow.title("Choose Display")
            chooseDispWindow = Window(root, root.winfo_x(), root.winfo_y(), HEIGHT, WIDTH, "Choose Display").getWindow()
            # *****************************************************************************************************************************

            nameLabel3 = tk.Label(chooseDispWindow,text="What would you like to display?", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=200,y=150)

            modeButton = tk.Button(chooseDispWindow, text="Display Pacing Modes", font=("Comic Sans MS", 15),command = lambda:pacingMode())
            modeButton.place(x = 250, y = 250, width = 300, height = 50)

            # ********************************************* Button demo ***********************************************************************************(*****
            #dataButton = tk.Button(chooseDispWindow, text="Input Data Values", font=("Comic Sans MS", 15),command = lambda:dataValues())
            #dataButton.place(x = 250, y = 350, width = 300, height = 50)
            dataButton = Button(chooseDispWindow, "Input Data Values", lambda: dataValues())
            dataButton.place(250, 350, 300, 50)
            # ***************************************************************************************************************************************************

        elif(username == user_list[i] and password != password_list[i]):
            incorrectPassLabel = tk.Label(root, text = "Incorrect Password!", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
        elif(username != user_list[i]):
            noUserLabel = tk.Label(root, text = "User not found!", bg = '#FFB6C1', font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)

def lowerRate():
    lowerRateWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    lowerRateWindow.title("Lower Rate Limit")

    lowerRateLabel1 = tk.Label(lowerRateWindow,text="Lower Rate Limit: Placeholder", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=225,y=260)



    # enterButton1 = tk.Button(lowerRateWindow, text="Enter", font=("Comic Sans MS", 15))
    # enterButton1.place(x = 250, y = 475, width = 300, height = 50)

    closeButton1 = tk.Button(lowerRateWindow, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(lowerRateWindow))
    closeButton1.place(x = 250, y = 575, width = 300, height = 50)

def upperRate():
    upperRateWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    upperRateWindow.title("Upper Rate Limit")
    
    upperRateLabel1 = tk.Label(upperRateWindow,text="Upper Rate Limit: Placeholder", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=225,y=260)



    # enterButton2 = tk.Button(upperRateWindow, text="Enter", font=("Comic Sans MS", 15))
    # enterButton2.place(x = 250, y = 475, width = 300, height = 50)

    closeButton2 = tk.Button(upperRateWindow, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(upperRateWindow))
    closeButton2.place(x = 250, y = 575, width = 300, height = 50)

def amplitude():
    amplitudeWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    amplitudeWindow.title("Atrial Amplitude")

    amplitudeLabel1 = tk.Label(amplitudeWindow,text="Atrial Amplitude: Placeholder", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=225,y=260)



    # enterButton3 = tk.Button(amplitudeWindow, text="Enter", font=("Comic Sans MS", 15))
    # enterButton3.place(x = 250, y = 475, width = 300, height = 50)

    closeButton3 = tk.Button(amplitudeWindow, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(amplitudeWindow))
    closeButton3.place(x = 250, y = 575, width = 300, height = 50)


def pulseWidth():
    pulseWidthWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    pulseWidthWindow.title("Atrial Pulse Width")

    pulseWidthLabel1 = tk.Label(pulseWidthWindow,text="Atrial Pulse Width: Placeholder", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=200,y=260)



    # enterButton4 = tk.Button(pulseWidthWindow, text="Enter", font=("Comic Sans MS", 15))
    # enterButton4.place(x = 250, y = 475, width = 300, height = 50)

    closeButton4 = tk.Button(pulseWidthWindow, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(pulseWidthWindow))
    closeButton4.place(x = 250, y = 575, width = 300, height = 50)


def ventricularAmp():
    ventricularAmpWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    ventricularAmpWindow.title("Ventricular Amplitude")

    ventricularAmpLabel1 = tk.Label(ventricularAmpWindow,text="Ventricular Amplitude: Placeholder", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=175,y=260)



    # enterButton5 = tk.Button(ventricularAmpWindow, text="Enter", font=("Comic Sans MS", 15))
    # enterButton5.place(x = 250, y = 475, width = 300, height = 50)

    closeButton5 = tk.Button(ventricularAmpWindow, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(ventricularAmpWindow))
    closeButton5.place(x = 250, y = 575, width = 300, height = 50)


def ventricularPulse():
    ventricularPulseWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    ventricularPulseWindow.title("Ventricular Pulse Width")

    ventricularPulseLabel1 = tk.Label(ventricularPulseWindow,text="Ventricular Pulse Width: Placeholder", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=175,y=260)



    # enterButton6 = tk.Button(ventricularPulseWindow, text="Enter", font=("Comic Sans MS", 15))
    # enterButton6.place(x = 250, y = 475, width = 300, height = 50)

    closeButton6 = tk.Button(ventricularPulseWindow, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(ventricularPulseWindow))
    closeButton6.place(x = 250, y = 575, width = 300, height = 50)


def VRP():
    VRPWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    VRPWindow.title("VRP")

    VRPLabel1 = tk.Label(VRPWindow,text="VRP: Placeholder", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=300,y=260)

    

    # enterButton7 = tk.Button(VRPWindow, text="Enter", font=("Comic Sans MS", 15))
    # enterButton7.place(x = 250, y = 475, width = 300, height = 50)

    closeButton7 = tk.Button(VRPWindow, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(VRPWindow))
    closeButton7.place(x = 250, y = 575, width = 300, height = 50)


def ARP():
    ARPWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    ARPWindow.title("ARP")  

    ARPLabel1 = tk.Label(ARPWindow,text="ARP: Placeholder", bg='#FFB6C1',font = ("Comic Sans MS", 20)).place(x=300,y=260)


    # enterButton8 = tk.Button(ARPWindow, text="Enter", font=("Comic Sans MS", 15))
    # enterButton8.place(x = 250, y = 475, width = 300, height = 50)

    closeButton8 = tk.Button(ARPWindow, text="Exit", font=("Comic Sans MS", 15), command=lambda:quit(ARPWindow))
    closeButton8.place(x = 250, y = 575, width = 300, height = 50)
            



def dataValues():
    loginWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    loginWindow.title("Logged In")

    lowerRateButton = tk.Button(loginWindow, text="Lower Rate Limit", font=("Comic Sans MS", 15),command = lambda:lowerRate())
    lowerRateButton.place(x = 250, y = 25, width = 300, height = 50)

    upperRateButton = tk.Button(loginWindow, text="Upper Rate Limit", font=("Comic Sans MS", 15),command = lambda:upperRate())
    upperRateButton.place(x = 250, y = 125, width = 300, height = 50)

    amplitudeButton = tk.Button(loginWindow, text="Atrial Amplitude", font=("Comic Sans MS", 15),command = lambda:amplitude())
    amplitudeButton.place(x = 250, y = 225, width = 300, height = 50)

    pulseWidthButton = tk.Button(loginWindow, text="Atrial Pulse Width", font=("Comic Sans MS", 15),command = lambda:pulseWidth())
    pulseWidthButton.place(x = 250, y = 325, width = 300, height = 50)

    ventricularAmpButton = tk.Button(loginWindow, text="Ventricular Amplitude", font=("Comic Sans MS", 15),command = lambda:ventricularAmp())
    ventricularAmpButton.place(x = 250, y = 425, width = 300, height = 50)

    ventricularPulseButton = tk.Button(loginWindow, text="Ventricular Pulse Width", font=("Comic Sans MS", 15),command = lambda:ventricularPulse())
    ventricularPulseButton.place(x = 250, y = 525, width = 300, height = 50)

    VRPButton = tk.Button(loginWindow, text="VRP", font=("Comic Sans MS", 15),command = lambda:VRP())
    VRPButton.place(x = 250, y = 625, width = 300, height = 50)

    ARPButton = tk.Button(loginWindow, text="ARP", font=("Comic Sans MS", 15),command = lambda:ARP())
    ARPButton.place(x = 250, y = 725, width = 300, height = 50)

def pacingMode():
    pacingModeWindow = tk.Toplevel(root,  height = HEIGHT, width = WIDTH, bg = '#FFB6C1')
    pacingModeWindow.title("Pacing Modes")

    AOOButton = tk.Button(pacingModeWindow, text="AOO", font=("Comic Sans MS", 15))
    AOOButton.place(x = 250, y = 175, width = 300, height = 50)

    VOOButton = tk.Button(pacingModeWindow, text="VOO", font=("Comic Sans MS", 15))
    VOOButton.place(x = 250, y = 300, width = 300, height = 50)

    AIIButton = tk.Button(pacingModeWindow, text="AII", font=("Comic Sans MS", 15))
    AIIButton.place(x = 250, y = 425, width = 300, height = 50)

    VVIButton = tk.Button(pacingModeWindow, text="VVI", font=("Comic Sans MS", 15))
    VVIButton.place(x = 250, y = 550, width = 300, height = 50)


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
    if(password.get() != confirmPassword.get()):
        incorrectPassLabel = tk.Label(signupWindow, text = "Not The Same Password!", font = ("Comic Sans MS", 20)).place(x = 150, y = 550, width = 500, height = 50)
        
    else: 
        password_list.append(confirmPassword.get())
        user_list.append(name.get())
        f = open("pacemaker_users.txt", "a")
        f.write(name.get() + "\n")
        f.close
        f = open("pacemaker_passwords.txt", "a")
        f.write(confirmPassword.get() + "\n")
        f.close
        uSureButton = tk.Button(signupWindow, text="Confirm", font=("Comic Sans MS", 15), command = lambda:quit(signupWindow))
        uSureButton.place(x = 500, y = 675, width = 100, height = 50)

	           
loginButton = tk.Button(root, text="Login", font=("Comic Sans MS", 15), command = lambda: chooseDisplay(nameEntry.get(), passwordEntry.get()))
loginButton.place(x = 350, y = 600, width = 100, height = 50)

signupButton = tk.Button(root, text="Sign Up", font=("Comic Sans MS", 15), command = lambda: signup())
signupButton.place(x = 350, y = 675, width = 100, height = 50)


                

root.mainloop()


# In[ ]:




