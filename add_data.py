from __future__ import annotations
from typing import TYPE_CHECKING
import customtkinter
from datetime import datetime
from models import PassInfo
from password_manager import PasswordManager
from constants import WindowConstants, KeybindConstants, FontConstants, TextConstants, ColorConstants
from collections.abc import Callable

if TYPE_CHECKING:
    from main_app import MainApp

class AddDataWindow:
    """
    The class for constructing the window that prompts the user to add new data.
    """
    def __init__(
            self,
            data: dict[str, PassInfo],
            key: bytes,
            on_save: Callable[[], None],
            pm: PasswordManager,
            show_password: Callable[[customtkinter.CTkEntry,
                                     customtkinter.CTkSwitch], None],
            main_app: MainApp):
        """
        Args:
            data: The user data as a plaintext dataclass.
            key: The key used for encrypting and decrypting data.
            on_save: The function that resets the data displayed as to show the newly added or removed entry.
            pm: The wrapper class for storing file and crypto functionalities.
            show_password: The function used for hiding and revealing password info.
            main_app: The main application window.
        """
        self.data = data
        self.key = key
        self.on_save = on_save
        self.pm = pm
        self.show_password = show_password

        new_data_window = customtkinter.CTkToplevel(main_app)
        new_data_window.grab_set()
        new_data_window.wm_attributes('-topmost', True)
        new_data_window.title(TextConstants.ADD_DATA)
        new_data_window.geometry(WindowConstants.NEW_DATA_WINDOW_SIZE)

        new_data_window.bind(KeybindConstants.CLOSE_WIND_KEYBIND, lambda event: new_data_window.destroy())

        new_data_window.columnconfigure((0, 2), weight=1)
        new_data_window.rowconfigure(0, weight=1)

        self.new_data_frame = customtkinter.CTkFrame(new_data_window, corner_radius=0)
        self.new_data_frame.grid(row=0, column=1, sticky='ns')

        application_label = customtkinter.CTkLabel(self.new_data_frame, text=TextConstants.APP, font=FontConstants.MEDIUM_FONT)
        application_label.grid(row=0, column=1, padx=5, sticky='w')

        self.application_entry = customtkinter.CTkEntry(self.new_data_frame, placeholder_text=TextConstants.APPLICATION, width=200)
        self.application_entry.grid(row=1, column=1, padx=5, pady=3, sticky='w')

        user_label = customtkinter.CTkLabel(self.new_data_frame, text=TextConstants.USER, font=FontConstants.MEDIUM_FONT)
        user_label.grid(row=2, column=1, padx=5, sticky='w')

        self.user_entry = customtkinter.CTkEntry(self.new_data_frame, placeholder_text=TextConstants.USERNAME, width=200)
        self.user_entry.grid(row=3, column=1, padx=5, pady=3, sticky='w')

        phone_label = customtkinter.CTkLabel(self.new_data_frame, text=TextConstants.PHONE, font=FontConstants.MEDIUM_FONT)
        phone_label.grid(row=4, column=1, padx=5, sticky='w')

        self.phone_entry = customtkinter.CTkEntry(self.new_data_frame, placeholder_text=TextConstants.PHONE, width=200)
        self.phone_entry.grid(row=5, column=1, padx=5, pady=3, sticky='w')

        password_label = customtkinter.CTkLabel(self.new_data_frame, text=TextConstants.PASSWORD, font=FontConstants.MEDIUM_FONT)
        password_label.grid(row=6, column=1, padx=5, sticky='w')

        self.password_entry = customtkinter.CTkEntry(self.new_data_frame, placeholder_text=TextConstants.PASSWORD, show='*', width=200)
        self.password_entry.grid(row=7, column=1, padx=5, sticky='w')

        show_pass_switch = customtkinter.CTkSwitch(self.new_data_frame, text=TextConstants.SHOW_PASSWORD, command=lambda: self.show_password(entry=self.password_entry, switch=show_pass_switch))
        show_pass_switch.grid(row=8, column=1, padx=5, pady=10, sticky='w')

        save_button = customtkinter.CTkButton(self.new_data_frame, text=TextConstants.SAVE, command=lambda: self.save_data(pass_info_cls=PassInfo))
        save_button.grid(row=9, column=1, padx=5, sticky='ew')

        cancel_button = customtkinter.CTkButton(self.new_data_frame, text=TextConstants.CANCEL, fg_color=ColorConstants.GRAY_COLOR, command=new_data_window.destroy)
        cancel_button.grid(row=10, column=1, padx=5, pady=5, sticky='ew')

        self.success_label = customtkinter.CTkLabel(self.new_data_frame, text='')
        self.success_label.grid(row=11, column=1, sticky='ew')

    def save_data(self, pass_info_cls: type[PassInfo]) -> None:
        app = self.application_entry.get().lower().strip()

        if app not in self.data:
            new_data = pass_info_cls(
                user=self.user_entry.get(),
                phone=self.phone_entry.get(),
                password=self.password_entry.get(),
                date=datetime.now().strftime('%b %d, %Y')
            )

            self.data[app] = new_data
            encrypted_data = self.pm.encrypt_data(data=self.data, key=self.key)
            self.pm.save_vault_data(encrypted_data=encrypted_data)

            for widget in self.new_data_frame.winfo_children():
                if isinstance(widget, customtkinter.CTkEntry):
                    widget.delete(0, 'end')

            self.success_label.configure(text=TextConstants.DATA_SAVED_TEXT, text_color=ColorConstants.SUCCESS_COLOR)

            self.on_save()
        else:
            self.success_label.configure(text=TextConstants.DATA_ERROR_TEXT, text_color=ColorConstants.FAIL_COLOR)