import json
import os
from pathlib import Path
from load_course_page import get_course_page_html

def scrape_course_pages():
  course_file = Path.cwd() / '..' / 'data' / 'json' / 'all_courses.json'
  if not os.path.exists(course_file):
    cf = open(course_file, 'w')
    cf.write("{}")
    cf.close()
  cf = open(course_file, 'r')
  ac_dict = json.load(cf)
  cf.close()

  with open('../data/json/subject_course.json', "r") as f:
    data = json.load(f)
    #print(data['all_subjects']['code'])
    start = False
    for subject in data['all_subjects']:
      course_list = subject.get('courses')
      for course in course_list:   
        if (course == 'LAWS3356' or start is True):
          start = True
          course_dict = get_course_page_html(course)
          if (course_dict == "SHTF"):
            print('exiting early')
            start = False
            break
          ac_dict.update(course_dict)
          print(course)
  f.close()

  # wipe original file, dump the updated json and we're done
  open(course_file, 'w').close()
  cf = open(course_file, 'w')
  json.dump(ac_dict, cf, sort_keys=True)
  cf.close()
  print('fuck yessssss')
  return

if __name__ == "__main__":
  scrape_course_pages()
  
