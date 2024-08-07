from datetime import datetime

import mysql.connector
from mysql.connector import Error, ProgrammingError

# database_create_script = "../SQL_scripts/MVP_database.sql"
database_create_script = "Backend/SQL_scripts/MVP_database.sql"


def establish_connection():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("DROP DATABASE financial_portfolio;")
        connection.commit()
        cursor.close()
        close_connection(connection)
        print("Creating database")
        execute_sql_script(database_create_script)
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
    if connection is not None and connection.is_connected():
        connection.close()
        print("Connection closed.")


# CRUD operations for Category
def create_category(name, description):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO Category (name, description) VALUES (%s, %s)", (name, description))
        connection.commit()
        return {'message': 'Category created'}, 201
    except mysql.connector.Error as err:
        return {'error': str(err)}, 400
    finally:
        cursor.close()
        close_connection(connection)


def read_categories():
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Category")
        categories = cursor.fetchall()
        return categories
    except mysql.connector.Error as err:
        return {'error': str(err)}, 400
    finally:
        cursor.close()
        close_connection(connection)


def update_category(name, description):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE Category SET description = %s WHERE name = %s", (description, name))
        connection.commit()
        if cursor.rowcount > 0:
            return {'message': 'Category updated'}, 200
        else:
            return {'message': 'Category not found'}, 404
    except mysql.connector.Error as err:
        return {'error': str(err)}, 400
    finally:
        cursor.close()
        close_connection(connection)


def delete_category(name):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM Category WHERE name = %s", (name,))
        connection.commit()
        if cursor.rowcount > 0:
            return {'message': 'Category deleted'}, 200
        else:
            return {'message': 'Category not found'}, 404
    except mysql.connector.Error as err:
        return {'error': str(err)}, 400
    finally:
        cursor.close()
        close_connection(connection)


# CRUD operations for Asset
def create_asset(symbol, name, category_name, total_purchase_price, quantity):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO asset (symbol, name, category_name, total_purchase_price, quantity, created_at, updated_at) "
            "VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
            (symbol, name, category_name, total_purchase_price, quantity)
        )
        connection.commit()
        asset_id = cursor.lastrowid
        return asset_id, {'message': 'Asset created'}, 201
    except mysql.connector.Error as err:
        return 400, {'error': str(err)}, 400
    finally:
        cursor.close()
        close_connection(connection)


def read_assets():
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Asset")
        assets = cursor.fetchall()
        return assets
    except mysql.connector.Error as err:
        return {'error': str(err)}, 400
    finally:
        cursor.close()
        close_connection(connection)


# getting the symbol and the category from the database
# def get_asset_details(symbol):
#     connection = connect_to_db()
#     cursor = connection.cursor(dictionary=True)
#     try:
#         query = "SELECT name, category, purchase_price, quantity FROM Asset WHERE symbol = %s"
#         cursor.execute(query, (symbol,))
#         asset = cursor.fetchone()
#         if asset is None:
#             raise KeyError(f"Asset details not found for symbol {symbol}")
#         return asset
#     except mysql.connector.Error as err:
#         return {'error': str(err)}, 400
#     finally:
#         cursor.close()
#         close_connection(connection)


def update_asset(id, symbol, name, category_name, total_purchase_price, quantity):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE Asset SET symbol = %s, name = %s, category_name = %s, total_purchase_price = %s, quantity = %s, "
            "updated_at = CURRENT_TIMESTAMP WHERE id = %s",
            (symbol, name, category_name, total_purchase_price, quantity, id)
        )
        connection.commit()
        if cursor.rowcount > 0:
            return {'message': 'Asset updated'}, 200
        else:
            return {'message': 'Asset not found'}, 404
    except mysql.connector.Error as err:
        return {'error': str(err)}, 400
    finally:
        cursor.close()
        close_connection(connection)


