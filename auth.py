import Crypto.Random
import monocypher
import base64
import re

# key = bytes(crypto.get_random_bytes(32))
# print(key)
# print("SMP".encode())
# pub = monocypher.crypto_sign_public_key(key, b"SMP")
# key = base64.b64encode(key).decode()
# print(key)
# print(base64.b64decode(key))


# loads a key

def load_key():
    with open("config/keys", "r") as k:
        key = k.read()
        #print(f"key is {key}\nreturn key is {bytes(key.encode())}")

    return key

# generates a key

def generate_key():
    keychain_start = Crypto.Random.get_random_bytes(16) + b"SMP"
    
    key = bytes(Crypto.Random.get_random_bytes(32))
    monocypher.crypto_sign_public_key(key, keychain_start)
    
    with open("config/keys", "w") as k:
        k.write(str(key))
    
    # print(f"str key is {str(key)}\nNormal key is {key}")
    
    # del key
    return str(key)

# distributes the key via a readable form, so converting it to base64 would make it a string 

def distribute_key(key : str):
    return key.replace('"', "quotm")
#     # print(f"distributed key is {base64.b64encode(key).decode()}")
#     return base64.b64encode(key).decode()

# since we want to verify it later, it would be nice if we could have the original form of the key

def receive_key(key : str):
    return key.replace("quotm", '"')
#     # print(f"To receive key : {key}\nreceived key is {bytes(base64.b64decode(key))}")

#     # return f"b'{base64.b64decode(key)}'"
#     try:
#         return str(base64.b64decode(key).decode())
#     except Exception as e:
#         print(e)
#         return b"Hopa nu ebn"

# finally the verifying part :D

def verify_key(received_key : str):
    #print(f"Cheia corecta : {load_key()}\nCheia incercata: {receive_key(received_key)}")
    return receive_key(received_key) == load_key()

# send the new keys to the one and only MAN

def retrieve_trustedman():
    with open('config/trusted-man', 'r') as trusted_man:
        trusted = trusted_man.readlines()
    return list(trusted)