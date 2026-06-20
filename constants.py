from typing import Final
from pathlib import Path

class FileConstants:
    """Class for storing constants regarding files used throughout the program as strings."""
    VAULT_PATH: Final[Path] = Path('vault.enc')
    PASS_PATH: Final[Path] = Path('pass.hash')
    SALT_PATH: Final[Path] = Path('salt.bin')
    CONFIG_PATH: Final[Path] = Path('config.json')

class WindowConstants:
    """Class for storing constants regarding window dimensions as strings."""
    NEW_DATA_WINDOW_SIZE: Final[str] = '400x400'
    DATA_WINDOW_SIZE: Final[str] = '400x450'
    START_WINDOW_SIZE: Final[str] = '400x500'
    MAIN_WINDOW_SIZE: Final[str] = '600x500'

class FontConstants:
    """Class for storing constants regarding fonts and their corresponding size as tuples."""
    SMALL_FONT: Final[tuple[str, int]] = ('Arial', 11)
    MEDIUM_FONT: Final[tuple[str, int]] = ('Arial', 15)
    LARGE_FONT: Final[tuple[str, int]] = ('Arial', 20)

class TextConstants:
    """Class for storing constants regarding UI text elements to be displayed as strings."""
    TITLE: Final[str] = 'PyPass'
    COPY_TEXT: Final[str] = '⧉'
    DATA_SAVED_TEXT: Final[str] = '✓ Data saved'
    DATA_ERROR_TEXT: Final[str] = '❌Application data already exists'
    INPUT_PASS_TEXT: Final[str] = 'Please input a password'
    PASS_NOT_MATCH_TEXT: Final[str] = 'Passwords do not match'
    SAVED_TEXT: Final[str] = '✓ Changes saved'
    UNSAVED_TEXT: Final[str] = '⚠️ Unsaved changes'
    PASS_VERIFY_ERR_TEXT: Final[str] = 'Password verification failed'
    NO_DATA_STORED: Final[str] = '❌ No data is stored'
    LOGIN: Final[str] = 'Login'
    PASSWORD: Final[str] = 'Password'
    SHOW_PASSWORD: Final[str] = 'Show password'
    CANCEL: Final[str] = 'Cancel'
    SEARCH: Final[str] = 'Search'
    ADD_DATA: Final[str] = 'Add data'
    USER: Final[str] = 'User'
    USERNAME: Final[str] = 'Username'
    APP: Final[str] = 'App'
    APPLICATION: Final[str] = 'Application'
    PHONE: Final[str] = 'Phone'
    SAVE: Final[str] = 'Save'
    CREATE_PASSWORD: Final[str] = 'Create password'
    CONFIRM_PASSWORD: Final[str] = 'Confirm password'
    CREATE: Final[str] = 'Create'
    SPACES_ALLOWED: Final[str] = 'Spaces are allowed in passwords'
    EXIT: Final[str] = 'Exit'
    DEL_DATA: Final[str] = 'Delete data'
    EDIT_MODE: Final[str] = 'Edit mode'

class ColorConstants:
    """Class for storing constants regarding color values as strings."""
    SUCCESS_COLOR: Final[str] = 'green'
    FAIL_COLOR: Final[str] = 'red'
    WARNING_COLOR: Final[str] = 'yellow'
    GRAY_COLOR: Final[str] = 'gray'
    COPY_PASTE_BTN_COLOR: Final[str] = '#343638'
    ODD_BTN_COLOR: Final[str] = '#212120'
    EVEN_BTN_COLOR: Final[str] = 'transparent'

class KeybindConstants:
    """Class for storing constants regarding keybinds for quicker navigation as strings."""
    CLOSE_WIND_KEYBIND: Final[str] = '<Escape>'
    DEL_DATA_KEYBIND: Final[str] = '<Shift-D>'
    CHECK_KEYBIND: Final[str] = '<Return>'
    ADD_DATA_KEYBIND: Final[str] = '<Shift-A>'
    LEFT_CLICK: Final[str] = '<Button-1>'
    ANY_KEYPRESS: Final[str] = '<Any-KeyPress>'
    ANY_BUTTONPRESS: Final[str] = '<Any-ButtonPress>'
    MOTION: Final[str] = '<Motion>'

class KDFParamConstants:
    """Class for storing constants regarding the params for the Argon2id KDF function as integers."""
    SALT_LENGTH: Final[int] = 16
    LENGTH: Final[int] = 32
    ITERATIONS: Final[int] = 3
    LANES: Final[int] = 4
    MEMORY_COST: Final[int] = 256 * 1024

class HasherParamConstants:
    """Class for storing constants regarding argon2's PasswordHasher class as integers."""
    TIME_COST: Final[int] = 3
    MEMORY_COST: Final[int] = 256 * 1024
    PARALLELISM: Final[int] = 4
    HASH_LENGTH: Final[int] = 32
    SALT_LENGTH: Final[int] = 16

class ErrorMessageConstants:
    """Class for storing constants regarding error messages and titles as strings."""
    ERROR: Final[str] = 'Error'
    SECURE_SIGN_OUT_TITLE: Final[str] = 'Secure sign-out'
    SECURE_SIGN_OUT_MSG: Final[str] = 'For your security, you have been signed out due to 5 minutes of inactivity.'
    SALT_ERR_MSG: Final[str] = ('The salt length for key derivation is invalid. '
                                'Data cannot be decrypted. Would you like to clear the vault?'
                                '\nNOTE: This will result in the permanent loss of all password data.')
    CANNOT_DECRYPT_MSG: Final[str] = 'Data will remain undecryptable.'
    ASK_CLEAR_VAULT: Final[str] = ('Data cannot be decrypted. Clear vault?' 
                                  '\nNOTE: This will result in permanent loss of all password data.')
    MAX_ATTEMPTS_MSG: Final[str] = 'Too many failed attempts'
    APP_NONEXISTENT_TITLE: Final[str] = 'App not found'
    APP_NONEXISTENT_MSG: Final[str] = ('Application was not found.'
                                      '\nEnsure the inputted data was spelt correctly.'
                                      '\nNOTE: Letter casing does not matter.')

class ConfigKeyConstants:
    """Class for storing constants regarding the keys for the config file as strings."""
    LOGIN_ATTEMPTS: Final[str] = 'login_attempts'
    LOCK_UNTIL: Final[str] = 'lock_until'

class TimeConstants:
    """Class for storing constants regarding timestamps as integers."""
    TIMEOUT_TIME: Final[int] = 300000 # 5 minutes in milliseconds
    CLEAR_CLIPBOARD_TIME: Final[int] = 30 # Standard 30 seconds
    LOCKOUT_TIME: Final[int] = 3600 # An hour in seconds