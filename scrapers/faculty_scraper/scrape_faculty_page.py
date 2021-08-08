from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random

def scrape_fac_page(driver):
  # //div[@class='e5gsavw0 css-1nc6plk-StyledLinkGroup-LinkGroup-css exq3dcx7']
  faculty_data_dict = {}

  full_body_xpath = "//div[@class='css-kew50s el3esdr0']"
  Wait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, full_body_xpath)))

  # get faculty name and description
  fac_header_dict = scrape_fp_header(driver)
  faculty_data_dict.update(fac_header_dict)
  time.sleep(1)

  full_sec_xpath = "//div[@class='browse-tab-content']"
  fps_list = driver.find_elements_by_xpath(full_sec_xpath)
  
  fpsname_list = []
  fps_names = driver.find_elements_by_xpath(full_sec_xpath + '//h3')
  for fps_name in fps_names:
    fpsname_list.append(fps_name.text)
  #print(fpsname_list)

  fac_body_dict = traverse_fpage_sections(fps_list, driver)
  faculty_data_dict.update(fac_body_dict)
  #print(faculty_data_dict)

  time.sleep(5)
  driver.back()
  return faculty_data_dict

def scrape_fp_header(driver):
  header_xpath = "//div[@class='css-1uws9aw-Box']"
  header = driver.find_element_by_xpath(header_xpath)
  fac_name = header.find_element_by_xpath(".//h2").text
  #print(fac_name)
  fac_desc = header.find_element_by_xpath(".//p").text
  #print(fac_desc)
  fac_header_dict = {'name': fac_name, 'overview': fac_desc}
  #print(fac_header_dict)
  return fac_header_dict

    # use './/' for relative search from particular element
  #['Programs', 'Double Degrees', 'Specialisations']
def traverse_fpage_sections(fps_list, driver):
  fac_page_dict = {}
  page_section_list = ['Programs', 'Double Degrees', 'Specialisations']
  for fps in fps_list:
    fps_dict = None
    page_section = fps.find_element_by_tag_name('h3').text
    if (page_section == 'Courses'):
      continue
    #print(page_section)
    if (page_section == 'Specialisations'):
      spec_dict = get_all_specialisation_types(fps, driver)
      fps_dict = {page_section: spec_dict}
    else:
      fps_elems = get_all_elements_inside_section(fps, driver)
      fps_dict = {page_section: fps_elems}
    #print(fps_dict)
    fac_page_dict.update(fps_dict)
  #print(fac_page_dict)
  return fac_page_dict

def get_all_specialisation_types(fps, driver):
  #print('currently in major section...')
  major_elems = get_all_elements_inside_section(fps, driver)
  #print(major_elems)
  spec_dict = {'Major': major_elems}

  minor_button_xpath = ".//span[@class='eruw9rv2 css-5tf4o9-Pill-Badge-css-SFilterBadge etsewye0' and text()='Minor']"
  minor_exists = fps.find_elements_by_xpath(minor_button_xpath)
  if minor_exists:
    minor_button = fps.find_element_by_xpath(minor_button_xpath)
    driver.execute_script("arguments[0].click();", minor_button)
    time.sleep(5)
    minor_elems = get_all_elements_inside_section(fps, driver)
    #print(minor_elems)
    spec_dict.update({'Minor': minor_elems})
  else: 
    spec_dict.update({'Minor': []})
    print('fuck you canberra\n')
  
  honours_button_xpath = ".//span[@class='eruw9rv2 css-5tf4o9-Pill-Badge-css-SFilterBadge etsewye0' and text()='Honours']"
  honours_button = fps.find_element_by_xpath(honours_button_xpath)
  driver.execute_script("arguments[0].click();", honours_button)
  time.sleep(5)
  honours_elems = get_all_elements_inside_section(fps, driver)
  #print(honours_elems)
  spec_dict.update({'Honours': honours_elems})
  #print(fps_dict)
  return spec_dict

  
def get_all_elements_inside_section(fps, driver):
  next_ten_button_xpath = ".//button[@id='pagination-page-next']"
  next_button_exists = fps.find_elements_by_xpath(next_ten_button_xpath)
  all_elements = []
  if not next_button_exists:
    #print("only one subpage")
    all_elements += traverse_ten_list(fps)
    time.sleep(5)
  else:
    #print('pagination exists')
    next_button = fps.find_element_by_xpath(next_ten_button_xpath)
    next_page = True
    while next_page:
      all_elements += traverse_ten_list(fps)
      next_button = fps.find_element_by_xpath(next_ten_button_xpath)   
      button_is_clickable = next_button.is_enabled()
      if not button_is_clickable:
        next_page = False
      else:
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(5)
  #print(all_elements)
  return all_elements

def traverse_ten_list(fps):
  ten_element_block_xpath = ".//div[@class='css-1161ecq-StyledAILinkHeaderSection exq3dcx4']"
  ten_codes = []
  ten_element_list = fps.find_elements_by_xpath(ten_element_block_xpath)
  if not ten_element_list:
    ten_codes = traverse_blocks(fps)
  else:
    for el in ten_element_list:
      #print(el.text)
      ten_codes.append(el.text)
  return ten_codes

def traverse_blocks(fps):
  single_block_xpath = ".//div[@class='StyledAILinkHeaderSection__content1 css-1x19cd9-StyledAILinkHeaderSection exq3dcx4']"
  ten_less_codes = []
  tenless_element_list = fps.find_elements_by_xpath(single_block_xpath)
  for el in tenless_element_list:
    #print(el.text)
    ten_less_codes.append(el.text)
  return ten_less_codes


  