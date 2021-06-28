from bs4 import BeautifulSoup
from pathlib import Path
import sys
import os
import json

def parse_head(head):
  name = head.find('h2').string.lstrip().rstrip()
  bottom_line = head.find_all('h5')
  code = bottom_line[0].string.lstrip().rstrip()
  uoc = bottom_line[1].string.lstrip().rstrip()
  head_dict = {'code': code, 'name': name, 'uoc': uoc}
  #print(head_dict)
  return head_dict

def parse_body(body):
  # overview section
  body_dict = {}
  desc = body.find('div', {'id': 'Overview'})
  desc_line = ''
  # overview box has either only one paragraph (no children)
  # multiple paragraphs
  # paragraph(s) and list
  if desc:
    desc_text = desc.find('div', {'aria-hidden': 'true'})
    if not desc_text:
      desc_text = desc.find('div', {'aria-hidden': 'false'})
    if desc_text:
      desc_elem = desc_text.find_all()
      if not desc_elem:
        desc_line += desc_text.text
      else:
        for desce in desc_elem:
          if desce.name == 'ul' or desce.name == 'strong':
            continue
          if desce.name == 'br':
            desc_line += '\n'
            continue
          if desce.name == 'li':
            desc_line += '\t- ' + desce.text
          else:
            desc_line += desce.text
          desc_line += '\n'
  #print(desc_line)
  body_dict.update({"overview": desc_line})  

  # conditions section
  coe = body.find('div', {'id': 'ConditionsforEnrolment'})
  conditions_line = ''
  if coe:
    coec = coe.find('div', {'class': 'css-1l0t84s-Box-CardBody e1q64pes0'})
    if coec:
      coe_text = coec.text.lstrip().rstrip()
      conditions_line += coe_text
  body_dict.update({'prereqs': conditions_line})

  # equivalent courses section
  # code n text class: unit-title css-1r4uxab-StyledAILinkBodySection exq3dcx6
  # only code class: uoc-text css-rf807j-StyledAILinkHeaderSection exq3dcx4
  equivc = body.find('div', {'id': 'EquivalentCourses'})
  equivc_list = []
  #print('Equivalent Courses:')
  if equivc:
    eq_list = equivc.find_all('div', {'class': 'uoc-text css-rf807j-StyledAILinkHeaderSection exq3dcx4'})
    for eq in eq_list:
      equivc_list.append(eq.text)
      #print(eq.text)
  body_dict.update({'equivalent_courses': equivc_list})

  # excluded courses section
  exclc = body.find('div', {'id': 'ExclusionCourses'})
  exclc_list = []
  #print('Exclusion Courses:')
  if exclc:
    exc_list = exclc.find_all('div', {'class': 'uoc-text css-rf807j-StyledAILinkHeaderSection exq3dcx4'})
    for exc in exc_list:
      exclc_list.append(exc.text)
      #print(exc.text)
  body_dict.update({'exclusion_courses': exclc_list})

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
        body_dict.update({title_text.lower().replace(' ', '_'): content_text})
        #print(title_text + ': ' + content_text)
  return body_dict
