class VaultError(Exception):
    """Parent class for storing errors regarding the vault file."""
    pass

class NoVaultError(VaultError):
    """Raised when the vault file is either nonexistent or empty."""
    pass

class VaultDecryptionError(VaultError):
    """Raised when the vault cannot be decrypted for any reason."""
    pass

class EntryNotFoundError(VaultError):
    """Raised when the user searches an entry that does not exist."""
    pass

class PasswordError(Exception):
    """Parent class for storing errors regarding password-related issues."""
    pass

class PasswordsNotMatchError(PasswordError):
    """Raised when the user inputs two passwords that do not match during password creation."""
    pass

class NoPasswordError(PasswordError):
    """Raised when the user does not input a password for either validation or creation."""
    pass

class PasswordVerificationError(PasswordError):
    """Raised when the user inputs a password that cannot be verified for any reason."""
    pass

class TooManyAttemptsError(PasswordError):
    """Raised when the user inputs too many attempts for attempting to sign in."""
    pass

class SaltError(Exception):
    """Parent class for storing errors regarding the salt."""
    pass

class InvalidSaltLengthError(SaltError):
    """Raised when the salt is not 16-bytes."""
    pass
