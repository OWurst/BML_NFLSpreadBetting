import pymysql
import yaml
import mysql.connector
from mysql.connector import Error

database = 'nfl_data'

# load config.yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Connect to MySQL server


try:
    conn = pymysql.connect(
    host=config["database"]["host"],
    port=config["database"]["port"],
    user=config["database"]["user"],
    password=config["database"]["password"]
)
    cursor = conn.cursor()

    # Step 1: Read the SQL file
    try:
        with open('./database_builds/sql/database_builds.sql', 'r') as file:
            sql_commands = file.read()  # This reads the entire file content
    except FileNotFoundError:
        print("SQL file not found. Please make sure 'setup.sql' is in the correct path.")
        cursor.close()
        conn.close()
        exit()

    # Step 2: Execute the SQL commands
    try:
        # Drop and create the database
        cursor.execute("DROP DATABASE IF EXISTS nfl_data")  # Optionally drop it first
        cursor.execute("CREATE DATABASE IF NOT EXISTS nfl_data")  # Create the database
        cursor.execute("USE nfl_data")  # Switch to the created database

        # Split commands and execute one by one
        commands = sql_commands.split(';')  # Split commands by semicolon

        for command in commands:
            command = command.strip()  # Remove leading/trailing whitespace
            if command:  # Only execute if the command is not empty
                print(f"Executing command: {command}")  # Log the command being executed
                cursor.execute(command)

        conn.commit()  # Commit changes to the database
        print("Database and tables created successfully!")

    except Error as err:
        print(f"Error: {err}")
        conn.rollback()

finally:
    cursor.close()
    conn.close()