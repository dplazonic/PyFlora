import tkinter as tk
from PIL import Image, ImageTk
import tkinter.messagebox
import customtkinter as ctk
from time import strftime
from user_editor import *
from db_manager.plants import *
from plant_tiles import PlantTiles
from add_plant import AddPlant
from plant_details import PlantDetails
from pots_screen import PotsTiles
from add_plant_to_pot import AddPlantToPot
from add_pot import AddPot


ctk.set_appearance_mode("light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window


        self.title("PyFlora app.py")
        self.geometry(f"{1500}x{1240}+{500}+{80}")

        # configure grid layout (3x4)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_columnconfigure((0,3), weight=0)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure((0,2), weight=0)



        ### ---- top frame ----- ###
        self.top_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.top_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")
        self.top_frame.grid_columnconfigure(2, weight=1)
        self.logo_label = ctk.CTkLabel(self.top_frame, text="PyFlora", font=ctk.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.topbar_button_1 = ctk.CTkButton(self.top_frame,text= "PyFlora Posude", command=self.pots_button_event)
        self.topbar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.topbar_button_2 = ctk.CTkButton(self.top_frame,text= "Biljke", command=self.plant_button_event)
        self.topbar_button_2.grid(row=1, column=1, padx=20, pady=10)
        self.topbar_button_3 = ctk.CTkButton(self.top_frame, text= "Moj Profil", command=create_edit_user_screen)
        self.topbar_button_3.grid(row=1, column=3, padx=20, pady=10)
        self.topbar_button_4 = ctk.CTkButton(self.top_frame, text= "Logout", command=self.sidebar_button_event)
        self.topbar_button_4.grid(row=0, column=3, padx=20, pady=10)
        self.sync_button = ctk.CTkButton(self.top_frame, text= "SYNC", command=self.sync_button_event)
        self.sync_button.grid(row = 1, column = 2, sticky="ne", padx=20, pady=10)
        


        ### ---- middle frame ----- ###

        self.mid_frame = None
     




        ### ---- bottom frame ----- ###
        self.bottom_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.bottom_frame.grid(row=2, column=0, columnspan=4, sticky="nsew")
        self.bottom_frame.grid_columnconfigure(2, weight=1)
        self.logo_label = ctk.CTkLabel(self.bottom_frame, text="v 1.0", font=ctk.CTkFont(size=10, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.time_label = ctk.CTkLabel(self.bottom_frame, font=ctk.CTkFont(size=10, weight="bold"))
        self.time_label.grid(row=0, column=1, padx=20, pady=(20, 10))




    def tile_view_click_event(self):
        print("Tile view clicked")
  

    def time(self):
        time_string = strftime('%H:%M:%S %p') # time format 
        self.time_label.configure(text = time_string)
        self.time_label.after(1000, self.time) # time delay of 1000 milliseconds 




    def open_input_dialog_event(self):
        dialog = ctk.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())






    def sidebar_button_event(self):
        print("Tile 1 clicked")


    def plant_button_event(self):
        if self.mid_frame is not None:
            self.mid_frame.grid_forget()

        self.mid_frame = PlantTiles(master=self)
        self.mid_frame.grid(row=1, column=0, columnspan=4, sticky="nswe", padx=20, pady=20)



    def pots_button_event(self):
        if self.mid_frame is not None:
            self.mid_frame.grid_forget()

        self.mid_frame = PotsTiles(master=self)
        self.mid_frame.grid(row=1, column=0, columnspan=4, sticky="nswe", padx=20, pady=20)

        

    def tile2_click_event(self):
        print("Tile 2 clicked")

    def tile3_click_event(self):
        print("Tile 3 clicked")
           
    
    
     ##----------PLANT TILES ---------##

    def update_plant_tiles(self):
        self.mid_frame.grid_forget()
        self.mid_frame = PlantTiles(self)
        self.mid_frame.grid(row=1, column=0, columnspan=4, sticky="nswe", padx=20, pady=20)

    def show_add_plant(self):
        self.mid_frame.grid_forget()
        self.mid_frame = AddPlant(self)
        self.mid_frame.grid(row=1, column=1, padx=20, pady=20, columnspan=2)
        self.mid_frame.grid_columnconfigure((1,2), weight=1)

    def show_plant_details(self, plant_id):
        self.mid_frame.grid_forget()
        self.mid_frame = PlantDetails(self, plant_id=plant_id)
        self.mid_frame.grid(row=1, column=1, padx=20, pady=20, columnspan=2)
        self.mid_frame.grid_columnconfigure((1,2), weight=1)

        ##----------POT TILES ---------##

    def update_pot_tiles(self):
         self.mid_frame.grid_forget()
         self.mid_frame = PotsTiles(self)
         self.mid_frame.grid(row=1, column=0, columnspan=4, sticky="nswe", padx=20, pady=20)

    def show_add_pot(self):
        self.mid_frame.grid_forget()
        self.mid_frame = AddPot(self)
        self.mid_frame.grid(row=1, column=1, padx=20, pady=20, columnspan=2)
        self.mid_frame.grid_columnconfigure((1,2), weight=1)

    # def show_pot_details(self, plant_id):
    #     self.mid_frame.grid_forget()
    #     self.mid_frame = PlantDetails(self, plant_id=plant_id)
    #     self.mid_frame.grid(row=1, column=1, padx=20, pady=20, columnspan=2)
    #     self.mid_frame.grid_columnconfigure((1,2), weight=1)

    def add_plant_to_pot(self, pot_id):
        self.mid_frame.grid_forget()
        self.mid_frame = AddPlantToPot(master=self, pot_id=pot_id)
        self.mid_frame.grid(row=1, column=1, padx=20, pady=20, columnspan=2)
        self.mid_frame.grid_columnconfigure((1,2), weight=1)

    def sync_button_event(self):
        pass

if __name__ == "__main__":
    app = App()
    app.time()
    app.mainloop()


















