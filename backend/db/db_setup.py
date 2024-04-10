import mysql.connector
from db.connect import db_connection
import os  # Import the os module for file path operations


def check_database_initialized(cursor):
    # Check if the database is already initialized
    # This can be checking for a specific table's existence, for example
    try:
        cursor.execute("SELECT * FROM Users LIMIT 1;")
        # If the above command doesn't throw an error, the table (and hence the DB) exists
        return True
    except mysql.connector.Error:
        # If an error is thrown, the table doesn't exist, and likely the DB is not initialized
        return False

def db_init():
    
    try:
        # Connect to the MySQL database
            # Database connection parameters
        conn = db_connection()
        cursor = conn.cursor()
        if not check_database_initialized(cursor):  

            # Open and read the SQL file
           
            # Specify the absolute path to the SQL file
            sql_file_path = os.path.join(os.path.dirname(__file__), 'db_init.sql')

            with open(sql_file_path, 'r') as file:
                sql_commands = file.read().split(';')  # Split by ';' to separate commands

            # Create all the tables along with initial users
            for command in sql_commands:
                if command.strip():  # Checking if command is not empty
                    cursor.execute(command)

            conn.commit()
            print("Database initialized.")
        else:
            print("Database already initialized. Skipping seeding.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == '__main__':
    db_init()