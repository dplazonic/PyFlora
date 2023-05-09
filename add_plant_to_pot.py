import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from db_manager.plants import *
from db_manager.pots_db import *



class AddPlantToPot(ctk.CTkFrame):
    def __init__(self, master, pot_id, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.pot_id = pot_id

        self.mid_frame = ctk.CTkScrollableFrame(self, label_text="Odabir biljke iz kolekcije")
        self.mid_frame.grid(column=0, row=0, rowspan=4, sticky="we")

        # Fetch plants from the database
        plants = get_plants()
        pot = get_pot_by_id(self.pot_id)
        
        

        # Create clickable plant items
        for i, plant in enumerate(plants):
            plant_label = ctk.CTkLabel(self.mid_frame, text=plant[2])
            plant_label.grid(row=i, column=0, padx=5, pady=5)
            plant_label.bind("<Button-1>", lambda event, plant_id=(plant[0]-1): self.plant_clicked(event, plants, plant_id, pot))

            
        img = Image.open("photos\\pot.png")
        img_tk = ctk.CTkImage(img, size=(90, 90))
        self.img_label = ctk.CTkLabel(self, text="", image=img_tk)
        self.img_label.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="nesw")

        self.pot_num = ctk.CTkLabel(self, text=f"Posuda br. {pot[0]}", font=ctk.CTkFont(size=18, weight="bold"))
        self.pot_num.grid(row=1, column=1, pady=10, padx=10, columnspan=2, sticky="we")

        self.pot_msg = ctk.CTkLabel(self, text=f"U posudu {pot[0]} dodajete biljku: ", font=ctk.CTkFont(size=18, weight="bold"))
        self.pot_msg.grid(row=2, column=1, pady=10, padx=10, columnspan=2, sticky="we")

        self.submit_button = ctk.CTkButton(self, text="Pohrani", command=self.submit)
        self.submit_button.grid(row=3,column=1, pady=10, padx=10)

        self.submit_button = ctk.CTkButton(self, text="Odustani", command=self.master.update_pot_tiles)
        self.submit_button.grid(row=3, column=2, pady=10, padx=10)

        self.submit_button = ctk.CTkButton(self, text="Isprazni posudu", text_color="black", fg_color="#FF6961", hover_color="#D60B00") #command=self.master.update_tiles)
        self.submit_button.grid(row=3, column=3, pady=10, padx=10)



    def plant_clicked(self, event, plants, plant_id, pot):
        #print(f"Biljka {plants[plant_id][2]} kliknuta!")
        self.pot_msg.configure(text=f"U posudu {pot[0]} dodajete biljku: {plants[plant_id][2]}")
        self.selected_plant_id = plants[plant_id][1]
    
    def submit(self):
        update_pot_with_plant(self.pot_id, self.selected_plant_id)
        self.master.update_pot_tiles()