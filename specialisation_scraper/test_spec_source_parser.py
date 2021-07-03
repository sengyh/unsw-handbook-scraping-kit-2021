import bs4
import time
import random
from pathlib import Path
from process_soup_to_json import parse_spec_soup
import os
import sys

def test():
  spec = 'filmb'
  if (len(sys.argv) == 2):
    spec = sys.argv[1]

  spec_file = spec + '.html'
  raw_spec_html = Path.cwd() / 'htmls' / spec_file
  rshf = open(raw_spec_html, 'r')
  soup = bs4.BeautifulSoup(rshf, "lxml")
  #print(soup)
  parse_spec_soup(soup)

  
  return



if __name__ == '__main__':
  test()