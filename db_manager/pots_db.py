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
                    id INTEGER PRIMARY KEY,
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
                SELECT pots.id, pots.material, pots.placement, pots.size, plants.id, plants.plant_name, plants.photo
                FROM pots
                LEFT JOIN plants ON pots.plant_id = plants.id;
            """)
            rows = cursor.fetchall()
            if rows is not None:  # Check if rows is not None before trying to enumerate
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


def get_pot_by_display_id(display_id):
    pots = get_pots()
    for pot in pots:
        if pot[0] == display_id:
            return pot

    return None

            

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


def remove_plant_from_pot(pot_id):
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            UPDATE pots 
            SET plant_id=NULL 
            WHERE id=?
            """, (pot_id,))
            conn.commit()
            print("plant removed from pot")
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()


def is_pots_table_empty() -> bool:
    """
    Checks if the 'pots' table in the database is empty.

    Returns:
        bool: True if the table is empty, False otherwise.
    """
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM pots")
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
    if is_pots_table_empty():
        generate_pots()



def generate_pots():
    add_pot("glina", "kuhinja", "srednja", None)


init_pots_table()
add_data_if_needed()