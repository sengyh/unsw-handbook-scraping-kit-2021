from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import postgresql
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()

class Course(Base):
  __tablename__ = 'courses'
  code = Column(String, primary_key=True)
  name = Column(String)
  overview = Column(String)
  subject = Column(String)
  level = Column(Integer)
  school = Column(String)
  credits = Column(Integer)
  terms_available = Column(postgresql.ARRAY(String))
  equivalent_courses = Column(postgresql.ARRAY(String))
  exclusion_courses = Column(postgresql.ARRAY(String))
  unlocked_by = Column(postgresql.ARRAY(String))
  unlocks = Column(postgresql.ARRAY(String))
  other_requirements = Column(postgresql.ARRAY(postgresql.JSON))
  is_gen_ed = Column(Boolean)
  is_intro = Column(Boolean)
  is_multi_term = Column(Boolean)

class Subject(Base):
  __tablename__ = 'subjects'
  code = Column(String, primary_key=True)
  name = Column(String, ForeignKey('courses.subject'))

class School(Base):
  __tablename__ = 'schools'
  name = Column(String, primary_key=True)
  subject_code = Column(String, ForeignKey('subjects.code'))

class Faculty(Base):
  __tablename__ = 'faculties'
  code = Column(String, primary_key=True)
  name = Column(String)
  overview = Column(String)

class FacSch(Base):
  __tablename__ = 'faculty_to_school'
  code = Column(String, ForeignKey('faculties.code'), nullable=False)
  school = Column(String, ForeignKey('schools.name'), nullable=False)

class Specialisation(Base):
  __tablename__ = 'specialisations'
  code = Column(String, primary_key=True)
  name = Column(String)
  overview = Column(String)
  type = Column(String)
  credits = Column(Integer)
  course_structure = Column(postgresql.ARRAY(postgresql.JSON))
  more_information = Column(postgresql.ARRAY(postgresql.JSON))
  school = Column(String, ForeignKey('schools.name'))

class Program(Base):
  __tablename__ = 'degrees'
  code = Column(String, primary_key=True)
  name = Column(String)
  credits = Column(Integer)
  overview = Column(String)
  duration = Column(Integer)
  structure_overview = Column(String)
  core_structure_uoc = Column(Integer)
  core_specialisations = Column(postgresql.ARRAY(postgresql.JSON))
  optional_specialisations = Column(postgresql.ARRAY(postgresql.JSON))
  core_course_components = Column(postgresql.ARRAY(postgresql.JSON))
  misc_course_components = Column(postgresql.ARRAY(postgresql.JSON))
  more_information = Column(postgresql.ARRAY(postgresql.JSON))
  faculty = Column(String, ForeignKey('faculties.name'))
  intake_period = Column(postgresql.array(String))
  academic_calendar = Column(String)
  award = Column(String)
  award_type = Column(String)

class Campus(Base):
  __tablename__ = 'campus'
  name = Column(String, primary_key=True)
  


