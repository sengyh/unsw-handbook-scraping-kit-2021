import bs4
from parse_spec_structure import parse_spec_structure

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
  main_body = body.find('div', {'class': 'css-1gviihd-Box-Col-Center-css e1jwwfpu0'})
  overview = main_body.find('div', id='Overview')
  parse_overview(overview)

  offered_programs = main_body.find('div', id='AvailableinProgram(s)')
  parse_offered_progs(offered_programs)

  spec_structure = main_body.find('div', id='SpecialisationStructure')
  parse_spec_structure(spec_structure)

  sidebar = body.find('div', {'data-testid': 'attributes-table'})
  process_sidebar(sidebar)

  return

def parse_overview(overview):
  overview_body_class = 'css-1x8hb4i-Box-CardBody e1q64pes0'
  obody = overview.find('div', {'class': overview_body_class})
  overview_text = overview.find('div', {'aria-hidden': 'false'})
  if not overview_text:
    overview_text = overview.find('div', {'aria-hidden': 'false'})
  print(overview_text.prettify())
  return

def parse_offered_progs(offered_programs):
  prog_row_elem_class = 'css-j3xo3o-Box-SAccordionItemHeader-SClickableAccordionItemHeader el7mbl40'
  all_prog_elems = offered_programs.find_all('div', {'class', prog_row_elem_class})
  for prog_elem in all_prog_elems:
    deg_fname_and_code = prog_elem.find_all('strong')
    deg_fname = deg_fname_and_code[0].text
    deg_code = deg_fname_and_code[1].text.split(' - ')[0]
    print(deg_code + ': ' + deg_fname)
  return



def process_sidebar(sidebar):
  # sidebar key value elems
  sidebar_dict = {}
  sidebar_elem_class = 'css-1cq5lls-Box-AttrContainer esd54cc0'
  sidebar_elems = sidebar.find_all('div', {'class': sidebar_elem_class})
  for elem in sidebar_elems:
    title = elem.find('h4', {'class': 'css-hl5pza-AttrHeader esd54cc1'})   
    if title:   
      content = elem.find('a')
      if not content:
        content = elem.find('div', {'class': 'css-1smylv8-Box-Flex'})
      if content:
        title_text = title.find(text=True).lstrip().rstrip().lower().replace(' ', '_')
        content_text = content.find(text=True).lstrip().rstrip()
        sidebar_dict.update({title_text: content_text})
  print(sidebar_dict)
  return sidebar_dict