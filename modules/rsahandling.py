"""
Tools for dealing with cryptographie
"""
import rsa
import pathlib as pl
#from modules.user import user

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
        self.pub_path = pl.Path('./keys/public_key.pem')
        self.priv_path = pl.Path('./keys/private_key.pem')
        print('init')
        
        #If no key pair exists in keys folder generate one.
        (public_key, private_key) = rsa.newkeys(1024)
        print('Keys generated') 
        if not pl.Path(self.pub_path).exists():    
            with open(self.pub_path, 'wb') as key:
                key.write(public_key.save_pkcs1('PEM'))
                print('pub written')

        if not pl.Path(self.priv_path).exists():    
            with open(self.priv_path, 'wb') as key:
                key.write(private_key.save_pkcs1('PEM'))
                print('priv written')

    def load_keys(self) -> tuple[rsa.PrivateKey, rsa.PublicKey]:
        """Load keys from `keys` folder

        Returns
        -------
        tuple[PrivateKey, PublicKey]
            Tuple with key pair.
        """
        with open(self.pub_path, 'rb') as key:
            public_key = rsa.PublicKey.load_pkcs1(key.read())
            print('pub read')
            
        with open(self.priv_path, 'rb') as key:
            private_key = rsa.PrivateKey.load_pkcs1(key.read())
            print('priv read')        
        return private_key, public_key
        
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
        pwd_crypt = rsa.encrypt(pwd_enc, self.load_keys()[1])
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
        pwd_decrypt = rsa.decrypt(pwd, self.load_keys()[0])
        return pwd_decrypt.decode('utf8')
        
    def __repr__(self) -> str:
        return str(vars(self))
        
    def __str__(self) -> str:
        return self.user_instance.username   
    
##################debug###############

# if __name__ == '__main__':     
#     a = user()
#     #RsaTools(a).generate_keys()
#     # print(RsaTools(a).load_keys())

#     pass1 = 'teststring pass1'
#     p1_encode = RsaTools(a).encrypt_pwd(pass1)
#     print('enc: ' + str(p1_encode))
#     #RsaTools(a).decrypt_pwd(p1_encode)
#     print('dec: ' + str(RsaTools(a).decrypt_pwd(p1_encode)))