from flask import Flask
from api.customer_api import customer_blueprint
from database import get_db_connection

app = Flask(__name__)
app.register_blueprint(customer_blueprint)

def create_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100)
    );
    """)
    connection.commit()
    connection.close()

# Call this function when the app starts
create_table()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
