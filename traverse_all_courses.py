from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

from selenium.webdriver.support.wait import WebDriverWait

def traverse_all_courses(driver, subject, codename):
  print(codename)
  subject_xpath = "//h4[contains(text(),'" + codename + "')]"
  subject_link = driver.find_element_by_xpath(subject_xpath)
  driver.execute_script("arguments[0].click();", subject_link)
  Wait(driver, 5).until(EC.presence_of_element_located((By.ID, 'subject-Courses')))
  Wait(driver, 5).until(EC.presence_of_element_located((By.ID, 'pagination-page-next')))

  # loop through with flag
  # get all courses first
  # if cant click on next button, break loop
  next_ten = True
  last_page = False
  while next_ten:
    Wait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'pagination-page-next')))
    next_page_button = driver.find_element_by_id('pagination-page-next')
    #print(next_page_button.get_attribute('outerHTML'))
    next_ten = next_page_button.is_enabled()
    if next_ten:
      full_ten_traversal(driver)
      driver.execute_script("arguments[0].click();", next_page_button)
      time.sleep(1)  
    else:
      full_ten_traversal(driver)
      last_page_traversal(driver)
      go_back_to_subject_page(driver)
      break
  return

def full_ten_traversal(driver):
  course_link_xpath = "//a[@class='cs-list-item css-ubozre-StyledLink-StyledAILink exq3dcx2']"
  course_list = driver.find_elements_by_xpath(course_link_xpath)
  for course in course_list:
    course_code = course.find_element_by_css_selector('div.css-1161ecq-StyledAILinkHeaderSection.exq3dcx4').text
    print(course_code)
    print("\n")
  return

def last_page_traversal(driver):
  course_link_xpath = "//a[@class='cs-item css-vgk9p5-StyledLink-StyledAILink exq3dcx2']"
  course_list = driver.find_elements_by_xpath(course_link_xpath)
  for course in course_list:
    course_code = course.find_element_by_xpath(".//div[@class='StyledAILinkHeaderSection__content1 css-1x19cd9-StyledAILinkHeaderSection exq3dcx4']").text
    print(course_code)
    print("\n")
  return

def go_back_to_subject_page(driver):
  home_xpath = "//a[text()[contains(.,'Home')]]"
  home_link = driver.find_element_by_xpath(home_xpath)
  driver.execute_script("arguments[0].click();", home_link)
  time.sleep(1)
  subject_page_xpath = "//li[contains(@class, 'react-tabs__tab') and text()[contains(.,'By Subject Area')]]"
  WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,subject_page_xpath)))
  subject_link = driver.find_element_by_xpath(subject_page_xpath)
  subject_link.click()
  return