import Crypto.Random as crypto
import monocypher
import base64

# key = bytes(crypto.get_random_bytes(32))
# print(key)
# print("SMP".encode())
# pub = monocypher.crypto_sign_public_key(key, b"SMP")
# key = base64.b64encode(key).decode()
# print(key)
# print(base64.b64decode(key))

# generates a key

def generate_key():
    keychain_start = b"SMP"
    key = bytes(crypto.get_random_bytes(32))
    pub = monocypher.crypto_sign_public_key(key, keychain_start)
    
    return pub

# distributes the key via a readable form, so converting it to base64 would make it a string 

def distribute_key(key : bytes):
    return base64.b64encode(key).decode()

# since we want to verify it later, it would be nice if we could have the original form of the key

def receive_key(key : str):
    return base64.b64decode(key)

# finally the verifying part :D

def verify_key(received_key : str, generated_key : bytes):
    return receive_key(received_key) == generated_key

# send the new keys to the one and only MAN

def retrieve_trustedman():
    with open('config/trusted-man', 'r') as trusted_man:
        trusted = trusted_man.read()
    return int(trusted)