import sqlite3

def create_connection():
    try:
        conn = sqlite3.connect("pyflora.db")
        return conn
    except sqlite3.Error as e:
        print(e)
        return None
    
def init_pots_table():
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    material TEXT,
                    placement TEXT,
                    size INTEGER,
                    plant_id INTEGER,
                    FOREIGN KEY (plant_id) REFERENCES plants(id)
                );
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()


def add_pot(material, placement, size, plant_id=None):
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        try: 
            cursor.execute("INSERT INTO pots (material, placement, size, plant_id) VALUES (?, ?, ?, ?)",
                           (material, placement, size, plant_id))
            conn.commit()
            print("pot added successfully")
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()


def get_pots():
    conn = create_connection()
    display_rows = []
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT pots.id, pots.material, pots.placement, pots.size, plants.id, plants.plant_name
                FROM pots
                LEFT JOIN plants ON pots.plant_id = plants.id;
            """)
            rows = cursor.fetchall()
            for display_id, row in enumerate(rows, start=1):
                display_row = (display_id,) + row
                display_rows.append(display_row)
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return display_rows



def get_pot_by_id(pot_id):
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM pots WHERE id = ?", (pot_id,))
            plant = cursor.fetchone()
            return plant
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

def update_pot_with_plant(pot_id, plant_id):
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            UPDATE pots 
            SET plant_id=? 
            WHERE id=?
            """, (plant_id, pot_id))
            conn.commit()
            print("pot updated")
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close
                          

def delete_pot(pot_id):
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM pots WHERE id=?;", (pot_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()






init_pots_table()

def generate_pots():
    add_pot("glina", "kuhinja", "srednja", None)
    add_pot("plastika", "hodnik", "srednja", None)
    add_pot("keramika", "dnevni boravak", "srednja", None)
    add_pot("glina", "terasa", "velika", None)

#generate_pots()

#update_pot_with_plant(1, 4)
#print(get_pots())