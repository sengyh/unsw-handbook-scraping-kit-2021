from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from scrape_faculty_page import scrape_fac_page
import time
import random
from pathlib import Path
import os
import json

def faculty_scraper():
  driver = setup_driver()
  driver.get('https://www.handbook.unsw.edu.au')
  # click into faculty section
  fac_button_xpath = "//li[@class='react-tabs__tab' and text()='By Faculty']"
  Wait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH,fac_button_xpath)))
  fac_button = driver.find_element_by_xpath(fac_button_xpath)
  fac_button.click()
  # get all faculties and put names into list
  fac_list_xpath = "//ul[@class='css-stoukz-STileList e1axjz0v0']"
  Wait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH,fac_list_xpath)))
  fac_elem_xpath = fac_list_xpath + '//h4'
  fac_elems = driver.find_elements_by_xpath(fac_elem_xpath)
  fac_list = []
  for fac_e in fac_elems:
    fac_list.append(fac_e.text)
  
  # ['DVC (Academic) Board of Studies', 'Faculty of Arts, Design and Architecture', 'Faculty of Engineering', 'Faculty of Law and Justice', 'Faculty of Medicine and Health', 'Faculty of Science', 'UNSW Business School', 'UNSW Canberra at ADFA', 'UNSW Global']
  all_fac_dict = {}
  for fac in fac_list:
    Wait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH,fac_list_xpath)))
    fac_xpath = fac_elem_xpath + "[text()='" + fac + "']"
    fac_div = driver.find_element_by_xpath(fac_xpath)
    time.sleep(2)
    driver.execute_script("arguments[0].click();", fac_div)
    # inside faculty page, do some more scraping...
    fac_page_data = scrape_fac_page(driver)
    fac_page_data_dict = {fac: fac_page_data}
    print(fac_page_data_dict)
    print('\n')
    all_fac_dict.update(fac_page_data_dict)
    time.sleep(2)
    fac_button = driver.find_element_by_xpath(fac_button_xpath)
    fac_button.click()
  driver.quit()

  print('\n\n\n')
  print(all_fac_dict)
  print('\n\n\n')

  # write all faculty data to json file
  fac_file = Path.cwd() / '..' / '..' / 'data' / 'json' / 'all_faculties.json'
  with open(fac_file, 'w') as facf:
    json.dump(all_fac_dict, facf)
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


if __name__ == "__main__":
  faculty_scraper()