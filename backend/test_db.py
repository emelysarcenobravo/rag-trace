
from app.db.database import test_connection

if __name__ == "__main__":
    try:
        result = test_connection()

        print("Successfully connected to PostgreSQL!")
        print(result)

    except Exception as error:
        print("Database connection failed:")
        print(error)