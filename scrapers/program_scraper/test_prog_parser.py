import bs4
import time
import random
from pathlib import Path
from process_soup_to_json import parse_prog_soup
import os
import sys
import json

def test():
  fac = 'FAC_ENG'
  prog = '3635'
  if (len(sys.argv) == 3):
    fac = sys.argv[1].upper()
    prog = sys.argv[2]
  prog_file = prog + '.html'
  raw_prog_html = Path.cwd() / '..' / '..' / 'data' / 'html' / 'programs' / fac / prog_file
  rphf = open(raw_prog_html, 'r')
  soup = bs4.BeautifulSoup(rphf, "lxml")
  prog_dict = parse_prog_soup(soup)
  print(json.dumps(prog_dict, indent=2))
  return

if __name__ == '__main__':
  test()
