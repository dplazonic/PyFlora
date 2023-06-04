import customtkinter as ctk
from db_manager.plants import *
from db_manager.pots_db import *


class AddPot(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, *args, **kwargs) -> None:
        """
        Initializes the AddPot frame.

        Args:
            master (ctk.CTk): custom tkinter parent widget.
        """
        super().__init__(master, *args, **kwargs)
        
        self.master = master
        
        self.mid_frame = ctk.CTkFrame(self)
        self.mid_frame.grid(padx=200, pady=200)

        self.form_frame = ctk.CTkFrame(self.mid_frame)
        self.form_frame.grid(padx=50, pady=100)
        self.form_frame_label = ctk.CTkLabel(self.mid_frame, text="DODAVANJE POSUDE", font=ctk.CTkFont(size=20, weight="bold"))
        self.form_frame_label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        self.material_label = ctk.CTkLabel(self.form_frame, text="Materijal posude:")
        self.material_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.material_entry = ctk.CTkComboBox(self.form_frame, values=["glina", "plastika", "keramika", "staklo",  ])
        self.material_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=2, sticky="we")

        self.position_label = ctk.CTkLabel(self.form_frame, text="Pozicija posude:")
        self.position_label.grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.position_entry = ctk.CTkComboBox(self.form_frame, values=["dnevni boravak", "soba", "balkon", "terasa", "hodnik", "kupaonica", "kuhinja", "terasa", "garaža"])
        self.position_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=2, sticky="we")

        self.size_label = ctk.CTkLabel(self.form_frame, text="Veličina posude:")
        self.size_label.grid(row=3, column=0, sticky="e", padx=10, pady=10)
        self.size_entry = ctk.CTkComboBox(self.form_frame, values=["mala", "srednja", "velika"])
        self.size_entry.grid(row=3, column=1, padx=10, pady=10, columnspan=2, sticky="we")
        
        self.submit_button = ctk.CTkButton(self.form_frame, text="Pohrani", command=self.submit)
        self.submit_button.grid(row=6,column=1, pady=10, padx=10)
        self.submit_button = ctk.CTkButton(self.form_frame, text="Odustani", command=self.master.update_pot_tiles)
        self.submit_button.grid(row=6, column=2, pady=10, padx=10)

    def submit(self) -> None:
        """
        Submits the entered pot details, adds them to the database, and updates the pot tiles.
        """
        material = self.material_entry.get()
        placement = self.position_entry.get()
        size = self.size_entry.get()

        add_pot(material, placement, size, plant_id=None)

        self.mid_frame.grid_forget()
        self.master.update_pot_tiles()
