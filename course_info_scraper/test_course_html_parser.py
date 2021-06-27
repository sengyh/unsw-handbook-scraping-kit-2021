from bs4 import BeautifulSoup
from pathlib import Path
import sys
import os

def test():
  sub = 'ACCT'
  code = '1511'
  if (len(sys.argv) == 3):
    sub = sys.argv[1].upper()
    code = sys.argv[2]
  
  course = sub + code + '.html'
  page_path = Path.cwd() / '..' / 'data' / 'html' / 'courses' / sub / course
  print(page_path)
  f = open(page_path, "r")
  soup = BeautifulSoup(f, 'lxml')
  head = soup.find("div", {"class":"css-1999l0b-Box-Flex-StyledFlex e3iudi70"})
  #print(head, type(head))
  parse_head(head)
  body = soup.find("div",{"class": "css-et39we-Box-Flex-Row-Row-Main e1gw5x5n1"})
  #print(body)
  parse_body(body)
  f.close()

def parse_head(head):
  name = head.find('h2').string.lstrip().rstrip()
  bottom_line = head.find_all('h5')
  code = bottom_line[0].string.lstrip().rstrip()
  uoc = bottom_line[1].string.lstrip().rstrip()
  print(code, name, uoc)
  return

def parse_body(body):
  # to be completed
  # overview section
  desc = body.find('div', {'id': 'Overview'})
  if desc:
    desc_text = desc.find('div', {'aria-hidden': 'true'})
    if not desc_text:
      desc_text = desc.find('div', {'aria-hidden': 'false'})
    if desc_text:
      print(desc_text)

  # conditions section
  coe = body.find('div', {'id': 'ConditionsforEnrolment'})
  if coe:
    coe_text = coe.find('div', {'class': 'css-1l0t84s-Box-CardBody e1q64pes0'})
    if coe_text:
      # TODO: figure out how to get properly formatted text from html jumble
      print(coe_text.text.lstrip().rstrip())

  # equivalent courses section
  # code n text class: unit-title css-1r4uxab-StyledAILinkBodySection exq3dcx6
  # only code class: uoc-text css-rf807j-StyledAILinkHeaderSection exq3dcx4
  equivc = body.find('div', {'id': 'EquivalentCourses'})
  print('Equivalent Courses:')
  if equivc:
    eq_list = equivc.find_all('div', {'class': 'uoc-text css-rf807j-StyledAILinkHeaderSection exq3dcx4'})
    for eq in eq_list:
      print(eq.text)


  # excluded courses section
  exclc = body.find('div', {'id': 'ExclusionCourses'})
  print('Exclusion Courses:')
  if exclc:
    exc_list = exclc.find_all('div', {'class': 'uoc-text css-rf807j-StyledAILinkHeaderSection exq3dcx4'})
    for exc in exc_list:
      print(exc.text)

  # get all sidebar data
  sidebar_elems = body.find_all('div', {'class': 'css-1cq5lls-Box-AttrContainer esd54cc0'})
  for div in sidebar_elems:
    title_div = div.find('h4', {'class': 'css-hl5pza-AttrHeader esd54cc1'})   
    if title_div:   
      content = div.find('a')
      if not content:
        content = div.find('div', {'class': 'css-1smylv8-Box-Flex'})
      if content:
        title_text = title_div.find(text=True).lstrip().rstrip()
        content_text = content.find(text=True).lstrip().rstrip()
        print(title_text + ': ' + content_text)
  return



if __name__ == "__main__":
  test()