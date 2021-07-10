import bs4
import time
import random
from pathlib import Path
from process_soup_to_json import parse_prog_soup
import os
import sys
import json

def traverse_cached_progs():
  prog_dir_path = Path.cwd() / '..' / 'data' / 'html' / 'programs'
  ts_file = Path.cwd() / '..' / 'data' / 'json' / 'new_progs.json'

  if not os.path.exists(ts_file):
    tsf = open(ts_file, 'w')
    tsf.write("{}")
    tsf.close()

  tsf = open(ts_file, 'r')
  tsdict = json.load(tsf)
  tsf.close()
  cont = True
  for root, dirs, files in os.walk(prog_dir_path):
    for directory in dirs:
      print(directory)
    for fi in sorted(files):
      if (fi == '3778.html' or cont is True):
        cont = True
        print(fi)
        f = open(os.path.join(root, fi), 'r')
        soup = bs4.BeautifulSoup(f, 'lxml')
        prog_dict = parse_prog_soup(soup)
        tsdict.update(prog_dict)
        f.close()

  open(ts_file, 'w').close()
  tsf = open(ts_file, 'w')
  json.dump(tsdict, tsf)
  tsf.close()
  return

def test():
  prog = '3635'
  if (len(sys.argv) == 2):
    prog = sys.argv[1].upper()
  fac = 'FAC_ENG' # 'FAC_ENG' 
  prog_file = prog + '.html'
  raw_prog_html = Path.cwd() / '..' / 'data' / 'html' / 'programs' / fac / prog_file
  #raw_prog_html = Path.cwd() / 'htmls' / prog_file
  rphf = open(raw_prog_html, 'r')
  soup = bs4.BeautifulSoup(rphf, "lxml")
  prog_dict = parse_prog_soup(soup)
  print(json.dumps(prog_dict, indent=2))
  return

if __name__ == '__main__':
  #test()
  traverse_cached_progs()