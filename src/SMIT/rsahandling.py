"""Public key cryptography

---
`RsaTools`
----------

- Generate Rsa key pair for application.
- Decrypt password from `user_data.toml` file.
- Encrypt password with application key.

Typical usage:

    app = Application()
    app.rsa.method()
"""
from collections import namedtuple
import pathlib as pl
import rsa
# Type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from SMIT.application import Application


class RsaTools():
    """Use Rsa encryption for password storing.

    ---

    Generate a Rsa key pair and store it in the config folder.
    If the user decides to save the password, this key pair 
    will be used to encrypt/decrypt the password.
    The password will be saved in the `user_data.toml`
    configuration file. 

    Attributes:
        app (class): Accepts `SMIT.application.Application` type attribute.
    """
    def __init__(self, app: 'Application') -> None:

        self.user = app
        self.logger = app.logger
        self.pub_path = pl.Path(self.user.Path['public_key'])
        self.priv_path = pl.Path(self.user.Path['private_key'])
        no_public_key = not self.pub_path.exists()
        no_private_key = not self.priv_path.exists()

        # If no key pair exists in config folder generate one.
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

        msg  = f'Class {self.__class__.__name__} of the '
        msg += f'module {self.__class__.__module__} '
        msg +=  'successfully initialized.'
        self.logger.debug(msg)

    def _load_rsa_keys(self) -> tuple[rsa.PrivateKey, rsa.PublicKey]:
        """Load keys from config folder.

        Make keys accessible via dot notation.
        
        Returns:
            tuple: A named tuple holding the 
                `public_key` and the `private_key`.
        """
        Keys = namedtuple("Keys", ["public_key", "private_key"])

        with open(self.pub_path, 'rb') as key:
            public_key = rsa.PublicKey.load_pkcs1(key.read())

        with open(self.priv_path, 'rb') as key:
            private_key = rsa.PrivateKey.load_pkcs1(key.read())

        return Keys(public_key, private_key)

    def encrypt_pwd(self, pwd: str) -> bytes:
        """Convert and encrypt input.

        Convert the input string to bytes object
        needed for storing in configuration files.  
        Encrypt the object using the rsa library and the 
        public key from the config folder.
        
        Note:
            A bytes object is used because TOML files need
            this data structure to store information.

        Args:
            pwd (string): String for encryption.

        Returns:
            bytes: Encrypted input.
        """
        pwd_enc = pwd.encode('utf8')
        pwd_crypt = rsa.encrypt(pwd_enc, self._load_rsa_keys().public_key)
        return pwd_crypt

    def decrypt_pwd(self, pwd: bytes) -> str:
        """Decrypt bytes object.

        Decrypt the input using the rsa library and the 
        private key from the config folder.  
        Decode the bytes object to string format.
        
        Note:
            A bytes object is used because TOML files need
            this data structure to store information.

        Args:
            pwd (bytes): Input for decryption.

        Returns:
            string: Decrypted input.
        """
        pwd_decrypt = rsa.decrypt(pwd, self._load_rsa_keys().private_key)
        return pwd_decrypt.decode('utf8')

    def __repr__(self) -> str:
        return f"Module '{self.__class__.__module__}.{self.__class__.__name__}'"


# Pdoc config get underscore methods
__pdoc__ = {name: True
            for name, classes in globals().items()
            if name.startswith('_') and isinstance(classes, type)}


__pdoc__.update({f'{name}.{member}': True
                 for name, classes in globals().items()
                 if isinstance(classes, type)
                 for member in classes.__dict__.keys()
                 if member not in {'__module__', '__dict__',
                                   '__weakref__', '__doc__'}})

__pdoc__.update({f'{name}.{member}': False
                 for name, classes in globals().items()
                 if isinstance(classes, type)
                 for member in classes.__dict__.keys()
                 if member.__contains__('__') and member not in {'__module__', '__dict__',
                                                                 '__weakref__', '__doc__'}})
