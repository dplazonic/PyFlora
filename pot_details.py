import tkinter as tk
import customtkinter as ctk
from PIL import Image
from db_manager.plants_db import *
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
        self.desc_label_0.grid(row=0, column=0, pady=20, padx=10, columnspan=3, sticky="we")

        ### ---- PHOTO ---- ###

        img = Image.open("photos\\pot.png" if self.pot[7]== None else self.pot[7])
        img_tk = ctk.CTkImage(img, size=(300, 300))
        self.img_label = ctk.CTkLabel(self, text="", image=img_tk)
        self.img_label.grid(row=1, column=3, padx=10, pady=10, sticky="we")
        
        ### ---- POT PROP ---- ###

        self.pot_properties= ctk.CTkFrame(self)
        self.pot_properties.grid(row=1, column=1, sticky= "we", padx=5, pady=5)
        self.desc_pot_material = ctk.CTkLabel(self.pot_properties, text=f"Materijal posude: {self.pot[2]}", font=ctk.CTkFont(size=14))
        self.desc_pot_material.grid(row=1, column=0, padx=5, pady=5, sticky="we")
        self.pot_placement = ctk.CTkComboBox(self.pot_properties, font=ctk.CTkFont(size=14), values=["dnevni boravak", "soba", "balkon", "terasa", "hodnik", "kupaonica", "kuhinja", "terasa", "garaža"])
        self.pot_placement.set(self.pot[3])
        self.pot_placement.grid(row=2, column=0, padx=5, pady=5, sticky="we")
        self.pot_size = ctk.CTkLabel(self.pot_properties, text=f"Veličina posude: {self.pot[4]}", font=ctk.CTkFont(size=14))
        self.pot_size.grid(row=3, column=0, padx=5, pady=5, sticky="we")
        self.save_button = ctk.CTkButton(self.pot_properties, text="Premjesti posudu", corner_radius=10, command=self.save_pot_placement)
        self.save_button.grid(row=2, column=1, sticky="we")


        ### ---- PLANT PROP ---- ###

        self.plant_properties= ctk.CTkFrame(self)
        self.plant_properties.grid(row=1, column=0, padx=5, pady=5, sticky="we")

        self.plant_name = ctk.CTkLabel(self, text=self.plant[1], font=ctk.CTkFont(size=40, weight="bold"))
        self.plant_name.grid(row=0, column=3, pady=20, padx=10, sticky="we")
        self.watering = ctk.CTkLabel(self.plant_properties, text=f"Zalijevanje: {self.plant[3]}", font=ctk.CTkFont(size=14))
        self.watering.grid(row=2, column=0, padx=10, pady=5, sticky="we")
        self.brightness = ctk.CTkLabel(self.plant_properties, text=f"Izloženost svjetlosti: {self.plant[4]}", font=ctk.CTkFont(size=14))
        self.brightness.grid(row=3, column=0, padx=10, pady=5, sticky="we")
        self.temperature = ctk.CTkLabel(self.plant_properties, text=f"Temperatura: {self.plant[5]}", font=ctk.CTkFont(size=14))
        self.temperature.grid(row=4, column=0, padx=10, pady=5, sticky="we")
        self.ph = ctk.CTkLabel(self.plant_properties, text=f"pH tla: {self.plant[6]}", font=ctk.CTkFont(size=14))
        self.ph.grid(row=5, column=0, padx=10, pady=5, sticky="we")
        self.salinity= ctk.CTkLabel(self.plant_properties, text=f"Salinitet: {self.plant[7]}", font=ctk.CTkFont(size=14))
        self.salinity.grid(row=6, column=0, padx=10, pady=5, sticky="we")
        self.supstrate = ctk.CTkLabel(self.plant_properties, text=f"Dodavanje supstrata: {'da' if self.plant[8] == 1 else 'ne'}", font=ctk.CTkFont(size=14))
        self.supstrate.grid(row=7, column=0, padx=10, sticky="we")

        ### ---- SENSOR STATUS ---- ###

        self.sensor_data = self.pots_tiles.get_sensor_data(self.pot)
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
        self.ph_label = ctk.CTkLabel(self.sensors_status, text=f"pH: {self.sensor_data['ph']}", font=ctk.CTkFont(size=14))
        self.ph_label.grid(row=4, column=0, padx=5, sticky="w")
        self.light_label = ctk.CTkLabel(self.sensors_status, text=f"Salinitet: {self.sensor_data['salinity']} ppm", font=ctk.CTkFont(size=14))
        self.light_label.grid(row=5, column=0, padx=5, sticky="w")

         ### ---- GRAPHS ---- ###
        
        self.sensors_graphs = ctk.CTkFrame(self)
        self.sensors_graphs.grid(row=3, sticky="we", padx=5, pady=10, columnspan=4, rowspan=2)
        self.sensors_graphs_label = ctk.CTkLabel(self, text="Grafički prikaz stanja senzora zadnja 24h", font=ctk.CTkFont(size=14))
        self.sensors_graphs_label.grid(row=2, column=0, sticky="we", pady=10)

        self.graphs_label = ctk.CTkLabel(self.sensors_graphs, text="Sinkronizirajte(SYNC) i osvježite senzore za prikaz novih podataka", font=ctk.CTkFont(size=14))
        self.graphs_label.grid(row=2, column=0, sticky="we", pady=10)
        self.sensor_plotter = SensorPlotter(self.sensors_graphs, self.pot_id)
        self.sensor_plotter.plot_sensor_data()


        ### ---- REFRESH btn ---- ###

        self.refresh_button = ctk.CTkButton(self, text="Osvježi", corner_radius=10, 
                                    command=lambda:(
                                    self.update_sensor_data(), 
                                    self.sensor_plotter.plot_sensor_data()
                                    ))
        self.refresh_button.grid(row=2, column=1, sticky="we")

        ### ---- DELETE PLANT FROM POT btn ---- ###

        self.refresh_button = ctk.CTkButton(self, text="Izbaci bljku iz posude", corner_radius=10, command=lambda pot_id=self.pot[1]: self.empty_the_pot(pot_id), text_color="black", fg_color="#FF6961", hover_color="#D60B00")
        self.refresh_button.grid(row=2, column=3, sticky="we")


    def empty_the_pot(self, pot_id: int) -> None:
        """
        Removes a plant from a pot and updates the pot tiles in the master window.

        Args:
            pot_id (int): The ID of the pot from which to remove the plant.
        """
        remove_plant_from_pot(pot_id)
        self.master.update_pot_tiles()

    def update_sensor_data(self):
        """
        updates sensor data labels after sync button press
        """
        self.sensor_data = self.pots_tiles.get_sensor_data(self.pot)
        self.temperature_label.configure(text=f"Temperatura: {self.sensor_data['temperature']} °C")
        self.moisture_label.configure(text=f"Vlažnost: {self.sensor_data['moisture']} %")
        self.light_label.configure(text=f"Svjetlost: {self.sensor_data['brightness']} lux")
        self.ph_label.configure(text=f"pH: {self.sensor_data['ph']}")
        self.light_label.configure(text=f"Salinitet: {self.sensor_data['salinity']} ppm")

    def save_pot_placement(self) -> None:
        """
        Saves the changes mate to the pot placement
        """
        new_pot_placement = self.pot_placement.get()
        change_pot_placement(new_pot_placement, self.pot[1] )
