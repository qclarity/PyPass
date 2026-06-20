from __future__ import annotations
from typing import TYPE_CHECKING
import customtkinter
import pyperclip
from constants import WindowConstants, KeybindConstants, FontConstants, TextConstants, ColorConstants, TimeConstants
import threading
from models import PassInfo
from password_manager import PasswordManager
from collections.abc import Callable

if TYPE_CHECKING:
    from main_app import MainApp

class DisplayDataWindow:
    """
    The class for displaying the user-selected entry data.
    """
    def __init__(
            self,
            data: dict[str, PassInfo],
            key: bytes,
            main_app: MainApp,
            name: str,
            pm: PasswordManager,
            show_password: Callable[[customtkinter.CTkEntry,
                                     customtkinter.CTkSwitch], None]):
        """
        Args:
            data: The user data as a plaintext dataclass.
            key: The key used for encrypting and decrypting data.
            main_app: The main application window.
            name: The name of the app to be displayed.
            pm: The wrapper class for storing file and crypto functionalities.
            show_password: The function used for hiding and revealing password info.
        """
        self.data = data
        self.name = name
        self.data_to_display = self.data[self.name]
        self.key = key
        self.main_app = main_app
        self.pm = pm
        self.show_password = show_password

        self.display_data_window = customtkinter.CTkToplevel(main_app)
        self.display_data_window.grab_set()
        self.display_data_window.wm_attributes('-topmost', True)
        self.display_data_window.title(self.name)
        self.display_data_window.geometry(WindowConstants.DATA_WINDOW_SIZE)

        self.display_data_window.bind(KeybindConstants.DEL_DATA_KEYBIND, lambda event: self.del_data())
        self.display_data_window.bind(KeybindConstants.CLOSE_WIND_KEYBIND, lambda event: self.display_data_window.destroy())

        self.display_data_window.columnconfigure((0, 2), weight=1)
        self.display_data_window.rowconfigure(1, weight=1)

        new_data_frame = customtkinter.CTkFrame(self.display_data_window, corner_radius=0)
        new_data_frame.grid(row=1, column=0, sticky='ens')

        user_label = customtkinter.CTkLabel(new_data_frame, text=f"{TextConstants.USERNAME}:", font=FontConstants.MEDIUM_FONT)
        user_label.grid(row=0, column=0, padx=10, sticky='w')

        self.user_var = customtkinter.StringVar()
        self.user_entry = customtkinter.CTkEntry(new_data_frame, textvariable=self.user_var)
        self.user_entry.insert(0, self.data_to_display.user)
        self.user_entry.grid(row=1, column=0, padx=10, pady=3, sticky='w')

        password_label = customtkinter.CTkLabel(new_data_frame, text=TextConstants.PASSWORD, font=FontConstants.MEDIUM_FONT)
        password_label.grid(row=2, column=0, padx=10, sticky='w')

        self.save_button = customtkinter.CTkButton(new_data_frame, text=TextConstants.SAVE, command=lambda app=self.data_to_display: self.save_changes(app=app))

        exit_button = customtkinter.CTkButton(new_data_frame, text=TextConstants.EXIT, command=self.display_data_window.destroy, fg_color=ColorConstants.GRAY_COLOR)
        exit_button.grid(row=7, column=0, padx=10, pady=3, sticky='w')

        del_button = customtkinter.CTkButton(new_data_frame, text=TextConstants.DEL_DATA, fg_color=ColorConstants.FAIL_COLOR, command=lambda: self.del_data())
        del_button.grid(row=9, column=0, padx=10, pady=3, sticky='w')
        
        self.password_var = customtkinter.StringVar()
        self.password_entry = customtkinter.CTkEntry(new_data_frame, textvariable=self.password_var)
        self.password_entry.insert(0, self.data_to_display.password)
        self.password_entry.grid (row=3, column=0, pady=3)

        copy_password_button = customtkinter.CTkButton(
            new_data_frame,
            text=TextConstants.COPY_TEXT,
            width=25,
            height=10,
            bg_color=ColorConstants.COPY_PASTE_BTN_COLOR,
            fg_color='transparent',
            hover_color=ColorConstants.GRAY_COLOR,
            corner_radius=0,
            command=lambda: self.copy(password=self.password_entry.get())
        )

        copy_password_button.grid(row=3, column=0, padx=15, sticky='e')

        show_password_switch = customtkinter.CTkSwitch(
            new_data_frame, text=TextConstants.SHOW_PASSWORD,
            command=lambda: self.show_password(entry=self.password_entry, switch=show_password_switch))
        show_password_switch.grid(row=4, column=0, padx=10, pady=3, sticky='w')

        phone_label = customtkinter.CTkLabel(new_data_frame, text=f'{TextConstants.PHONE}:', font=FontConstants.MEDIUM_FONT)
        phone_label.grid(row=0, column=1, padx=10, sticky='w')

        self.phone_var = customtkinter.StringVar()
        self.phone_entry = customtkinter.CTkEntry(new_data_frame, textvariable=self.phone_var)
        self.phone_entry.insert(0, self.data_to_display.phone)
        self.phone_entry.grid(row=1, column=1, padx=10)

        self.edit_mode_switch = customtkinter.CTkSwitch(new_data_frame, text=TextConstants.EDIT_MODE, command = self.edit_mode)
        self.edit_mode_switch.grid(row=5, column=0, padx=10, pady=3, sticky='w')

        self.err_label = customtkinter.CTkLabel(new_data_frame, text='')
        self.err_label.grid(row=3, column=1, padx=10, sticky='w')

        self.show_password(entry=self.password_entry, switch=show_password_switch)
        self.edit_mode()

        self.user_var.trace_add('write', self.on_change)
        self.phone_var.trace_add('write', self.on_change)
        self.password_var.trace_add('write', self.on_change)

    @staticmethod
    def copy(password: str) -> None:
        pyperclip.copy(password)

        def clear_clipboard() -> None:
            if pyperclip.paste() == password:
                pyperclip.copy('')

        timer = threading.Timer(TimeConstants.CLEAR_CLIPBOARD_TIME, clear_clipboard)
        timer.start()

    def del_data(self) -> None:
        self.pm.del_data(data=self.data, name=self.name, key=self.key)
        self.display_data_window.destroy()
        self.main_app.refresh_display()
            
    def edit_mode(self) -> None:
        entry_list = [self.user_entry, self.password_entry, self.phone_entry]
        switch_status = self.edit_mode_switch.get()
        if switch_status == 0:
            for e in entry_list:
                e.configure(state='disabled')
        else:
            for e in entry_list:
                e.configure(state='normal')

    def on_change(self, *args) -> None:
        self.save_button.grid(row=6, column=0, pady=3)
        self.err_label.configure(text=TextConstants.UNSAVED_TEXT, text_color=ColorConstants.FAIL_COLOR)

    def save_changes(self, app) -> None:
        app.user = self.user_entry.get()
        app.phone = self.phone_entry.get()
        app.password = self.password_entry.get()

        encrypted_data = self.pm.encrypt_data(self.data, key=self.key)
        self.pm.save_vault_data(encrypted_data=encrypted_data)

        self.err_label.configure(text=TextConstants.SAVED_TEXT, text_color=ColorConstants.SUCCESS_COLOR)
