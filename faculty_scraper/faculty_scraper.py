from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import time
import random

def faculty_scraper():
  driver = setup_driver()
  driver.get('https://www.handbook.unsw.edu.au')
  # click into faculty section
  fac_button_xpath = "//li[@class='react-tabs__tab' and text()='By Faculty']"
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
  print(fac_list)
  for fac in fac_list:
    Wait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH,fac_list_xpath)))
    fac_xpath = fac_elem_xpath + "[text()='" + fac + "']"
    fac_div = driver.find_element_by_xpath(fac_xpath)
    time.sleep(2)
    driver.execute_script("arguments[0].click();", fac_div)
    time.sleep(5)
    driver.back()
    time.sleep(2)
    fac_button = driver.find_element_by_xpath(fac_button_xpath)
    fac_button.click()
    print(fac_xpath)



  driver.quit()
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