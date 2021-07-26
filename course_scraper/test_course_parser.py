from bs4 import BeautifulSoup
from pathlib import Path
import sys
import os
import json
from course_page_parser import create_course_json

def test_course_parser():
  sub = 'COMP'
  code = '2521'
  if (len(sys.argv) == 3):
    sub = sys.argv[1].upper()
    code = sys.argv[2]
  
  course = sub + code + '.html'
  page_path = Path.cwd() / '..' / 'data' / 'html' / 'courses' / sub / course
  f = open(page_path, "r")
  soup = BeautifulSoup(f, 'lxml')
  head = soup.find("div", {"class":"css-1999l0b-Box-Flex-StyledFlex e3iudi70"})
  body = soup.find("div",{"class": "css-et39we-Box-Flex-Row-Row-Main e1gw5x5n1"})
  course_json = create_course_json(head, body)
  print(json.dumps(course_json, indent=2))
  #print(course_json)
  f.close()
  return

if __name__ == "__main__":
  test_course_parser()