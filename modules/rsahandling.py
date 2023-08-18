"""
Tools for dealing with cryptography
"""
from collections import namedtuple
import pathlib as pl
import rsa

class RsaTools():
    """Methods for accessing the rsa library
    
    Attributes
    ----------
    UserClass : class type
        Holds user information      
    Methods
    -------
    
    """    
    def __init__(self, user: 'user') -> None:
        """Initialize user class variables, set path variables for rsa keys.

        Parameters
        ----------
        UserClass : class type
            User data initiated via `user()` function from user module. 
        """        
        user : 'user'
        
        self.user = user
        self.pub_path = pl.Path(self.user.public_key_path)
        self.priv_path = pl.Path(self.user.private_key_path)
        no_public_key = not pl.Path(self.pub_path).exists()
        no_private_key = not pl.Path(self.priv_path).exists()
        
        #If no key pair exists in keys folder generate one.
        (public_key, private_key) = rsa.newkeys(1024)
        
        if no_public_key:    
            with open(self.pub_path, 'wb') as key:
                key.write(public_key.save_pkcs1('PEM'))

        if no_private_key:    
            with open(self.priv_path, 'wb') as key:
                key.write(private_key.save_pkcs1('PEM'))

    def load_keys(self) -> tuple[rsa.PrivateKey, rsa.PublicKey]:
        """Load keys from `keys` folder

        Returns
        -------
        named tuple
            Private and public key
        """
        Keys = namedtuple("Keys", ["public_key", "private_key"])
        
        with open(self.pub_path, 'rb') as key:
            public_key = rsa.PublicKey.load_pkcs1(key.read())
            
        with open(self.priv_path, 'rb') as key:
            private_key = rsa.PrivateKey.load_pkcs1(key.read())
        
        keys = Keys(public_key, private_key)
        return keys
        
    def encrypt_pwd(self, pwd: str) -> bytes:
        """Encrypt `pwd` with public key.

        Parameters
        ----------
        pwd : str
            String for encryption.

        Returns
        -------
        bytes
            Encrypted input.
        """
        pwd_enc = pwd.encode('utf8')
        pwd_crypt = rsa.encrypt(pwd_enc, self.load_keys().public_key)
        return pwd_crypt
    
    def decrypt_pwd(self, pwd: bytes) -> str:
        """Decrypt `pwd` with private key.

        Parameters
        ----------
        pwd : bytes
            Input for decryption.

        Returns
        -------
        str
            Decrypted input.
        """
        pwd_decrypt = rsa.decrypt(pwd, self.load_keys().private_key)
        return pwd_decrypt.decode('utf8')
        
    def __repr__(self) -> str:
        return str(vars(self))
        
    def __str__(self) -> str:
        return self.user.username