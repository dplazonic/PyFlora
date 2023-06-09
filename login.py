import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from sensors import simulate_data
from db_manager.login_db import *
 

class LoginScreen(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        """Initializes the LoginScreen class that provides a user interface to log into the system.

        Args:
            master (ctk.CTk): The parent widget.
        """
        self.master = master
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        simulate_data()
        self.create_login_screen()

    def check_credentials(self) -> None:
        """
        Verifies the entered username and password.

        If the credentials are correct, a success message is displayed and the login screen is forgotten.
        If the credentials are incorrect, an error message is displayed.
        """
        username = self.username.get()
        password = self.password.get()

        if check_user(username, password) and check_password(username, password):
            messagebox.showinfo("Prijava uspješna", "Dobrodošli")
            self.grid_forget()
            self.master.update_pot_tiles() 
        else:
            messagebox.showerror("Prijava neuspješna!", "Netočno korisničko ime ili lozinka. Pokušajte ponovno.")

    def create_login_screen(self) -> None:
        """Constructs the user interface for the login screen.

        The interface includes labels and entry fields for the username and password, and a login button.
        """
        self.mid_frame = ctk.CTkFrame(self, width=200)
        self.mid_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.mid_frame, text="Korisničko ime:").grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkLabel(self.mid_frame, text="Lozinka:").grid(row=1, column=0, padx=10, pady=10)

        ctk.CTkEntry(self.mid_frame, textvariable=self.username).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkEntry(self.mid_frame, textvariable=self.password, show="*").grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkButton(self.mid_frame, text="Prijavi se", command=self.check_credentials).grid(row=2, columnspan=2, padx=10, pady=10, sticky="we")
        





