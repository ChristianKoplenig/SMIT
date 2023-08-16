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
        self.pub_path = pl.Path('./keys/public_key.pem')
        self.priv_path = pl.Path('./keys/private_key.pem') 
        #print(key_path)
        print('init')
    
    def generate_keys(self) -> 'Keys':
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

    def load_keys(self) -> 'KeyPair':
        with open(self.pub_path, 'rb') as key:
            public_key = rsa.PublicKey.load_pkcs1(key.read())
            print('pub read')
            
        with open(self.priv_path, 'rb') as key:
            private_key = rsa.PrivateKey.load_pkcs1(key.read())
            print('priv read')        
        return private_key, public_key
        
    def encode_pwd(self, pwd: str) -> str:
        pwd_enc = pwd.encode('utf8')
        pwd_crypt = rsa.encrypt(pwd_enc, self.load_keys()[1])
        return pwd_crypt
    
    def decrypt_pwd(self, pwd: str) -> str:
        pwd_decrypt = rsa.decrypt(pwd, self.load_keys()[0])
        return pwd_decrypt.decode('utf8')
        
a = user()
#RsaTools(a).generate_keys()
# print(RsaTools(a).load_keys())

pass1 = 'teststring pass1'
p1_encode = RsaTools(a).encode_pwd(pass1)
print('enc: ' + str(p1_encode))
#RsaTools(a).decrypt_pwd(p1_encode)
print('dec: ' + str(RsaTools(a).decrypt_pwd(p1_encode)))