import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from db_manager.login_db import *


class UserEditScreen(ctk.CTkFrame):
    """
    UserEditScreen class for managing the user edit screen, allowing the user to edit
    their data and saving changes in the database.

    Inherits from ctk.CTkFrame.

    Args:
        master (ctk.CTkFrame): The parent frame for this UserEditScreen.
    """
    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)

        self.master = master
      
        self.create_edit_user_screen()

    def save_user_data(self) -> None:
        """
        Save the user data to the database. Shows an error message box if any field is left empty.
        """
        first_name = self.ime.get().strip()
        last_name = self.prezime.get().strip()
        username = self.username.get().strip()
        password = self.lozinka.get().strip()

        if not first_name or not last_name or not username or not password:
            messagebox.showerror("Error", "Sva polja su obavezna.")
            return

        user_id = get_user_id(username)

        if user_id is not None:
            update_user(user_id, first_name, last_name, username, password)
        else:
            add_user(first_name, last_name, username, password)
        
        messagebox.showinfo("Spremljeno", "Vaši podaci su uspješno spremljeni.")
        self.grid_forget()
    
    def close(self):
        """
        Close the user edit screen by hiding it.
        """
        self.grid_forget()
    
    def create_edit_user_screen(self) -> None:
        """
        Create and display the user edit screen with input fields and buttons.
        """
        self.edit_user_screen = ctk.CTkFrame(self)
        self.edit_user_screen.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(self.edit_user_screen, text="Ime:").grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkLabel(self.edit_user_screen, text="Prezime:").grid(row=1, column=0, padx=10, pady=10)
        ctk.CTkLabel(self.edit_user_screen, text="Korisničko ime:").grid(row=2, column=0, padx=10, pady=10)
        ctk.CTkLabel(self.edit_user_screen, text="Lozinka:").grid(row=3, column=0, padx=10, pady=10)

        self.ime = ctk.CTkEntry(self.edit_user_screen)
        self.prezime = ctk.CTkEntry(self.edit_user_screen)
        self.username = ctk.CTkEntry(self.edit_user_screen)
        self.lozinka = ctk.CTkEntry(self.edit_user_screen, show="*")

        self.ime.grid(row=0, column=1, padx=10, pady=10)
        self.prezime.grid(row=1, column=1, padx=10, pady=10)              
        self.username.grid(row=2, column=1, padx=10, pady=10)              
        self.lozinka.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkButton(self.edit_user_screen, text="Spremi podatke", command=self.save_user_data).grid(row=4, column=0, columnspan=1, padx=10, pady=10)
        ctk.CTkButton(self.edit_user_screen, text="Odustani", command=self.close).grid(row=4,column=1, columnspan=1, padx=10, pady=10)

       
