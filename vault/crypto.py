from cryptography.fernet import Fernet
import base64
import os

KEY_FILE = "vault.key"

def load_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()

    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key


fernet = Fernet(load_or_create_key())

def encrypt(data: bytes) -> bytes:
    if isinstance(data, str):
        data = data.encode()
    return fernet.encrypt(data)

def decrypt(data: bytes) -> bytes:
    return fernet.decrypt(data)
