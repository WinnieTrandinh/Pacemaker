#!/usr/bin/env python
# coding: utf-8

# In[1]:


class user: 
    def __init__(self, name, password):
        self.name = name
        self.password = password
    
    def change_name(self, new_name):
        self.name = new_name
        
    def change_password(self, new_password):
        self.password = new_password
        
    def error_name(self, name_check):
        if self.name == name_check:
            return True
        else:
            return False
        
    def error_password(self, password_check):
        if self.password == password_check:
            return True
        else:
            return False

def signup():
    new_name = input("Name: ") 
    flag = 0
    while(flag == 0):
        new_password = input("Password: ")
        confirm_password = input("Confirm Password: ")
        if (new_password != confirm_password):
            print("Incorrect password, please try again.")
        else:
            flag = 1
            
    user_name = user(new_name, new_password)
    return user_name
    

def main():
    import sys
    max_users = 10 
    user_list = []
    user_count = -1
    correct_intentions = 0
    correct_password = False
    
    print("Welcome!")
    
    while(1):
        while(correct_intentions == 0):
            intentions = input("What would you like to do? (signup, login, stop): ")
            if (intentions == "signup" or intentions == "login"):
                correct_intentions = 1
            if (intentions == "stop"):
                sys.exit()
                
        #resets intentions
        correct_intentions = 0
        #sign up 
        if (intentions == "signup"):
            if (user_count + 1 == max_users):
                print("Already reached max users.")
            else:
                user_list.append(signup())  #creates a new user and adds it to the list of users 
                user_count = user_count + 1

        #login
        if (intentions == "login"):
            check_name = input("Enter your name: ")
            for i in user_list:  #loops through all names within the user list 
                if(i.name == check_name):
                    while(correct_password == False):  #checks user's password
                        check_password = input("Enter your password: ")
                        correct_password = i.error_password(check_password)
                        print("Welcome "+ i.name)  
                    break

                if (i == user_list[user_count]):
                    print("Name not in system.")


    
main()


# In[ ]:



            


# In[ ]:




