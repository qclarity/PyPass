from __future__ import annotations
from typing import TYPE_CHECKING
import customtkinter
from display_data import DisplayDataWindow
from errors import EntryNotFoundError
import tkinter
import tkinter.messagebox
from add_data import AddDataWindow
from constants import KeybindConstants, ColorConstants, TextConstants, ErrorMessageConstants
from password_manager import PasswordManager
from collections.abc import Callable
from models import PassInfo

if TYPE_CHECKING:
    from pypass import PyPass

class MainApp(customtkinter.CTkFrame):
    """
    Class for constructing the main screen of PyPass that displays current saved apps, add data, and search data.
    """
    def __init__(
            self,
            master: PyPass,
            data: dict[str, PassInfo],
            key: bytes,
            pm: PasswordManager,
            salt: bytes,
            show_password: Callable[[customtkinter.CTkEntry,
                                     customtkinter.CTkSwitch], None]):
        """
        Args:
            master: The main application window.
            data: The user data as a plaintext dataclass.
            key: The key used for encrypting and decrypting data.
            pm: The wrapper class for storing file and crypto functionalities.
            salt: The salt used for key derivation required by Argon2id.
            show_password: The function used for hiding and revealing password info.
        """
        super().__init__(master)
        self.data = data
        self.key = key
        self.pm = pm
        self.salt = salt
        self.show_password = show_password

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)   

        sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        sidebar_frame.grid(row=0, column=0, padx=5, pady=5, sticky='ns')

        self.data_display_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0)
        self.data_display_frame.grid(row=0, column=1, padx=(0, 5), pady=5, sticky='nsew')

        self.bind(KeybindConstants.CLOSE_WIND_KEYBIND, lambda event: self.quit())

        add_application_button = customtkinter.CTkButton(
                sidebar_frame,
                text=TextConstants.ADD_DATA,
                anchor='w', 
                command=self.open_add_data)
        add_application_button.grid(row=0, column=0, padx=3, pady=5)

        self.search_application_entry = customtkinter.CTkEntry(
            sidebar_frame,
            placeholder_text=TextConstants.SEARCH,
        )
        self.search_application_entry.grid(row=1, column=0, padx=3, pady=3)

        self.master.bind(KeybindConstants.ADD_DATA_KEYBIND, lambda event: self.open_add_data())
        self.search_application_entry.bind(KeybindConstants.CHECK_KEYBIND, lambda event: self.search_data())

        sidebar_frame.bind(KeybindConstants.LEFT_CLICK, lambda event: self.defocus_search(event=event))

        sidebar_frame.focus_set()
        
        self.no_items_saved_label = customtkinter.CTkLabel(self.data_display_frame, text='')

        if not self.data:
            self.no_items_saved_label.pack()
            self.no_items_saved_label.configure(text=TextConstants.NO_DATA_STORED)
        else:
            self.display_data()

        self.data_display_frame.columnconfigure((0, 2), weight=1)

    def refresh_display(self) -> None:
        for widget in self.data_display_frame.winfo_children():
            widget.destroy()
        if not self.data:
            self.no_items_saved_label = customtkinter.CTkLabel(self.data_display_frame, text=TextConstants.NO_DATA_STORED)
            self.no_items_saved_label.pack()
        else:
            self.display_data()

    def open_add_data(self) -> None:
        AddDataWindow(
            main_app=self,
            pm=self.pm,
            on_save=self.refresh_display,
            key=self.key,
            data=self.data,
            show_password=self.show_password,
        )

    def create_button(self, text: str, color: str, name: str) -> None:
        btn = customtkinter.CTkButton(
            self.data_display_frame,
            text=text,
            fg_color=color,
            anchor='w',
            corner_radius=0,
            command=lambda name=name: DisplayDataWindow(name=name, data=self.data, pm=self.pm, main_app=self, key=self.key, show_password=self.show_password)
        )
        btn.pack(fill='both')

    def display_data(self) -> None:
        for i, name in enumerate(sorted(self.data.keys()), start=1):
            date = self.data[name].date
            text = f'{i}. {name.title()} | {date}'

            color = ColorConstants.EVEN_BTN_COLOR if i % 2 == 0 else ColorConstants.ODD_BTN_COLOR

            self.create_button(
                text=text,
                color=color,
                name=name
                )

    def search_data(self) -> None:
        app = self.search_application_entry.get().lower().strip()
        try:
            self.pm.search_data(name=app, data=self.data)
            DisplayDataWindow(
                name=app, 
                data=self.data, 
                pm=self.pm,  
                main_app=self, 
                key=self.key,
                show_password=self.show_password)
        except EntryNotFoundError:
            tkinter.messagebox.showerror(
                title=ErrorMessageConstants.APP_NONEXISTENT_TITLE,
                message=ErrorMessageConstants.APP_NONEXISTENT_MSG
            )

    def defocus_search(self, event) -> None:
        if event.widget != self.search_application_entry and event.widget != self.search_application_entry._entry:
            self.focus_set()