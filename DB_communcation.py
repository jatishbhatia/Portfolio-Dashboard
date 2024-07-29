import mysql.connector
from mysql.connector import Error


def establish_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="c0nygre",
            database="financial_portfolio"
        )
        if connection.is_connected():
            print("Connection established successfully.")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None


def fetch_assets(connection):
    if connection is None:
        print("Connection is not established.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM assets")
        results = cursor.fetchall()

        if results:
            for row in results:
                print(row)
        else:
            print("No data found.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()


def main():
    connection = establish_connection()
    fetch_assets(connection)

    # Close the connection after use
    if connection is not None and connection.is_connected():
        connection.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()