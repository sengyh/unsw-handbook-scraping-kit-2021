import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os

try:
  connection = psycopg2.connect(user=os.getenv('USERNAME'), database=os.getenv('DB_NAME'))
  cursor = connection.cursor()
  print("PostgreSQL server information")
  print(connection.get_dsn_parameters(), "\n")
  # Executing a SQL query
  cursor.execute("SELECT version();")
  # Fetch result
  record = cursor.fetchone()
  print("You are connected to - ", record, "\n")
except (Exception, Error) as error:
  print("Error while connecting to PostgreSQL", error)
finally:
  if connection:
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")