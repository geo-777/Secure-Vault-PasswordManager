import mysql.connector as connector  # MySQL connector for database interactions
from cryptography.fernet import Fernet
import pickle
import os  # Password generator and strength checker
import pyfiglet  # Module for generating ASCII art
import pwinput  # Used to hide inputted text
import tabulate  # Used for tabular representation

# Define colors using ANSI Escape codes
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = "\033[95m"
RESET = '\033[0m'  # Reset to default color

# Required values
db_name = "password_manager"
app_name = "Secure Vault"
ascii_title_art = pyfiglet.figlet_format(app_name, font="doom")
user = None  # Logged-in user, initialized as None and changed upon login

def create_db(name):
    '''
    This function is used to create the required database if it aint there on the pc. It also 
    generates a fernet key for the code.
    '''
    # connecting
    con = connector.connect(host="localhost",
                            user="root",
                            password="password",
                            charset="utf8")
    
    cur = con.cursor()
    cur.execute(f"create database {name}")
    cur.execute(f"use {name}")
    cur.execute("create table users (username varchar(30),password varchar(1000), primary key(username)) ")
    key = Fernet.generate_key()
    with open('key.dat', 'wb') as key_file:
        pickle.dump(key, key_file)
    con.commit()
    cur.close()
    con.close()

def encrypt(password):
    # loading key from binary file and creating key object
    key = Fernet(pickle.load(open("key.dat", "rb")))
    password_bytes = password.encode()  # converting string to bytes
    encrypted_pass_bytes = key.encrypt(password_bytes)  # bytes are being encrypted 
    encrypted_pass = encrypted_pass_bytes.decode()  # the encrypted bytes are decoded to text format
    return encrypted_pass

def decrypt(encrypted):
    # loading key from binary file and creating key object
    key = Fernet(pickle.load(open("key.dat", "rb")))
    encrypted_bytes = encrypted.encode()  # converting string to bytes
    decrypted_bytes = key.decrypt(encrypted_bytes)  # bytes are decrypted
    password = decrypted_bytes.decode()
    return password

# Password strength checker and generator functions
def strength_checker(password: str):
    import string
    strength = 0
    length_criteria = len(password) >= 8
    upper_criteria = lower_criteria = digit_criteria = special_criteria = False

    for ch in password:
        if ch.isupper():
            upper_criteria = True
        if ch.islower():
            lower_criteria = True
        if ch.isdigit():
            digit_criteria = True
        if ch in string.punctuation:
            special_criteria = True

    if length_criteria:
        strength += 1
    if upper_criteria:
        strength += 1
    if lower_criteria:
        strength += 1
    if digit_criteria:
        strength += 1
    if special_criteria:
        strength += 1

    if strength == 5:
        return "Strong password"
    elif 3 <= strength < 5:
        return "Moderate password"
    else:
        return "Weak password"

def generate_password(length=8):
    import random
    import string
    if length < 8:
        raise ValueError("Password length should be at least 8 characters.")
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ""
    while True:
        for _ in range(length):
            password += ''.join(random.choice(characters))
       
        if strength_checker(password) == "Strong password":
            return password
        

def login_screen():
    global user
    print("""MENU
1) Login    2) Register
""")
    while True:
        print()
        try:
            choice = int(input("Choice: "))
        except ValueError:
            print(f"{RED}Please enter a valid integer.{RESET}")
            continue
        print()

        if choice == 1:  # Login
            username = input("Username: ")
            cur = con.cursor()
            cur.execute(f"SELECT * FROM users WHERE username='{username}'")
            data = cur.fetchall()

            if data == []:
                print(f"{RED}Invalid username.{RESET}\n")
            else:
                password = pwinput.pwinput("Password: ", mask='*')
                if decrypt(data[0][1]) == password:
                    print(f"\n{GREEN}Login Successful{RESET}")
                    user = username
                else:
                    print(f"{RED}Invalid password{RESET}")
        elif choice == 2:  # Register
            username = input("Username: ")
            if username == "users":
                print(f"{YELLOW}Username cannot be 'users'.{RESET}")
                continue

            cur = con.cursor()
            cur.execute(f"SELECT * FROM users WHERE username='{username}'")
            if cur.fetchall() == []:  # Ensure unique username
                password = pwinput.pwinput("Password: ", mask='*')
                cur.execute(f"INSERT INTO users VALUES('{username}','{encrypt(password)}')")
                cur.execute(f"CREATE TABLE {username} (website VARCHAR(50), username VARCHAR(50), password VARCHAR(2000));")
                con.commit()
                user = username
                print(f"{GREEN}Registration Successful{RESET}\n")
            else:
                print(f"{RED}User already registered. Please login.{RESET}")
        else:
            print(f"{RED}Invalid Choice!{RESET}")

        if user:
            break

