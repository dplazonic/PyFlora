import tkinter as tk 
from tkinter import *
from PIL import Image
from db_manager.plants_db import *
import customtkinter as ctk
from plant_details import *




class PlantTiles(ctk.CTkScrollableFrame):
    """
    A class representing a scrollable frame with plant tiles.
    It is used to represent a frame which contains tiles of different plants. 
    Each plant tile includes 
    an image, name, and a description of the plant.

    Args:
        master (tkinter.Tk): The parent window for this frame.
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.mid_frame = ctk.CTkFrame(self)
        self.mid_frame.grid(row=1, column=0, columnspan=4, sticky="nswe", padx=10, pady=10)        
        
        plants=get_plants()

        row, col = 0, 0
        grid_row, grid_col = 0, 0
        if plants:

            for plant in plants:
                self.tile = ctk.CTkFrame(self.mid_frame, corner_radius=5)

                img = Image.open(plant[3])
                img_tk = ctk.CTkImage(img, size=(150, 150))

                self.left_tile = ctk.CTkFrame(self.tile, fg_color="transparent")
                self.left_tile.grid(row=0, column=0, padx=5)

                self.img_label = ctk.CTkLabel(self.left_tile,text="", image=img_tk)
                self.img_label.grid(row=0, column=0, padx=5, pady=20)
                    
                self.detail_button = ctk.CTkButton(self.left_tile, text="Detalji",font=("TkDefaultFont", 12))
                self.detail_button.grid(row=1, column=0, padx=5, pady=10)
                self.detail_button.bind("<Button-1>", lambda event, plant_id=plant[1]: self.tile_clicked(event, plant_id))

                self.right_tile = ctk.CTkFrame(self.tile, fg_color="transparent")
                self.right_tile.grid(row=0, column=1, padx=5)

                self.desc_label_title = ctk.CTkLabel(self.right_tile, text=plant[2], font=ctk.CTkFont(size=20, weight="bold"))
                self.desc_label_title.grid(row=0, column=0, pady=2)
                self.desc_label_watering = ctk.CTkLabel(self.right_tile, text=f"Zalijevanje: {plant[4]}", font=ctk.CTkFont(size=12))
                self.desc_label_watering.grid(row=1, column=0, padx=5, pady=2, sticky="w")
                self.desc_label_brightness = ctk.CTkLabel(self.right_tile, text=f"Izloženost svjetlosti: {plant[5]}", font=ctk.CTkFont(size=12))
                self.desc_label_brightness.grid(row=2, column=0, padx=5, pady=2, sticky="w")
                self.desc_label_temperatrure = ctk.CTkLabel(self.right_tile, text=f"Temperatura: {plant[6]}", font=ctk.CTkFont(size=12))
                self.desc_label_temperatrure.grid(row=3, column=0, padx=5, pady=2, sticky="w")
                self.desc_label_ph = ctk.CTkLabel(self.right_tile, text=f"odgovarajući pH tla: {plant[7]}", font=ctk.CTkFont(size=12))
                self.desc_label_ph.grid(row=4, column=0, padx=5, pady=2, sticky="w")
                self.desc_label_salinity = ctk.CTkLabel(self.right_tile, text=f"Salinitet tla: {plant[8]}", font=ctk.CTkFont(size=12))
                self.desc_label_salinity.grid(row=5, column=0, padx=5, pady=2, sticky="w")
                self.desc_label_supstrate = ctk.CTkLabel(self.right_tile, text=f"Dodavanje supstrata: {'da' if plant[9] == 1 else 'ne'}", font=ctk.CTkFont(size=12))
                self.desc_label_supstrate.grid(row=6, column=0, padx=5, sticky="w")

                self.del_button = ctk.CTkButton(self.tile, text="X", text_color="black", fg_color="#FF6961", hover_color="#D60B00", corner_radius=100, width=10, height=10)
                self.del_button.grid(row=0, column=1, sticky="ne")
                self.del_button.bind("<Button-1>", lambda event, plant_id=plant[1]: self.tile_clicked(event, plant_id, delete=True))

                # Define grid - grid_row, grid_col = row,col (row x col)
                grid_row, grid_col = 4,4
                row = (plant[0] - 1) // grid_row
                col = (plant[0] - 1) % grid_col
                
                self.tile.grid(row=row, column=col, padx=5, pady=5)


        add_img = Image.open("photos\\add.png")
        add_img_tk= ctk.CTkImage(add_img, size=(125, 125))

        self.button_tile = ctk.CTkFrame(self.mid_frame)
        self.button_tile.grid(row = row if col < grid_col-1 else row+1, column=col+1 if col < grid_col-1 else col==0, padx=10, pady=10)
       
        self.button_photo = ctk.CTkLabel(self.button_tile, text="", image=add_img_tk, )
        self.button_photo.grid(row=0, column=0, pady=20, padx=10, rowspan=2)

        self.add_button = ctk.CTkButton(self.button_tile, text="Dodaj novu biljku", font=("TkDefaultFont", 12))
        self.add_button.grid(row=0, column=1, pady=20, padx=10, rowspan=2)  
        self.add_button.bind("<Button-1>", lambda event, plant_id=-1: self.tile_clicked(event, plant_id))

    def tile_clicked(self, event: tk.Event, plant_id: int, delete: bool=False):        
        """
        Handle the event when a plant tile is clicked.
        If the tile is marked for deletion, it deletes the plant from the database
        and updates the plant tiles in the master frame. If a new plant is to be
        added, it shows the add plant form. Otherwise, it shows the details of the
        clicked plant.

        Args:
            event (tkinter.Event): The event object.
            plant_id (int): The id of the clicked plant.
            delete (bool, optional): Indicates if the clicked tile is marked for deletion. Defaults to False.
        """
        if delete:
            delete_plant(plant_id)
            self.master.update_plant_tiles()
        elif plant_id == -1:
            self.master.show_add_plant()
        else:
            self.master.show_plant_details(plant_id)




