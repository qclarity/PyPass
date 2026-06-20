import customtkinter
import tkinter.messagebox
from errors import NoVaultError, VaultDecryptionError, InvalidSaltLengthError
from login_page import LoginPageWindow
from create_password import CreatePasswordWindow
from main_app import MainApp
from models import PassInfo
import time
from constants import WindowConstants, TimeConstants, KeybindConstants, ErrorMessageConstants, TextConstants
from password_manager import PasswordManager

class PyPass(customtkinter.CTk):
    """
    The class for controlling the start-up logic of the program.
    """
    def __init__(
            self,
            pm: PasswordManager):
        """
        Args:
            pm: The wrapper class for storing file and crypto functionalities.
        """
        super().__init__()
        self.pm = pm
        self.current = None
        self.title(TextConstants.TITLE)
        self.geometry(WindowConstants.START_WINDOW_SIZE)
        customtkinter.set_default_color_theme('dark-blue')

        check_lock = self.pm.check_lock()

        if time.time() < check_lock:
            remaining = check_lock - time.time()
            tkinter.messagebox.showerror(title='Locked', message=f'Locked. Try again in {remaining // 60} minutes.')
            exit()

        self.allow_timeout = False
        self.timer_id = None

        self.start_timer()
        
        self.bind_all(KeybindConstants.ANY_KEYPRESS, lambda event: self.reset_timer())
        self.bind_all(KeybindConstants.ANY_BUTTONPRESS, lambda event: self.reset_timer())
        self.bind_all(KeybindConstants.MOTION, lambda event: self.reset_timer())

        if not self.pm.verify_password_file():
            self.show_signup()
        else:
            self.show_login()

    @staticmethod
    def show_reason_sign_out_msg() -> None:
        tkinter.messagebox.showinfo(
            title=ErrorMessageConstants.SECURE_SIGN_OUT_TITLE,
            message=ErrorMessageConstants.SECURE_SIGN_OUT_MSG
        )

    @staticmethod
    def invalid_salt_len_msg() -> bool:
        return tkinter.messagebox.askyesno(
            title=ErrorMessageConstants.ERROR,
            message=ErrorMessageConstants.SALT_ERR_MSG
        )

    @staticmethod
    def close_msg() -> None:
        tkinter.messagebox.showerror(
            title=ErrorMessageConstants.ERROR,
            message=ErrorMessageConstants.CANNOT_DECRYPT_MSG
        )

    @staticmethod
    def toggle_password(entry: customtkinter.CTkEntry, switch: customtkinter.CTkSwitch) -> None:
        entry.configure(show='' if switch.get() else '*')

    def start_timer(self) -> None:
        if self.allow_timeout:
            self.timer_id = self.after(TimeConstants.TIMEOUT_TIME, self.go_inactive)

    def reset_timer(self) -> None:
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.start_timer()

    def go_inactive(self) -> None:
        self.show_login()
        self.show_reason_sign_out_msg()

    def show_signup(self) -> None:
        self.allow_timeout = False
        self.clear()
        self.current = CreatePasswordWindow(master=self, pm=self.pm, on_success=self.show_login, on_cancel=self.destroy)
        self.current.pack(expand=True, fill='both')

    def show_login(self) -> None:
        self.allow_timeout = False
        self.geometry(WindowConstants.START_WINDOW_SIZE)
        self.clear()
        self.current = LoginPageWindow(master=self, pm=self.pm, on_success=self.show_main, on_cancel=self.destroy, show_password=self.toggle_password)
        self.current.pack(expand=True, fill='both')

    def show_main(self, password: str) -> None:
        self.allow_timeout = True
        self.clear()
        self.geometry(WindowConstants.MAIN_WINDOW_SIZE)

        try:
            salt = self.pm.get_or_create_salt()
        except InvalidSaltLengthError:
            salt = self.handle_invalid_salt()

        key = self.pm.key_derivation(password=password, salt=salt)

        try:
            self.data = self.pm.load_data(pass_info_cls=PassInfo, key=key)
        except NoVaultError:
            self.data = {}
        except VaultDecryptionError:
            self.data = {}
            self.handle_corrupt_vault()

        self.current = MainApp(
            master=self, 
            pm=self.pm, 
            salt=salt,
            key=key,
            data=self.data,
            show_password=self.toggle_password)
        self.current.pack(expand=True, fill='both')

    def handle_invalid_salt(self) -> bytes:
        should_wipe = self.invalid_salt_len_msg()
        if should_wipe:
            self.data = {}
            self.pm.clear_vault()
            self.pm.clear_salt()
            return self.pm.get_or_create_salt()
        else:
            self.close_msg()
            exit()

    def handle_corrupt_vault(self) -> None:
        error_msg = tkinter.messagebox.askyesno(
                title=ErrorMessageConstants.ERROR,
                message=ErrorMessageConstants.ASK_CLEAR_VAULT
        )
        if error_msg:
            self.pm.clear_vault()
        else:
            self.close_msg()
            self.quit()

    def clear(self) -> None:
        if self.current is not None:
            self.current.destroy()        
