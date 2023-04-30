import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter as ctk
from db_manager.plants import *
import os
from db_manager.plants import *
from plant_tiles_class import *


class PlantDetails(ctk.CTkFrame):
    def __init__(self, master, plant_id, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        

        plant=get_plant_by_id(plant_id)
        #print(plant)

        self.mid_frame = ctk.CTkFrame(self)
        self.mid_frame.grid(row=1, column=0, sticky="nw")
        

    

        img = Image.open(plant[2])
        img_tk = ctk.CTkImage(img, size=(250, 250))
        self.img_label = ctk.CTkLabel(self.mid_frame,text="", image=img_tk)
        self.img_label.grid(row=0, column=0, padx=5, pady=5)
                

        self.desc_label_0 = ctk.CTkLabel(self.mid_frame, text=plant[1], font=ctk.CTkFont(size=20, weight="bold"), wraplength=150)
        self.desc_label_0.grid(row=0, column=1, pady=5)
        self.desc_label_1 = ctk.CTkLabel(self.mid_frame, text=f"Zalijevanje: {plant[3]}", font=ctk.CTkFont(size=12),  wraplength=150)
        self.desc_label_1.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.desc_label_2 = ctk.CTkLabel(self.mid_frame, text=f"Izloženost svjetlosti: {plant[4]}", font=ctk.CTkFont(size=12), wraplength=150)
        self.desc_label_2.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.desc_label_3 = ctk.CTkLabel(self.mid_frame, text=f"Temperetura: {plant[5]}", font=ctk.CTkFont(size=12), wraplength=150)
        self.desc_label_3.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.desc_label_4 = ctk.CTkLabel(self.mid_frame, text=f"Dodavanje supstrata: {'da' if plant[6] == 0 else 'ne'}", font=ctk.CTkFont(size=12), wraplength=150)
        self.desc_label_4.grid(row=4, column=1, padx=5, sticky="w")


