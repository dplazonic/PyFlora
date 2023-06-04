import tkinter as tk
import customtkinter as ctk
from PIL import Image
from db_manager.plants import *
from db_manager.pots_db import *



class AddPlantToPot(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, display_pot_id: int, *args, **kwargs) -> None:
        """
        Initializes the AddPlantToPot frame.

        Args:
            master (ctk.CTk): CustomTkinter parent widget.
            display_pot_id (int): ID of the pot to which a plant is to be added.
        """
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.display_pot_id = display_pot_id

        self.grid(row=1)

        self.mid_frame = ctk.CTkScrollableFrame(self, label_text="Odabir biljke iz kolekcije", width=500)
        self.mid_frame.grid(row=1, columnspan=5, sticky="we")

        # Fetch pots and plants from the database
        self.plants = get_plants()
        self.pot = get_pot_by_display_id(self.display_pot_id)
        self.pot_id= self.pot[1]

        # Create clickable plant list
        for i, plant in enumerate(self.plants):
            plant_list = ctk.CTkLabel(self.mid_frame, text=plant[2])
            plant_list.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            plant_list.bind("<Button-1>", lambda event, plant_id=(plant[0]-1): self.plant_clicked(event, self.plants, plant_id, self.pot))
            
        img = Image.open("photos\\pot.png")
        img_tk = ctk.CTkImage(img, size=(90, 90))
        self.img_label = ctk.CTkLabel(self, text="", image=img_tk)
        self.img_label.grid(row=0, column=2, columnspan=2, padx=10, pady=10, sticky="nesw")

        self.pot_num = ctk.CTkLabel(self, text=f"Posuda br. {self.pot[0]}", font=ctk.CTkFont(size=18, weight="bold"))
        self.pot_num.grid(row=0, pady=10, padx=10, column=0, columnspan=2, sticky="we")

        self.pot_msg = ctk.CTkLabel(self, text=f"U posudu {self.pot[0]} dodajete biljku: ", font=ctk.CTkFont(size=18, weight="bold"))
        self.pot_msg.grid(row=2, pady=10, padx=10, columnspan=4, sticky="w")

        self.submit_button = ctk.CTkButton(self, text="Pohrani", command=self.submit)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="we")

        self.submit_button = ctk.CTkButton(self, text="Odustani", command=self.master.update_pot_tiles)
        self.submit_button.grid(row=3, column=2, columnspan=2, pady=10, padx=10, sticky="we")

    def plant_clicked(self, event: tk.Event, plants: list, plant_id: int, pot: list) -> None:
        """
        Updates the plant to be added to the pot when a plant is clicked.

        Args:
            event (tk.Event): The event that triggers the function.
            plants (list): List of all plants.
            plant_id (int): ID of the selected plant.
            pot (list): List containing details of the selected pot.
        """
        self.pot_msg.configure(text=f"U posudu {pot[0]} dodajete biljku: {plants[plant_id][2]}")
        self.selected_plant_id = plants[plant_id][1]
    
    def submit(self) -> None:
        """
        Updates the pot with the selected plant and refreshes the pot tiles.
        """
        update_pot_with_plant(self.pot_id, self.selected_plant_id)
        self.master.update_pot_tiles()