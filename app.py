from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Replace with your actual MySQL database credentials
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sudhir@1682',
    'database': 'feedback',
}

def insert_data(name, subject, email, message):
    # Create a connection to MySQL
    conn = mysql.connector.connect(**db_config)

    # Check connection
    if not conn.is_connected():
        raise Exception("Could not connect to the database.")

    try:
        # Prepare and execute the SQL query to insert data into the table
        cursor = conn.cursor()
        sql = "INSERT INTO contact_form_data (name, subject, email, message) VALUES (%s, %s, %s, %s)"
        values = (name, subject, email, message)
        cursor.execute(sql, values)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        # Close the connection
        cursor.close()
        conn.close()

@app.route('/', methods=['GET', 'POST'])
def contact_form():
    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['Subject']
        email = request.form['_replyto']
        message = request.form['message']

        # Insert data into the database
        insert_data(name, subject, email, message)
        
        return redirect(url_for('thank_you'))

    return render_template('index.html')

@app.route('/thank_you')
def thank_you():
    return "Thank you! Your message has been sent."

if __name__ == '__main__':
    app.run(debug=True)
