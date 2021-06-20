from traverse_all_courses import traverse_all_courses
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

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
  i = 0
  for subject in subject_list:
    WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH,subject_list_xpath)))
    #print(subject.get_attribute('innerHTML'))
    if (i == 3):
      break
    subject_codename = subject.find_element_by_tag_name('h4').get_attribute('innerHTML')
    #if (subject_codename != 'MATH: Mathematics'):
    #  continue
    traverse_all_courses(driver, subject, subject_codename)
    time.sleep(2)
    i += 1

  return