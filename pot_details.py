import tkinter as tk
import customtkinter as ctk
from PIL import Image
from db_manager.plants import *
from db_manager.pots_db import *
from pots_screen import *
from sensors import *

class PotDetails(ctk.CTkScrollableFrame):
    """A tkinter based application interface to view and manage the details of pots and plants.

    Args:
        master (optional, ctk.CTk): The parent window. Defaults to None.
        pot_id (optional, str): The unique identifier of a pot. Defaults to None.
"""    
    def __init__(self, master: ctk.CTk = None, pot_id: int = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.pot_id = pot_id
        self.edit_mode = False
        self.pots_tiles = PotsTiles(self.master) 


        if self.pot_id is not None:
            self.pots_details_screen()

    def pots_details_screen(self):
        """
        Display the pot details screen.
        """

        self.grid(padx=20, pady=20, sticky="nswe")

        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        self.pot = get_pot_by_display_id(self.pot_id)   
        self.plant = get_plant_by_id(self.pot[5])
        
        self.desc_label_0 = ctk.CTkLabel(self, text=f"Posuda br. {self.pot[0]}", font=ctk.CTkFont(size=24, weight="bold"))
        self.desc_label_0.grid(row=0, column=0, pady=20, padx=10, columnspan=4, sticky="we")

        ### ---- PHOTO ---- ###

        img = Image.open("photos\\pot.png" if self.pot[7]== None else self.pot[7])
        img_tk = ctk.CTkImage(img, size=(300, 300))
        self.img_label = ctk.CTkLabel(self, text="", image=img_tk)
        self.img_label.grid(row=1, column=3, padx=10, pady=10, sticky="we")
        
        ### ---- POT PROP ---- ###

        self.pot_properties= ctk.CTkFrame(self)
        self.pot_properties.grid(row=1, column=1, sticky= "we", padx=5, pady=5)
        self.desc_label_1 = ctk.CTkLabel(self.pot_properties, text=f"Materijal posude: {self.pot[2]}", font=ctk.CTkFont(size=14))
        self.desc_label_1.grid(row=1, column=0, padx=5, pady=5, sticky="we")
        self.desc_label_2 = ctk.CTkLabel(self.pot_properties, text=f"Pozicija posude: {self.pot[3]}", font=ctk.CTkFont(size=14))
        self.desc_label_2.grid(row=2, column=0, padx=5, pady=5, sticky="we")
        self.desc_label_3 = ctk.CTkLabel(self.pot_properties, text=f"Veličina posude: {self.pot[4]}", font=ctk.CTkFont(size=14))
        self.desc_label_3.grid(row=3, column=0, padx=5, pady=5, sticky="we")

        ### ---- PLANT PROP ---- ###

        self.plant_properties= ctk.CTkFrame(self)
        self.plant_properties.grid(row=1, column=0, padx=5, pady=5, sticky="we")

        self.plant_name = ctk.CTkLabel(self.plant_properties, text=self.plant[1], font=ctk.CTkFont(size=40, weight="bold"))
        self.plant_name.grid(row=1, column=0, pady=20, padx=10, sticky="we")
        self.watering = ctk.CTkLabel(self.plant_properties, text=f"Zalijevanje: {self.plant[3]}", font=ctk.CTkFont(size=14))
        self.watering.grid(row=2, column=0, padx=10, pady=5, sticky="we")
        self.brightness = ctk.CTkLabel(self.plant_properties, text=f"Izloženost svjetlosti: {self.plant[4]}", font=ctk.CTkFont(size=14))
        self.brightness.grid(row=3, column=0, padx=10, pady=5, sticky="we")
        self.temperature = ctk.CTkLabel(self.plant_properties, text=f"Temperatura: {self.plant[5]}", font=ctk.CTkFont(size=14))
        self.temperature.grid(row=4, column=0, padx=10, pady=5, sticky="we")
        self.supstrate = ctk.CTkLabel(self.plant_properties, text=f"Dodavanje supstrata: {'da' if self.plant[6] == 1 else 'ne'}", font=ctk.CTkFont(size=14))
        self.supstrate.grid(row=5, column=0, padx=10, sticky="we")

        ### ---- SENSOR STATUS ---- ###

        self.sensor_data = self.pots_tiles.generate_sensor_data(self.pot)
        self.plant_status_texts = self.pots_tiles.check_plant_status()
        self.status_text = self.plant_status_texts[self.pot[0] - 1]

        self.sensors_status= ctk.CTkFrame(self)
        self.sensors_status.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        self.temperature_label = ctk.CTkLabel(self.sensors_status, text=f"Temperatura: {self.sensor_data['temperature']} °C", font=ctk.CTkFont(size=14))
        self.temperature_label.grid(row=1, column=0, padx=5, sticky="w")        
        self.moisture_label = ctk.CTkLabel(self.sensors_status, text=f"Vlažnost: {self.sensor_data['moisture']} %", font=ctk.CTkFont(size=14))
        self.moisture_label.grid(row=2, column=0, padx=5, sticky="w")        
        self.light_label = ctk.CTkLabel(self.sensors_status, text=f"Svjetlost: {self.sensor_data['brightness']} lux", font=ctk.CTkFont(size=14))
        self.light_label.grid(row=3, column=0, padx=5, sticky="w")

         ### ---- GRAPHS ---- ###
        
        self.sensors_graphs = ctk.CTkFrame(self)
        self.sensors_graphs.grid(row=3,column=0, sticky="we", padx=5, pady=5, columnspan=4)
        self.sensors_graphs_label = ctk.CTkLabel(self.sensors_graphs, text="Grafički prikaz stanja senzora zadnja 24h", corner_radius=6)
        self.sensors_graphs_label.grid(row=0, sticky="we", columnspan=4)
        self.sensor_plotter = SensorPlotter(self.sensors_graphs, self.pot_id)
        self.sensor_plotter.plot_sensor_data()


        ### ---- REFRESH ---- ###

        self.refresh_button = ctk.CTkButton(self.sensors_graphs, text="Refresh", corner_radius=10, command=self.sensor_plotter.plot_sensor_data)
        self.refresh_button.grid(row=0, column=0, sticky="we")

        ### ---- DELETE PLANT FROM POT ---- ###

        self.refresh_button = ctk.CTkButton(self.sensors_graphs, text="Izbaci bljku iz posude", corner_radius=10, command=lambda pot_id=self.pot[0]: self.empty_the_pot(pot_id))
        self.refresh_button.grid(row=0, column=2, sticky="we")


    def empty_the_pot(self, pot_id):
        remove_plant_from_pot(pot_id)
        self.master.update_pot_tiles()
