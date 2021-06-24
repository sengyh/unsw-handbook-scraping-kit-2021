from bs4 import BeautifulSoup
from pathlib import Path
import os

def parse_course_page_html(course_code, page_html):
  soup = BeautifulSoup(page_html, 'html.parser')
  pretty = soup.prettify()
  save_course_page(course_code, pretty)
  full_head = soup.find("div", {"class":"css-1999l0b-Box-Flex-StyledFlex e3iudi70"})
  print(full_head)
  full_body = soup.find("div",{"class": "css-et39we-Box-Flex-Row-Row-Main e1gw5x5n1"})
  #print(full_body)

def save_course_page(course, course_info_html):
  course_html_dir_path = Path.cwd() / '..' / 'data' / 'raw' / 'course_page_source' 
  if not course_html_dir_path.exists():
    os.makedirs(course_html_dir_path, exist_ok=True)
  course_path = os.path.join(course_html_dir_path, course)
  f = open(course_path, "w")
  f.write(course_info_html)
  f.close()
  return