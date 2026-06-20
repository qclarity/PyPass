from argon2 import PasswordHasher
from dataclasses import asdict
from errors import NoVaultError, EntryNotFoundError, PasswordsNotMatchError, NoPasswordError, PasswordVerificationError, TooManyAttemptsError
from pathlib import Path
from crypto_service import CryptoService
from file_service import FileService
from models import PassInfo
from constants import ConfigKeyConstants

class PasswordManager:
    """
    Class for storing methods of hashing, encrypting, decrypting, formatting, and the storing of sensitive data.
    """
    def __init__(
            self,
            password_file: Path,
            ph: PasswordHasher,
            salt_file: Path,
            vault_file: Path):
        """
        Args:
            ph: The class for hashing a plaintext password.
            password_file: The text-file for storing hashed password.
            salt_file: The binary-file for storing a constant salt.
            vault_file: The encrypted-file for storing sensitive data.
        """
        self.password_file = password_file
        self.ph = ph
        self.salt_file = salt_file
        self.vault_file = vault_file
        self.fs = FileService(vault_file=vault_file, password_file=password_file, salt_file=salt_file)
        self.cs = CryptoService(ph=self.ph)
        self.data = self.fs.load_lock_state()

    @staticmethod
    def search_data(name: str, data: dict[str, PassInfo]) -> PassInfo:
        if name in data:
            return data[name]
        raise EntryNotFoundError('App data could not be located.')

    @staticmethod
    def compare_passwords(pass1: str, pass2: str) -> None:
        if pass1 == '' or pass2 == '':
            raise NoPasswordError('A password must be inputted for creation.')
        if pass1 != pass2:
            raise PasswordsNotMatchError('Passwords do not match.')

    @staticmethod
    def dataclass_to_dict(app_data: dict[str, PassInfo]) -> dict[str, dict[str, str]]:
        return {entry: asdict(data) for entry, data in app_data.items()}

    @staticmethod
    def dict_to_dataclass(app_data: dict[str, dict[str, str]], pass_info_cls: type[PassInfo]) -> dict[str, PassInfo]:
        return {entry: pass_info_cls(**data) for entry, data in app_data.items()}

    def hash_password(self, plaintext_pass: str) -> str:
        return self.cs.hash_password(plaintext_pass=plaintext_pass)

    def verify_password(self, attempt: str) -> bool:
        password = self.fs.read_password()

        if len(attempt) == 0:
            raise NoPasswordError('A password cannot be blank for validation.')
 
        if self.data[ConfigKeyConstants.LOGIN_ATTEMPTS] >= 3:
            self.fs.lock_for_hour(data=self.data)
            raise TooManyAttemptsError('Too many attempts. Lock the program.')
        
        try:
            is_valid = self.cs.verify_password(hashed_pass=password, plaintext=attempt)
            if is_valid:
                self.data[ConfigKeyConstants.LOGIN_ATTEMPTS] = 0
                self.fs.save_lock_state(data=self.data)
                self.check_rehash(stored_hash=password, plaintext=attempt)
            return is_valid
        
        except PasswordVerificationError:
            self.data[ConfigKeyConstants.LOGIN_ATTEMPTS] += 1

            if self.data[ConfigKeyConstants.LOGIN_ATTEMPTS] >= 3:
                self.fs.lock_for_hour(data=self.data)
                self.fs.save_lock_state(data=self.data)
                raise TooManyAttemptsError('Too many failed attempts. Lock the program.')

            self.fs.save_lock_state(data=self.data)
            raise

    def check_rehash(self, stored_hash: str, plaintext: str) -> None:
        if self.ph.check_needs_rehash(stored_hash):
            new_hash = self.ph.hash(plaintext)
            self.fs.save_pass(password=new_hash)
    
    def check_lock(self):
        return self.fs.check_lock()

    def get_or_create_salt(self) -> bytes:
        return self.cs.get_or_create_salt(salt_file=self.salt_file) 
            
    def key_derivation(self, password: str, salt: bytes) -> bytes:
        return self.cs.key_derivation(password=password, salt=salt)
    
    def decrypt_data(self, raw_data: bytes, key: bytes) -> dict[str, dict[str, str]]:
        return self.cs.decrypt_data(raw_data=raw_data, key=key)
    
    def encrypt_data(self, data: dict[str, PassInfo], key: bytes) -> bytes:
        formatted_data = self.dataclass_to_dict(app_data=data)
        return self.cs.encrypt_data(key=key, formatted_data=formatted_data)
    
    def clear_vault(self) -> None:
        return self.fs.clear_vault_file()
    
    def read_raw_data(self) -> bytes:
        return self.fs.read_raw_data()
    
    def read_password(self) -> str:
        return self.fs.read_password()
    
    def save_vault_data(self, encrypted_data: bytes) -> None:
        return self.fs.save_vault_data(encrypted_data=encrypted_data)
    
    def verify_vault_file(self) -> bool:
        return self.fs.verify_vault_file()
    
    def verify_password_file(self) -> bool:
        return self.fs.verify_password_file()
    
    def save_salt(self, salt: bytes) -> None:
        return self.fs.save_salt(salt=salt)
    
    def initialize_password(self, plaintext: str) -> None:
        self.clear_vault()
        hashed_password = self.hash_password(plaintext_pass=plaintext)
        self.fs.save_pass(password=hashed_password)

    def load_data(self, pass_info_cls: type[PassInfo], key: bytes) -> dict[str, PassInfo]:
        if not self.verify_vault_file():
            raise NoVaultError('Vault file does not exist.')

        raw_data = self.read_raw_data()
        decrypted_data = self.decrypt_data(raw_data=raw_data, key=key)
        return self.dict_to_dataclass(app_data=decrypted_data, pass_info_cls=pass_info_cls)
    
    def del_data(self, data: dict[str, PassInfo], name: str, key: bytes) -> None:
        del data[name]
        encrypted_data = self.encrypt_data(data=data, key=key)
        self.save_vault_data(encrypted_data=encrypted_data)

    def clear_salt(self) -> None:
        self.fs.clear_salt_file()