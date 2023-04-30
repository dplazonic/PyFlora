import sqlite3



def create_connection():
    try:
        conn = sqlite3.connect("pyflora.db")
        return conn
    except sqlite3.Error as e:
        print(e)
        return None

def init_users_table():
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    last_name TEXT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                );
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()



def add_user(first_name, last_name, username, password):
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (first_name, last_name, username, password) VALUES (?, ?, ?, ?)",
                           (first_name, last_name, username, password))
            conn.commit()
            print("User added successfully.")
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

def get_user_id(username):
    conn= create_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            user_id = cursor.fetchone()
            if user_id is not None:
                return user_id[0]
            else:
                return None
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()


def update_user(user_id, first_name, last_name, username, password):
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE users
                SET first_name = ?, last_name = ?, username = ?, password = ?
                WHERE id = ?
            """, (first_name, last_name, username, password, user_id))
            conn.commit()
            print("User updated successfully.")
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()


def check_password(username, password):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        db_password = cursor.fetchone()
        
        if db_password is None:
            return False
        
        stored_password = db_password[0]

    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

    return stored_password == password


def check_user(username, password):
    conn = create_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT username FROM users WHERE password=?", (password,))
        db_username = cursor.fetchone()
        
        if db_username is None:
            return False
        
        stored_username = db_username[0]
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()
    return stored_username == username

init_users_table()

# add_user("davor", "plazonic", "admin", "admin")
# add_user("pero", "perić", "admin1", "admin1")

# get_user_id("admin")




print(check_password("admin", "admin"))
print(check_user("admin", "admin"))