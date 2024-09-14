def create_db(name):
    '''
This function is used to create the required database if it aint there on the pc. It also 
generates a fernet key for the code.
    '''
    #necessary imports
    from cryptography.fernet import Fernet
    import pickle
    import mysql.connector as connector 
    #connecting
    con=connector.connect(host="localhost",
                    user="root",
                    password="password",
                    charset="utf8")
    
    cur=con.cursor()
    cur.execute(f"create database {name}")
    cur.execute(f"use {name}")
    #cur.execute("create table passwords (website varchar(30),username varchar(25),password varchar(120),primary key(website));")
    #generates a key for fernet
    cur.execute("create table users (username varchar(30),password varchar(1000), primary key(username)) ")
    key=Fernet.generate_key()
    with open('key.dat', 'wb') as key_file:
        pickle.dump(key, key_file)
    con.commit()
    cur.close()
    con.close()


