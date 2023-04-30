import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from user_editor import *
from db_manager.login_db import *
from main_screen import *

ctk.set_appearance_mode("light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


def check_credentials():
    if check_user(username.get(), password.get()) and check_password(username.get(), password.get()):
        messagebox.showinfo("Prijava uspješna", "Dobrodošli")
        login_screen.destroy()
        app = App()
        app.time()
        app.mainloop()
    else:
        messagebox.showerror("Prijava neuspješna!", "Netočno korisničko ime ili lozinka. Pokušajte ponovno.")


def create_login_screen():
    global login_screen, username, password

    login_screen = ctk.CTk()
    login_screen.geometry(f"{420}x{280}+{1000}+{500}")
    login_screen.title("Prijava u aplikaciju")

    ctk.CTkLabel(login_screen, text="Korisničko ime:").grid(row=0, column=0, padx=10, pady=10)
    ctk.CTkLabel(login_screen, text="Lozinka:").grid(row=1, column=0, padx=10, pady=10)

    username = tk.StringVar()
    password = tk.StringVar()

    ctk.CTkEntry(login_screen, textvariable=username).grid(row=0, column=1, padx=10, pady=10)
    ctk.CTkEntry(login_screen, textvariable=password, show="*").grid(row=1, column=1, padx=10, pady=10)

    ctk.CTkButton(login_screen, text="Prijavi se", command=check_credentials).grid(row=2, column=0, padx=10, pady=10)
    ctk.CTkButton(login_screen, text="Korisnički podaci", command=create_edit_user_screen).grid(row=2, column=1, padx=10, pady=10)

    login_screen.mainloop()

#if __name__ == "__main__":
create_login_screen()