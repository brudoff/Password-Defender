from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import hashlib


class Crypter:
    """ Crypter objects responsible for encrypt/decrypt data """

    def __init__(self):
        self.__fernet_key = None
        self.__master_key = ""

    def load_master_key(self, filename):
        # Read hash of MK from file excepted salt
        with open(filename, 'rb') as file:
             hash = file.read()
             self.__salt = hash[:33]
             self.__master_key = hash[32:]
        return 0

    def check_master_key(self, _key):
        # Compare master key hash with storage hash
        if self.__master_key == hashlib.sha256(_key.encode('utf-8')).digest():
            self.__initKey(_key)
            return True
        else:
            return False

    def create_master_key(self, key, filename):
        # Create file for storage MK
        with open(filename, 'wb') as file:
            # Generate salt
            self.__salt = os.urandom(32)
            # Encode password
            self.__master_key = hashlib.sha256(key.encode('utf-8')).digest()
            # Save hash of MK to file
            hash = self.__salt + self.__master_key
            file.write(hash)
            self.__initKey(key)

    def __initKey(self, _key):
        kdf = PBKDF2HMAC(algorithm=hashes.SHA512(), salt=self.__salt,
                         length=32, iterations=400000)
        self.__fernet_key = base64.urlsafe_b64encode(kdf.derive(_key.encode()))
        self.__fernet = Fernet(self.__fernet_key)

    def encrypt(self, data):
        if data:
            return self.__fernet.encrypt(data.encode('utf-8'))

    def decrypt(self, data):
        if data:
            return self.__fernet.decrypt(data)

    def fernetKey(self):
        return self.__fernet_key
