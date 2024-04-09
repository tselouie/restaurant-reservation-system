import mysql.connector
from mysql.connector import Error
from db.connect import db_connection

# ******** TABLE FUNCTIONS ********
def get_tables():
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Tables")
        records = cursor.fetchall()
        print(records)
        cursor.close()
        conn.close()
        return records, None
    except Error as e:
        print(e)
        return None, str(e)
def get_available_tables(capacity, date,time):
    try:
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)
        date_time = date + ' ' + time
        print('date_time',date_time)
        print('capacity',capacity)
        query ="""
            SELECT t.*
            FROM Tables AS t
            LEFT JOIN Reservations AS r ON t.TableID = r.TableID
                AND r.ReservationDateTime = %s
            WHERE r.ReservationID IS NULL 
            AND t.Capacity = %s 
            AND t.TableID NOT IN (
        SELECT TableID 
        FROM Reservations 
        WHERE ReservationDateTime BETWEEN DATE_ADD(%s, INTERVAL -2 HOUR) 
        AND DATE_ADD(%s, INTERVAL 2 HOUR)
    );
        """
        cursor.execute(query,(date_time, capacity,date_time,date_time))
        records = cursor.fetchall()
        print(query)
        print('records')
        print(records)
        cursor.close()
        conn.close()
        return records, None
    except Error as e:
        print(e)
        return None, str(e)

def insert_table(table_number, capacity):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO Tables (TableNumber, Capacity) VALUES (%s, %s)"
        cursor.execute(query, (table_number, capacity))
        conn.commit()
        cursor.close()
        conn.close()
        return cursor.lastrowid, None  # Return the last inserted ID
    except Error as e:
        print(e)
        return None, str(e)
        
def get_table_by_id(table_id):
    try:
        print('get_table_by_id',table_id)
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Tables WHERE TableID = %s LIMIT 1", (table_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row, None
    except Error as e:
        print(e)
        return None, str(e)

def update_table_by_id(table_id, table_number, capacity):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        query = "UPDATE Tables SET TableNumber = %s, Capacity = %s WHERE TableID = %s"
        cursor.execute(query, (table_number, capacity, table_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Error as e:
        print(e)
        return False, str(e)

def delete_table_by_id(table_id):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM Tables WHERE TableID = %s"
        cursor.execute(query, (table_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Error as e:
        print(e)
        return False, str(e)

# ******RESERVATION FUNCTIONS ********
def get_reservations():
    try:
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Reservations")
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return records, None
    except Error as e:
        return None, str(e)

def insert_reservation(customer_id, table_id, reservation_datetime, number_of_guests):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO Reservations (CustomerID, TableID, ReservationDateTime, NumberOfGuests) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (customer_id, table_id, reservation_datetime, number_of_guests))
        conn.commit()
        cursor.close()
        conn.close()
        return cursor.lastrowid, None  # Return the last inserted ID
    except Error as e:
        print(e)
        return None, str(e)
        
def get_reservation_by_id(reservation_id):
    try:
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Reservations WHERE ReservationID = %s LIMIT 1", (reservation_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row, None
    except Error as e:
        print(e)
        return None, str(e)

def update_reservation_by_id(reservation_id, reservation_datetime, number_of_guests):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        query = "UPDATE Reservations SET ReservationDateTime = %s, NumberOfGuests = %s WHERE ReservationID = %s"
        cursor.execute(query, (reservation_datetime, number_of_guests,reservation_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Error as e:
        print(e)
        return False, str(e)

def update_reservation_status(reservation_id, status):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        query = "UPDATE Reservations SET Status = %s WHERE ReservationID = %s"
        cursor.execute(query, (status,reservation_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Error as e:
        print(e)
        return False, str(e)

def delete_reservation_by_id(reservation_id):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM Reservations WHERE ReservationID = %s"
        cursor.execute(query, (reservation_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Error as e:
        print(e)
        return False, str(e)

# ******CUSTOMER FUNCTIONS ********
def get_customers():
    try:
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Customers")
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return records, None
    except Error as e:
        print(e)
        return None, str(e)

def insert_customer(name, email, phone):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO Customers (Name, Email, Phone) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, phone))
        conn.commit()
       
        customer_id = cursor.lastrowid # Return the last inserted ID
    except Error as e:
        print(e)
        if 'duplicate' in str(e).lower():
            #if the phone number already exists, return the existing customer id
            cursor.execute("SELECT CustomerID FROM Customers WHERE Phone = %s", (phone,))
            existing_customer = cursor.fetchone()
            customer_id = existing_customer[0] if existing_customer else None
    finally:
        cursor.close()
        conn.close()
    return customer_id, None
        
def get_customer_by_id(customer_id):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Customers WHERE CustomerID = %s LIMIT 1", (customer_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row, None
    except Error as e:
        print(e)
        return None, str(e)

def update_customer_by_id(customer_id, name, email, phone):
    print('in update customer by id')
    try:
        conn = db_connection()
        cursor = conn.cursor()
        query = "UPDATE Customers SET Name = %s, Email = %s, Phone = %s WHERE CustomerID = %s"
        cursor.execute(query, (name, email, phone, customer_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Error as e:
        print(e)
        return False, str(e)

def delete_customer_by_id(customer_id):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM Customers WHERE CustomerID = %s"
        cursor.execute(query, (customer_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Error as e:
        print(e)
        return False, str(e)
