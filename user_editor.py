import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from db_manager.login_db import *

ctk.set_appearance_mode("light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"



def save_user_data(edit_user_screen, ime, prezime, username, lozinka):
    first_name = ime.get()
    last_name = prezime.get()
    username = username.get()
    password = lozinka.get()
    user_id = get_user_id(username)

    #print(user_id, first_name,last_name,username,password)
    if get_user_id(username) is not None:
        update_user(user_id, first_name, last_name, username, password)
    else:
        add_user(first_name, last_name, username, password)
        
    messagebox.showinfo("Spremljeno", "Vaši podaci su uspješno spremljeni.")
    edit_user_screen.destroy()
   

def create_edit_user_screen():
    edit_user_screen = ctk.CTk()
    edit_user_screen.title("Uredi korisničke podatke")
    edit_user_screen.geometry(f"{420}x{280}+{1000}+{500}")

    ctk.CTkLabel(edit_user_screen, text="Ime:").grid(row=0, column=0, padx=10, pady=10)
    ctk.CTkLabel(edit_user_screen, text="Prezime:").grid(row=1, column=0, padx=10, pady=10)
    ctk.CTkLabel(edit_user_screen, text="Korisničko ime:").grid(row=2, column=0, padx=10, pady=10)
    ctk.CTkLabel(edit_user_screen, text="Lozinka:").grid(row=3, column=0, padx=10, pady=10)

    ime = ctk.CTkEntry(edit_user_screen)
    prezime = ctk.CTkEntry(edit_user_screen)
    username = ctk.CTkEntry(edit_user_screen)
    lozinka = ctk.CTkEntry(edit_user_screen, show="*")

    ime.grid(row=0, column=1, padx=10, pady=10)
    prezime.grid(row=1, column=1, padx=10, pady=10)              
    username.grid(row=2, column=1, padx=10, pady=10)              
    lozinka.grid(row=3, column=1, padx=10, pady=10)

    ctk.CTkButton(edit_user_screen, text="Spremi podatke", command=lambda: save_user_data(edit_user_screen, ime, prezime, username, lozinka)).grid(row=4, columnspan=2, padx=10, pady=10)

    edit_user_screen.mainloop()


