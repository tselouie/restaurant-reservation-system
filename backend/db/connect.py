from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()  # take environment variables from .env.

# function to connect to database

def db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DATABASE_URL"),
        user=os.environ.get("DATABASE_USER"),
        database=os.environ.get("DATABASE_NAME"),
        password=os.environ.get("DATABASE_PASSWORD"))