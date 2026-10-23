
import os
import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        ssl_disabled=False,
        connection_timeout=20
    )
    print("Connected to Aiven MySQL successfully")
    return connection


print("DB_HOST set:", bool(os.getenv("DB_HOST")))
print("DB_PASSWORD set:", bool(os.getenv("DB_PASSWORD")))


# Close connection
def connection_closed(cursor, connection):

    cursor.close()
    connection.close()



# ==================================================
# 1. CREATE TABLE
# ==================================================
if __name__ == "__main__":

    query = """
    CREATE TABLE IF NOT EXISTS appointment_list (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    token_number INT NOT NULL,
    UNIQUE (appointment_date, token_number)
    )
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query)

    connection_closed(cursor, connection)

    print('Table created successfully')


    # ==================================================
    # 2. INSERT
    # ==================================================

    connection = get_connection()
    cursor = connection.cursor()

    sql = """
    INSERT INTO appointment_list
    (patient_name, age, appointment_date, appointment_time, phone_number, token_number)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        'Bharath',
        23,
        '2026-09-22',
        '23:00:53',
        '6387687664',
        14
    )

    cursor.execute(sql, values)

    connection.commit()

    print('Patient inserted successfully')

    connection_closed(cursor, connection)


    # ==================================================
    # 3. SELECT - ALL DETAILS
    # ==================================================

    connection = get_connection()
    cursor = connection.cursor()

    select_query = """
    SELECT * FROM appointment_list
    """

    cursor.execute(select_query)

    all_details = cursor.fetchall()

    for patient in all_details:
        print(patient)

    connection_closed(cursor, connection)


    # ==================================================
    # 4. UPDATE
    # ==================================================

    connection = get_connection()
    cursor = connection.cursor()

    update_query = """
    UPDATE appointment_list
    SET phone_number = %s
    WHERE patient_id = %s
    """

    values = (
    '6379854153',
    1
    )

    cursor.execute(update_query, values)

    connection.commit()

    print('Patient updated successfully')

    connection_closed(cursor, connection)


    # ==================================================
    # 5. DELETE
    # ==================================================

    connection = get_connection()
    cursor = connection.cursor()

    delete_query = """
    DELETE FROM appointment_list
    WHERE patient_id = %s
    """

    values = (4,)

    cursor.execute(delete_query, values)

    connection.commit()

    print('Patient deleted successfully')

    connection_closed(cursor, connection)