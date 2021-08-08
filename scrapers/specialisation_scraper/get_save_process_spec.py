from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import bs4
from process_soup_to_json import parse_spec_soup
from fake_useragent import UserAgent
import time
import random
from pathlib import Path
import os

def process_spec(fac_code, spec):
  spec_page_html = get_spec_page_html(spec)
  if (spec_page_html == "SHTF"):
    return "SHTF"
  soup = bs4.BeautifulSoup(spec_page_html, "lxml")
  spec_dict = parse_spec_soup(soup)
  save_spec_page_html(fac_code, spec, str(soup))
  time.sleep(random.randint(7,12))
  return spec_dict

def get_spec_page_html(spec):
  spec_url = "https://www.handbook.unsw.edu.au/undergraduate/specialisations/2021/" + spec + "?year=2021"
  driver = setup_driver()
  driver.get(spec_url)
  spec_full_body_xpath = "//div[@class='css-et39we-Box-Flex-Row-Row-Main e1gw5x5n1']"
  try:
    Wait(driver,30).until(EC.visibility_of_element_located((By.XPATH, spec_full_body_xpath)))
  except:
    print('shit hit the fan, aborting...')
    return "SHTF"
  time.sleep(3)
  all_expand_buttons_xpath = "//button[@class='css-180fdj3-CallToActionButton-css evc83j21']"
  all_expand_buttons = driver.find_elements_by_xpath(all_expand_buttons_xpath)
  for expand_button in all_expand_buttons:
    driver.execute_script("arguments[0].scrollIntoView(true);", expand_button)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", expand_button)
    time.sleep(3)
  full_spec_page_xpath = "//div[@class='css-1m79oji-SLayoutContainer el608uh1']"
  Wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, full_spec_page_xpath)))
  full_spec_page = driver.find_element_by_xpath(full_spec_page_xpath)
  fsp_html = full_spec_page.get_attribute('outerHTML')
  driver.quit()
  return fsp_html

def save_spec_page_html(fac_code, spec, spec_html):
  spec_html_dir_path = Path.cwd() / '..' / '..' / 'data' / 'html' / 'specialisations' / fac_code
  if not spec_html_dir_path.exists():
    os.makedirs(spec_html_dir_path, exist_ok=True)
  spec_path = os.path.join(spec_html_dir_path, spec + '.html')
  sf = open(spec_path, 'w')
  sf.write(spec_html)
  sf.close()
  return

def setup_driver():
  OPTS = Options()
  ua = UserAgent()
  user_agent = ua.random
  OPTS.add_argument(f'user-agent={user_agent}')
  OPTS.add_argument("--window-size=1920,1080")
  OPTS.add_argument("--headless")
  DRIVER_PATH = '../chromedriver'
  driver = Chrome(options=OPTS, executable_path=DRIVER_PATH)
  return driver
