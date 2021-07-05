import re
import json

def parse_spec_structure(spec_structure):
  if not spec_structure:
    return {'structure': {}}
  structure_val_dict = {}
  section_box_class = 'css-8x1vkg-Box-Card-EmptyCard-css-SAccordionContainer e1450wuy4'
  spec_struct_sects = spec_structure.find_all('div', {'class': section_box_class})
  #print('number of sections: ' + str(len(spec_struct_sects)))
  for section in spec_struct_sects:
    section_dict = parse_section(section) 
    structure_val_dict.update(section_dict)
    #print('\n\n')
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
  bdesc_dict = {'description': bdesc_text}
  sect_val_dict.update(bdesc_dict)

  # stores all codes from section
  section_codes = []

  # check if there are collapsible sections
  collapsible_sect_class = 'AccordionItem css-1dfs90h-Box-CardBody e1q64pes0'
  collapsible_sects = full_body.find_all('div', {'class': collapsible_sect_class})
  if collapsible_sects:
    for csect in collapsible_sects:
      #print(csect.text)
      csect_codes = get_course_codes_from_section(csect)
      if not csect.strong:
        continue
      if csect.strong.text == "One of the following:":
        separator = " | "
        csect_codes = [separator.join(csect_codes)]
      if csect.strong.text.split(' ')[0] == 'List':
        # spec that has this so far: ECONF1
        print('fucking list edge case')
        csect_codes += ['End of ' + csect.strong.text]
      #print(csect_codes)
      
      section_codes += csect_codes
  
  
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