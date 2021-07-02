import bs4
import time
import random
from pathlib import Path
from process_soup_to_json import parse_spec_soup
import os

def test():
  raw_spec_html = Path.cwd() / 'htmls' / 'solaa.html'
  rshf = open(raw_spec_html, 'r')
  soup = bs4.BeautifulSoup(rshf, "lxml")
  #print(soup)
  parse_spec_soup(soup)

  
  return



if __name__ == '__main__':
  test()