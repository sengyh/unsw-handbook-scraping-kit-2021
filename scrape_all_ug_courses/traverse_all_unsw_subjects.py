from .traverse_all_courses import traverse_all_courses
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random

def traverse_all_subjects(driver):
  
  #print(driver.page_source)
  # click the 'By Subject Area' tab
  subject_page_xpath = "//li[contains(@class, 'react-tabs__tab') and text()[contains(.,'By Subject Area')]]"
  subject_link = driver.find_element_by_xpath(subject_page_xpath)
  subject_link.click()
  # find all subject area links
  subject_list_xpath = "//a[contains(@href,'/browse/By Subject Area/')]/div[contains(@class,'css-14ezrsm-STileHeader e16r0ulu2')]"
  subject_list = driver.find_elements_by_xpath(subject_list_xpath)
  curr_url = driver.current_url
  print(curr_url)
  
  WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH,subject_list_xpath)))

  subject_nlist = []
  for subject in subject_list:
    subject_codename = subject.find_element_by_tag_name('h4').get_attribute('innerHTML')
    subject_nlist.append(subject_codename)

  i = 1
  start_here = False
  for subjectn in subject_nlist:
    subjectn = subjectn.replace('&amp;','&')
    sn_xpath = "//h4[contains(text(), '" + subjectn + "')]"
    #if (subjectn == "ZZEN: Engineering Accelerated"):
    #  start_here = True
    if start_here:
      subject_link = driver.find_element_by_xpath(sn_xpath)
      driver.execute_script("arguments[0].scrollIntoView(true);", subject_link)
      time.sleep(1.5)
      traverse_all_courses(driver, subject_link, subjectn)
      wait = random.randint(2,5)
      time.sleep(wait)
    i+=1
  return
 