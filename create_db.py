import pymysql
import os

# Get database configuration from environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def create_database():
    try:
        # Connect to MySQL server without selecting a database
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"Database {DB_NAME} created successfully!")
            
            # Switch to the created database
            cursor.execute(f"USE {DB_NAME}")
            
            # Create tables here if needed
            # cursor.execute("""CREATE TABLE IF NOT EXISTS ...""")
            
        connection.commit()
        
    except Exception as e:
        print(f"Error creating database: {e}")
        
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    create_database() 