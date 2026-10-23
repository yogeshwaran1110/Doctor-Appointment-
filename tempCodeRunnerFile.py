import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'yokeshwaran12',
        database = 'doctor_appointment'
    )

    print('mysql connect successfully')

    return connection;


def connection_closed(cursor,connection):
    cursor.close()
    connection.close();

connection = get_connection();
cursor = connection.cursor();
update_query = """ update appointment_list 
                    set phone_number = '6379854153' 
                        where patient_id = %s """

values = (1,)
cursor.execute(update_query,values);
connection.commit();
print('update successfully')
connection_closed(cursor,connection);
