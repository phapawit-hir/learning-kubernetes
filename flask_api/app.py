from flask import Flask, jsonify, request
import string
import random
import psycopg2
from psycopg2 import sql

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def generate_random_integer(start, end):
    return random.randint(start, end)

app = Flask(__name__)

@app.route('/')
def home():
    conn = None
    rows = []
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="db",
            port="5432"
        )
        print("Connected to the database.")

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM abc")
            rows = cur.fetchall()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if conn:
            conn.close()
            print("Database connection closed.")
    return str([x for x in rows])

@app.route('/data', methods=['GET'])
def get_data():
    conn = None
    rows = []
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="db",
            port="5432"
        )
        print("Connected to the database.")

        with conn.cursor() as cur:
            create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS abc (id SERIAL PRIMARY KEY, name VARCHAR(255), age INT);")
            cur.execute(create_table_query)
            conn.commit()
            insert_query = sql.SQL("INSERT INTO abc (name, age) VALUES (%s, %s)")
            cur.execute(insert_query, (generate_random_string(10), generate_random_integer(1,20)))
            conn.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if conn:
            conn.close()
            print("Database connection closed.")
    return "Inserting data was successful"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
