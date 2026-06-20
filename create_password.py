from __future__ import annotations
from typing import TYPE_CHECKING
import customtkinter
from errors import PasswordsNotMatchError, NoPasswordError
from constants import FontConstants, TextConstants, ColorConstants, KeybindConstants
from collections.abc import Callable
from password_manager import PasswordManager

if TYPE_CHECKING:
    from pypass import PyPass

class CreatePasswordWindow(customtkinter.CTkFrame):
    """
    Class for constructing the window for password creation / first-time use.
    """
    def __init__(
            self,
            master: PyPass,
            on_success: Callable[[], None],
            on_cancel: Callable[[], None],
            pm: PasswordManager):
        """
        Args:
            master: The main application window.
            on_success: The callback function for calling the sign-in window when the correct password is entered.
            on_cancel: The callback function for closing the program.
            pm: The wrapper class for storing file and crypto functionalities.
        """
        super().__init__(master)
        self.on_success = on_success
        self.on_cancel = on_cancel
        self.pm = pm

        master.bind(KeybindConstants.CLOSE_WIND_KEYBIND, lambda event: self.quit())

        self.columnconfigure((0, 2), weight=1)
        self.rowconfigure(0, weight=1)

        create_pass_frame = customtkinter.CTkFrame(self, corner_radius=0)
        create_pass_frame.grid(row=0, column=1, sticky='ns')

        create_pass_label = customtkinter.CTkLabel(create_pass_frame, text=TextConstants.CREATE_PASSWORD, font=FontConstants.LARGE_FONT)
        create_pass_label.grid(row=0, column=1, padx=5, pady=3, sticky='w')

        self.create_pass_entry = customtkinter.CTkEntry(create_pass_frame, placeholder_text=TextConstants.CREATE_PASSWORD, width=200, show='*')
        self.create_pass_entry.grid(row=1, column=1, padx=5, pady=3, sticky='w')

        confirm_pass_label = customtkinter.CTkLabel(create_pass_frame, text=TextConstants.CONFIRM_PASSWORD, font=FontConstants.LARGE_FONT)
        confirm_pass_label.grid(row=2, column=1, padx=5, pady=3, sticky='w')

        self.confirm_pass_entry = customtkinter.CTkEntry(create_pass_frame, placeholder_text=TextConstants.CONFIRM_PASSWORD, width=200, show='*')
        self.confirm_pass_entry.grid(row=3, column=1, padx=5, pady=3, sticky='w')

        self.err_label = customtkinter.CTkLabel(create_pass_frame, text='')
        self.err_label.grid(row=4, column=1, padx=5, sticky='w')

        create_pass_button = customtkinter.CTkButton(create_pass_frame, text=TextConstants.CREATE, command=self.compare_passwords)
        create_pass_button.grid(row=5, column=1, padx=5, pady=3, sticky='ew')

        cancel_button = customtkinter.CTkButton(create_pass_frame, text=TextConstants.CANCEL, fg_color=ColorConstants.GRAY_COLOR, command=self.on_cancel)
        cancel_button.grid(row=6, column=1, padx=5, pady=3, sticky='ew')

        warning_label = customtkinter.CTkLabel(create_pass_frame, text=TextConstants.SPACES_ALLOWED, font=FontConstants.SMALL_FONT)
        warning_label.grid(row=7, column=1, padx=5)

    def compare_passwords(self) -> None:
        pass1 = self.create_pass_entry.get()
        pass2 = self.confirm_pass_entry.get()

        try:
            self.pm.compare_passwords(pass1=pass1, pass2=pass2)
            self.pm.initialize_password(plaintext=pass1)
            del pass1, pass2
            self.on_success()
        except NoPasswordError:
            self.err_label.configure(text=TextConstants.INPUT_PASS_TEXT, text_color=ColorConstants.WARNING_COLOR)
        except PasswordsNotMatchError:
            self.err_label.configure(text=TextConstants.PASS_NOT_MATCH_TEXT, text_color=ColorConstants.FAIL_COLOR)
