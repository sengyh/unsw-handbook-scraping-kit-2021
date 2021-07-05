import bs4
import time
import random
from pathlib import Path
from process_soup_to_json import parse_spec_soup
import os
import sys
import json

def traverse_dir():
  spec_dir_path = Path.cwd() / '..' / 'data' / 'html' / 'specialisations'
  ts_file = Path.cwd() / '..' / 'data' / 'json' / 'test_ordered_specs.json'

  if not os.path.exists(ts_file):
    tsf = open(ts_file, 'w')
    tsf.write("{}")
    tsf.close()

  tsf = open(ts_file, 'r')
  tsdict = json.load(tsf)
  tsf.close()
  cont = True
  for root, dirs, files in os.walk(spec_dir_path):
    for directory in dirs:
      print(directory)
    for fi in sorted(files, key=lambda x: (x[5], x[0])):
      if (fi == 'COMPA1' or cont is True):
        cont = True
        print(fi)
        f = open(os.path.join(root, fi), 'r')
        soup = bs4.BeautifulSoup(f, 'lxml')
        spec_dict = parse_spec_soup(soup)
        tsdict.update(spec_dict)
        f.close()

  open(ts_file, 'w').close()
  tsf = open(ts_file, 'w')
  json.dump(tsdict, tsf)
  tsf.close()
  return

def test():
  spec = 'filmb'
  if (len(sys.argv) == 2):
    spec = sys.argv[1]

  spec_file = spec + '.html'
  raw_spec_html = Path.cwd() / 'htmls' / spec_file
  rshf = open(raw_spec_html, 'r')
  soup = bs4.BeautifulSoup(rshf, "lxml")
  spec_dict = parse_spec_soup(soup)
  print(json.dumps(spec_dict, indent=2))
  return



if __name__ == '__main__':
  #test()
  traverse_dir()