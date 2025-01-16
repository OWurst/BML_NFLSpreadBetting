import pymysql
import yaml

try:
    # load config.yaml
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # Connect to MySQL server
    connection = pymysql.connect(
        host=config["database"]["host"],
        port=config["database"]["port"],
        user=config["database"]["user"],
        password=config["database"]["password"]
    )
    
    print("Connected to MySQL server")

    cursor = connection.cursor()

    # Create the database
    database_name = "my_new_database"
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    print(f"Database '{database_name}' created or already exists.")

    # Use the database
    cursor.execute(f"USE {database_name}")
    print(f"Using database: {database_name}")

    # Optional: Create a table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS example_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255)
        )
    """)
    print("Table 'example_table' created.")

except pymysql.MySQLError as e:
    print(f"Error: {e}")
finally:
    connection.close()
    print("MySQL connection closed.")