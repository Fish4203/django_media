import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet



def enc(data, password):
    password_encode = password.encode()
    data_encode = data.encode()
    salt = os.urandom(16)

    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
    )

    f = Fernet(base64.urlsafe_b64encode(kdf.derive(password_encode)))

    return f.encrypt(data_encode)


def denc(data, password):
    password_encode = password.encode()
    salt = os.urandom(16)

    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
    )

    f = Fernet(base64.urlsafe_b64encode(kdf.derive(password_encode)))

    return f.decrypt(data)
