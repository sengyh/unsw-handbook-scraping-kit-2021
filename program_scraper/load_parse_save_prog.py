from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from pathlib import Path
from process_soup_to_json import parse_prog_soup
import bs4
import time
import random
import os
import json

def process_prog(fac_code, prog):
  prog_page_html = get_prog_page_html(prog)
  if (prog_page_html == "SHTF"):
    return "SHTF"
  soup = bs4.BeautifulSoup(prog_page_html, "lxml")
  prog_dict = parse_prog_soup(soup)
  print(json.dumps(prog_dict, indent=2))
  save_prog_page_html(fac_code, prog, str(soup))
  time.sleep(random.randint(8,15))
  return prog_dict

def get_prog_page_html(prog):
  prog_url = "https://www.handbook.unsw.edu.au/undergraduate/programs/2021/" + prog
  driver = setup_driver()
  driver.get(prog_url)
  prog_full_body_xpath = "//div[@class='css-et39we-Box-Flex-Row-Row-Main e1gw5x5n1']"
  #try:
  Wait(driver,30).until(EC.visibility_of_element_located((By.XPATH, prog_full_body_xpath)))
  #except:
  #  print('shit hit the fan, aborting...')
  #  return "SHTF"
  time.sleep(4)
  # change from specialisation scraper, only clicks expand button 
  #   on overview and program structure sections
  overview_section = driver.find_elements_by_xpath("//div[@id='Overview']")
  prog_structure_section = driver.find_elements_by_xpath("//div[@id='ProgramStructure']")
  prog_rest_section = driver.find_elements_by_xpath("//div[@id='ProgramConstraints']")
  all_clickable_sects = overview_section + prog_structure_section + prog_rest_section
  all_expand_buttons_xpath = ".//button[@class='css-180fdj3-CallToActionButton-css evc83j21']"
  for sec in all_clickable_sects:
    all_expand_buttons = sec.find_elements_by_xpath(all_expand_buttons_xpath)
    for expand_button in all_expand_buttons:
      driver.execute_script("arguments[0].scrollIntoView(true);", expand_button)
      time.sleep(1)
      driver.execute_script("arguments[0].click();", expand_button)
      time.sleep(3)
  # gets the whole html of the page to be souped and parsed
  full_prog_page_xpath = "//div[@class='css-1m79oji-SLayoutContainer el608uh1']"
  Wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, full_prog_page_xpath)))
  full_prog_page = driver.find_element_by_xpath(full_prog_page_xpath)
  fsp_html = full_prog_page.get_attribute('outerHTML')
  driver.quit()
  return fsp_html

def save_prog_page_html(fac_code, prog, prog_html):
  prog_html_dir_path = Path.cwd() / '..' / 'data' / 'html' / 'programs' / fac_code
  if not prog_html_dir_path.exists():
    os.makedirs(prog_html_dir_path, exist_ok=True)
  prog_path = os.path.join(prog_html_dir_path, prog + '.html')
  sf = open(prog_path, 'w')
  sf.write(prog_html)
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
