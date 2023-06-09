import sqlite3


def create_connection():
    try:
        conn = sqlite3.connect("pyflora.db")
        return conn
    except sqlite3.Error as e:
        print(e)
        return None
    
def init_plants_table():
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS plants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plant_name TEXT UNIQUE,
                    photo TEXT,
                    watering TEXT,
                    brightness TEXT,
                    temperature TEXT,
                    ph TEXT,
                    salinity TEXT, 
                    supstrate BOOL
                );
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()



def add_plant(plant_name, photo, watering, brightness, temperature, ph, salinity, supstrate):
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        try: 
            cursor.execute("INSERT INTO plants (plant_name, photo, watering, brightness, temperature, ph, salinity, supstrate) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (plant_name, photo, watering, brightness, temperature, ph, salinity, supstrate))
            conn.commit()
            print("plant added successfully")
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()


def get_plant_id(plant_name):
    conn= create_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM plants WHERE plant_name = ?", (plant_name,))
            plant_id = cursor.fetchone()
            if plant_id is not None:
                return plant_id[0]
            else:
                return None
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

def update_plant(plant_id, watering, brightness, temperature, ph, salinity, supstrate):
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            UPDATE plants
            SET watering = ?, brightness = ?, temperature = ?, ph = ?, salinity = ?, supstrate = ?
            WHERE id = ?
            """, (watering, brightness, temperature, ph, salinity, supstrate, plant_id))
            conn.commit()
            print("Plants updated successfully.")
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

def get_plants():
    conn= create_connection()
    display_rows = []
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM plants")
            rows = cursor.fetchall()
            for display_id, row in enumerate (rows, start=1):
                
                display_row = (display_id,) + row
                display_rows.append(display_row)
            
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return display_rows


def get_plant_by_id(plant_id):
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM plants WHERE id = ?", (plant_id,))
            plant = cursor.fetchone()
            return plant
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()


def delete_plant(plant_id):
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM plants WHERE id=?;", (plant_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()


def is_plants_table_empty() -> bool:
    """
    Checks if the 'plants' table in the database is empty.

    Returns:
        bool: True if the table is empty, False otherwise.
    """
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM plants")
            count = cursor.fetchone()[0]
            return count == 0
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

def add_data_if_needed() -> None:
    """
    Adds test data to the 'plants' table if it is empty.
    """
    if is_plants_table_empty():
        add_plant_data()


def add_plant_data():
    add_plant("Orhideja", "photos\\orhideja.jpg", "tjedno", "tamno", "hladnije","lužnato (>7)", "niži", False)
    add_plant("Ruža", "photos\\ruza.jpg", "tjedno", "svijetlo", "hladnije","lužnato (>7)", "niži", False)
    add_plant("Blitva", "photos\\blitva.jpg", "tjedno", "tamno", "toplije","kiselo (<7)", "viši", True)
    add_plant("Rajčica", "photos\\rajcica.jpg", "tjedno", "svijetlo", "toplije","lužnato (>7)", "niži", True)
    add_plant("Tulipan", "photos\\tulipan.jpg", "dnevno", "svijetlo", "toplije","kiselo (<7)", "viši", False)
    add_plant("Kaktus", "photos\\kaktus.jpg", "mjesečno", "tamno", "hladnije","lužnato (>7)", "srednji", True)
    add_plant("Zamija", "photos\\zamija.jpg", "tjedno", "tamno", "hladnije","kiselo (<7)", "niži", False)
    add_plant("Bosiljak", "photos\\bosiljak.jpg", "tjedno", "svijetlo", "toplije","lužnato (>7)", "viši", True)
    add_plant("Fikus", "photos\\fikus.jpg", "tjedno", "tamno", "hladnije","lužnato (>7)", "niži", True)
    add_plant("Paprat", "photos\\paprat.jpg", "tjedno", "svijetlo", "toplije","kiselo (<7)", "srednji", False)

init_plants_table()
add_data_if_needed()