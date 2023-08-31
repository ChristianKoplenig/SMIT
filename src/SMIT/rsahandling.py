"""
Tools for dealing with cryptography
"""
from collections import namedtuple
import pathlib as pl
import rsa
# Type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from SMIT.application import Application
    
class RsaTools():
    """Methods for accessing the rsa library
    
    Attributes
    ----------
    app : class type
        Holds user information      
    Methods
    -------
    _load_rsa_keys():
        Make keys available for signing.
    encrypt_pwd(pwd):
        Encrypt pwd string with public key.
    decrypt_pwd(pwd):
        Decrypt pwd bytes object with private key.
    """    
    def __init__(self, app: 'Application') -> None:
        """Initialize class with all attributes from user config files.

        Parameters
        ----------
        app : class instance
            Holds the configuration data for program run.         
        """        
        self.user = app
        self.logger = app.logger
        self.pub_path = pl.Path(self.user.Path['public_key'])
        self.priv_path = pl.Path(self.user.Path['private_key'])
        no_public_key = not self.pub_path.exists()
        no_private_key = not self.priv_path.exists()
        
        #If no key pair exists in config folder generate one.
        if no_public_key or no_private_key:
            (public_key, private_key) = rsa.newkeys(1024)
            self.logger.warning('No Rsa key pair found')
        
        # Write public key    
            with open(self.pub_path, 'wb') as key:
                key.write(public_key.save_pkcs1('PEM'))
                self.logger.info('Public key written')
        # Write private key   
            with open(self.priv_path, 'wb') as key:
                key.write(private_key.save_pkcs1('PEM'))
                self.logger.info('Private key written')
        self.logger.debug('Module initialized successfully.')

    def _load_rsa_keys(self) -> tuple[rsa.PrivateKey, rsa.PublicKey]:
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
        
        return Keys(public_key, private_key)
        
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
        pwd_crypt = rsa.encrypt(pwd_enc, self._load_rsa_keys().public_key)
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
        pwd_decrypt = rsa.decrypt(pwd, self._load_rsa_keys().private_key)
        return pwd_decrypt.decode('utf8')
        
    def __repr__(self) -> str:
        return f"Module '{self.__class__.__module__}.{self.__class__.__name__}'"