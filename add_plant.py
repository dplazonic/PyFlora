import tkinter as tk
from tkinter import filedialog
from PIL import Image
import customtkinter as ctk
from db_manager.plants_db import *
import os
from db_manager.plants_db import *


class AddPlant(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, *args, **kwargs) -> None:
        """
        Initializes the AddPlant frame.

        Args:
            master (ctk.CTk): custom tkinter parent widget.
        """
        super().__init__(master, *args, **kwargs)

        self.master = master
        
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "photos")
        self.image_icon_image = ctk.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        
        self.mid_frame = ctk.CTkFrame(self)
        self.mid_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nswe")

        self.form_frame = ctk.CTkFrame(self.mid_frame)
        self.form_frame.grid(padx=50, pady=50)
        self.form_frame_label = ctk.CTkLabel(self.mid_frame, text="UNOS NOVE BILJKE", font=ctk.CTkFont(size=20, weight="bold"))
        self.form_frame_label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        self.name_label = ctk.CTkLabel(self.form_frame, text="Naziv biljke:")
        self.name_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.name_entry = ctk.CTkEntry(self.form_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2, sticky="we")

        self.water_label = ctk.CTkLabel(self.form_frame, text="Frekvencija zalijevanja:")
        self.water_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.water_entry = ctk.CTkComboBox(self.form_frame, values=["dnevno", "tjedno", "mjesečno"])
        self.water_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=2, sticky="we")

        self.light_label = ctk.CTkLabel(self.form_frame, text="Izloženost svjetlosti:")
        self.light_label.grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.light_entry = ctk.CTkComboBox(self.form_frame, values=["svijetlo", "tamno"])
        self.light_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=2, sticky="we")

        self.temperature_label = ctk.CTkLabel(self.form_frame, text="Temperatura držanja:")
        self.temperature_label.grid(row=3, column=0, sticky="e", padx=10, pady=10)
        self.temperature_entry = ctk.CTkComboBox(self.form_frame, values=["toplije", "hladnije"])
        self.temperature_entry.grid(row=3, column=1, padx=10, pady=10, columnspan=2, sticky="we")

        self.ph_label = ctk.CTkLabel(self.form_frame, text="Odgovarajuća pH tla:")
        self.ph_label.grid(row=4, column=0, sticky="e", padx=10, pady=10)
        self.ph_entry = ctk.CTkComboBox(self.form_frame, values=["kiselo (<7)", "lužnato (>7)"])
        self.ph_entry.grid(row=4, column=1, padx=10, pady=10, columnspan=2, sticky="we")

        self.salinity_label = ctk.CTkLabel(self.form_frame, text="Odgovarajuća razina saliniteta tla:")
        self.salinity_label.grid(row=5, column=0, sticky="e", padx=10, pady=10)
        self.salinity_entry = ctk.CTkComboBox(self.form_frame, values=["viši", "niži", "srednji"])
        self.salinity_entry.grid(row=5, column=1, padx=10, pady=10, columnspan=2, sticky="we")
    
        self.supstrate_label = ctk.CTkLabel(self.form_frame, text="Dodavanje supstrata:")
        self.supstrate_label.grid(row=6, column=0, sticky="e", padx=10, pady=10)
        self.supstrate_entry = ctk.CTkComboBox(self.form_frame, values=["da", "ne"])
        self.supstrate_entry.grid(row=6, column=1, padx=10, pady=10, columnspan=2, sticky="we")

        self.image_label = ctk.CTkLabel(self.form_frame, text="Upload fotografije:")
        self.image_label.grid(row=7, column=0, sticky="e", padx=10, pady=10)
        self.img_upload_button = ctk.CTkButton(self.form_frame, text="Odaberi fotografiju", image=self.image_icon_image, compound="right", command=self.upload_image)
        self.img_upload_button.grid(row=7, column=1, padx=20, pady=10, columnspan=2, sticky="we")
        
        self.submit_button = ctk.CTkButton(self.form_frame, text="Pohrani", command=self.submit)
        self.submit_button.grid(row=8,column=1, pady=10, padx=10)
        self.submit_button = ctk.CTkButton(self.form_frame, text="Odustani", command=self.master.update_plant_tiles)
        self.submit_button.grid(row=8, column=2, pady=10, padx=10)

    def upload_image(self) -> str:
        """
        Opens a dialog box to upload an image. The path of the uploaded image is stored in the class attribute `filepath`.

        Returns:
            str: The path of the uploaded image.
        """
        self.filepath = tk.filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
        filename = os.path.basename(self.filepath)
        relative_filepath = os.path.join("photos", filename)
        self.filepath = relative_filepath
        self.img_upload_button.configure(fg_color="#dbdb35", text_color="black", text=f"{relative_filepath}")
        return(self.filepath)

    def submit(self) -> None:
        """
        Submits the entered plant details, adds them to the database, and updates the plant tiles.
        """
        plant_name = self.name_entry.get()
        photo = self.filepath
        watering = self.water_entry.get()
        brightness = self.light_entry.get()
        temperature = self.temperature_entry.get()
        ph = self.ph_entry.get()
        salinity = self.salinity_entry.get()
        supstrate = True if self.supstrate_entry.get() == "Da" else False

        add_plant(plant_name,photo,watering,brightness,temperature,ph,salinity,supstrate)

        self.mid_frame.grid_forget()
        self.master.update_plant_tiles()
        self.mid_frame.grid(row=1, column=0, columnspan=4, sticky="nswe", padx=20, pady=20)
