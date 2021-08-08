from typing import final
import bs4
import json
import re
from parse_ddeg_structure import parse_ddeg_structure
from body_parser_helpers import parse_overview, parse_stand_alone_progs, process_sidebar

def parse_ddeg_soup(soup):
  head = soup.find('div', {'id': 'intro-container'})
  head_dict = parse_head(head)
  full_body = soup.find('div', {'class': 'css-et39we-Box-Flex-Row-Row-Main e1gw5x5n1'})
  body_dict = parse_body(full_body)
  code = head_dict.pop('code')
  ddeg_val_dict = head_dict
  ddeg_val_dict.update(body_dict)
  ddeg_dict = {code: ddeg_val_dict}
  #print(json.dumps(ddeg_dict, indent=2))
  return ddeg_dict

def parse_head(head):
  head_dict = {}
  name = head.find('h2').text
  bottom_row = head.find_all('h5')
  code = bottom_row[0].text
  uoc = bottom_row[1].text.lstrip().rstrip()
  processed_uoc = ""
  if re.match("[0-9]+ Units of Credit", uoc):
    processed_uoc = uoc.split(' ')[0]
  #print(code, name, uoc)
  head_dict.update({'code': code})
  head_dict.update({'name': name})
  head_dict.update({'uoc': processed_uoc})
  #print(json.dumps(head_dict, indent=2))
  return head_dict

def parse_body(body):
  body_dict = {}
  main_body = body.find('div', {'class': 'css-1gviihd-Box-Col-Center-css e1jwwfpu0'})
  overview = main_body.find('div', id='Overview')
  overview_text = parse_overview(overview)
  overview_dict = {'overview': overview_text}
  body_dict.update(overview_dict)

  stand_alone_progs = main_body.find('div', id='StandAlonePrograms')
  stand_alone_progs_dict = parse_stand_alone_progs(stand_alone_progs)
  body_dict.update(stand_alone_progs_dict)

  ddeg_structure = main_body.find('div', id='DoubleDegreeStructure')
  sap_list = stand_alone_progs_dict.get('stand_alone_programs')
  ddeg_structure_dict = parse_ddeg_structure(ddeg_structure, sap_list)
  body_dict.update(ddeg_structure_dict)

  sidebar = body.find('div', {'data-testid': 'attributes-table'})
  sidebar_dict = process_sidebar(sidebar)
  body_dict.update(sidebar_dict)

  #print(json.dumps(body_dict, indent=2))
  return body_dict

