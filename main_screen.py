import customtkinter as ctk
from time import strftime
from user_editor import *
from db_manager.plants_db import *
from plant_sceen import PlantTiles
from add_plant import AddPlant
from plant_details import PlantDetails
from pots_screen import PotsTiles
from add_plant_to_pot import AddPlantToPot
from add_pot import AddPot
from pot_details import PotDetails
from login import LoginScreen
from user_editor import UserEditScreen
from sensors import simulate_data



ctk.set_appearance_mode("light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ctk.CTk):
    """
    Represents the main application window.
    """

    def __init__(self) -> None:
        """Initializes a new instance of the App class.

        The application window is configured, including the creation and configuration of widgets for the interface.
        """
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
        self.topbar_button_3 = ctk.CTkButton(self.top_frame, text= "Moj Profil", command=self.edit_user_display)
        self.topbar_button_3.grid(row=1, column=3, padx=20, pady=10)
        self.topbar_button_4 = ctk.CTkButton(self.top_frame, text= "Logout", command=self.login_display)
        self.topbar_button_4.grid(row=0, column=3, padx=20, pady=10)
        self.sync_button = ctk.CTkButton(self.top_frame, text= "SYNC", command=self.sync_button_event)
        self.sync_button.grid(row = 1, column = 2, sticky="ne", padx=20, pady=10)
        
        ### ---- middle frame ----- ###

        self.login_display()

        ### ---- bottom frame ----- ###
        self.bottom_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.bottom_frame.grid(row=2, column=0, columnspan=4, sticky="nsew")
        self.bottom_frame.grid_columnconfigure(2, weight=1)
        self.logo_label = ctk.CTkLabel(self.bottom_frame, text="v1.0", font=ctk.CTkFont(size=10, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.time_label = ctk.CTkLabel(self.bottom_frame, font=ctk.CTkFont(size=10, weight="bold"))
        self.time_label.grid(row=0, column=1, padx=20, pady=(20, 10))

    def login_display(self) -> None:
        """
        Display the login screen.
        """
        self.mid_frame = LoginScreen(master=self)
        self.mid_frame.grid(row=0, column=0, columnspan=3, sticky="nsew", rowspan=2)

    def edit_user_display(self) -> None:
        """
        Display the user editor screen.
        """
        self.mid_frame = UserEditScreen(master=self)
        self.mid_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)



    def time(self) -> None:
        """
        Display current time.
        """
        time_string = strftime('%H:%M:%S %p')
        self.time_label.configure(text = time_string)
        self.time_label.after(1000, self.time)  

    def plant_button_event(self) -> None:
        """
        Display the plant tiles screen.
        """
        if self.mid_frame is not None:
            self.mid_frame.grid_forget()

        self.mid_frame = PlantTiles(master=self)
        self.mid_frame.grid(row=1, column=0, columnspan=4, sticky="nswe", padx=10, pady=10)

    def pots_button_event(self) -> None:
        """
        Display the pots tiles screen.
        """
        if self.mid_frame is not None:
            self.mid_frame.grid_forget()

        self.mid_frame = PotsTiles(master=self)
        self.mid_frame.grid(row=1, column=0, columnspan=4, sticky="nswe", padx=10, pady=10) 
    
     ##----------PLANT TILES ---------##

    def update_plant_tiles(self) -> None:
        """
        Update and display the plant tiles screen.
        """
        self.mid_frame.grid_forget()
        self.mid_frame = PlantTiles(self)
        self.mid_frame.grid(row=1, column=0, columnspan=4, sticky="nswe", padx=10, pady=10)

    def show_add_plant(self) -> None:
        """
        Display the add plant screen.
        """
        self.mid_frame.grid_forget()
        self.mid_frame = AddPlant(self)
        self.mid_frame.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
        self.mid_frame.grid_columnconfigure((1,2), weight=1)

    def show_plant_details(self, plant_id: str) -> None:
        """
        Display the plant details screen for a specific plant.

        Args:
            plant_id (str): The id of the plant.

        """
        self.mid_frame.grid_forget()
        self.mid_frame = PlantDetails(self, plant_id=plant_id)
        self.mid_frame.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
        self.mid_frame.grid_columnconfigure((1,2), weight=1)

        ##----------POT TILES ---------##

    def update_pot_tiles(self) -> None:
        """       
        Display the add pot screen.

        """
        self.mid_frame.grid_forget()
        self.mid_frame = PotsTiles(master=self)
        self.mid_frame.grid(row=1, column=0, columnspan=4, sticky="nswe", padx=10, pady=10)

    def show_add_pot(self) -> None:
        """
        Display the add pot screen.
        """

        self.mid_frame.grid_forget()
        self.mid_frame = AddPot(self)
        self.mid_frame.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
        self.mid_frame.grid_columnconfigure((1,2), weight=1)

    def show_pot_details(self, pot_id: str) -> None:
        """
        Display the pot details screen for a specific pot.

        Args:
            pot_id (str): The id of the pot.

        """
        self.mid_frame.grid_forget()
        self.mid_frame = PotDetails(master=self, pot_id=pot_id)
        self.mid_frame.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
        self.mid_frame.grid_columnconfigure((1,2), weight=1)

    def add_plant_to_pot(self, display_pot_id: str) -> None:
        """
        Display the add plant to pot screen.

        Args:
            display_pot_id (str): The id of the pot to display.
        """
        self.mid_frame.grid_forget()
        self.mid_frame = AddPlantToPot(master=self, display_pot_id=display_pot_id)
        self.mid_frame.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
        self.mid_frame.grid_columnconfigure((1,2), weight=1)

    def sync_button_event(self) -> None:
        """
        On sync button click sensor data is simulated and written in json.
        Button changes color after 10s to yellow which suggests user to use it again to get new fresh data.
        """
        simulate_data()
        self.sync_button.configure(fg_color=["#2CC985", "#2FA572"], text_color=["gray98", "#DCE4EE"])
        self.after(10000, self.change_button_color)

    def change_button_color(self):
        self.sync_button.configure(fg_color="#dbdb35", text_color="black")



if __name__ == "__main__":
    app = App()
    app.time()
    app.mainloop()


















