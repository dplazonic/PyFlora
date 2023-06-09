import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter as ctk
from db_manager.plants_db import *
import os
from db_manager.plants_db import *


class PlantDetails(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, plant_id: int, *args, **kwargs) -> None:
        """
        Initializes the PlantDetails frame.
        A class representing a frame with plant details

        Args:
            master (ctk.CTk): Tkinter parent widget.
            plant_id (str): ID of the plant to be detailed.
        """
        super().__init__(master, *args, **kwargs)

        self.plant_id = plant_id
        self.edit_mode = False

        
        self.plant_details_screen()

    def plant_details_screen(self) -> None:
        """
        Displays the details of the plant on the screen.
        """
        self.grid_columnconfigure((1,2), weight=1)

        self.plant = get_plant_by_id(self.plant_id)

        img = Image.open(self.plant[2])
        img_tk = ctk.CTkImage(img, size=(300, 300))
        self.img_label = ctk.CTkLabel(self, text="", image=img_tk)
        self.img_label.grid(row=1, column=0, padx=20, pady=10, rowspan=6)

        self.plant_name = ctk.CTkLabel(self, text=self.plant[1], font=ctk.CTkFont(size=30, weight="bold"))
        self.plant_name.grid(row=0, column=0, pady=20, padx=10, columnspan=3, sticky="nswe")

        self.watering = ctk.CTkLabel(self, text=f"Zalijevanje: {self.plant[3]}", font=ctk.CTkFont(size=14))
        self.watering.grid(row=1, column=1, padx=10, pady=5, sticky="we", columnspan=2)

        self.brightness = ctk.CTkLabel(self, text=f"Izloženost svjetlosti: {self.plant[4]}", font=ctk.CTkFont(size=14))
        self.brightness.grid(row=2, column=1, padx=10, pady=5, sticky="we", columnspan=2)

        self.temperature = ctk.CTkLabel(self, text=f"Temperatura: {self.plant[5]}", font=ctk.CTkFont(size=14))
        self.temperature.grid(row=3, column=1, padx=10, pady=5, sticky="we", columnspan=2)

        self.ph = ctk.CTkLabel(self, text=f"Ph tla: {self.plant[6]}", font=ctk.CTkFont(size=14))
        self.ph.grid(row=4, column=1, padx=10, pady=5, sticky="we", columnspan=2)

        self.salinity = ctk.CTkLabel(self, text=f"Salinitet: {self.plant[7]}", font=ctk.CTkFont(size=14))
        self.salinity.grid(row=5, column=1, padx=10, pady=5, sticky="we", columnspan=2)

        self.supstrate = ctk.CTkLabel(self, text=f"Dodavanje supstrata: {'da' if self.plant[8] == 1 else 'ne'}", font=ctk.CTkFont(size=14))
        self.supstrate.grid(row=6, column=1, padx=10, sticky="we", columnspan=2)

        self.editbtn = ctk.CTkButton(self, text="Ažuriraj podatke o biljci", command=self.toggle_edit_mode)
        self.editbtn.grid(row=7, column=0, pady=20, padx=10, sticky="we", columnspan=3)

    def toggle_edit_mode(self) -> None:
        """
        Toggles the edit mode between viewing and editing plant details.
        """
        if self.edit_mode:
            self.save_changes()
            self.edit_mode = False
            self.editbtn.configure(text="Ažuriraj podatke o biljci")
            self.plant_details_screen()
        else:
            self.edit_mode = True
            self.editbtn.configure(text="Spremi")
            self.details_editing()

    def details_editing(self) -> None:
        """
        Allows the user to edit the details of the plant.
        """
        self.watering.destroy()
        self.brightness.destroy()
        self.temperature.destroy()
        self.ph.destroy()
        self.salinity.destroy()
        self.supstrate.destroy()
        
        self.grid_columnconfigure((1,2), weight=1)

        self.watering = ctk.CTkLabel(self, text=f"Zalijevanje:", font=ctk.CTkFont(size=12))
        self.watering.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.entry_watering =ctk.CTkComboBox(self, values=["dnevno", "tjedno", "mjesečno"])
        self.entry_watering.set(self.plant[3])
        self.entry_watering.grid(row=1, column=2, padx=10, pady=5, sticky="we")

        self.brightness = ctk.CTkLabel(self, text=f"Izloženost svjetlosti:", font=ctk.CTkFont(size=12))
        self.brightness.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.entry_brightness = ctk.CTkComboBox(self, values=["svijetlo", "tamno"])
        self.entry_brightness.set(self.plant[4])
        self.entry_brightness.grid(row=2, column=2, padx=10, pady=5, sticky="we")

        self.temperature = ctk.CTkLabel(self, text=f"Temperatura:", font=ctk.CTkFont(size=12))
        self.temperature.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.entry_temperature = ctk.CTkComboBox(self, values=["toplije", "hladnije"])
        self.entry_temperature.set(self.plant[5])
        self.entry_temperature.grid(row=3, column=2, padx=10, pady=5, sticky="we")

        self.ph = ctk.CTkLabel(self, text=f"ph Tla:", font=ctk.CTkFont(size=12))
        self.ph.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.entry_ph = ctk.CTkComboBox(self, values=["kiselo (<7)", "lužnato (>7)"])
        self.entry_ph.set(self.plant[6])
        self.entry_ph.grid(row=4, column=2, padx=10, pady=5, sticky="we")

        self.salinity = ctk.CTkLabel(self, text=f"Salinitet:", font=ctk.CTkFont(size=12))
        self.salinity.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        self.entry_salinity = ctk.CTkComboBox(self, values=["viši", "niži", "srednji"])
        self.entry_salinity.set(self.plant[7])
        self.entry_salinity.grid(row=5, column=2, padx=10, pady=5, sticky="we")

        self.supstrate = ctk.CTkLabel(self, text=f"Dodavanje supstrata:", font=ctk.CTkFont(size=12))
        self.supstrate.grid(row=6, column=1, padx=10, sticky="w")
        self.entry_substrate = ctk.CTkComboBox(self, values=["da", "ne"])
        self.entry_substrate.set(f"{'da' if self.plant[8] == 1 else 'ne'}")
        self.entry_substrate.grid(row=6, column=2, padx=10, sticky="we")

    def save_changes(self) -> None:
        """
        Saves the changes made to the plant details.
        """
        updated_watering = self.entry_watering.get()
        updated_light = self.entry_brightness.get()
        updated_temperature = self.entry_temperature.get()
        updated_ph = self.entry_ph.get()
        updated_salinity = self.entry_salinity.get()
        updated_substrate = True if self.entry_substrate.get() == "da" else False

        update_plant(self.plant_id, updated_watering, updated_light, updated_temperature,updated_ph,updated_salinity, updated_substrate)