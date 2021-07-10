import json
# helper functions
def parse_overview(overview):
  if not overview:
    return ""
  overview_body_class = 'css-1x8hb4i-Box-CardBody e1q64pes0'
  ovrbody = overview.find('div', {'class': overview_body_class})
  overview_text = ovrbody.find('div', {'aria-hidden': 'false'})
  formatted_overview_text = ""
  if not overview_text:
    overview_text = overview.find('div', {'aria-hidden': 'false'})
  if overview_text:
    formatted_overview_text = format_overview_text(overview_text)
  #print(formatted_overview_text)
  return formatted_overview_text

def parse_stand_alone_progs(stand_alone_progs):
  program_block_class = "css-vgk9p5-StyledLink-StyledAILink exq3dcx2"
  program_blocks = stand_alone_progs.find_all('a', {'class': program_block_class})
  prog_codes = []
  for pblock in program_blocks:
    prog_code_class = "uoc-text css-rf807j-StyledAILinkHeaderSection exq3dcx4"
    prog_code_el = pblock.find('div', {'class': prog_code_class})
    if prog_code_el:
      prog_code = prog_code_el.text.lstrip().rstrip()
      prog_codes.append(prog_code)
  sap_dict = {'stand_alone_programs': prog_codes}
  #print(json.dumps(sap_dict, indent=2))
  return sap_dict

def process_sidebar(sidebar):
  sidebar_dict = {}
  sidebar_elem_class = 'css-1cq5lls-Box-AttrContainer esd54cc0'
  sidebar_elems = sidebar.find_all('div', {'class': sidebar_elem_class})
  for elem in sidebar_elems:
    title = elem.find('h4', {'class': 'css-hl5pza-AttrHeader esd54cc1'})   
    if title:   
      content = elem.find_all('a')
      if not content:
        content = elem.find_all('div', {'class': 'css-1smylv8-Box-Flex'})
      if not content:
        content = elem.find_all('div', {'class': 'css-1l0t84s-Box-CardBody e1q64pes0'})
      if content:
        title_text = title.find(text=True).lstrip().rstrip().lower().replace(' ', '_')
        if len(content) == 1:
          content_text = parse_sidebar_content(content[0]).rstrip()
          ct_list = content_text.split('\n')
          if len(ct_list) == 1:
            sidebar_dict.update({title_text: content_text})
          else:
            sidebar_dict.update({title_text: ct_list})
        elif len(content) > 1:
          content_texts = []
          for el in content:
            content_texts.append(el.find(text=True))
          sidebar_dict.update({title_text: content_texts})
  print(json.dumps(sidebar_dict, indent=2))
  return sidebar_dict

def format_overview_text(overview_text):
  final_ovw_text = ""
  ovtext_elems = overview_text.find_all('p')
  if not ovtext_elems:
    #print('no paragraphs found')
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

def parse_sidebar_content(sb_elem):
  desc = ""
  for el in sb_elem.contents:
    if el.name == 'div':
      continue
    if el.name == 'br':
      desc += '\n'
      continue
    desc += el
  return desc