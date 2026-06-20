from pypass import PyPass
from password_manager import PasswordHasher, PasswordManager
from constants import FileConstants, HasherParamConstants

def main() -> None:
    ph = PasswordHasher(
        time_cost=HasherParamConstants.TIME_COST,
        memory_cost=HasherParamConstants.MEMORY_COST,
        parallelism=HasherParamConstants.PARALLELISM,
        hash_len=HasherParamConstants.HASH_LENGTH,
        salt_len=HasherParamConstants.SALT_LENGTH,
    )

    pm = PasswordManager(
        ph=ph, 
        password_file=FileConstants.PASS_PATH,
        salt_file=FileConstants.SALT_PATH,
        vault_file=FileConstants.VAULT_PATH,
    )
    
    pypass = PyPass(pm=pm)
    pypass.mainloop()

if __name__ == "__main__":
    main()
