import bs4
import time
import random
from pathlib import Path
from process_soup_to_json import parse_ddeg_soup
import os
import sys
import json

def traverse_cached_ddegs():
  ddeg_dir_path = Path.cwd() / '..' / 'data' / 'html' / 'ddegrams'
  ts_file = Path.cwd() / '..' / 'data' / 'json' / 'tweaked_new_ordered_ddegs.json'

  if not os.path.exists(ts_file):
    tsf = open(ts_file, 'w')
    tsf.write("{}")
    tsf.close()

  tsf = open(ts_file, 'r')
  tsdict = json.load(tsf)
  tsf.close()
  cont = True
  for root, dirs, files in os.walk(ddeg_dir_path):
    for directory in dirs:
      print(directory)
    for fi in sorted(files): #, key=lambda x: (x[5], x[0])):
      if (fi == 'BINFB1.html' or cont is True):
        cont = True
        print(fi)
        f = open(os.path.join(root, fi), 'r')
        soup = bs4.BeautifulSoup(f, 'lxml')
        ddeg_dict = parse_ddeg_soup(soup)
        tsdict.update(ddeg_dict)
        f.close()

  open(ts_file, 'w').close()
  tsf = open(ts_file, 'w')
  json.dump(tsdict, tsf)
  tsf.close()
  return

def test():
  ddeg = 'advmath_engg'
  if (len(sys.argv) == 2):
    ddeg = sys.argv[1].upper()
  ddeg_file = ddeg + '.html'
  print(ddeg_file)
  #raw_ddeg_html = Path.cwd() / '..' / 'data' / 'html' / 'ddegs' / ddeg_file
  raw_ddeg_html = Path.cwd() / 'htmls' / ddeg_file
  rphf = open(raw_ddeg_html, 'r')
  soup = bs4.BeautifulSoup(rphf, "lxml")
  ddeg_dict = parse_ddeg_soup(soup)
  #print(json.dumps(ddeg_dict, indent=2))
  return

if __name__ == '__main__':
  test()
  #traverse_cached_ddegs()