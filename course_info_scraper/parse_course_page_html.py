from bs4 import BeautifulSoup
from pathlib import Path
import os
import re

def parse_course_page_html(course_code, page_html):
  soup = BeautifulSoup(page_html, 'lxml')
  #pretty = soup.prettify()
  #print(soup)
  #print(type(soup))
  save_course_page(course_code, str(soup))
  extract_course_info(soup)

  # need to cache all course page htmls (just in case)
def save_course_page(course, course_info_html):
  subject_code = re.sub('[0-9]+', '', course)
  course_html_dir_path = Path.cwd() / '..' / 'data' / 'html' / 'courses' / subject_code
  if not course_html_dir_path.exists():
    os.makedirs(course_html_dir_path, exist_ok=True)
  course_path = os.path.join(course_html_dir_path, course + '.html')
  f = open(course_path, "w")
  f.write(course_info_html)
  f.close()
  return

def extract_course_info(p_soup):
  head = p_soup.find("div", {"class":"css-1999l0b-Box-Flex-StyledFlex e3iudi70"})
  print(head)
  body = p_soup.find("div",{"class": "css-et39we-Box-Flex-Row-Row-Main e1gw5x5n1"})
  print(body)
  return