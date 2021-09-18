import json
from sqlalchemy import insert
from sqlalchemy.sql.expression import null
from sqlalchemy.sql import exists
from schema import Faculty, School, Subject, SchSub

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
        faculty="NO_FAC"
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


# other_requirements: {
#    uoc?: number;
#    wam?: number;
#    subject?: string;
#    level?: number;
#    specialisations?: string[];
#    programs?: string[];
#    corequisites?: string[];
#    all_found_courses?: string[];
#    course_group_boolean?: string;
#    raw_str?: string;
#  };


def insert_courses():
  f = open('../../data/json/refined_courses.json', "r")
  course_data = json.loads(f.read())
  for course_code in course_data:
    print(course_data[course_code]['subject'] + ' - ' + course_data[course_code]['school'])
  return

def insert_specialisations():
  f = open('../../data/json/refined_specialisations.json', "r")
  spec_data = json.loads(f.read())
  for spec_code in spec_data:
    spec_attrs = spec_data[spec_code]
    #print(spec_attrs['school'] + ' - ' + spec_attrs['faculty'])
    print(json.dumps(spec_attrs['course_structure'], indent=2))
    break
  return

