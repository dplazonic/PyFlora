import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import json
import os
from matplotlib.figure import Figure
from db_manager.pots_db import *

class PotSensor:
    def __init__(self, pot_id: int) -> None:
        """Initializes a PotSensor instance with a pot_id.

        Args:
            pot_id (int): The identifier of the pot.
        """
        self.pot_id = pot_id
        self.sensor_data = self.load_sensor_data()

    def generate_sensor_data(self) -> dict:
        """Generates sensor data with random values for different attributes.

        Returns:
            dict: A dictionary with the sensor data.
        """
        temperature = round(random.uniform(10, 35), 2)
        moisture = round(random.uniform(0, 100), 2)
        brightness = round(random.uniform(0, 1000), 2)
        ph = round(random.uniform(0, 14))
        salinity = round(random.uniform(0, 500), 2)

        sensor_data = {
            "pot_id": self.pot_id,
            "temperature": temperature,
            "moisture": moisture,
            "brightness": brightness,
            "ph": ph,
            "salinity": salinity,
        }

        return sensor_data
    
    def add_pot_sensor_data(self) -> dict:
        """Adds sensor data for a pot to a json file.

        Returns:
            dict: The sensor data added.
        """
        sensor_data = self.generate_sensor_data()

        with open('sensor_data.json', 'r') as json_file:
            all_pots_data = json.load(json_file)
        
        all_pots_data[str(self.pot_id)] = [sensor_data]

        with open('sensor_data.json', 'w') as json_file:
            json.dump(all_pots_data, json_file, indent=4)
            
        return sensor_data

    def load_sensor_data(self) -> dict:
        """Loads sensor data for a pot from a json file. If no data is found, new data is generated and added.

        Returns:
            dict: The sensor data loaded.
        """
        try:
            with open('sensor_data.json', 'r') as json_file:
                all_pots_data = json.load(json_file)
            
            if str(self.pot_id) in all_pots_data:
                sensor_data = all_pots_data[str(self.pot_id)][0]
                return sensor_data
            else:
                return self.add_pot_sensor_data()
        except FileNotFoundError:
            return self.add_pot_sensor_data()
        

    def temperature_status(self) -> str:
        """
        Checks the status of the temperature sensor data and returns a string indicating its status.

        :return: A string stating "hladnije" if the temperature is less than 15, "toplije" if the temperature is greater than 15, and "-" if the temperature data is not available.
        """
        temperature = self.sensor_data.get('temperature') if self.sensor_data else None
        if temperature is None:
            return "-"
        return "hladnije" if temperature < 15 else "toplije"

    def moisture_status(self) -> str:
        """
        Checks the status of the moisture sensor data and returns a string indicating its status.

        :return: A string stating "suho" if the moisture is less than 50, "vlažno" if the moisture is greater than 50, and "-" if the moisture data is not available.
        """
        moisture = self.sensor_data.get('moisture') if self.sensor_data else None
        if moisture is None:
            return "-"
        return "suho" if moisture < 50 else "vlažno"

    def light_status(self) -> str:
        """
        Checks the status of the light sensor data and returns a string indicating its status.

        :return: A string stating "tamno" if the brightness is less than 500, "svijetlo" if the brightness is greater than 500, and "-" if the brightness data is not available.
        """
        brightness = self.sensor_data.get('brightness') if self.sensor_data else None
        if brightness is None:
            return "-"
        return "tamno" if brightness < 500 else "svijetlo"

    def ph_status(self) -> str:
        """
        Checks the status of the pH sensor data and returns a string indicating its status.

        :return: A string stating "kiselo (<7)" if the pH level is less than 7, "lužnato (>7)" if the pH level is greater than 7, and "-" if the pH data is not available.
        """
        ph = int(self.sensor_data.get('ph')) if self.sensor_data else None
        if ph is None:
            return "-"
        return "kiselo (<7)" if ph < 7 else "lužnato (>7)"

    def salinity_status(self) -> str:
        """
        Checks the status of the salinity sensor data and returns a string indicating its status.

        :return: A string stating "niži" if the salinity is less than 150, "srednji" if the salinity is less than 300, "viši" if the salinity is greater than 300, and "-" if the salinity data is not available.
        """
        salinity = self.sensor_data.get('salinity') if self.sensor_data else None
        if salinity is None:
            return "-"
        if salinity < 150:
            return "niži"
        if salinity < 300:
            return "srednji"
        return "viši"
    

    
