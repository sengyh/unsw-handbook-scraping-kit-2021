from bs4 import BeautifulSoup
from pathlib import Path
from course_page_parser import create_course_json
import os
import re
import json

# saves course html, extracts key data into json and appends it to data file
def parse_course_page_html(course_code, page_html):
  soup = BeautifulSoup(page_html, 'lxml')
  save_course_page(course_code, str(soup))
  course_dict = extract_course_info(soup)
  #save_into_json_file(course_info_dict)
  return course_dict

# need to cache all course page htmls (just in case)
def save_course_page(course, course_info_html):
  subject_code = re.sub('[0-9]+', '', course)
  course_html_dir_path = Path.cwd() / '..' / '..' / 'data' / 'html' / 'courses' / subject_code
  if not course_html_dir_path.exists():
    os.makedirs(course_html_dir_path, exist_ok=True)
  course_path = os.path.join(course_html_dir_path, course + '.html')
  f = open(course_path, "w")
  f.write(course_info_html)
  f.close()
  return

# returns the course data in json format
def extract_course_info(p_soup):
  head = p_soup.find("div", {"class":"css-1999l0b-Box-Flex-StyledFlex e3iudi70"})
  body = p_soup.find("div",{"class": "css-et39we-Box-Flex-Row-Row-Main e1gw5x5n1"})
  course_dict = create_course_json(head, body)
  return course_dict

# updates json file
def save_into_json_file(course_dict):
  course_file = Path.cwd() / '..' / '..' / 'data' / 'json' / 'all_courses.json'
  if not os.path.exists(course_file):
    cf = open(course_file, 'w')
    cf.write("{}")
    cf.close()
  cf = open(course_file, 'r')
  ac_dict = json.load(cf)
  cf.close()
  open(course_file, 'w').close()
  ac_dict.update(course_dict)
  cf = open(course_file, 'w')
  json.dump(ac_dict, cf, sort_keys=True)
  cf.close()
  return