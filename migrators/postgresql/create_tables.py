import sqlalchemy
import os
from sqlalchemy import create_engine
from sqlalchemy.schema import DropTable, DropConstraint
from dotenv import load_dotenv
from models import Base



def connect_to_db():
  DATABASE_URI = generate_db_uri()
  print(DATABASE_URI)
  engine = create_engine(DATABASE_URI)
  print(engine)
  engine.execute("DROP TABLE IF EXISTS Courses CASCADE")
  engine.execute("DROP TABLE IF EXISTS Subjects CASCADE")
  Base.metadata.create_all(engine)
  return


def generate_db_uri():
  load_dotenv()
  username = os.getenv('USERNAME')
  password = os.getenv('PASSWORD')
  port = os.getenv('PORT')
  server_addr = os.getenv('SERVER_ADDR')
  db_name = os.getenv('DB_NAME')
  # use postgresql instead of postgres (deprecated)
  DATABASE_URI = "postgresql+psycopg2://" + username + ':' + password + '@' + server_addr + ':' + port + '/' + db_name
  return DATABASE_URI

if __name__ == "__main__":
  connect_to_db()