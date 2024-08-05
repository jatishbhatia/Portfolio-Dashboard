import mysql.connector
from mysql.connector import Error, ProgrammingError

database_create_script = "../../SQL_scripts/MVP_database.sql"


def establish_connection():
    """
    Establishes a connection to the MySQL database and returns the connection object.

    Returns:
        connection (mysql.connector.connection_cext.CMySQLConnection): MySQL connection object
    """
    try:
        connect_to_db()
    except ProgrammingError as e:
        if e.errno == 1049:
            print("Creating database")
            execute_sql_script(database_create_script)
            connect_to_db()
        else:
            print(f"Error: {e}")
            return None
    except Error as e:
        print(f"Error: {e}")
        return None


def connect_to_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="c0nygre",
        database="financial_portfolio"
    )
    if connection.is_connected():
        print("Connection established successfully.")
        return connection

def close_connection(connection):
    """
    Closes the database connection if it's open.

    Args:
        connection (mysql.connector.connection_cext.CMySQLConnection): MySQL connection object
    """
    if connection is not None and connection.is_connected():
        connection.close()
        print("Connection closed.")

### Asset Operations ###


def create_asset(asset_name, purchase_date, purchase_price, quantity):
    """
    Creates a new asset in the database.

    Args:
        asset_name (str): Name of the asset
        purchase_date (str): Date of purchase (YYYY-MM-DD)
        purchase_price (float): Purchase price of the asset
        quantity (float): Quantity of the asset
    """
    connection = establish_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        sql = """
        INSERT INTO Assets (asset_name, purchase_date, purchase_price, quantity)
        VALUES (%s, %s, %s, %s)
        """
        values = (asset_name, purchase_date, purchase_price, quantity)
        cursor.execute(sql, values)
        connection.commit()
        print("Asset created successfully.")
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)


def fetch_assets():
    """
    Fetches all assets from the database and returns them as a list of dictionaries.

    Returns:
        list: List of assets
    """
    connection = establish_connection()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT a.asset_name, c.category_name AS asset_category, a.purchase_price, a.quantity, "
                       "(a.purchase_price * a.quantity) AS total_value FROM  Assets  JOIN  Asset_Category ac ON "
                       "a.asset_id = ac.asset_id JOIN  Categories c ON ac.category_id = c.category_id; ")
        results = cursor.fetchall()

        assets = [
            {
                "asset_id": asset[0],
                "asset_name": asset[1],
                "asset_category": asset[2],
                "purchase_price": float(asset[3]),
                "total_value": asset[4],
                "quantity": float(asset[5])
            }
            for asset in results
        ]

        return assets

    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        close_connection(connection)


def update_asset(asset_id, asset_name=None, purchase_date=None, purchase_price=None, quantity=None):
    """
    Updates an existing asset in the database.

    Args:
        asset_id (int): ID of the asset to update
        asset_name (str, optional): New name of the asset
        purchase_date (str, optional): New purchase date (YYYY-MM-DD)
        purchase_price (float, optional): New purchase price
        quantity (float, optional): New quantity
    """
    connection = establish_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        fields = []
        values = []

        if asset_name is not None:
            fields.append("asset_name = %s")
            values.append(asset_name)
        if purchase_date is not None:
            fields.append("purchase_date = %s")
            values.append(purchase_date)
        if purchase_price is not None:
            fields.append("purchase_price = %s")
            values.append(purchase_price)
        if quantity is not None:
            fields.append("quantity = %s")
            values.append(quantity)

        values.append(asset_id)

        sql = f"UPDATE Assets SET {', '.join(fields)} WHERE asset_id = %s"
        cursor.execute(sql, tuple(values))
        connection.commit()
        print("Asset updated successfully.")
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)


def delete_asset(asset_id):
    """
    Deletes an asset from the database.

    Args:
        asset_id (int): ID of the asset to delete
    """
    connection = establish_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        sql = "DELETE FROM Assets WHERE asset_id = %s"
        cursor.execute(sql, (asset_id,))
        connection.commit()
        print("Asset deleted successfully.")
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)

### Category Operations ###


def create_category(category_name, category_description):
    """
    Creates a new category in the database.

    Args:
        category_name (str): Name of the category
        category_description (str): Description of the category
    """
    connection = establish_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        sql = """
        INSERT INTO Categories (category_name, category_description)
        VALUES (%s, %s)
        """
        values = (category_name, category_description)
        cursor.execute(sql, values)
        connection.commit()
        print("Category created successfully.")
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)


def fetch_categories():
    """
    Fetches all categories from the database and returns them as a list of dictionaries.

    Returns:
        list: List of categories
    """
    connection = establish_connection()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Categories")
        results = cursor.fetchall()

        categories = [
            {
                "category_id": category[0],
                "category_name": category[1],
                "category_description": category[2]
            }
            for category in results
        ]

        return categories

    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        close_connection(connection)


def update_category(category_id, category_name=None, category_description=None):
    """
    Updates an existing category in the database.

    Args:
        category_id (int): ID of the category to update
        category_name (str, optional): New name of the category
        category_description (str, optional): New description of the category
    """
    connection = establish_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        fields = []
        values = []

        if category_name is not None:
            fields.append("category_name = %s")
            values.append(category_name)
        if category_description is not None:
            fields.append("category_description = %s")
            values.append(category_description)

        values.append(category_id)

        sql = f"UPDATE Categories SET {', '.join(fields)} WHERE category_id = %s"
        cursor.execute(sql, tuple(values))
        connection.commit()
        print("Category updated successfully.")
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)


def delete_category(category_id):
    """
    Deletes a category from the database.

    Args:
        category_id (int): ID of the category to delete
    """
    connection = establish_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        sql = "DELETE FROM Categories WHERE category_id = %s"
        cursor.execute(sql, (category_id,))
        connection.commit()
        print("Category deleted successfully.")
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)

### Asset_Category Operations ###


def create_asset_category(asset_id, category_id):
    """
    Assigns a category to an asset in the database.

    Args:
        asset_id (int): ID of the asset
        category_id (int): ID of the category
    """
    connection = establish_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        sql = """
        INSERT INTO Asset_Category (asset_id, category_id)
        VALUES (%s, %s)
        """
        values = (asset_id, category_id)
        cursor.execute(sql, values)
        connection.commit()
        print("Asset-Category mapping created successfully.")
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)


def fetch_asset_categories():
    """
    Fetches all asset-category mappings from the database and returns them as a list of dictionaries.

    Returns:
        list: List of asset-category mappings
    """
    connection = establish_connection()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Asset_Category")
        results = cursor.fetchall()

        asset_categories = [
            {
                "asset_id": mapping[0],
                "category_id": mapping[1]
            }
            for mapping in results
        ]

        return asset_categories

    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        close_connection(connection)


def delete_asset_category(asset_id, category_id):
    """
    Deletes an asset-category mapping from the database.

    Args:
        asset_id (int): ID of the asset
        category_id (int): ID of the category
    """
    connection = establish_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        sql = "DELETE FROM Asset_Category WHERE asset_id = %s AND category_id = %s"
        cursor.execute(sql, (asset_id, category_id))
        connection.commit()
        print("Asset-Category mapping deleted successfully.")
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)


def execute_sql_script(path:str):

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="c0nygre"
        )
        cursor = connection.cursor(buffered=True)

        with open(path) as file:
            script = file.read()

        for sql_statement in script.split(';'):
            sql_statement = sql_statement.strip()
            cursor.execute(sql_statement)

        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Database creation failed: {e}")


establish_connection()
