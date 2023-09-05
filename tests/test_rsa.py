# pylint: disable=no-member
import rsa
import pytest # pylint: disable=import-error
from SMIT.application import Application

app = Application(True)

@pytest.mark.crypto
def test_load_keys():
    """Test load rsa key function
    """
    with open(app.Path['public_key'], 'rb') as key:
        public_key = rsa.PublicKey.load_pkcs1(key.read())

    with open(app.Path['private_key'], 'rb') as key:
        private_key = rsa.PrivateKey.load_pkcs1(key.read())
    
    assert app.rsa._load_rsa_keys().private_key == private_key
    assert app.rsa._load_rsa_keys().public_key == public_key

@pytest.mark.crypto
def test_encryption() -> None:
    """Test rsa encrypt/decrypt.
    """
    test_pwd = 'String to test Rsa functionality'
    pwd_enc = app.rsa.encrypt_pwd(test_pwd)
    pwd_dec = app.rsa.decrypt_pwd(pwd_enc)
    assert test_pwd == pwd_dec