from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import postgresql
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import ForeignKey, PrimaryKeyConstraint

Base = declarative_base()

class Campus(Base):
  __tablename__ = 'campus'
  name = Column(String, primary_key=True)

class Faculty(Base):
  __tablename__ = 'faculties'
  code = Column(String, primary_key=True, unique=True)
  name = Column(String, unique=True)
  overview = Column(String, nullable=True)

class School(Base):
  __tablename__ = 'schools'
  name = Column(String, primary_key=True)
  faculty = Column(String, ForeignKey('faculties.code'))

class Subject(Base):
  __tablename__ = 'subjects'
  code = Column(String, primary_key=True)
  name = Column(String)

class SchSub(Base):
  __tablename__ = 'schools_to_subjects'
  school = Column(String, ForeignKey('schools.name'))
  subject = Column(String, ForeignKey('subjects.code'))
  __table_args__ = (PrimaryKeyConstraint('school', 'subject'),) 

class Course(Base):
  __tablename__ = 'courses'
  code = Column(String, primary_key=True)
  name = Column(String)
  overview = Column(String)
  subject = Column(String, ForeignKey('subjects.code'))
  level = Column(Integer)
  school = Column(String, ForeignKey('schools.name'))
  credits = Column(Integer)
  equivalent_courses = Column(postgresql.ARRAY(String))
  exclusion_courses = Column(postgresql.ARRAY(String))
  unlocked_by = Column(postgresql.ARRAY(String))
  # turn this into a table
  unlocks = Column(postgresql.ARRAY(String))
  other_requirements = Column(postgresql.JSON)
  is_gen_ed = Column(Boolean)
  is_intro = Column(Boolean)
  is_multi_term = Column(Boolean)

class CourseTerm(Base):
  __tablename__ = 'course_terms'
  course = Column(String, ForeignKey('courses.code'))
  term = Column(String)
  __table_args__ = (PrimaryKeyConstraint('course', 'term'),)

class CourseUnlocks(Base):
  __tablename__ = 'course_unlocks'
  curr_course = Column(String, ForeignKey('courses.code'))
  unlocked_course = Column(String, ForeignKey('courses.code'))
  __table_args__ = (PrimaryKeyConstraint('curr_course', 'unlocked_course'),)

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
  core_structure_desc = Column(String)
  core_specialisations = Column(postgresql.ARRAY(postgresql.JSON))
  optional_specialisations = Column(postgresql.ARRAY(postgresql.JSON))
  core_course_components = Column(postgresql.ARRAY(postgresql.JSON))
  misc_course_components = Column(postgresql.ARRAY(postgresql.JSON))
  more_information = Column(postgresql.ARRAY(postgresql.JSON))
  faculty = Column(String, ForeignKey('faculties.name'))
  intake_period = Column(postgresql.ARRAY(String))
  academic_calendar = Column(String)
  award = Column(String)
  award_type = Column(String)


  


