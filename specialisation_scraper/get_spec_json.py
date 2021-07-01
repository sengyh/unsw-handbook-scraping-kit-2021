from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import bs4
from fake_useragent import UserAgent
import time
import random
from pathlib import Path
import os

def process_spec(spec):
  specp_html = get_spec_page_html(spec)
  #print(fsp_html)
  #soup = bs4.BeautifulSoup(fsp_html, "lxml")
  #print(soup.prettify())
  return

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
  all_expand_buttons_xpath = "//button[@class='css-180fdj3-CallToActionButton-css evc83j21']"
  all_expand_buttons = driver.find_elements_by_xpath(all_expand_buttons_xpath)
  for expand_button in all_expand_buttons:
    expand_button.click()
    time.sleep(4)
  full_spec_page_xpath = "//div[@class='css-1m79oji-SLayoutContainer el608uh1']"
  Wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, full_spec_page_xpath)))
  full_spec_page = driver.find_element_by_xpath(full_spec_page_xpath)
  fsp_html = full_spec_page.get_attribute('outerHTML')
  
  return fsp_html

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
