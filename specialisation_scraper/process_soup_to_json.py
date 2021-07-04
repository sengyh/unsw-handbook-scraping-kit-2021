from typing import final
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
  ovrbody = overview.find('div', {'class': overview_body_class})
  overview_text = ovrbody.find('div', {'aria-hidden': 'false'})
  formatted_overview_text = ""
  if not overview_text:
    overview_text = overview.find('div', {'aria-hidden': 'false'})
  if overview_text:
    formatted_overview_text = format_overview_text(overview_text)
  print(formatted_overview_text)
  return formatted_overview_text

def format_overview_text(overview_text):
  final_ovw_text = ""
  ovtext_elems = overview_text.find_all('p')
  if not ovtext_elems:
    print('no paragraphs found')
    ovt_list = overview_text.contents
    for ovt_elem in ovt_list:
      if str(ovt_elem) == "<br/>":
        final_ovw_text += '\n'
        continue
      final_ovw_text += str(ovt_elem).lstrip().rstrip() + ' '
  else:  
    #print('paragraph tags found')
    ovtext_elems = overview_text.find_all()
    for elem in ovtext_elems:
      if elem.name == 'br':
        final_ovw_text += '\n'
        continue
      if elem.name in ['strong', 'a']:
        continue
      if elem.name == 'p':
        pc_list = elem.contents
        for pc_el in pc_list:
          if pc_el.name in ['strong', 'a']:
            final_ovw_text += (pc_el.text).lstrip().rstrip() 
            continue
          if pc_el.name in ['br']:
            final_ovw_text += '\n'
            continue
          final_ovw_text += str(pc_el).lstrip().rstrip() + ' ' 
      if elem.name == 'li':
        final_ovw_text += '\t- ' + str(elem.text) 
      final_ovw_text += '\n'
  formatted_overview = final_ovw_text.rstrip()
  return formatted_overview

def parse_offered_progs(offered_programs):
  offered_prog_codes = []
  prog_row_elem_class = 'css-j3xo3o-Box-SAccordionItemHeader-SClickableAccordionItemHeader el7mbl40'
  all_prog_elems = offered_programs.find_all('div', {'class', prog_row_elem_class})
  for prog_elem in all_prog_elems:
    deg_fname_and_code = prog_elem.find_all('strong')
    deg_fname = deg_fname_and_code[0].text
    deg_code = deg_fname_and_code[1].text.split(' - ')[0]
    offered_prog_codes.append(deg_code)
    #print(deg_code + ': ' + deg_fname)
  offeredp_dict = {'available_in_program(s)': offered_prog_codes}
  print(offeredp_dict)
  return offeredp_dict

def process_sidebar(sidebar):
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