import re
import json
from body_parser_helpers import format_overview_text


def parse_prog_structure(prog_structure):
  if not prog_structure:
    return {'structure': {}}

  structure_val_dict = {}
  # addition: get the content/description of program structure
  prog_struct_desc_class = "css-1l0t84s-Box-CardBody e1q64pes0"
  prog_strucure_desc = prog_structure.find('div', {'class': prog_struct_desc_class})
  ps_desc = ""
  if prog_strucure_desc:
    ps_desc = parse_psdesc(prog_strucure_desc)
  structure_val_dict.update({'requirements': ps_desc})
  
  section_box_class = 'css-8x1vkg-Box-Card-EmptyCard-css-SAccordionContainer e1450wuy4'
  prog_struct_sects = prog_structure.find_all('div', {'class': section_box_class})
  for section in prog_struct_sects:
    section_dict = parse_section(section) 
    structure_val_dict.update(section_dict)

  structure_dict = {'structure': structure_val_dict}
  #print(json.dumps(structure_dict, indent=2))
  return structure_dict

# inside the 'blue box'
def parse_section(section):
  sect_val_dict = {}
  # obtains requirement section title and uocs from section header
  header_class = 'css-1wt42lu-Box-Flex-SAccordionHeader-css e1450wuy5'
  header = section.find('div', {'class': header_class})
  sec_title = header.strong.text
  sec_uoc = ""
  #print(sec_title)
  if header.small:
    sec_desc = header.small.text.lstrip().rstrip()
    confirmed_uoc_line = re.search("[0-9]+ Units of Credit:$", sec_desc)
    if confirmed_uoc_line:
      sec_uoc = confirmed_uoc_line.string.split(' ')[0]
  #print(sec_uoc)
  uoc_dict = {'uoc': sec_uoc}
  sect_val_dict.update(uoc_dict)

  # start parsing body section
  full_body_class = 'css-10hsoix-SAccordionRegion e1450wuy11'
  body_desc_class = 'css-127bpwp-Box-SAccordionDescription-css e1450wuy7'
  full_body = section.find('div', {'class': full_body_class})
  body_desc = full_body.find('div', {'class': body_desc_class})
  bdesc_text = ""
  if body_desc:
    bdesc_list = body_desc.contents
    #print(bdesc_list)
    for bdl_elem in bdesc_list:
      if str(bdl_elem) == "<br/>":
        bdesc_text += '\n'
        continue
      bdesc_text += str(bdl_elem).lstrip().rstrip() + ' '
  bdesc_text = bdesc_text.rstrip()
  #print(bdesc_text)
  bdesc_dict = {'requirements': bdesc_text}
  sect_val_dict.update(bdesc_dict)

  # stores all codes from section
  section_codes = []

  # check if there are collapsible sections
  collapsible_sect_class = 'AccordionItem css-1dfs90h-Box-CardBody e1q64pes0'
  collapsible_sects = full_body.find_all('div', {'class': collapsible_sect_class}, recursive=False)
  csects_dict = {}
  if collapsible_sects:
    csect_count = 0
    for csect in collapsible_sects:
      csect_count +=1
      # get header, subheader, contents and courses/specs from collapsible section
      csect_dict = process_csect(csect)
      csects_dict.update(csect_dict)
    # since collapsibles are all already processed, compile sect_dict and return early
    sect_val_dict.update(csects_dict)
    sect_dict = {sec_title: sect_val_dict}
    #print(json.dumps(sect_dict, indent=2))
    return sect_dict  
  
  # no collapsibles, just one body section in the 'blue box'
  no_collapsible_sect_class = 'css-tne7gz-StyledLinkGroup exq3dcx7'
  no_collapsible_sect = full_body.find('div', {'class': no_collapsible_sect_class})
  if no_collapsible_sect:
    ncsect_codes = get_course_codes_from_section(no_collapsible_sect)
    #print(ncsect_codes)
    section_codes += ncsect_codes

  # one body, but in list instead of block form
  list_display_sect_class = 'css-liz132-StyledLinkGroup exq3dcx7'
  list_display_sect = full_body.find('div', {'class': list_display_sect_class})
  if list_display_sect:
    ldsect_codes = get_course_codes_from_section(section)
    #print(ldsect_codes)
    section_codes += ldsect_codes
  
  #print(section_codes)
  sec_code_dict = {'courses': section_codes}
  sect_val_dict.update(sec_code_dict)
  
  sect_dict = {sec_title: sect_val_dict}
  #print(json.dumps(sect_dict, indent=2))

  return sect_dict

