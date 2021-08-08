from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from pathlib import Path
from process_soup_to_json import parse_ddeg_soup
import bs4
import time
import random
import os
import json

def process_ddeg(ddeg):
  ddeg_page_html = get_ddeg_page_html(ddeg)
  if (ddeg_page_html == "SHTF"):
    return "SHTF"
  soup = bs4.BeautifulSoup(ddeg_page_html, "lxml")
  #print(soup)
  ddeg_dict = parse_ddeg_soup(soup)
  print(json.dumps(ddeg_dict, indent=2))
  save_ddeg_page_html(ddeg, str(soup))
  time.sleep(random.randint(8,15))
  return ddeg_dict

def get_ddeg_page_html(ddeg):
  ddeg_url = "https://www.handbook.unsw.edu.au/undergraduate/programs/2021/" + ddeg
  driver = setup_driver()
  driver.get(ddeg_url)
  ddeg_full_body_xpath = "//div[@class='css-et39we-Box-Flex-Row-Row-Main e1gw5x5n1']"
  try:
    Wait(driver,30).until(EC.visibility_of_element_located((By.XPATH, ddeg_full_body_xpath)))
  except:
    print('shit hit the fan, aborting...')
    return "SHTF"
  time.sleep(4)
  # change from specialisation scraper, only clicks expand button 
  #   on overview and ddegram structure sections
  overview_section = driver.find_elements_by_xpath("//div[@id='Overview']")
  ddeg_structure_section = driver.find_elements_by_xpath("//div[@id='DoubleDegreeStructure']")
  all_clickable_sects = overview_section + ddeg_structure_section
  all_expand_buttons_xpath = ".//button[@class='css-180fdj3-CallToActionButton-css evc83j21']"
  for sec in all_clickable_sects:
    all_expand_buttons = sec.find_elements_by_xpath(all_expand_buttons_xpath)
    for expand_button in all_expand_buttons:
      driver.execute_script("arguments[0].scrollIntoView(true);", expand_button)
      time.sleep(1)
      driver.execute_script("arguments[0].click();", expand_button)
      time.sleep(3)
  # gets the whole html of the page to be souped and parsed
  full_ddeg_page_xpath = "//div[@class='css-1m79oji-SLayoutContainer el608uh1']"
  Wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, full_ddeg_page_xpath)))
  full_ddeg_page = driver.find_element_by_xpath(full_ddeg_page_xpath)
  fsp_html = full_ddeg_page.get_attribute('outerHTML')
  driver.quit()
  return fsp_html

def save_ddeg_page_html(ddeg, ddeg_html):
  ddeg_html_dir_path = Path.cwd() / '..' / '..' / 'data' / 'html' / 'double_degrees'
  if not ddeg_html_dir_path.exists():
    os.makedirs(ddeg_html_dir_path, exist_ok=True)
  ddeg_path = os.path.join(ddeg_html_dir_path, ddeg + '.html')
  sf = open(ddeg_path, 'w')
  sf.write(ddeg_html)
  sf.close()
  return

def setup_driver():
  OPTS = Options()
  ua = UserAgent()
  user_agent = ua.random
  OPTS.add_argument(f'user-agent={user_agent}')
  OPTS.add_argument("--window-size=1920,1080")
  #OPTS.add_argument("--headless")
  DRIVER_PATH = '../chromedriver'
  driver = Chrome(options=OPTS, executable_path=DRIVER_PATH)
  return driver
