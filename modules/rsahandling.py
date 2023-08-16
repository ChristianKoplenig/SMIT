'''
Tools for dealing with cryptographie
'''
import rsa
import pathlib as pl
from user import user

class RsaTools():
    """Methods for accessing the rsa library
    
    Attributes
    ----------
    
    Methods
    -------
    """
    def __init__(self, UserClass: user) -> None:
        
        UserClass : user
        
        self.UserClass = UserClass
        self.pub_key = pl.Path('./keys/public_key.pem')
        self.priv_key = pl.Path('./keys/private_key.pem') 
        #print(key_path)
        print('init')
    
    def generate_keys(self) -> 'Keys':
        (public_key, private_key) = rsa.newkeys(1024)
        print('Keys generated')

        with open(self.pub_key, 'wb') as key:
            key.write(public_key.save_pkcs1('PEM'))
            print('pub written')
            
        with open(self.priv_key, 'wb') as key:
            key.write(private_key.save_pkcs1('PEM'))
            print('priv written')

a = user()
RsaTools(a).generate_keys()