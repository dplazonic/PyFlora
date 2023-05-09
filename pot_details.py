import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
from db_manager.plants import *
import os
from db_manager.plants import *




class PlantDetails(ctk.CTkFrame):
    def __init__(self, master, pot_id, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.pot_id = pot_id
        self.edit_mode = False

        
        self.pot_details_screen()

    def plant_details_screen(self):

        self.mid_frame = ctk.CTkFrame(self,  bg_color="transparent")
        self.mid_frame.grid(row=1, column=0, padx=50, pady=50)

        self.mid_frame.grid_columnconfigure((0,1), weight=1)

        self.plant = get_pot_by_id(self.plant_id)


        img = Image.open(self.plant[2])
        img_tk = ctk.CTkImage(img, size=(400, 400))
        self.img_label = ctk.CTkLabel(self.mid_frame, text="", image=img_tk)
        self.img_label.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        self.plant_name = ctk.CTkLabel(self.mid_frame, text=self.plant[1], font=ctk.CTkFont(size=30, weight="bold"))
        self.plant_name.grid(row=0, column=0, pady=20, padx=10, columnspan=2)

        self.watering = ctk.CTkLabel(self.mid_frame, text=f"Zalijevanje: {self.plant[3]}", font=ctk.CTkFont(size=14))
        self.watering.grid(row=2, column=0, padx=10, pady=5, sticky="we", columnspan=2)

        self.brightness = ctk.CTkLabel(self.mid_frame, text=f"Izloženost svjetlosti: {self.plant[4]}", font=ctk.CTkFont(size=14))
        self.brightness.grid(row=3, column=0, padx=10, pady=5, sticky="we", columnspan=2)

        self.temperature = ctk.CTkLabel(self.mid_frame, text=f"Temperatura: {self.plant[5]}", font=ctk.CTkFont(size=14))
        self.temperature.grid(row=4, column=0, padx=10, pady=5, sticky="we", columnspan=2)

        self.supstrate = ctk.CTkLabel(self.mid_frame, text=f"Dodavanje supstrata: {'da' if self.plant[6] == 1 else 'ne'}", font=ctk.CTkFont(size=14))
        self.supstrate.grid(row=5, column=0, padx=10, sticky="we", columnspan=2)

        self.editbtn = ctk.CTkButton(self.mid_frame, text="Ažuriraj podatke o biljci", command=self.toggle_edit_mode)
        self.editbtn.grid(row=6, column=0, pady=20, padx=10, sticky="we", columnspan=2)

    def toggle_edit_mode(self):
        if self.edit_mode:
            self.save_changes()
            self.edit_mode = False
            self.editbtn.configure(text="Ažuriraj podatke o biljci")
            self.plant_details_screen()
        else:
            self.edit_mode = True
            self.editbtn.configure(text="Spremi")
            self.details_editing()

    def details_editing(self):
        self.watering.destroy()
        self.brightness.destroy()
        self.temperature.destroy()
        self.supstrate.destroy()

        self.mid_frame.grid_columnconfigure(0, weight=0)
        self.mid_frame.grid_columnconfigure(1, weight=1) 


        self.watering = ctk.CTkLabel(self.mid_frame, text=f"Zalijevanje:", font=ctk.CTkFont(size=12))
        self.watering.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_watering = ctk.CTkEntry(self.mid_frame, width=30, textvariable=tk.StringVar(value=self.plant[3]))
        self.entry_watering.grid(row=2, column=1, padx=10, pady=5, sticky="we", columnspan=2)

        self.brightness = ctk.CTkLabel(self.mid_frame, text=f"Izloženost svjetlosti:", font=ctk.CTkFont(size=12))
        self.brightness.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_brightness = ctk.CTkEntry(self.mid_frame, width=30, textvariable=tk.StringVar(value=self.plant[4]))
        self.entry_brightness.grid(row=3, column=1, padx=10, pady=5, sticky="we", columnspan=2)

        self.temperature = ctk.CTkLabel(self.mid_frame, text=f"Temperatura:", font=ctk.CTkFont(size=12))
        self.temperature.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.entry_temperature = ctk.CTkEntry(self.mid_frame, width=30, textvariable=tk.StringVar(value=self.plant[5]))
        self.entry_temperature.grid(row=4, column=1, padx=10, pady=5, sticky="we", columnspan=2)

        self.supstrate = ctk.CTkLabel(self.mid_frame, text=f"Dodavanje supstrata:", font=ctk.CTkFont(size=12))
        self.supstrate.grid(row=5, column=0, padx=10, sticky="w")
        self.entry_substrate = ctk.CTkEntry(self.mid_frame, width=30, textvariable=tk.StringVar(value=f"{'da' if self.plant[6] == 1 else 'ne'}"))
        self.entry_substrate.grid(row=5, column=1, padx=10, sticky="we", columnspan=2)


    def save_changes(self):
        updated_watering = self.entry_watering.get()
        updated_light = self.entry_brightness.get()
        updated_temperature = self.entry_temperature.get()
        updated_substrate = True if self.entry_substrate.get() == "da" else False

        update_plant(self.plant_id, updated_watering, updated_light, updated_temperature, updated_substrate)