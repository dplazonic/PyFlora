import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import json
from matplotlib.figure import Figure
from db_manager.pots_db import *

class PotSensor:
    def __init__(self, pot_id):
        self.pot_id = pot_id
        self.sensor_data = self.generate_sensor_data()

    def generate_sensor_data(self):
        temperature = round(random.uniform(10, 35), 2)
        moisture = round(random.uniform(0, 100), 2)
        brightness = round(random.uniform(0, 1000), 2)

        sensor_data = {
            "pot_id": self.pot_id,
            "temperature": temperature,
            "moisture": moisture,
            "brightness": brightness
        }

        return sensor_data

    def temperature_status(self, temperature):
        temperature = self.sensor_data['temperature']

        if temperature < 15:
            temperature = "hladnije"
        else:
            temperature = "toplije"

        return temperature

    def moisture_status(self, moisture):
        moisture = self.sensor_data['moisture']

        if moisture < 50:
            moisture = "suho"
        else:
            moisture = "vlažno"
            
        return moisture

    def light_status(self, brightness):
        brightness = self.sensor_data['brightness']

        if brightness < 500:
            brightness = "tamno"
        else:
            brightness = "svijetlo"

        return brightness
    

    
class SensorPlotter:
    def __init__(self, master, pot_id):
        self.master = master
        self.pot_id = pot_id
        self.canvases = [None, None, None]

    def plot_sensor_data(self):
        with open('sensor_data.json', 'r') as json_file:
            data = json.load(json_file)
        
        pot_data = data[str(self.pot_id)]
        times = [datetime.strptime(i['time'], "%Y-%m-%d %H:%M") for i in pot_data]
        temperatures = [i['temperature'] for i in pot_data]
        moistures = [i['moisture'] for i in pot_data]
        brightness = [i['brightness'] for i in pot_data]

        self.plot_graph(times, temperatures, "Temperatura", 0)
        self.plot_graph(times, moistures, "Vlaga", 1)
        self.plot_graph(times, brightness, "Svjetlost", 2)

    def plot_graph(self, times, y_values, title, column):
        fig = Figure(figsize=(6, 4), dpi=90)
        ax = fig.add_subplot(111)
        ax.plot(times, y_values)
        ax.set_title(title)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

        if self.canvases[column] is None:
            canvas = FigureCanvasTkAgg(fig, master=self.master) 
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(row=1, column=column, padx=2, pady=2)
            self.canvases[column] = canvas
        else:
            canvas = self.canvases[column]
            canvas.figure.clear()
            new_ax = canvas.figure.subplots(1, 1)
            new_ax.plot(times, y_values)
            new_ax.set_title(title)
            new_ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            canvas.draw()


def simulate_data():
    pots = get_pots()
    pot_ids=[]
    for pot in pots:
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








