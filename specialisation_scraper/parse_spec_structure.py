def parse_spec_structure(spec_structure):
  section_box_class = 'css-8x1vkg-Box-Card-EmptyCard-css-SAccordionContainer e1450wuy4'
  spec_struct_sects = spec_structure.find_all('div', {'class': section_box_class})
  print('number of sections: ' + str(len(spec_struct_sects)))
  for section in spec_struct_sects:
    parse_section(section) 
    print('\n\n')
  return

# inside the 'blue box'
def parse_section(section):
  # obtains requirement section title and uocs from section header
  header_class = 'css-1wt42lu-Box-Flex-SAccordionHeader-css e1450wuy5'
  header = section.find('div', {'class': header_class})
  req_title = header.strong.text
  req_uoc = ""
  print(req_title)
  if header.small:
    req_uoc = header.small.text
  print(req_uoc)

  # start parsing body section
  full_body_class = 'css-10hsoix-SAccordionRegion e1450wuy11'
  body_desc_class = 'css-127bpwp-Box-SAccordionDescription-css e1450wuy7'
  full_body = section.find('div', {'class': full_body_class})
  body_desc = full_body.find('div', {'class': body_desc_class})
  bdesc_text = ""
  if body_desc:
    bdesc_text = body_desc.text
  print(bdesc_text)

  collapsible_sect_class = 'AccordionItem css-1dfs90h-Box-CardBody e1q64pes0'
  # check if there are collapsible sections
  collapsible_sects = full_body.find_all('div', {'class': collapsible_sect_class})
  print(len(collapsible_sects))
  if collapsible_sects:
    for csect in collapsible_sects:
      csect_codes = get_course_codes_from_section(csect)
      if csect.strong.text == "One of the following:":
        print('choose one')
        separator = " | "
        csect_codes = [separator.join(csect_codes)]
      print(csect_codes)
  
  # no collapsibles, just one body section in the 'blue box'
  no_collapsible_sect_class = 'css-tne7gz-StyledLinkGroup exq3dcx7'
  no_collapsible_sect = full_body.find('div', {'class': no_collapsible_sect_class})
  if no_collapsible_sect:
    ncsect_codes = get_course_codes_from_section(no_collapsible_sect)
    print(ncsect_codes)

  # one body, but in list instead of block form
  list_display_sect_class = 'css-liz132-StyledLinkGroup exq3dcx7'
  list_display_sect = full_body.find('div', {'class': list_display_sect_class})
  if list_display_sect:
    ldsect_codes = get_course_codes_from_section(section)
    print(ldsect_codes)
      #print(csect.prettify())
      #print('\nwoop\n')



  return

  #   any_level_course_block_class = 'cs-item css-1sd39x-StyledLink-StyledAILink exq3dcx2'

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