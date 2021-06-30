from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random

def scrape_fac_page(driver):
  # //div[@class='e5gsavw0 css-1nc6plk-StyledLinkGroup-LinkGroup-css exq3dcx7']
  full_body_xpath = "//div[@class='css-kew50s el3esdr0']"
  Wait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, full_body_xpath)))
  full_sec_xpath = "//div[@class='browse-tab-content']"
  fps_list = driver.find_elements_by_xpath(full_sec_xpath)
  
  # skip Courses section
  fpsname_list = []
  fps_names = driver.find_elements_by_xpath(full_sec_xpath + '//h3')
  for fps_name in fps_names:
    fpsname_list.append(fps_name.text)
  print(fpsname_list)

  traverse_fpage_sections(fps_list, driver)
  time.sleep(5)
  driver.back()

  
  return

def traverse_fpage_sections(fps_list, driver):
  ps_body_xpath = "//div[@class='e5gsavw0 css-1nc6plk-StyledLinkGroup-LinkGroup-css exq3dcx7']"
  print(len(fps_list))
  for fps in fps_list:
    page_section = fps.find_element_by_tag_name('h3').text
    if (page_section == 'Courses'):
      continue
    print(page_section)
    # use './/' for relative search from particular element
    get_all_elements_inside_section(fps, driver)


  
def get_all_elements_inside_section(fps, driver):
  # check if there is page next button and is not disabled
  # check if the 10-list elements exist
  # check if there are singular prog 'boxes'
  ten_element_block_xpath = ".//div[@class='css-1ww1yyg-LinkGroupWrapper exq3dcx9']//div[@class='css-1161ecq-StyledAILinkHeaderSection exq3dcx4']"
  nav_footer_xpath = ".//div[@class='PaginationFooter css-4onoth-SPaginatorFooter-css eruw9rv3']"
  ten_element_list = fps.find_elements_by_xpath(ten_element_block_xpath)
  if not ten_element_list:
    print('oops, no ten element block here!')
  else:
    for el in ten_element_list:
      print(el.text)
  return
    

  return

  