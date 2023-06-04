import sqlite3

def create_connection():
    """
    Creates a connection to the SQLite database.

    Returns:
        The connection object or None if an error occurred.
    """
    try:
        conn = sqlite3.connect("pyflora.db")
        return conn
    except sqlite3.Error as e:
        print(e)
        return None

def init_users_table() -> None:
    """
    Initializes the 'users' table in the database. If the table already exists, this function does nothing.
    """
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



def add_user(first_name: str, last_name: str, username: str, password: str) -> None:
    """
    Adds a new user to the 'users' table.

    Args:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        username (str): The username of the user.
        password (str): The password of the user.
    """
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

def get_user_id(username: str) -> int:
    """
    Retrieves the ID of a user by their username.

    Args:
        username (str): The username of the user.

    Returns:
        The ID of the user or None if the user does not exist.
    """
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


def update_user(user_id: int, first_name: str, last_name: str, username: str, password: str) -> None:
    """
    Updates the details of a user.

    Args:
        user_id (int): The ID of the user to update.
        first_name (str): The new first name of the user.
        last_name (str): The new last name of the user.
        username (str): The new username of the user.
        password (str): The new password of the user.
    """
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


def check_password(username: str, password: str) -> bool:
    """
    Checks if a password matches the stored password for a given username.

    Args:
        username (str): The username to check.
        password (str): The password to check.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    try:
        conn = sqlite3.connect('pyflora.db')
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        db_password = cursor.fetchone()
        if db_password is None:
            return False
        stored_password = db_password[0]
    except sqlite3.Error as e:
        print(f"An error occurred while checking password: {e}")
        return False
    finally:
        conn.close()
    return stored_password == password


def check_user(username: str, password: str) -> bool:
    """
    Checks if a username matches the stored username for a given password.

    Args:
        username (str): The username to check.
        password (str): The password to check.

    Returns:
        bool: True if the username matches, False otherwise.
    """
    try:
        conn = sqlite3.connect('pyflora.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE password=?", (password,))
        db_user = cursor.fetchone()
        if db_user is None:
            return False
        stored_user = db_user[0]
    except sqlite3.Error as e:
        print(f"An error occurred while checking password: {e}")
        return False

    finally:
        conn.close()
    return stored_user == username

init_users_table()

add_user("davor", "plazonic", "admin", "admin")

