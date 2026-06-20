from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from errors import PasswordVerificationError, VaultDecryptionError, NoPasswordError, InvalidSaltLengthError
import os
import base64
from pathlib import Path
import json
from json import JSONDecodeError
from constants import KDFParamConstants

class CryptoService:
    """
    Class for storing methods of data/password encryption and hashing.
    """
    def __init__(
            self,
            ph: PasswordHasher):
        """
        Attributes:
            ph: Class for hashing a plaintext password.
        """
        self.ph = ph

    @staticmethod
    def get_or_create_salt(salt_file: Path) -> bytes:
        """
            Retrieves or generates a 16-byte salt used for key derivation.

            Args:
                salt_file: Filepath for storing the location of the uniquely generated salt in binary.

            Returns:
                bytes: The 16-byte salt required for Argon2id key derivation function.
            """
        if os.path.exists(salt_file) and os.path.getsize(salt_file) > 0:
            with open(salt_file, 'rb') as f:
                current_salt = f.read()
                if len(current_salt) != KDFParamConstants.SALT_LENGTH:
                    raise InvalidSaltLengthError('A valid salt must be 16-bytes.')
                return current_salt

        salt = os.urandom(KDFParamConstants.SALT_LENGTH)
        with open(salt_file, 'wb') as f:
            f.write(salt)
        return salt

    @staticmethod
    def key_derivation(password: str, salt: bytes) -> bytes:
        """
        Securely derives an encryption key using Argon2id's key derivation function.
        For more information: https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/

        Args:
            password: The plaintext password to be used to derive encryption key.
            salt: The 16-byte salt required to always generate a unique derivation key.

        Returns:
            bytes: The key used to encrypt and decrypt the user's data.
        """
        kdf = Argon2id(
            salt=salt,
            length=KDFParamConstants.LENGTH,
            iterations=KDFParamConstants.ITERATIONS,
            lanes=KDFParamConstants.LANES,
            memory_cost=KDFParamConstants.MEMORY_COST,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    @staticmethod
    def decrypt_data(raw_data: bytes, key: bytes) -> dict[str, dict[str, str]]:
        fernet = Fernet(key)
        try:
            decrypted_bytes = fernet.decrypt(raw_data)
            return json.loads(decrypted_bytes.decode())
        except InvalidToken:
            raise VaultDecryptionError('Failed to decrypt vault data.')
        except JSONDecodeError:
            raise VaultDecryptionError('Failed to decrypt vault data.')

    @staticmethod
    def encrypt_data(key: bytes, formatted_data: dict[str, dict[str, str]]) -> bytes:
        fernet = Fernet(key)
        data_bytes = json.dumps(formatted_data).encode()
        return fernet.encrypt(data_bytes)

    def hash_password(self, plaintext_pass: str) -> str:
        if not plaintext_pass:
            raise NoPasswordError('A password length cannot be 0.')
        return self.ph.hash(plaintext_pass)

    def verify_password(self, hashed_pass: str, plaintext: str) -> bool:
        try:
            return self.ph.verify(hash=hashed_pass, password=plaintext)

        except VerificationError:
            raise PasswordVerificationError('Password could not be verified.')