class SensorPlotter:
    def __init__(self, master, pot_id: int) -> None:
        """Initializes a SensorPlotter instance with a master and a pot_id.

        Args:
            pot_id (int): The identifier of the pot.
        """
        self.master = master
        self.pot_id = pot_id
        self.canvases = [None]*5 


    def plot_sensor_data(self):
        """Reads sensor data from a json file and plots it."""
        with open('sensor_data.json', 'r') as json_file:
            data = json.load(json_file)
        
        if str(self.pot_id) not in data: 
             return
        
        pot_data = data[str(self.pot_id)]

        if len(pot_data) < 2:
            print(f"nedovoljno podataka u {self.pot_id} za plotanje")
            return

        times = [datetime.strptime(i['time'], "%Y-%m-%d %H:%M") for i in pot_data]
        temperatures = [i['temperature'] for i in pot_data]
        moistures = [i['moisture'] for i in pot_data]
        brightness = [i['brightness'] for i in pot_data]
        ph = [i['ph'] for i in pot_data]
        salinity = [i['salinity'] for i in pot_data]

        self.plot_graph(times, temperatures, "Temperatura", 0, 0)
        self.plot_graph(times, moistures, "Vlaga", 1, 0)
        self.plot_graph(times, brightness, "Svjetlost", 2, 0)
        self.plot_graph(times, ph, "pH", 0, 1)
        self.plot_graph(times, salinity, "Salinitet", 1, 1)

    def plot_graph(self, times: list, y_values: list, title: str, column: int, row: int):
        """Plots a graph of y_values over time.

        Args:
            times (list): The list of time points.
            y_values (list): The list of corresponding y-values.
            title (str): The title of the graph.
            column (int): The column index for the graph.
            row (int): The row index for the graph.
        """
        fig = Figure(figsize=(6, 4), dpi=90)
        ax = fig.add_subplot(111)
        ax.plot(times, y_values)
        ax.set_title(title)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

        if self.canvases[column + row*3] is None:
            canvas = FigureCanvasTkAgg(fig, master=self.master) 
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(row=row, column=column, padx=2, pady=2)
            self.canvases[column + row*3] = canvas
        else:
            canvas = self.canvases[column + row*3]
            canvas.figure.clear()
            new_ax = canvas.figure.subplots(1, 1)
            new_ax.plot(times, y_values)
            new_ax.set_title(title)
            new_ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            canvas.draw()


def simulate_data() -> json:
    """Generates sensor data for all pots and saves it in a json file."""
    pots = get_pots()
    pot_ids=[]
    for pot in pots:
        if pot[5] is None:
            continue
        pot_ids.append(pot[0])
    
    all_pots_data = {}

    for pot_id in pot_ids:
        pot_sensor = PotSensor(pot_id)
        pot_data = []
        time = datetime.now()

        # Generate 72 records (for 24 hours, every 20 minutes)
        for _ in range(72):
            sensor_data = pot_sensor.generate_sensor_data()
            # Format time as a string in the format "HH:MM"
            sensor_data['time'] = time.strftime("%Y-%m-%d %H:%M")
            pot_data.append(sensor_data)
            # Go backwards for 20 minutes from now
            time -= timedelta(minutes=20)

        all_pots_data[pot_id] = pot_data

    with open('sensor_data.json', 'w') as json_file:
        json.dump(all_pots_data, json_file, indent=4)








