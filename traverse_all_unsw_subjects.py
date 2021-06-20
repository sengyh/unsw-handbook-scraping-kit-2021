from traverse_all_courses import traverse_all_courses
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def traverse_all_subjects(browser):
  
  #print(browser.page_source)
  # click the 'By Subject Area' tab
  subject_page_xpath = "//li[contains(@class, 'react-tabs__tab') and text()[contains(.,'By Subject Area')]]"
  subject_link = browser.find_element_by_xpath(subject_page_xpath)
  subject_link.click()
  # find all subject area links
  subject_list_xpath = "//a[contains(@href,'/browse/By Subject Area/')]/div[contains(@class,'css-14ezrsm-STileHeader e16r0ulu2')]"
  subject_list = browser.find_elements_by_xpath(subject_list_xpath)
  curr_url = browser.current_url
  print(curr_url)
  
  WebDriverWait(browser, 5).until(EC.visibility_of_all_elements_located((By.XPATH,subject_list_xpath)))
  i = 0
  for subject in subject_list:
    if (i == 1):
      break
    subject_codename = subject.find_element_by_tag_name('h4').get_attribute('innerHTML')
    traverse_all_courses(browser, subject, subject_codename)
    i += 1

  return