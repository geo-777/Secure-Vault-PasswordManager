import mysql.connector as connector #importing mysql connector for storing passwords and data
from encryption import encrypt,decrypt
import os
from passgen import * #importing password generator , strength checker
import pyfiglet as ascii_art_generator # this module is used for generating ascii arts
import pwinput #used to hide inputted text
import tabulate #used for grid representation 

# Installations
# pip install tabulate
# pip install pwinput
# pip install cryptography
# pip install mysql-connector-python
# pip install pyfiglet

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
7) Password Strength Checker 8) Exit 

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
                password = pwinput.pwinput("Password : ", mask='*')
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
                password = pwinput.pwinput("Password : ", mask='*')
    
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
            con=connector.connect(host="localhost",
                user="root",
                charset="utf8",
                password="password",
                database=db_name)
            cur = con.cursor()
            site = input("Enter the app or website associated with the password : ")
            site = site.lower()
            username_site =input("Enter username : ")
            pass_site = pwinput.pwinput("Enter password : ", mask='*')
            pass_fernet = encrypt(pass_site)
            cur.execute(f"insert into {user} values('{site}','{username_site}','{pass_fernet}')")
            con.commit()
            print("Password successfully stored")
            print()
            print()    
            con.commit()
            cur.close()
            con.close()           
        elif choice==2:
            con=connector.connect(host="localhost",
                    user="root",
                    charset="utf8",
                    password="password",
                    database=db_name)
            cur = con.cursor()
            search = input("Enter Website/Application name : ")
            search = search.lower()
            cur.execute(f"select * from {user} where website like '{search.lower()}'")
            data = cur.fetchall()
            if data == []:
                print("Login details for ",search," not found")
            elif len(data)>1:
                print("You have multiple accounts on this Application/Website")
                for i in data:
                    print("USERNAME : ",i[1])
                    print("PASSWORD : ",decrypt(i[2]))
                    print()

            else:
                for i in data:
                    print("USERNAME : ",i[1])
                    print("PASSWORD : ",decrypt(i[2]))
            print()
            print()  
            con.commit()
            cur.close()
            con.close()      
        elif choice==3:
            con=connector.connect(host="localhost",
                    user="root",
                    charset="utf8",
                    password="password",
                    database=db_name)
            cur = con.cursor()
            cur.execute(f"select * from {user}")
            data = cur.fetchall()

            if data == []:
                print("No usernames or passwords stored yet")
            else:
                table_data=[]
                # Decrypt passwords and prepare the data for tabulation
                for i in data:
                    table_data.append([f"{GREEN}{i[0]}{RESET}", i[1], decrypt(i[2])])
          
                # Display table with headers using tabulate
                print(tabulate.tabulate(table_data, headers=[f"{YELLOW}Website{RESET}", f"{YELLOW}Username{RESET}", f"{YELLOW}Password{RESET}"], tablefmt="grid"))
            print()
            print()
            con.commit()
            cur.close()
            con.close()
        elif choice==4:
            con=connector.connect(host="localhost",
                    user="root",
                    charset="utf8",
                    password="password",
                    database=db_name)
            cur = con.cursor()
            delete = input("Enter Website/Application name for Deletion : ")
            cur.execute(f"select * from {user} where website = '{delete.lower()}'")
            data = cur.fetchall()
            if data == []:
                print("Login details for ",delete," not found")
            elif len(data)>1:
                print("You have multiple accounts on that Application/Website")
                print()
                cur.execute(f"select * from {user} where website = '{delete.lower()}'")
                data = cur.fetchall()
                for i in data:
                    print("USERNAMES : ",i[1])
                print()
                check_user = input("Enter the username of the account you want to delete : ")
                cur.execute(f"delete from {user} where username = '{check_user}'")
                con.commit()
                cur.close()
                con.close()
                print("Deleted successfully")
            else:
                cur.execute(f"delete from {user} where website = '{delete.lower()}'")
                print("Deleted Successfully")
            con.commit()
            print()
            print()
        elif choice==5:
            con=connector.connect(host="localhost",
                    user="root",
                    charset="utf8",
                    password="password",
                    database=db_name)
            cur = con.cursor()
            Updation = input("Enter Website/Application name for Updation : ")
            cur.execute(f"select * from {user} where website = '{Updation.lower()}'")
            data = cur.fetchall()
            if data == []:
                print("Login details for ",Updation," not found")
            elif len(data)>1:
                print("You have multiple accounts on that Application/Website")
                print()
                cur.execute(f"select * from {user} where website = '{Updation.lower()}'")
                data = cur.fetchall()
                for i in data:
                    print("USERNAMES : ",i[1])
                print()
                check_user = input("Enter the username of the account you want to update : ")
                new_user = input("Enter new username : ")
                
                new_pass = pwinput.pwinput("Enter new password : ", mask='*') 
                cur.execute(f"update {user} set username = '{new_user}',password = '{encrypt(new_pass)}' where username = '{check_user}'")
                con.commit()
                print("Successfully Updated")
            else:
                new_user = input("Enter new username : ")
                new_pass = pwinput.pwinput("Enter new password : ", mask='*')
                cur.execute(f"update {user} set username = '{new_user}',password = '{encrypt(new_pass)}' where website = '{Updation.lower()}'")
                con.commit()
                print("Successfully Updated")
            print()
            print()      
            con.commit()
            cur.close()
            con.close()     
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