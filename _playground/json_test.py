import json

with open('../data/json/subject_course.json', "r") as f:
  data = json.load(f)
  #print(data['all_subjects']['code'])
  for subject in data['all_subjects']:
    subject_code = subject.get('code')
    scrape_all = True
    if (subject_code == 'COMP'):
      course_list = subject.get('courses')
      for course in course_list:
        print(course)

f.close()