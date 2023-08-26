# Imports to make custom modules work
import sys
import pathlib as pl
import base64
import tomlkit

# Add custom modules path to sys.path and import
module_dir = pl.Path("__file__").resolve().parent

if sys.path[0] != str(module_dir):
    sys.path.insert(0, str(module_dir))
################################################
# Setup
from SMIT.user import user
from SMIT.rsahandling import RsaTools
from SMIT.filehandling import TomlTools
user = user() 
################################################
rsa = RsaTools(user)
toml = TomlTools(user)
toml_file = pl.Path('./rsa_test.toml')
pwd = 'rsa_test with \n newline and\nnew inline'
pwd_bytes = b'rsa_test with \n newline and\nnew inline'

def pwd_to_string(pwd: bytes) -> str:
    """Takes password object and converts it to string.

    Parameters
    ----------
    pwd : bytes
        Object for conversion to string.

    Returns
    -------
    str
        String representation of bytes object.
    """

############## store password ##############    
# #Crypto
# pwd_enc = rsa.encrypt_pwd(pwd)
# #pwd_dec = rsa.decrypt_pwd(pwd_enc)

# #Toml input
# pwd_toml = base64.b64encode(pwd_enc).decode('utf-8')
# #toml_dec = base64.b64decode(pwd_toml).decode('utf-8')

# #Toml write
# data = toml.load_toml_file(toml_file)
# data['Login']['password'] = pwd_toml #tomlkit.parse(pwd_enc)
# toml.save_toml_file(toml_file, data)


# print('pwd_enc')
# print(type(pwd_enc))
# print(f"{pwd_enc}\n")

# print('pwd_toml')
# print(type(pwd_toml))
# print(f"{pwd_toml}\n")

# print('toml data')
# print(type(data))
# print(f"{data}\n")

################# retrieve password ####################
#load file
data = toml.load_toml_file(toml_file)
print('toml data')
print(type(data))
print(f"{data['Login']['password']}\n")

#base64 decode
to_dec = data['Login']['password']
print('to_dec')
print(type(to_dec))
print(f"{to_dec}\n")

b64_decode = base64.b64decode(to_dec)#.decode('utf-8')
print('b64_decode')
print(type(b64_decode))
print(f"{b64_decode}\n")


password = rsa.decrypt_pwd(b64_decode)
print('password')
print(type(password))
print(f"{password}\n")