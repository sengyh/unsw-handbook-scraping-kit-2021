from bs4 import BeautifulSoup
from pathlib import Path
import os

def test():
  page_path = Path.cwd() / '..' / 'data' / 'raw' / 'course_page_source' / 'MATH1011'
  print(page_path)
  f = open(page_path, "r")
  soup = BeautifulSoup(f, 'html.parser')
  full_head = soup.find("div", {"class":"css-1999l0b-Box-Flex-StyledFlex e3iudi70"})
  #print(full_head)
  full_body = soup.find("div",{"class": "css-et39we-Box-Flex-Row-Row-Main e1gw5x5n1"})
  print(full_body)
  f.close()

if __name__ == "__main__":
  test()