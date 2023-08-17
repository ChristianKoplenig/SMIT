"""
Tools for dealing with cryptography
"""
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
    def __init__(self, UserInstance: 'user') -> None:
        """Initialize user class variables, set path variables for rsa keys.

        Parameters
        ----------
        UserClass : class type
            User data initiated via `user()` function from user module. 
        """        
        UserInstance : 'user'
        
        self.user_instance = UserInstance
        self.pub_path = pl.Path(self.user_instance.public_key_path)
        self.priv_path = pl.Path(self.user_instance.private_key_path)
        
        #If no key pair exists in keys folder generate one.
        (public_key, private_key) = rsa.newkeys(1024)
        
        if not pl.Path(self.pub_path).exists():    
            with open(self.pub_path, 'wb') as key:
                key.write(public_key.save_pkcs1('PEM'))

        if not pl.Path(self.priv_path).exists():    
            with open(self.priv_path, 'wb') as key:
                key.write(private_key.save_pkcs1('PEM'))

    def load_keys(self) -> tuple[rsa.PrivateKey, rsa.PublicKey]:
        """Load keys from `keys` folder

        Returns
        -------
        dict
            Private and public key
        """
        with open(self.pub_path, 'rb') as key:
            public_key = rsa.PublicKey.load_pkcs1(key.read())
            
        with open(self.priv_path, 'rb') as key:
            private_key = rsa.PrivateKey.load_pkcs1(key.read())
        keys = {
            'private_key': private_key,
            'public_key': public_key
        }        
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
        pwd_crypt = rsa.encrypt(pwd_enc, self.load_keys()['public_key'])
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
        pwd_decrypt = rsa.decrypt(pwd, self.load_keys()['private_key'])
        return pwd_decrypt.decode('utf8')
        
    def __repr__(self) -> str:
        return str(vars(self))
        
    def __str__(self) -> str:
        return self.user_instance.username