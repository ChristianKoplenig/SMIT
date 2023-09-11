"""Test the crypto functionality
"""
# pylint: disable=no-member
import rsa
import pytest # pylint: disable=import-error

from SMIT.application import Application

app = Application(True)

@pytest.mark.smoke
@pytest.mark.crypto
def test_load_rsakeys():
    """Test load rsa keys.
    
    Assert:
        Static loaded keys against dynamically loaded keys.
        
    Note:
        The application uses rsa cryptography to store the 
        encrypted user password. The keys are generated on the
        first instantiation of the Application class and are stored
        in the config folder. 
    """
    with open(app.Path['public_key'], 'rb') as key:
        public_key = rsa.PublicKey.load_pkcs1(key.read())

    with open(app.Path['private_key'], 'rb') as key:
        private_key = rsa.PrivateKey.load_pkcs1(key.read())
    
    assert app.rsa._load_rsa_keys().private_key == private_key
    assert app.rsa._load_rsa_keys().public_key == public_key

@pytest.mark.smoke
@pytest.mark.crypto
def test_encryption():
    """Test rsa encrypt/decrypt.
    
    Assert:
        If variable gets correctly encrypted and decrypted.
    """
    test_pwd = 'String to test Rsa functionality'
    pwd_enc = app.rsa.encrypt_pwd(test_pwd)
    pwd_dec = app.rsa.decrypt_pwd(pwd_enc)
    assert test_pwd == pwd_dec