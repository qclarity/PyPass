from __future__ import annotations
from typing import TYPE_CHECKING
import customtkinter
import tkinter
import tkinter.messagebox
from errors import NoPasswordError, PasswordVerificationError, TooManyAttemptsError
from constants import FontConstants, KeybindConstants, TextConstants, ColorConstants, ErrorMessageConstants
from password_manager import PasswordManager
from collections.abc import Callable

if TYPE_CHECKING:
    from pypass import PyPass

class LoginPageWindow(customtkinter.CTkFrame):
    """
    Class for constructing the login-page of the program.
    """
    def __init__(
            self,
            master: PyPass,
            on_cancel: Callable[[], None],
            on_success: Callable[[str], None],
            pm: PasswordManager,
            show_password: Callable[[customtkinter.CTkEntry,
                                     customtkinter.CTkSwitch], None]):
        """
        Args:
            master: The main application window.
            on_cancel: The callback function for closing the program.
            on_success: The callback function for calling the sign-in window when the correct password is entered.
            pm: The wrapper class for storing file and crypto functionalities.
            show_password: The function used for hiding and revealing password info.
        """
        super().__init__(master)
        self.on_cancel = on_cancel
        self.on_success = on_success
        self.pm = pm
        self.show_password = show_password

        master.bind(KeybindConstants.CLOSE_WIND_KEYBIND, lambda event: self.quit())

        self.columnconfigure((0, 2), weight=1)
        self.rowconfigure(0, weight=1)

        login_frame = customtkinter.CTkFrame(self, corner_radius=0)
        login_frame.grid(row=0, column=1, sticky='ns')

        login_frame.bind(KeybindConstants.LEFT_CLICK, lambda event: self.defocus_login(event=event))

        login_label = customtkinter.CTkLabel(login_frame, text=TextConstants.LOGIN, font=FontConstants.LARGE_FONT)
        login_label.grid(row=0, column=1, padx=5, pady=3, sticky='ws')

        self.err_label = customtkinter.CTkLabel(login_frame, text='', font=FontConstants.SMALL_FONT)
        self.err_label.grid(row=0, column=1, padx=7, pady=0, sticky='se')

        self.login_entry = customtkinter.CTkEntry(login_frame, placeholder_text=TextConstants.PASSWORD, width=200, show='*')
        self.login_entry.grid(row=1, column=1, padx=5, sticky='w')

        self.login_entry.bind(KeybindConstants.CHECK_KEYBIND, lambda event: self.check_attempt())

        show_pass_switch = customtkinter.CTkSwitch(login_frame, text=TextConstants.SHOW_PASSWORD, command=lambda: self.show_password(entry=self.login_entry, switch=show_pass_switch))
        show_pass_switch.grid(row=2, column=1, padx=5, pady=10, sticky='w')

        login_button = customtkinter.CTkButton(login_frame, text=TextConstants.LOGIN, width=200, command=self.check_attempt)
        login_button.grid(row=3, column=1, padx=5, sticky='w')

        cancel_button = customtkinter.CTkButton(login_frame, text=TextConstants.CANCEL, width=200, fg_color=ColorConstants.GRAY_COLOR, command=self.on_cancel)
        cancel_button.grid(row=4, column=1, padx=5, pady=5, sticky='w')

    @staticmethod
    def quit_messagebox() -> None:
        tkinter.messagebox.showerror(title=ErrorMessageConstants.ERROR, message=ErrorMessageConstants.MAX_ATTEMPTS_MSG)

    def check_attempt(self) -> None:
        attempt = self.login_entry.get()
        try:
            self.pm.verify_password(attempt=attempt)
            self.on_success(attempt)
        except NoPasswordError:
            self.err_label.configure(text=TextConstants.INPUT_PASS_TEXT, text_color=ColorConstants.WARNING_COLOR, font=FontConstants.SMALL_FONT)
        except PasswordVerificationError:
            self.err_label.configure(text=TextConstants.PASS_VERIFY_ERR_TEXT, text_color=ColorConstants.FAIL_COLOR, font=FontConstants.SMALL_FONT)
        except TooManyAttemptsError:
            self.quit_messagebox()
            self.quit()

    def defocus_login(self, event) -> None:
        if event.widget != self.login_entry and event.widget != self.login_entry._entry:
            self.focus_set()
