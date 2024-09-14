import mysql.connector as connector #importing mysql connector for storing passwords and data
from encryption import encrypt,decrypt
import os
from passgen import * #importing password generator , strength checker
import pyfiglet as ascii_art_generator # this module is used for generating ascii arts
# Defining colors using ANSI Escape codes
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGNETA="\033[95m"
RESET = '\033[0m'  # Reset to default color
#required values
db_name="password_manager"
app_name="Pass GO"
ascii_title_art=ascii_art_generator.figlet_format(app_name,font="doom")
user=None #name of the logged in user. initally set to None and later changed on login
#connecting to the database
menu_text="""MENU
1) Store a password         2) Load a password
3) View all Passwords       4) Delete a password
5) Update a password        6) Password Generator
7) Password Strenth Checker 8) Exit 

          """
try:
    con=connector.connect(host="localhost",
                    user="root",
                    password="password",
                    charset="utf8",
                    database=db_name)
except Exception:
    from dbcreator import create_db
    create_db(db_name)
    con=connector.connect(host="localhost",
                    user="root",
                    charset="utf8",
                    password="password",
                    database=db_name)

def login_screen():
    global user
    print("""MENU
1) Login    2) Register
""")    
    while True:
        #empty print statements are added to here cleanliness and readability 
        print()
        try:
            choice=int(input("Choice : ")) #inputting choice
        except ValueError:
            print(f"{RED}Please enter a proper integer according to the menu.{RESET}")
            continue
        print()
        if choice==1:
            username=input("Username : ")
            
            
            
            cur=con.cursor()
            #taking info from database
            cur.execute(f"select * from users where username='{username}' ")
            data=cur.fetchall()
            #this implies that user hasnt registered yet
            #[[username,password]]
            if data==[]:
                 print(f"{RED}Invalid username.{RESET}\n")
            else: 
                password=input("Password : ")
                #checking if the decrypted value from database and the inputted password matches.
                if decrypt(data[0][1])==password:
                    print(f"\n{GREEN}Login Succesful{RESET}")
                    user=username
                else:
                    print(f"{RED}Invalid password{RESET}")
                
                 
        elif choice==2:
            username=input("Username : ")
            
            if username=="users":
                print(f"{YELLOW}Username cannot be users.{RESET}")#this is done bcz we have a table of users in the same database
                continue 
            #inputting value from db
            cur=con.cursor()
            cur.execute(f"select * from users where username='{username}'")
            if cur.fetchall()==[]:#this is done to ensure the uniqueness of usernames
                password=input("Password : ")
    
                cur.execute(f"insert into users values('{username}','{encrypt(password)}')")
                #a respective table is created for the user
                cur.execute(f"create table {username} (website varchar(50),username varchar(50),password varchar(2000));")
                con.commit()
                user=username
                print("\nRegistration Succesful")
            else:print("User is already registered.Please login.")

        else:print(f"{RED}Invalid Choice !{RESET}")

        if user is None:continue
        else:break


#password manager menu
def menu():
    global user
    global menu_text
    text_decorator=ascii_art_generator.figlet_format(user,font="big") #using pyfiglet to create ascii art with users name
    print(f"{MAGNETA}{text_decorator}{RESET}")

    print(menu_text)
    while True:

# 1) Store a password         2) Load a password
# 3) View all Passwords       4) Delete a password
# 5) Update a password        6) Password Generator
# 7) Password Strenth Checker 8) Exit 
        try:
            choice=int(input("Choice : ")) 
        except ValueError:
            print(f"{RED}Please enter a proper integer according to the menu.{RESET}")
            print(menu_text)
            continue

        #edit here valo
        if choice==1:
            pass
        elif choice==2:
            pass
        elif choice==3:
            pass
        elif choice==6:
            
            length=input("Enter the length for your password : ")
            if length=="":
                print(f"{RED}Enter a proper integer.{RESET}\n")
                print(menu_text)
            else:
                print(f"{YELLOW}Generated password : {generate_password(int(length))}{RESET}\n")
        elif choice==7:
            passw = input("Enter your password : ")
            if passw=="":
                print(f"{RED}Enter a proper password.{RESET}\n")
                print(menu_text)
            else:print(f"{YELLOW}{strength_checker(passw)}{RESET}\n")
        elif choice==8:
            print("Thank You !!")
            break
        else:
            print(f"{RED}Invalid choice !!{RESET}")
            print(menu_text)
#main part of code  
def main():
    global user
    print(f"{BLUE}{ascii_title_art}{RESET}")
    login_screen()
    os.system("cls")# clears the terminal
    print(f"{GREEN}Logged in as {user}.{RESET}")
    menu()

    

    
if con.is_connected():
    main()
else:
    print("Unable to connect , try again.")