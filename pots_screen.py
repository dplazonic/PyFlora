import tkinter as tk 
from tkinter import *
from PIL import Image, ImageTk
from db_manager.plants import *
from db_manager.pots_db import *
import customtkinter as ctk
from sensors import PotSensor



class PotsTiles(ctk.CTkScrollableFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.status_labels = {}




        self.mid_frame = ctk.CTkFrame(self)
        self.mid_frame.grid(row=1, column=0, columnspan=4, sticky="nswe", padx=20, pady=20)        
        
        

    

        
# Create a frame to hold the tiles

    
        pots=get_pots()
        plant_status_texts = self.check_plant_status()


# Loop through the plant data and create a tile for each one
        for pot in pots:
            # Create a label to hold the image, name, and description
            self.tile = ctk.CTkFrame(self.mid_frame, corner_radius=5)
            sensor_data = self.generate_sensor_data(pot)



            self.top_tile = ctk.CTkFrame(self.tile, fg_color="transparent")
            self.top_tile.grid(row=0, column=0, padx=5, columnspan=2, sticky="we")
            # self.top_tile.grid_columnconfigure((0,1), weight=1)
            # self.top_tile.grid_rowconfigure((1,2,3), weight=1)
            # self.top_tile.grid_rowconfigure((0,4), weight=0)


            img = Image.open("photos\\pot.png")
            img_tk = ctk.CTkImage(img, size=(90, 90))
            self.img_label = ctk.CTkLabel(self.top_tile,text="", image=img_tk)
            self.img_label.grid(row=1, column=0, rowspan=3, padx=10, pady=25, sticky="nesw")
                
            self.detail_button = ctk.CTkButton(self.top_tile, text="Detalji",font=("TkDefaultFont", 12))
            self.detail_button.grid(row=4, column=0, padx=5, pady=10, sticky="nesw", columnspan=2)
            self.detail_button.bind("<Button-1>", lambda event, pot_id=pot[1]: self.tile_clicked(event, pot_id))

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
            self.bottom_tile.grid_columnconfigure(0, weight=1)
            self.bottom_tile.grid_columnconfigure(1, weight=1)

            
            self.desc_label_4 = ctk.CTkLabel(self.bottom_tile, text=f"Biljka u posudi: {'prazno' if pot[6] == None else pot[6]}", font=ctk.CTkFont(size=12))
            self.desc_label_4.grid(row=0, column=0, padx=5, sticky="we", columnspan=2)

            status_text = plant_status_texts[pot[0] - 1]

            self.status = ctk.CTkLabel(self.bottom_tile, text=f"Status biljke:", font=ctk.CTkFont(size=12))
            self.status.grid(row=1, column=1, padx=5, sticky="we")
            self.status_sensors = ctk.CTkLabel(self.bottom_tile, text=f"{status_text}", font=ctk.CTkFont(size=12), wraplength=100)
            self.status_sensors.grid(row=2, column=1, padx=5, sticky="w", rowspan=2)



            self.add_plant_button = ctk.CTkButton(self.bottom_tile, text="Dodaj biljku",font=("TkDefaultFont", 12))
            self.add_plant_button.grid(row=4, column=0, padx=5, pady=10, sticky="we", columnspan=2)
            self.add_plant_button.bind("<Button-1>", lambda event, pot_id=pot[1]: self.add_plant_to_pot(event, pot_id))


            self.del_button = ctk.CTkButton(self.tile, text="X", text_color="black", fg_color=("#FF6961"), hover_color="#D60B00", corner_radius=100, width=10, height=10)
            self.del_button.grid(row=0, column=1, sticky="ne")
            self.del_button.bind("<Button-1>", lambda event, pot_id=pot[1]: self.tile_clicked(event, pot_id, delete=True))


            self.temperature_label = ctk.CTkLabel(self.bottom_tile, text=f"Temperatura: {sensor_data['temperature']} °C", font=ctk.CTkFont(size=12))
            self.temperature_label.grid(row=1, column=0, padx=5, sticky="w")
            
            self.moisture_label = ctk.CTkLabel(self.bottom_tile, text=f"Vlažnost: {sensor_data['moisture']} %", font=ctk.CTkFont(size=12))
            self.moisture_label.grid(row=2, column=0, padx=5, sticky="w")
            
            self.light_label = ctk.CTkLabel(self.bottom_tile, text=f"Svjetlost: {sensor_data['light']} lux", font=ctk.CTkFont(size=12))
            self.light_label.grid(row=3, column=0, padx=5, sticky="w")





            # generate grid of labels
            row = (pot[0]-1) // 3
            col = (pot[0]-1) % 3
            
            self.tile.grid(row=row, column=col, padx=5, pady=5)


        self.button_tile = ctk.CTkFrame(self.mid_frame)
        self.button_tile.grid(row=row , column=col+1)
        self.button_tile.grid_columnconfigure((0,1), weight=1)
        self.button_tile.grid_rowconfigure(0, weight=1)

        add_img = Image.open("photos\\add.png")
        add_img_tk= ctk.CTkImage(add_img, size=(100, 100))

        self.button_photo = ctk.CTkLabel(self.button_tile, text="", image=add_img_tk, )
        self.button_photo.grid(row=0, column=0, pady=20, padx=30, columnspan=2, sticky="nswe")

        self.add_button = ctk.CTkButton(self.button_tile, text="Dodaj novu posudu", font=("TkDefaultFont", 12))
        self.add_button.grid(row=1, column=1, pady=20, padx=30, columnspan=2, sticky="nswe")  

        #self.add_button.plant_id = -1  
        #self.add_button.bind("<Button-1>", self.tile_clicked)
        self.add_button.bind("<Button-1>", lambda event, pot_id=-1: self.tile_clicked(event, pot_id))




    def add_plant_to_pot(self, event, pot_id):
        #print(f"dodajem biljku u lonac {pot_id}")
        self.master.add_plant_to_pot(pot_id)

    def tile_clicked(self, event, pot_id, delete=False):
        if delete:
            print(f"Deleting pot {pot_id}")
            delete_pot(pot_id)
            self.master.update_pot_tiles()
        elif pot_id == -1:
            # print(f"Pot {pot_id} clicked!")
            self.master.show_add_pot()
        else:
            print(f"Pot {pot_id} clicked!")
            # self.master.show_plant_details(pot_id)


    def generate_sensor_data(self, pot):
        plant_pot = PotSensor(pot_id=pot[1])
        sensor_data = plant_pot.generate_sensor_data()
        return sensor_data



    def get_pots_with_plant_requirements(self):
        pots = get_pots()
        pots_with_req = []

        for pot in pots:
            display_id, pot_id, material, placement, size, plant_id, plant_name = pot
            plant = get_plant_by_id(plant_id)
            if plant:
                plant_id, plant_name, photo, watering, brightness, temperature, supstrate = plant
                pot_with_req = (pot_id, material, placement, size, plant_name, watering, brightness, temperature, supstrate)
                pots_with_req.append(pot_with_req)
            else:
                pot_with_no_plant = (pot_id, material, placement, size, None, None, None, None, None)
                pots_with_req.append(pot_with_no_plant)
        

        return pots_with_req 




    def check_plant_status(self):
        pots_with_preferences = self.get_pots_with_plant_requirements()
        #print(f"{pots_with_preferences}")
        status_texts=[]
        for pot in pots_with_preferences:
            pot_id, material, placement, size, plant_name, watering, brightness, temperature, supstrate = pot
            #print(f" pot: {pot}")
            #print(f"plant_name: {plant_name}")
            status_text = f""



            pot_sensor = PotSensor(pot_id)
            light_status = pot_sensor.light_status(brightness)
            temperature_status = pot_sensor.temperature_status(temperature)
            moisture_status = pot_sensor.moisture_status(watering)
            if plant_name is not None:

                light_check = "OK" if light_status == brightness else f"zahtjeva uvjete: {brightness}!"
                temp_check = "OK" if temperature_status == temperature else f"zahtjeva {temperature} uvjete!"
                moist_check = "OK" if moisture_status == watering else f"zahtjeva zalijevanje: {watering}!"

            else:
                
                light_check = "posuda prazna!"
                temp_check = "posuda prazna!"
                moist_check = "posuda prazna!"

            status_text += f"svjetlost: {light_check}\ntemperatura: {temp_check}\nvlažnost: {moist_check}"
            status_texts.append(status_text)  
        
        
        print(f"status_texts: {status_texts}")  # Add this line to print the status_texts

        return status_texts 
    