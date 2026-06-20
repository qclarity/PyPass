from pathlib import Path
import tempfile
import os
import json
from json import JSONDecodeError
from constants import FileConstants, ConfigKeyConstants, TimeConstants
import time

class FileService:
    """
    Class for storing methods of file handling.
    """
    def __init__(
            self,
            vault_file: Path,
            password_file: Path,
            salt_file: Path):
        """
        Args:
            vault_file: Filepath for storing the location of the vault file.
            password_file: Filepath for storing the location of the hashed password file.
            salt_file: Filepath for storing the location of the uniquely generated salt in binary.
        """
        self.vault_file = vault_file
        self.password_file = password_file
        self.salt_file = salt_file

    @staticmethod
    def _has_content(path: Path) -> bool:
        return path.exists() and path.stat().st_size > 0

    @staticmethod
    def lock_for_hour(data: dict) -> None:
        with open(FileConstants.CONFIG_PATH, 'w') as f:
            lock_time = time.time() + TimeConstants.LOCKOUT_TIME
            data[ConfigKeyConstants.LOCK_UNTIL] = lock_time
            data[ConfigKeyConstants.LOGIN_ATTEMPTS] = 0
            json.dump(data, f, indent=4)

    @staticmethod
    def save_lock_state(data: dict) -> None:
        with open(FileConstants.CONFIG_PATH, 'w') as f:
            json.dump(data, f, indent=4)
            os.chmod(FileConstants.CONFIG_PATH, 0o600)

    @staticmethod
    def get_config_defaults() -> dict[str, int]:
        return {
            ConfigKeyConstants.LOGIN_ATTEMPTS: 0,
            ConfigKeyConstants.LOCK_UNTIL: 0
            }

    def clear_vault_file(self) -> None:
        self.vault_file.write_text('')
        os.chmod(self.vault_file, 0o600)

    def read_raw_data(self) -> bytes:
        return self.vault_file.read_bytes()
    
    def read_password(self) -> str:
        return self.password_file.read_text()

    def save_vault_data(self, encrypted_data: bytes) -> None:
        with tempfile.NamedTemporaryFile('wb', dir=self.vault_file.parent, delete=False) as temp_file:
            temp_file.write(encrypted_data)
            temp_file.flush()
            os.fsync(temp_file.fileno())
            temp_name = temp_file.name

        Path(temp_name).replace(Path(self.vault_file))
        os.chmod(self.vault_file, 0o600)

    def verify_vault_file(self) -> bool:
        return self._has_content(path=self.vault_file)
        
    def verify_password_file(self) -> bool:
        return self._has_content(path=self.password_file)
    
    def save_salt(self, salt: bytes) -> None:
        self.salt_file.write_bytes(salt)
        os.chmod(self.salt_file, 0o600)

    def save_pass(self, password: str) -> None:
        self.password_file.write_text(password)
        os.chmod(self.password_file, 0o600)

    def check_lock(self) -> float:
        if self._has_content(path=FileConstants.CONFIG_PATH):
            try:
                with open(FileConstants.CONFIG_PATH, 'r') as f:
                    data = json.load(f)
                    return data[ConfigKeyConstants.LOCK_UNTIL]
            except JSONDecodeError:
                data = self.get_config_defaults()
                lock_time = data[ConfigKeyConstants.LOCK_UNTIL]
                return lock_time
        return self.load_lock_state()[ConfigKeyConstants.LOCK_UNTIL]

    def load_lock_state(self) -> dict:
        if not self._has_content(path=FileConstants.CONFIG_PATH):
            return self.get_config_defaults() 
        
        try:
            with open(FileConstants.CONFIG_PATH, 'r') as f:
                return json.load(f)
        except JSONDecodeError:
            return self.get_config_defaults()

    def clear_salt_file(self) -> None:
        self.salt_file.write_bytes(b'')
        os.chmod(self.salt_file, 0o600)