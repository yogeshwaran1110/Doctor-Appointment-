from flask import Flask, render_template, request, redirect, url_for
from python_sql import get_connection,connection_closed

app = Flask(__name__, template_folder="html")


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        patient_name = request.form["patient_name"]
        age = request.form["age"]
        appointment_date = request.form["appointment_date"]
        appointment_time = request.form["appointment_time"]
        phone_number = request.form["phone_number"]
        token_number = request.form["token_number"]

        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        INSERT INTO appointment_list
        (patient_name, age, appointment_date, appointment_time, phone_number, token_number)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            patient_name,
            age,
            appointment_date,
            appointment_time,
            phone_number,
            token_number
        )

        cursor.execute(sql, values)
        connection.commit()

        connection_closed(cursor, connection)

        return redirect(url_for("appointments"))

    return render_template("index.html")


@app.route("/appointments")
def appointments():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    sql = "SELECT * FROM appointment_list"

    cursor.execute(sql)

    appointments = cursor.fetchall()

    connection_closed(cursor, connection)

    return render_template(
        "appointments.html",
        appointments=appointments
    )



@app.route("/edit/<int:patient_id>", methods=["GET", "POST"])
def edit_appointment(patient_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        patient_name = request.form["patient_name"]
        age = request.form["age"]
        appointment_date = request.form["appointment_date"]
        appointment_time = request.form["appointment_time"]
        phone_number = request.form["phone_number"]
        token_number = request.form["token_number"]

        sql = """
        UPDATE appointment_list
        SET patient_name = %s,
            age = %s,
            appointment_date = %s,
            appointment_time = %s,
            phone_number = %s,
            token_number = %s
        WHERE patient_id = %s
        """

        values = (
            patient_name,
            age,
            appointment_date,
            appointment_time,
            phone_number,
            token_number,
            patient_id
        )

        cursor.execute(sql, values)
        connection.commit()

        connection_closed(cursor, connection)

        return redirect(url_for("appointments"))

    sql = "SELECT * FROM appointment_list WHERE patient_id = %s"

    cursor.execute(sql, (patient_id,))

    patient = cursor.fetchone()

    connection_closed(cursor, connection)

    return render_template("update.html", patient=patient)



@app.route("/delete/<int:patient_id>")
def delete_appointment(patient_id):

    connection = get_connection()
    cursor = connection.cursor()

    sql = """
    DELETE FROM appointment_list
    WHERE patient_id = %s
    """

    cursor.execute(sql, (patient_id,))
    connection.commit()

    connection_closed(cursor, connection)

    return redirect(url_for("appointments"))



if __name__ == "__main__":
    app.run(debug=True)