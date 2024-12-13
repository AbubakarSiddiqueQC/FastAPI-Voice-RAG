# Main imports
import sqlite3
from contextlib import contextmanager
import os, sys
# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the path to the parent directory
parent_dir = os.path.dirname(current_dir)
# Add the parent directory to the Python path
sys.path.append(parent_dir)
#imports functions or constants
from Constants import DB_NAME


#imports functions or constants
@contextmanager
def get_db_connection():
    """
    Context manager for managing SQLite database connections.
    Ensures proper resource cleanup.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        # Log the error (customize logging as needed)
        print(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def create_file_table():
    """
    Creates the 'file_uploaded' table if it doesn't exist.
    """
    with get_db_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS file_uploaded
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         file_name TEXT,
                         file_type TEXT,
                         file_path TEXT,
                         department TEXT,
                         uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

def insert_file(file_name, file_type, file_path, department):
    """
    Inserts a new file record into the database.
    """
    with get_db_connection() as conn:
        conn.execute('INSERT INTO file_uploaded (file_name, file_type, file_path, department) VALUES (?, ?, ?, ?)',
                     (file_name, file_type, file_path, department))
        conn.commit()

def delete_file(file_id):
    """
    Deletes a file record from the database by its ID.
    """
    with get_db_connection() as conn:
        conn.execute('DELETE FROM file_uploaded WHERE id = ?', (file_id,))
        conn.commit()
    return True

def get_all_files():
    """
    Fetches all files from the 'file_uploaded' table.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, file_name, uploaded_at FROM file_uploaded ORDER BY uploaded_at DESC')
        documents = cursor.fetchall()
    return [dict(doc) for doc in documents]

def get_all_file_dep(department):
    """
    Fetches all files from the 'file_uploaded' table by department.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, file_name, uploaded_at FROM file_uploaded WHERE department = ? ORDER BY uploaded_at DESC', 
                       (department,))
        documents = cursor.fetchall()
    return [dict(doc) for doc in documents]

# Ensure the table is created when the script runs
if __name__ == "__main__":
    print("Files table created")
    create_file_table()  