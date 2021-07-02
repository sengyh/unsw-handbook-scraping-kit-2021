import bs4

def parse_spec_soup(soup):
  head = soup.find('div', {'id': 'intro-container'})
  spec_dict = parse_head(head)
  full_body = soup.find('div', {'class': 'css-et39we-Box-Flex-Row-Row-Main e1gw5x5n1'})
  body_dict = parse_body(full_body)
  return

def parse_head(head):
  head_dict = {}
  name = head.find('h2').text
  bottom_row = head.find_all('h5')
  code = bottom_row[0].text
  uoc = bottom_row[1].text
  print(code, name, uoc)
  return

def parse_body(body):
  body_dict = {}


  return