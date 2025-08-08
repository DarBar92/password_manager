import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend

SALT_FILE = "salt.salt"
ITERATIONS = 390000

def generate_salt():
    return os.urandom(16)

def get_salt():
    if not os.path.exists(SALT_FILE):
        with open(SALT_FILE, "wb") as f:
            f.write(generate_salt())
    with open(SALT_FILE, "rb") as f:
        return f.read()

def derive_key(password: str) -> bytes:
    salt = get_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_data(data: str, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(data: bytes, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(data).decode()