from bs4 import BeautifulSoup
from pathlib import Path
import sys
import os
import json
from course_page_parser import parse_head, parse_body


def test():
  sub = 'ACCT'
  code = '1511'
  if (len(sys.argv) == 3):
    sub = sys.argv[1].upper()
    code = sys.argv[2]
  
  course = sub + code + '.html'
  page_path = Path.cwd() / '..' / 'data' / 'html' / 'courses' / sub / course
  f = open(page_path, "r")
  soup = BeautifulSoup(f, 'lxml')
  head = soup.find("div", {"class":"css-1999l0b-Box-Flex-StyledFlex e3iudi70"})
  head_dict = parse_head(head)
  body = soup.find("div",{"class": "css-et39we-Box-Flex-Row-Row-Main e1gw5x5n1"})
  body_dict = parse_body(body)
  course_dict = head_dict
  course_dict.update(body_dict)
  course_json = json.dumps(course_dict)
  #print(course_json)
  c = json.loads(course_json)
  #print(c['Overview'].rstrip())
  print(c)
  f.close()

if __name__ == "__main__":
  test()