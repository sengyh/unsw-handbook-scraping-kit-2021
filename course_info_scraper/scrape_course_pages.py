import json
from get_course_page_html import get_course_page_html

def scrape_course_pages():
  with open('../data/json/subject_course.json', "r") as f:
    data = json.load(f)
    #print(data['all_subjects']['code'])
    for subject in data['all_subjects']:
      subject_code = subject.get('code')
      scrape_all = True
      if (subject_code == 'MATH'):
        course_list = subject.get('courses')
        i = 0
        for course in course_list:
          if (i == 1):
            break
          print(course)
          get_course_page_html(course)
          i+=1
  f.close()
  return

if __name__ == "__main__":
  scrape_course_pages()
  
