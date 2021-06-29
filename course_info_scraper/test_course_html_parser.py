from bs4 import BeautifulSoup
from pathlib import Path
import sys
import os
import json
from course_page_parser import create_course_json

# need to create course file, put empty json if dont exist
# open and append new course objs 
# TODO: file operations are cooked, come back later
def traverse_dir():
  hc_path = Path.cwd() / '..' / 'data' / 'html' / 'courses'
  tc_file = Path.cwd() / '..' / 'data' / 'json' / 'all_courses.json'
  # if file doesnt exist, make file later and write into it
  if not os.path.exists(tc_file):
    tcf = open(tc_file, 'w')
    tcf.write("{}")
    tcf.close()
  # if file exists, get json, append, wipe file and rewrite it with updated json
  tcf = open(tc_file, 'r')
  tcdict = json.load(tcf)
  tcf.close()
  open(tc_file, 'w').close()
  for root, dirs, files in os.walk(hc_path):
    #for di in dirs:
    #  print(di)
    cont = True
    for fi in files:
      # this part is fine
      #print(fi)
      #if (fi == "COMM3101.html"):
      #  cont = True
      #else: 
      #  continue
      if cont:
        f = open(os.path.join(root, fi), 'r')
        soup = BeautifulSoup(f, 'lxml')
        head = soup.find("div", {"class":"css-1999l0b-Box-Flex-StyledFlex e3iudi70"})
        body = soup.find("div",{"class": "css-et39we-Box-Flex-Row-Row-Main e1gw5x5n1"})
        course_json = create_course_json(head, body)
        #print(type(course_json))
        tcdict.update(course_json)
        f.close()
  tcf = open(tc_file, 'w')
  json.dump(tcdict, tcf, sort_keys=True)
  tcf.close()
  return


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
  body = soup.find("div",{"class": "css-et39we-Box-Flex-Row-Row-Main e1gw5x5n1"})
  course_json = create_course_json(head, body)
  print(json.dumps(course_json, indent=2))
  print(course_json)
  f.close()
  return

if __name__ == "__main__":
  traverse_dir()
  #test()