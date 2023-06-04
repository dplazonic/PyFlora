from tkinter import *
from PIL import Image
from db_manager.plants import *
from db_manager.pots_db import *
import customtkinter as ctk
from sensors import PotSensor




class PotsTiles(ctk.CTkScrollableFrame):
    def __init__(self, master: ctk.CTk, *args, **kwargs) -> None:
        """
        Initializes a PotsTiles instance.

        Args:
            master (ctk.Tk): customTkinter parent widget.
        """
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.status_labels = {}

        self.mid_frame = ctk.CTkFrame(self)
        self.mid_frame.grid(row=1, column=0, columnspan=4, sticky="nswe", padx=20, pady=20) 

        pots=get_pots()
        row, col = 0, 0
        grid_row, grid_col = 0,0

        if pots:
            plant_status_texts = self.check_plant_status()

            for pot in pots:
                self.tile = ctk.CTkFrame(self.mid_frame, corner_radius=5)
                sensor_data = self.generate_sensor_data(pot)

                self.top_tile = ctk.CTkFrame(self.tile, fg_color="transparent")
                self.top_tile.grid(row=0, column=0, padx=5, columnspan=2, sticky="we")

                img = Image.open("photos\\pot.png" if pot[7]== None else pot[7])
                img_tk = ctk.CTkImage(img, size=(90, 90))
                self.img_label = ctk.CTkLabel(self.top_tile,text="", image=img_tk)
                self.img_label.grid(row=1, column=0, rowspan=3, padx=10, pady=25, sticky="nesw")

                self.del_button = ctk.CTkButton(self.tile, text="X", text_color="black", fg_color=("#FF6961"), hover_color="#D60B00", corner_radius=100, width=10, height=10)
                self.del_button.grid(row=0, column=1, sticky="ne")
                self.del_button.bind("<Button-1>", lambda event, pot_id=pot[1]: self.tile_clicked(event, pot_id, delete=True))
                    
                self.detail_button = ctk.CTkButton(self.top_tile, text="Detalji posude",font=("TkDefaultFont", 12))
                self.detail_button.grid(row=4, column=0, padx=5, pady=10, sticky="nesw", columnspan=2)
                if pot[6] is None:
                    self.detail_button.configure(state="disabled", text_color="black", text="Prazna posuda")
                else:
                    self.detail_button.bind("<Button-1>", lambda event, pot_id=pot[0]: self.tile_clicked(event, pot_id))
                self.desc_label_0 = ctk.CTkLabel(self.top_tile, text=f"Posuda br. {pot[0]}", font=ctk.CTkFont(size=18, weight="bold"))
                self.desc_label_0.grid(row=0, column=0, pady=10, padx=10, columnspan=2, sticky="we")
                self.desc_label_1 = ctk.CTkLabel(self.top_tile, text=f"Materijal posude: {pot[2]}", font=ctk.CTkFont(size=12),  wraplength=150)
                self.desc_label_1.grid(row=1, column=1, padx=5, pady=5, sticky="w")
                self.desc_label_2 = ctk.CTkLabel(self.top_tile, text=f"Pozicija posude: {pot[3]}", font=ctk.CTkFont(size=12), wraplength=150)
                self.desc_label_2.grid(row=2, column=1, padx=5, pady=5, sticky="w")
                self.desc_label_3 = ctk.CTkLabel(self.top_tile, text=f"Veličina posude: {pot[4]}", font=ctk.CTkFont(size=12), wraplength=150)
                self.desc_label_3.grid(row=3, column=1, padx=5, pady=5, sticky="w")

                # Create a frame for the name and description
                self.bottom_tile = ctk.CTkFrame(self.tile, fg_color="transparent")
                self.bottom_tile.grid(row=1, column=0, padx=5, sticky="we", columnspan=2)
                self.bottom_tile.grid_columnconfigure((0,1,2), weight=1)
                
                self.desc_label_4 = ctk.CTkLabel(self.bottom_tile, text=f"Biljka u posudi: {'prazno' if pot[6] == None else pot[6]}", font=ctk.CTkFont(size=12))
                self.desc_label_4.grid(row=0, column=0, padx=5, sticky="we", columnspan=2)

                status_text = plant_status_texts[pot[0] - 1]

                self.status_sensors = ctk.CTkLabel(self.bottom_tile, text=f"{status_text}", font=ctk.CTkFont(size=12), wraplength=100)
                self.status_sensors.grid(row=1, column=1, padx=5, sticky="ns", rowspan=3)

                self.temperature_label = ctk.CTkLabel(self.bottom_tile, text=f"Temperatura: {sensor_data['temperature']} °C", font=ctk.CTkFont(size=12))
                self.temperature_label.grid(row=1, column=0, padx=5, sticky="w")
                
                self.moisture_label = ctk.CTkLabel(self.bottom_tile, text=f"Vlažnost: {sensor_data['moisture']} %", font=ctk.CTkFont(size=12))
                self.moisture_label.grid(row=2, column=0, padx=5, sticky="w")
                
                self.light_label = ctk.CTkLabel(self.bottom_tile, text=f"Svjetlost: {sensor_data['brightness']} lux", font=ctk.CTkFont(size=12))
                self.light_label.grid(row=3, column=0, padx=5, sticky="w")

                self.add_plant_button = ctk.CTkButton(self.bottom_tile, text="Promijeni biljku",font=("TkDefaultFont", 12))
                self.add_plant_button.grid(row=4, column=0, padx=5, pady=10, sticky="nesw", columnspan=2)
                if pot[6] is None:
                    self.add_plant_button.configure(text="Dodaj biljku")
                    self.add_plant_button.bind("<Button-1>", lambda event, display_pot_id=pot[0]: self.add_plant_to_pot(event, display_pot_id))
                else:
                    self.add_plant_button.configure(text="Promijeni biljku")
                    self.add_plant_button.bind("<Button-1>", lambda event, display_pot_id=pot[0]: self.add_plant_to_pot(event, display_pot_id))

                # Define grid for pots - grid_row, grid_col = row,col (row x col)
                grid_row, grid_col = 4,4
                row = (pot[0] - 1) // grid_row
                col = (pot[0] - 1) % grid_col
                
                self.tile.grid(row=row, column=col, padx=5, pady=5)

        self.button_tile = ctk.CTkFrame(self.mid_frame)
        self.button_tile.grid(row = row if col < grid_col-1 else row+1, column=col+1 if col < grid_col-1 else col==0)
        self.button_tile.grid_columnconfigure((0,1), weight=1)
        self.button_tile.grid_rowconfigure(0, weight=1)

        add_img = Image.open("photos\\add.png")
        add_img_tk= ctk.CTkImage(add_img, size=(100, 100))

        self.button_photo = ctk.CTkLabel(self.button_tile, text="", image=add_img_tk, )
        self.button_photo.grid(row=0, column=0, pady=20, padx=30, columnspan=2, sticky="nswe")

        self.add_button = ctk.CTkButton(self.button_tile, text="Dodaj novu posudu", font=("TkDefaultFont", 12))
        self.add_button.grid(row=1, column=1, pady=20, padx=30, columnspan=2, sticky="nswe")  

        self.add_button.bind("<Button-1>", lambda event, pot_id=-1: self.tile_clicked(event, pot_id))

    def add_plant_to_pot(self, event, display_pot_id: int) -> None:
        """
        Adds a plant to a pot in the GUI.

        Args:
            event (tk.Event): customTkinter event.
            display_pot_id (int): Pot ID.
        """
        self.master.add_plant_to_pot(display_pot_id)

    def tile_clicked(self, event, pot_id: int, delete: bool = False) -> None:
        """
        Handles events for pot tiles.

        Args:
            event (tk.Event): customTkinter event.
            pot_id (int): Pot ID.
            delete (bool, optional): If true, deletes the pot. Default is False.
        """
        if delete:
            delete_pot(pot_id)
            self.master.update_pot_tiles()
        elif pot_id == -1:
            self.master.show_add_pot()
        else:
            self.master.show_pot_details(pot_id)

    def generate_sensor_data(self, pot: tuple) -> dict:
        """
        Generates sensor data for a given pot.

        Args:
            pot (Tuple): Tuple containing pot information.

        Returns:
            Dict: Dictionary containing sensor data.
        """
        plant_pot = PotSensor(pot_id=pot[1])
        sensor_data = plant_pot.generate_sensor_data()
        return sensor_data

    def get_pots_with_plant_requirements(self) -> list[tuple]:
        """
        Fetches pot's information along with plant's requirements.

        Returns:
            List[Tuple]: List of tuples containing pot and plant information.
        """
        pots = get_pots()
        pots_with_req = []

        for pot in pots:
            display_id, pot_id, material, placement, size, plant_id, plant_name, photo = pot
            plant = get_plant_by_id(plant_id)
            if plant:
                plant_id, plant_name, photo, watering, brightness, temperature, supstrate = plant
                pot_with_req = (pot_id, material, placement, size, plant_name, watering, brightness, temperature, supstrate)
                pots_with_req.append(pot_with_req)
            else:
                pot_with_no_plant = (pot_id, material, placement, size, None, None, None, None, None)
                pots_with_req.append(pot_with_no_plant)

        return pots_with_req 

    def check_plant_status(self) -> list[tuple[str]]:
        """
        Checks the status of plants in each pot based on their current sensor
        readings and their ideal conditions.

        Returns:
            List[Tuple[str]]: List of tuples, where each tuple contains a string representing the status of a plant.
        """
        pots_with_preferences = self.get_pots_with_plant_requirements()
        status_texts=[]
        for pot in pots_with_preferences:
            pot_id, material, placement, size, plant_name, watering, brightness, temperature, supstrate = pot
            status_text = f""
            pot_sensor = PotSensor(pot_id)
            brightness_status = pot_sensor.light_status(brightness)
            temperature_status = pot_sensor.temperature_status(temperature)
            moisture_status = pot_sensor.moisture_status(watering)
            
            if plant_name is not None:
                temp_check = "OK\n" if temperature_status == temperature else f"zahtjeva {temperature} uvjete!\n"
                moist_check = "OK\n" if moisture_status == "vlažno" else f"zahtjeva zalijevanje!\n"
                brightness_check = "OK\n" if brightness_status == brightness else f"potrebno: {brightness}!\n"
            else:
                temp_check = "posuda prazna!\n"
                moist_check = "posuda prazna!\n"
                brightness_check = "posuda prazna!\n"

            status_text += f"temperatura: {temp_check}\nvlažnost: {moist_check}\nsvjetlost: {brightness_check}"
            status_texts.append(status_text)  
            
        return status_texts 
    


    