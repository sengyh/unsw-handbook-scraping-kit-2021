import json
from sqlalchemy import insert
from sqlalchemy.sql.expression import null
from sqlalchemy.sql import exists
from schema import Faculty, School, Subject, SchSub, Course, CourseTerm, Specialisation, Program

def insert_fac_sch(Session):
  s = Session()
  facf = open('../../data/json/faculties.json', "r")
  faculties = json.loads(facf.read())
  empty_fac = Faculty(
    name=None,
    code="NO_FAC",
    overview=None
  )
  s.add(empty_fac)
  for fac_code in faculties:
    fac_attrs = faculties[fac_code]
    fac = Faculty(
      name=fac_attrs['name'],
      code=fac_code,
      overview=fac_attrs['overview']
    )
    fac_schools = fac_attrs['schools']
    for fsch in fac_schools:
      sch = School(
        name=fsch,
        faculty=fac_code
      )
      s.add(sch)
    s.add(fac)
  s.commit()
  s.close()
  return

def insert_subjects(Session):
  s = Session()
  schf = open('../../data/json/schools.json', "r")
  subf = open('../../data/json/subjects.json', "r")
  schools = json.loads(schf.read())
  subjects = json.loads(subf.read())
  # create record where there is no school
  empty_sch = School(
    name="NONE_AVAILABLE",
    faculty="NO_FAC"
  )
  s.add(empty_sch)
  # fill out subjects table
  for sub in subjects:
    subj = Subject(
      code=sub,
      name=subjects[sub]['name']
    )
    s.add(subj)
  # some schools (well, one) do not have faculties
  for school in schools:
    school_exists = s.query(exists().where(School.name == school)).scalar()
    if school_exists is False:
      print(school)
      sch = School(
        name=school,
        faculty='NO_FAC'
      )
      s.add(sch)
  # create junction table for schools and subjects
  for sch in schools:
    for sub in schools[sch]['subjects']:
      sch2sub = SchSub(
        school=sch,
        subject=sub
      )
      s.add(sch2sub)
  s.commit()
  s.close()
  return


def insert_courses(Session):
  s = Session()
  f = open('../../data/json/refined_courses.json', "r")
  course_data = json.loads(f.read())
  # iterate through courses and create records of the course and its offered terms
  for course_code in course_data:
    course_attrs = course_data[course_code]
    new_course_record = create_course_record(course_code, course_attrs)
    s.add(new_course_record)
    for term in course_attrs['terms_available']:
      new_course_term = CourseTerm(
        course=course_code,
        term=term
      )
      s.add(new_course_term)
  s.commit()
  s.close()
  return

def create_course_record(code, attrs):
  homogenised_sch = attrs['school']
  if attrs['school'] == "":
    homogenised_sch = "NONE_AVAILABLE"

  new_course_record = Course(
    code=code,
    name=attrs['name'],
    overview=attrs['overview'],
    subject=attrs['subject'],
    level=attrs['level'],
    school=homogenised_sch,
    credits=attrs['uoc'],
    equivalent_courses=attrs['equivalent_courses'],
    exclusion_courses=attrs['exclusion_courses'],
    unlocked_by=attrs['unlocked_by'],
    unlocks=attrs['unlocks'],
    other_requirements=homogenise_other_reqs(attrs['other_requirements']),
    is_gen_ed=attrs['is_gen_ed'],
    is_intro=attrs['is_intro'],
    is_multi_term=attrs['is_multi_term'],
  )
  return new_course_record
  
def homogenise_other_reqs(other_reqs):
  homogenised_oreq = {
    "uoc": None,
    "wam": None,
    "subject": None,
    "level": None,
    "specialisations": None,
    "programs": None,
    "corequisites": None,
    "all_found_courses": None,
    "course_group_boolean": None,
    "raw_str": None
  }
  for key in homogenised_oreq.keys():
    if key in other_reqs:
      homogenised_oreq[key] = other_reqs[key]
  return homogenised_oreq

def insert_specialisations(Session):
  s = Session()
  f = open('../../data/json/refined_specialisations.json', "r")
  spec_data = json.loads(f.read())
  for spec_code in spec_data:
    spec_attrs = spec_data[spec_code]
    school_exists = s.query(exists().where(School.name == spec_attrs['school'])).scalar()
    if school_exists is False:
      print(spec_attrs['school'])
      sch = School(
        name=spec_attrs['school'],
        faculty='NO_FAC'
      )
      s.add(sch)
    new_spec_record = Specialisation(
      code=spec_code,
      name=spec_attrs['name'],
      overview=spec_attrs['overview'],
      type=spec_attrs['specialisation_type'],
      credits=spec_attrs['uoc'],
      course_structure=spec_attrs['course_structure'],
      more_information=spec_attrs['more_information'],
      school=spec_attrs['school']
    )
    s.add(new_spec_record)
  s.commit()
  s.close()
  return

def insert_degrees(Session):
  s = Session()
  f = open('../../data/json/refined_programs.json', "r")
  deg_data = json.loads(f.read())
  for deg_code in deg_data:
    deg_attrs = deg_data[deg_code]
    new_deg_record = Program(
      code=deg_code,
      name=deg_attrs['name'],
      credits=deg_attrs['uoc'],
      overview=deg_attrs['overview'],
      duration=deg_attrs['program_duration'],
      structure_overview=deg_attrs['program_structure_overview'],
      core_structure_uoc=deg_attrs['core_structure_uoc'],
      core_structure_desc=deg_attrs['core_structure_desc'],
      core_specialisations=deg_attrs['core_specialisations'],
      optional_specialisations=deg_attrs['optional_specialisations'],
      core_course_components=deg_attrs['core_course_component'],
      misc_course_components=deg_attrs['misc_course_components'],
      more_information=deg_attrs['more_information'],
      faculty=deg_attrs['faculty'],
      intake_period=deg_attrs['intake_period'],
      academic_calendar=deg_attrs['academic_calendar'],
      award=deg_attrs['award'],
      award_type=deg_attrs['award_type']
    )
    s.add(new_deg_record)
  s.commit()
  s.close()
  return


#class Program(Base):
#  __tablename__ = 'degrees'
#  code = Column(String, primary_key=True)
#  name = Column(String)
#  credits = Column(Integer)
#  overview = Column(String)
#  duration = Column(Integer)
#  structure_overview = Column(String)
#  core_structure_uoc = Column(Integer)
#  core_specialisations = Column(postgresql.ARRAY(postgresql.JSON))
#  optional_specialisations = Column(postgresql.ARRAY(postgresql.JSON))
#  core_course_components = Column(postgresql.ARRAY(postgresql.JSON))
#  misc_course_components = Column(postgresql.ARRAY(postgresql.JSON))
#  more_information = Column(postgresql.ARRAY(postgresql.JSON))
#  faculty = Column(String, ForeignKey('faculties.name'))
#  intake_period = Column(postgresql.ARRAY(String))
#  academic_calendar = Column(String)
#  award = Column(String)
#  award_type = Column(String)