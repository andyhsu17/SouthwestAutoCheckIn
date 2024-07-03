import mysql.connector

class db:
    def __init__(self, db_name):
        # Replace these variables with your MySQL server details
        # self.password = 'your_password'
        self.db_name = db_name
        self.host = '127.0.0.1'  # or the server IP
        self.user = 'root'

        # Establish a connection to the MySQL server
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
        )

        # Create a cursor object
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
        # Select the database
        self.cursor.execute(f"USE {self.db_name}")

    def create_table(self):

        # Create a new table users
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            reservation_number VARCHAR(255) NOT NULL,
            check_in_time INT
        )
        """)

    def insert_data(self, data):
        """ Function to insert data into the database
        data (list): list of tuples containing first name, last name, reservation num, check in time
        """
        insert_query = """
        INSERT INTO users (first_name, last_name, reservation_number, check_in_time)
        VALUES (%s, %s, %s, %s)
        """
        if not isinstance(data, list) or not all(isinstance(item, tuple) for item in data):
            print('Malformed data input into db')
            return False

        self.cursor.executemany(insert_query, data)

        # Commit the transaction
        self.connection.commit()

        print("Data inserted into 'users' table")
        return True

    def delete_reservation(self, reservation_number):
        pass

    def get_all(self):
        # Query the data
        select_query = "SELECT * FROM users"
        self.cursor.execute(select_query)

        # Fetch all rows from the executed query
        rows = self.cursor.fetchall()
        return rows 

    def print_all(self):
        # Query the data
        select_query = "SELECT * FROM users"
        self.cursor.execute(select_query)

        # Fetch all rows from the executed query
        rows = self.cursor.fetchall()

        for row in rows:
            print(row)

    def delete_all(self):
        """ For testing only
        """
        # Retrieve the list of all tables
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()

        # Generate and execute truncate statements for each table
        for (table_name,) in tables:
            self.cursor.execute(f"TRUNCATE TABLE {table_name}")
            print(f"Truncated table {table_name}")
