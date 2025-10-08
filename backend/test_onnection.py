import psycopg2
from psycopg2 import sql, OperationalError

def test_connection():
    try:
        connection = psycopg2.connect(
            dbname = "weatherDB",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432"
        )
        print("connection successful")

         # Optional: test a query
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("PostgreSQL version:", record)

        cursor.close()
        connection.close()
        print("🔒 Connection closed successfully.")
    except OperationalError as e:
        print("connection failed", e)


if __name__ == "__main__":
    test_connection()

