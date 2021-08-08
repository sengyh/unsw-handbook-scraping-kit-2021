from bs4 import BeautifulSoup
from pathlib import Path
import sys
import os
import json
from course_page_parser import create_course_json

# need to create course file, put empty json if dont exist
# open and append new course objs 
# TODO: file operations are cooked, come back later
def traverse_cached_courses():
  hc_path = Path.cwd() / '..' / '..' / 'data' / 'html' / 'courses'
  tc_file = Path.cwd() / '..' / '..' / 'data' / 'json' / 'all_courses.json'
  # if file doesnt exist, make file later and write into it
  if not os.path.exists(tc_file):
    tcf = open(tc_file, 'w')
    tcf.write("{}")
    tcf.close()
  # if file exists, get json, append, wipe file and rewrite it with updated json
  tcf = open(tc_file, 'r')
  tcdict = json.load(tcf)
  tcf.close()
  cont = True
  for root, dirs, files in os.walk(hc_path):
    dirs.sort()
    for fi in sorted(files):
      if (fi == 'COMP1511.html' or cont is True):
        cont = True
        course = fi.split('.')[0]

        print(course + '=', end='')

        f = open(os.path.join(root, fi), 'r')
        soup = BeautifulSoup(f, 'lxml')
        head = soup.find("div", {"class":"css-1999l0b-Box-Flex-StyledFlex e3iudi70"})
        body = soup.find("div",{"class": "css-et39we-Box-Flex-Row-Row-Main e1gw5x5n1"})
        course_json = create_course_json(head, body)
       
        print(course_json[course]['uoc'] + '=', end='')
        print(course_json[course]['prereqs'])
        #print(json.dumps(course_json, indent=2))

        tcdict.update(course_json)
        f.close()
      
  write_json_to_file(tc_file, tcdict)
  return

def write_json_to_file(tc_file, tcdict):
  open(tc_file, 'w').close()
  tcf = open(tc_file, 'w')
  json.dump(tcdict, tcf, sort_keys=False)
  tcf.close()
  return

if __name__ == "__main__":
  traverse_cached_courses()
