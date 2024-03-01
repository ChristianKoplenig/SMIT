"""Argon2ID password hashing and verification."""
from typing import Annotated
from argon2 import PasswordHasher

class Hasher:
    """Provide password hashing and verification.
    
    Use argon2id algorithm for hashing.

    Attributes:
        ph (PasswordHasher): Instance of argon2 library.

    Methods:
        verify_password: Verify if a plain text password matches a hashed password.
        hash_password: Create hash for input string.
        needs_rehash: Check if a hash needs to be updated.
    """

    def __init__(self) -> None:
        """Initialise PasswordHasher instance.

        Use default settings from PasswordHasher class.

        Settings:
            - time_cost=3 
            - memory_cost=65536
            - parallelism=4
            - hash_len=32
            - salt_len=16
            - encoding='utf-8'
            - type=Type.ID
        """
        self.ph = PasswordHasher()

    def verify_password(
            self,
            plain_password: Annotated[bytes | str, 'Plain text password to verify.'],
            hashed_password: Annotated[bytes | str, 'Hashed password to compare with.']
            ) -> bool:
        """
        Verify if a plain text password matches a hashed password.

        Args:
            plain_password (bytes | str): Plain text password to verify.
            hashed_password (bytes | str): Hashed password to compare with.

        Returns:
            bool: Verification status.
        """
        try:
            self.ph.verify(hashed_password, plain_password)
            return True
        except Exception:
            return False

    def hash_password(
                self,
                password: Annotated[bytes | str, 'Password to hash']
                ) -> str:
            """Create hash for input string.

            Use default settings from Hasher class to generate hash.

            Args:
                password (bytes | str): Password to hash.

            Returns:
                str: Hashed password.

            Raises:
                Exception: argon2.exceptions.HashingError.
            """
            try:
                hash: str = self.ph.hash(password)
                return hash
            except Exception as e:
                raise e
            
    def needs_rehash(
              self,
              hash: Annotated[str, 'Hashed password to check']
              ) -> bool:
        """Check if a hash needs to be updated.

        Check if there was a change in the hashing default settings.
        Use to stay up to date with the latest security standards.

        Returns:
            bool: True if default settings changed.
        """
        return self.ph.check_needs_rehash(hash)