# collapsibles inside the 'blue box'
# specialisation scraper didnt need this because the 'blue boxes'' collapsibles
# are still part of the 'blue box' when it comes to course offereings
# however, programs have a 'disciplinary structure' section that have discrete
# entries which cannot be homogenised into one single list
def process_csect(csect):
  #print(csect.text)
  # course or spec list
  header_class = "css-1smylv8-Box-Flex"
  header = csect.find('div', {'class': header_class})
  header_title = "collapsible_title"
  header_uoc = ""
  if header:
    header_title = header.strong.text
    header_subtitle = header.small
    if header_subtitle:
      subtitle_line = header_subtitle.text.lstrip().rstrip()
      confirmed_uoc_line = re.search("[0-9]+ Units of Credit:$", subtitle_line)
      if confirmed_uoc_line:
        header_uoc = subtitle_line.split(' ')[0]
  #print(header_title + '\nuoc: ' + header_uoc)

  body_class = "css-1t185r9-SAccordionContentContainer e1450wuy10"
  body = csect.find('div', {'class': body_class})
  if not body:
    body_alt_class = "css-1chr68r-Box-SAccordionBody e1450wuy0"
    body = csect.find('div', {'class': body_alt_class})
  desc_text = ""
  if body:
    desc_text = parse_csect_desc(body)
  #print(desc_text)

  # check for collapsibles inside... the collapsible (jfc this is so cursed)
  collapsible_class = "AccordionItem css-1dfs90h-Box-CardBody e1q64pes0"
  yellow_button_class = "css-1td4qbd-Pill-Badge-css etsewye0"
  collapsibles = body.find_all('div', {'class': collapsible_class})
  collapsibles_exist = False
  one_list_only = False
  if collapsibles:
    collapsibles_exist = True
    if len(collapsibles) == 1:
      one_list_only = True
    for elem in collapsibles:  
      yellow_button = elem.find('span', {'class': yellow_button_class})
      if yellow_button:
        yb_text = yellow_button.text.lstrip().rstrip()
        if yb_text == "One of the following:":
          one_list_only = True

  # check if there are yellow(or grey) specialisation buttons
  button_bar_class = "css-1h5izuv-Box-Flex-FilterContainer-filters ebfvri70"
  button_bar = body.find('div', {'class': button_bar_class})
  list_key_name = "courses"
  spec_dict = {}
  if button_bar:
    yellow_button_class = "undefined active css-18a30wi-Pill-Badge-css etsewye0"
    grey_button_class = "undefined css-18a30wi-Pill-Badge-css etsewye0"
    active_button = button_bar.find('button', {'class': yellow_button_class})
    inactive_button = button_bar.find('button', {'class': grey_button_class})
    if active_button:
      list_key_name = active_button.text.lower()
      if list_key_name in ['major', 'minor']:
        list_key_name = list_key_name + 's'
      list_val_list = get_course_codes_from_section(body)
      spec_dict = {list_key_name: list_val_list}
    if inactive_button:
      list_key_name = inactive_button.text.lower() + 's'
      spec_dict.update({list_key_name: []})
  else:
    if collapsibles_exist:
      spec_dict = parse_ccollapsible(collapsibles, one_list_only)
    else:
      course_list = get_course_codes_from_section(body)
      spec_dict = {list_key_name: course_list}

  csect_dict_val = {'name': header_title}
  csect_dict_val.update({'uoc': header_uoc})
  csect_dict_val.update({'requirements': desc_text})
  csect_dict_val.update(spec_dict)
  csect_dict = {header_title: csect_dict_val}
  #print(json.dumps(csect_dict, indent=2))
  return csect_dict

# finds all 'blocks' under every collapsible blue box
def get_course_codes_from_section(section):
  sec_ccodes = []
  # block for specific course
  course_link_block_class = 'show css-vgk9p5-StyledLink-StyledAILink exq3dcx2'
  course_code_class = 'StyledAILinkHeaderSection__content1 css-1x19cd9-StyledAILinkHeaderSection exq3dcx4'
  course_link_blocks = section.find_all('a', {'class': course_link_block_class})
  for cl_block in course_link_blocks:
    course_code = cl_block.find('div', {'class': course_code_class})
    sec_ccodes.append(course_code.text)

  # 'any level X SUBJECT course'
  any_level_course_block_class = 'cs-item css-1sd39x-StyledLink-StyledAILink exq3dcx2'
  any_level_line_class = 'cs-item-description css-1ijziz0-Box'
  any_level_cblocks = section.find_all('a', {'class': any_level_course_block_class})
  for al_cblock in any_level_cblocks:
    any_level_line = al_cblock.find('div', {'class': any_level_line_class})
    sec_ccodes.append(any_level_line.text)

  # course in list element
  list_elem_class = 'show css-ubozre-StyledLink-StyledAILink exq3dcx2'
  list_elems = section.find_all('a', {'class': list_elem_class})
  le_code_class = 'css-1161ecq-StyledAILinkHeaderSection exq3dcx4'
  for list_elem in list_elems:
    le_code = list_elem.find('div', {'class': le_code_class})
    #print(le_code.text)
    sec_ccodes.append(le_code.text)


  return sec_ccodes

def parse_csect_desc(body):
  desc = ""
  for el in body.contents:
    if el.name == 'div':
      continue
    if el.name == 'br':
      desc += '\n'
      continue
    desc += el
  return desc

# get course list/groups from the collapsible inside the collapsible
def parse_ccollapsible(collapsibles, one_list_only):
  yellow_button_class = "css-1td4qbd-Pill-Badge-css etsewye0"
  c_list_dict = {}
  c_list = []
  for elem in collapsibles:  
    yellow_button = elem.find('span', {'class': yellow_button_class})
    if yellow_button:
      yb_text = yellow_button.text.lstrip().rstrip()
      # one of the following means that it's one cohesive course list
      if one_list_only:
        if yb_text == "One of the following:":
          pick_one_list = get_course_codes_from_section(elem)
          separator = ' | '
          choose_one = separator.join(pick_one_list)
          c_list.append(choose_one)
          continue
        else:
          section_list = get_course_codes_from_section(elem)
          c_list += section_list
      else:
        csect_courses = get_course_codes_from_section(elem)
        group_dict = {yb_text: csect_courses}
        c_list.append(group_dict)
  if one_list_only:
    c_list_dict = {'courses': c_list}
  else:
    c_list_dict = {'course_groups': c_list}
  return c_list_dict

def parse_psdesc(prog_strucure_desc):
  ps_desc = format_overview_text(prog_strucure_desc)
  ps_desc = re.sub('[\n]{3,}', '\n\n', ps_desc)
  return ps_desc