def delete_asset(asset_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM asset WHERE id = %s", (asset_id,))
        connection.commit()
        if cursor.rowcount > 0:
            return {'message': 'Asset deleted'}, 200
        else:
            return {'message': 'Asset not found'}, 404
    except mysql.connector.Error as err:
        return {'error': str(err)}, 400
    finally:
        cursor.close()
        close_connection(connection)


# CRUD operations for Transaction
def create_transaction(asset_id, transaction_type, quantity, price, transaction_date):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        quantity = str(quantity)
        price = str(price)
        asset_id = str(asset_id)
        cursor.execute(
            "INSERT INTO transaction (asset_id, transaction_type, quantity, price, transaction_date) VALUES (%s, %s, "
            "%s, %s, %s)",
            (asset_id, transaction_type, quantity, price, transaction_date)
        )
        connection.commit()
        return {'message': 'Transaction created'}, 201
    except mysql.connector.Error as err:
        return {'error': str(err)}, 400
    finally:
        cursor.close()
        close_connection(connection)


def read_transactions():
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Transaction t LEFT JOIN asset a ON t.asset_id = a.id ORDER BY transaction_date DESC")
        transactions = cursor.fetchall()
        return transactions
    except mysql.connector.Error as err:
        return {'error': str(err)}, 400
    finally:
        cursor.close()
        close_connection(connection)


def update_transaction(id, asset_id, transaction_type, quantity, price, transaction_date):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE Transaction SET asset_id = %s, transaction_type = %s, quantity = %s, price = %s, transaction_date "
            "= %s WHERE id = %s",
            (asset_id, transaction_type, quantity, price, transaction_date, id)
        )
        connection.commit()
        if cursor.rowcount > 0:
            return {'message': 'Transaction updated'}, 200
        else:
            return {'message': 'Transaction not found'}, 404
    except mysql.connector.Error as err:
        return {'error': str(err)}, 400
    finally:
        cursor.close()
        close_connection(connection)


def delete_transaction(id):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM Transaction WHERE id = %s", (id,))
        connection.commit()
        if cursor.rowcount > 0:
            return {'message': 'Transaction deleted'}, 200
        else:
            return {'message': 'Transaction not found'}, 404
    except mysql.connector.Error as err:
        return {'error': str(err)}, 400
    finally:
        cursor.close()
        close_connection(connection)


def execute_sql_script(path: str):
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


def buy_stock(input_symbol, long_name, purchase_price, input_quantity):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:

        # Check if the asset already exists
        cursor.execute(
            "SELECT id, name, total_purchase_price, quantity FROM asset WHERE symbol = %s AND category_name = 'Stock'",
            (input_symbol,)
        )
        result = cursor.fetchone()

        if result:
            # Asset exists, update it
            asset_id, long_name, total_purchase_price, existing_quantity = result
            new_quantity = existing_quantity + input_quantity
            new_total_purchase_price = total_purchase_price + (purchase_price * input_quantity)
            update_result, status_code = update_asset(asset_id, input_symbol, long_name, "Stock",
                                         new_total_purchase_price, new_quantity)
            if 'error' in update_result:
                return update_result, status_code
        else:
            # Asset does not exist, create it
            asset_id, create_result, status_code = create_asset(input_symbol, long_name, 'Stock',
                                                                purchase_price * input_quantity, input_quantity)

            if status_code != 201:
                return create_result, status_code

        # Insert the transaction record
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        transaction_result, status_code = create_transaction(asset_id, 'buy', input_quantity, purchase_price, current_timestamp)
        if 'error' in transaction_result:
            return transaction_result, status_code

        return {'message': 'Stock purchased successfully'}, 201
    except mysql.connector.Error as err:
        connection.rollback()
        return {'error': str(err)}, 400
    finally:
        cursor.close()
        close_connection(connection)


def sell_stock(input_symbol, selling_price, input_quantity):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:

        # Check if the asset exists and retrieve details
        cursor.execute(
            "SELECT id, name, total_purchase_price, quantity FROM asset WHERE symbol = %s AND category_name = 'Stock'",
            (input_symbol,)
        )
        result = cursor.fetchone()

        if result:
            asset_id, name, total_purchase_price, existing_quantity = result

            if existing_quantity >= input_quantity:
                # Calculate new values and update asset
                new_quantity = existing_quantity - input_quantity

                # if new_quantity > 0:
                # Update Asset

                # avg_stock_price = total_purchase_price / existing_quantity
                new_total_purchase_price = total_purchase_price - (input_quantity * selling_price)
                update_result, status_code = update_asset(asset_id, input_symbol, name, 'Stock',
                                             new_total_purchase_price, new_quantity)
                if 'error' in update_result:
                    return update_result, status_code

                # Insert Transaction record
                current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                transaction_result = create_transaction(asset_id, 'sell', input_quantity, selling_price,
                                                        current_timestamp)

                if 'error' in transaction_result:
                    return transaction_result, status_code

                return {'message': 'Stock sold successfully'}, 201
            else:
                return {'message': 'Insufficient quantity'}, 400
        else:
            return {'message': 'Asset not found'}, 404
    except mysql.connector.Error as err:
        connection.rollback()
        return {'error': str(err)}, 400
    finally:
        cursor.close()
        close_connection(connection)


establish_connection()

# print(buy_stock('TLT', 'yo', 6, 5))
# print(read_assets())
# print("\n--------------------------\nTRANSACTIONS\n")
# print(read_transactions())
# print(sell_stock('TLT', 6, 5))
# print("\n--------------------------\nAFTER SELLING\n")
# print(read_assets())
# print("\n--------------------------\nTRANSACTIONS\n")
# print(read_transactions())
