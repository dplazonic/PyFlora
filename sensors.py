import random

class PotSensor:
    def __init__(self, pot_id):
        self.pot_id = pot_id

    def generate_sensor_data(self):
        temperature = round(random.uniform(10, 35), 2)
        moisture = round(random.uniform(0, 100), 2)
        light = round(random.uniform(0, 1000), 2)

        sensor_data = {
            "pot_id": self.pot_id,
            "temperature": temperature,
            "moisture": moisture,
            "light": light
        }

        return sensor_data
    
    def temperature_status(self, temp):
        sensor_data = self.generate_sensor_data()
        temperature = sensor_data['temperature']

        if temperature < 15:
            temperature = "hladnije"
        else:
            temperature = "toplije"

        return temperature
    
    def moisture_status(self, moist):
        sensor_data = self.generate_sensor_data()
        moisture = sensor_data['moisture']

        if moisture < 50:
            moisture = "suho"
        else:
            moisture = "vlažno"
            
        return moisture
    
    def light_status(self, light):
        sensor_data = self.generate_sensor_data()
        light = sensor_data['light']

        if light < 500:
            light = "tamno"
        else:
            light = "svijetlo"

        return light