def menu():
    global user
    print(f"{MAGENTA}{pyfiglet.figlet_format(user, font='big')}{RESET}")
    menu_text = """
MENU
1) Store a password         2) Load a password
3) View all Passwords       4) Delete a password
5) Update a password        6) Password Generator
7) Password Strength Checker 8) Exit 
"""
    
    while True:
        print(menu_text)
        try:
            choice = int(input("Choice: "))
            os.system("cls")
        except ValueError:
            print(f"{RED}Please enter a valid integer.{RESET}")
            continue

        # Store a password
        if choice == 1:
            site = input("Enter website/application: ").lower()
            username_site = input("Enter username: ")
            pass_site = pwinput.pwinput("Enter password: ", mask='*')
            cur = con.cursor()
            cur.execute(f"INSERT INTO {user} VALUES('{site}','{username_site}','{encrypt(pass_site)}')")
            con.commit()
            print(f"{GREEN}Password successfully stored!{RESET}\n")

        # Load a password
        elif choice == 2:
            search = input("Enter Website/Application name: ").lower()
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {user} WHERE website = '{search}'")
            data = cur.fetchall()
            
            if data == []:
                print(f"{RED}No details found for {search}{RESET}")
            else:
                for record in data:
                    print(f"Username: {record[1]}\nPassword: {decrypt(record[2])}\n")

        # View all passwords
        elif choice == 3:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {user}")
            data = cur.fetchall()

            if data == []:
                print(f"{RED}No stored passwords.{RESET}")
            else:
                table_data = [[f"{GREEN}{i[0]}{RESET}", i[1], decrypt(i[2])] for i in data]
                print(tabulate.tabulate(table_data, headers=[f"{YELLOW}Website{RESET}", f"{YELLOW}Username{RESET}", f"{YELLOW}Password{RESET}"], tablefmt="grid"))

        # Delete a password (Handles multiple accounts)
        elif choice == 4:
            delete = input("Enter Website/Application name to delete: ").lower()
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {user} WHERE website = '{delete}'")
            data = cur.fetchall()

            if data == []:
                print(f"{RED}No details found for {delete}{RESET}")
                continue
            elif len(data) > 1:  # Multiple accounts for the same website
                print("Multiple accounts found:")
                for record in data:
                    print(f"Username: {record[1]}")
                check_user = input("Enter the username to delete: ")
                cur.execute(f"DELETE FROM {user} WHERE website = '{delete}' AND username = '{check_user}'")
            else:
                cur.execute(f"DELETE FROM {user} WHERE website = '{delete}'")
            con.commit()
            print(f"{GREEN}Deleted successfully!{RESET}\n")

        # Update a password (Handles multiple accounts)
        elif choice == 5:
            update_site = input("Enter Website/Application name to update: ").lower()
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {user} WHERE website = '{update_site}'")
            data = cur.fetchall()

            if data == []:
                print(f"{RED}No details found for {update_site}{RESET}")
                continue
            elif len(data) > 1:  # Multiple accounts for the same website
                print("Multiple accounts found:")
                for record in data:
                    print(f"Username: {record[1]}")
                check_user = input("Enter the username to update: ")
                new_username = input("Enter new username: ")
                new_password = pwinput.pwinput("Enter new password: ", mask='*')
                cur.execute(f"UPDATE {user} SET username = '{new_username}', password = '{encrypt(new_password)}' WHERE website = '{update_site}' AND username = '{check_user}'")
            else:
                new_username = input("Enter new username: ")
                new_password = pwinput.pwinput("Enter new password: ", mask='*')
                cur.execute(f"UPDATE {user} SET username = '{new_username}', password = '{encrypt(new_password)}' WHERE website = '{update_site}'")
            con.commit()
            print(f"{GREEN}Updated successfully!{RESET}\n")

        # Password Generator
        elif choice == 6:
            length = input("Enter the length for your password: ")
            if length.isdigit():
                try:
                    print(f"{YELLOW}Generated password: {generate_password(int(length))}{RESET}\n")
                except Exception as e:
                    print(f"{RED}{e}{RESET}")
            else:
                print(f"{RED}Enter a valid length!{RESET}\n")

        # Password Strength Checker
        elif choice == 7:
            passw = input("Enter your password: ")
            print(f"{YELLOW}{strength_checker(passw)}{RESET}\n")

        # Exit
        elif choice == 8:
            print(f"{GREEN}Thank you for using {app_name}!{RESET}")
            break

        else:
            print(f"{RED}Invalid choice!{RESET}\n")



# Main part of the code  
def main():
    global user
    print(f"{BLUE}{ascii_title_art}{RESET}")
    login_screen()
    os.system("cls")  # Clear terminal
    print(f"{GREEN}Logged in as {user}.{RESET}")
    menu()
    input("Press enter to exit !")
# Database connection setup
try:
    con = connector.connect(host="localhost", user="root", password="password", charset="utf8", database=db_name)
except Exception:
    create_db(db_name)  # Ensure the DB is created if it doesn't exist
    con = connector.connect(host="localhost", user="root", charset="utf8", password="password", database=db_name)

if con.is_connected():
    main()
else:
    print(f"{RED}Unable to connect, try again.{RESET}")

