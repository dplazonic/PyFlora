
from db_manager.pots_db import *
from db_manager.plants import *

def get_pots_with_plant_requirements():
    pots = get_pots()
    pots_with_req = []

    for pot in pots:
        display_id, pot_id, material, placement, size, plant_id, plant_name = pot
        plant = get_plant_by_id(plant_id)
        if plant:
            plant_id, plant_name, photo, watering, brightness, temperature, supstrate = plant
            pot_with_req = (pot_id, material, placement, size, plant_name, watering, brightness, temperature, supstrate)
            pots_with_req.append(pot_with_req)
        else:
            pot_with_no_plant = (pot_id, material, placement, size, None, None, None, None, None)
            pots_with_req.append(pot_with_no_plant)

    return pots_with_req 



pots_with_req = get_pots_with_plant_requirements()
pot_id =1
print(pots_with_req[pot_id])