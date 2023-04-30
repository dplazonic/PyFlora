import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from db_manager.plants import *
from plant_editor import *
import customtkinter as ctk
from plant_details import *

#ctk.set_appearance_mode("light")  # Modes: "System" (standard), "Dark", "Light"
#tk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"



class PlantTiles(ctk.CTkFrame):
    def __init__(self,master, *args, **kwargs):
        super().__init__(master,*args, **kwargs)



        self.mid_frame = ctk.CTkFrame(self)
        self.mid_frame.grid(pady=10,padx=10)





        # self.sync_button_frame = ctk.CTkFrame(self.mid_frame,  fg_color=["gray86", "gray17"])
        # self.sync_button_frame.grid(row = 0, column = 3, sticky="ne")
        # self.sync_button = ctk.CTkButton(self.mid_frame, text= "SYNC", command=self.sidebar_button_event)
        # self.sync_button.grid(row = 0, column = 3, sticky="ne")
        
# Create a frame to hold the tiles
        self.mid_frame_tiles = ctk.CTkFrame(self.mid_frame)
        self.mid_frame_tiles.grid(row=0, column=0, columnspan=3, sticky="nw")


    
        plants=get_plants()

# Loop through the plant data and create a tile for each one
        for plant in plants:
            # Create a label to hold the image, name, and description
            self.tile = ctk.CTkFrame(self.mid_frame_tiles, corner_radius=5)
                

            # Load the plant image using PIL
            img = Image.open(plant[3])
            img_tk = ctk.CTkImage(img, size=(150, 150))

            self.left_tile = ctk.CTkFrame(self.tile, fg_color="transparent")
            self.left_tile.grid(row=0, column=0, padx=5)

            # Create an image and detalji widget for the plant image
            self.img_label = ctk.CTkLabel(self.left_tile,text="", image=img_tk)
            self.img_label.grid(row=0, column=0, padx=5, pady=20)
                
            self.detail_button = ctk.CTkButton(self.left_tile, text="Detalji",font=("TkDefaultFont", 12))
            self.detail_button.grid(row=1, column=0, padx=5, pady=10)
            #self.detail_button.plant_id = plant[1]
            #self.detail_button.bind("<Button-1>", self.tile_clicked)
            self.detail_button.bind("<Button-1>", lambda event, plant_id=plant[1]: self.tile_clicked(event, plant_id))




            # Create a frame for the name and description
            self.right_tile = ctk.CTkFrame(self.tile, fg_color="transparent")
            self.right_tile.grid(row=0, column=1, padx=5)


            self.desc_label_0 = ctk.CTkLabel(self.right_tile, text=plant[2], font=ctk.CTkFont(size=20, weight="bold"), wraplength=150)
            self.desc_label_0.grid(row=0, column=0, pady=5)
            self.desc_label_1 = ctk.CTkLabel(self.right_tile, text=f"Zalijevanje: {plant[4]}", font=ctk.CTkFont(size=12),  wraplength=150)
            self.desc_label_1.grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.desc_label_2 = ctk.CTkLabel(self.right_tile, text=f"Izloženost svjetlosti: {plant[5]}", font=ctk.CTkFont(size=12), wraplength=150)
            self.desc_label_2.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            self.desc_label_3 = ctk.CTkLabel(self.right_tile, text=f"Temperetura: {plant[6]}", font=ctk.CTkFont(size=12), wraplength=150)
            self.desc_label_3.grid(row=3, column=0, padx=5, pady=5, sticky="w")
            self.desc_label_4 = ctk.CTkLabel(self.right_tile, text=f"Dodavanje supstrata: {'da' if plant[7] == 0 else 'ne'}", font=ctk.CTkFont(size=12), wraplength=150)
            self.desc_label_4.grid(row=4, column=0, padx=5, sticky="w")

            self.del_button = ctk.CTkButton(self.tile, text="X", text_color="black", fg_color=("#FF6961"), hover_color="#D60B00", corner_radius=100, width=10, height=10)
            self.del_button.grid(row=0, column=1, sticky="ne")
            #self.del_button.plant_id_del = plant[1]
            #self.del_button.bind("<Button-1>", self.tile_clicked)
            self.del_button.bind("<Button-1>", lambda event, plant_id=plant[1]: self.tile_clicked(event, plant_id, delete=True))



            # generate grid of labels
            row = (plant[0]-1) % 3 
            col = (plant[0]-1) // 3 
            
            self.tile.grid(row=row, column=col, padx=5, pady=5)

        add_img = Image.open("photos\\add.png")
        add_img_tk= ctk.CTkImage(add_img, size=(125, 125))

        self.button_tile = ctk.CTkFrame(self.mid_frame_tiles)
        self.button_tile.grid(row=row+1 , column=col, padx=10, pady=10)
       
        self.button_photo = ctk.CTkLabel(self.button_tile, text="", image=add_img_tk, )
        self.button_photo.grid(row=0, column=0, pady=20, padx=10, rowspan=2)

        self.add_button = ctk.CTkButton(self.button_tile, text="Dodaj novu biljku", font=("TkDefaultFont", 12))
        self.add_button.grid(row=0, column=1, pady=20, padx=10, rowspan=2)  

        #self.add_button.plant_id = -1  
        #self.add_button.bind("<Button-1>", self.tile_clicked)
        self.add_button.bind("<Button-1>", lambda event, plant_id=-1: self.tile_clicked(event, plant_id))

            

    def tile_clicked(self, event, plant_id, delete=False):
        if delete:
            #print(f"Deleting plant {plant_id}")
            delete_plant(plant_id)
            self.mid_frame.grid_forget()
            self.mid_frame = PlantTiles(master=self)
            self.mid_frame.grid()
        elif plant_id == -1:
            self.mid_frame.grid_forget()
            self.mid_frame = PlantEditor(master=self)
            self.mid_frame.grid()
        else:
            #print(f"Plant {plant_id} clicked!")
            self.mid_frame.grid_forget()
            self.mid_frame = PlantDetails(master=self, plant_id=plant_id)
            self.mid_frame.grid()

    def sidebar_button_event(self):
        print("sidebar_button click")


# if __name__ == "__main__":
#     app = PlantTiles()
    
#     app.mainloop()


