from cryptography.fernet import Fernet
from decouple import config


def cipher_suite():
    key = config('CRYPT').encode()
    return Fernet(key)