import sqlalchemy
import os
from sqlalchemy import create_engine
from sqlalchemy.schema import DropTable, DropConstraint
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.sql.expression import insert
from dotenv import load_dotenv
from schema import Base
from convert_json_to_sql import insert_courses, insert_specialisations, insert_fac_sch, insert_subjects



def construct_db():
  engine = initialise_db()
  Session = sessionmaker(bind=engine)
  #insert_fac_sch(Session)
  #insert_subjects(Session)
  return;


def initialise_db():
  DATABASE_URI = generate_db_uri()
  engine = create_engine(DATABASE_URI)
  #wipe_db(engine)
  Base.metadata.create_all(engine)
  return engine

def wipe_db(engine):
  tables = ['courses', 'subjects', 'schools', 'faculties', 'faculty_to_school', 
  'specialisations', 'degrees', 'campus', 'course_table', 'course_unlocks', 
  'school_to_subjects', 'schools_to_subjects']
  for table in tables:
    drop_query = "DROP TABLE IF EXISTS " + table + " CASCADE"
    print(drop_query)
    engine.execute(drop_query) 
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
  construct_db()