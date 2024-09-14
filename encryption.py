def encrypt(password):
    from cryptography.fernet import Fernet
    import pickle
   
    #loading key from binary file and creating key object
    key=Fernet(pickle.load(open("key.dat","rb")))

    password_bytes=password.encode() # converting string to bytes
    encrypted_pass_bytes=key.encrypt(password_bytes)#bytes are being encrypted 

    encrypted_pass=encrypted_pass_bytes.decode()# the encrypted bytes are decoded to text format

    return encrypted_pass


def decrypt(encrypted):
    from cryptography.fernet import Fernet
    import pickle
   
    #loading key from binary file and creating key object
    key=Fernet(pickle.load(open("key.dat","rb")))
    encrypted_bytes=encrypted.encode()#converting string to bytes

    decrypted_bytes=key.decrypt(encrypted_bytes)#bytes are decrypted

    password=decrypted_bytes.decode()
    return password

