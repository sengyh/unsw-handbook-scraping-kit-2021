from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

from selenium.webdriver.support.wait import WebDriverWait

def traverse_all_courses(driver, subject, codename):
  print(codename)
  subject_xpath = "//h4[contains(text(),'" + codename + "')]"
  subject_link = driver.find_element_by_xpath(subject_xpath)
  driver.execute_script("arguments[0].click();", subject_link)
  Wait(driver,5)
  # entered subject courses page
  # check if there are any ug courses
  str = "We couldn't find anything for"
  str_xp = "//p[contains(text(),\"" + str + "\")]"
  try:
    Wait(driver,10).until(EC.visibility_of_element_located((By.XPATH, str_xp)))
    go_back_to_subject_page(driver)
    return
  except:
    pass
  #print(str_xp)


  # normal page w courses
  Wait(driver, 5).until(EC.presence_of_element_located((By.ID, 'subject-Courses')))
  one_page_only = False
  npb = driver.find_elements_by_id('pagination-page-next')
  #print(npb)
  if not npb:
    one_page_only = True
  else:
    Wait(driver, 5).until(EC.presence_of_element_located((By.ID, 'pagination-page-next')))

  # loop through with flag
  # get all courses first
  # if cant click on next button, break loop
  next_ten = True
  last_page = False
  while next_ten:
    if one_page_only is False:
      Wait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'pagination-page-next')))
      next_page_button = driver.find_element_by_id('pagination-page-next')
      next_ten = next_page_button.is_enabled()
    else:
      next_ten = False

    if next_ten:
      full_ten_traversal(driver)
      driver.execute_script("arguments[0].click();", next_page_button)
      time.sleep(1)  
    else:
      full_ten_traversal(driver)
      last_page_traversal(driver)
      go_back_to_subject_page(driver)
      time.sleep(4)
      break
    wait = random.randint(2,7)
    time.sleep(wait)
  return

def full_ten_traversal(driver):
  course_link_xpath = "//a[@class='cs-list-item css-ubozre-StyledLink-StyledAILink exq3dcx2']"
  course_list = driver.find_elements_by_xpath(course_link_xpath)
  for course in course_list:
    course_code = course.find_element_by_css_selector('div.css-1161ecq-StyledAILinkHeaderSection.exq3dcx4').text
    print(course_code)
  return

def last_page_traversal(driver):
  #print('last page')
  course_link_xpath = "//a[@class='cs-item css-vgk9p5-StyledLink-StyledAILink exq3dcx2']"
  course_list = driver.find_elements_by_xpath(course_link_xpath)
  for course in course_list:
    course_code = course.find_element_by_xpath(".//div[@class='StyledAILinkHeaderSection__content1 css-1x19cd9-StyledAILinkHeaderSection exq3dcx4']").text
    print(course_code)
  return

def go_back_to_subject_page(driver):
  home_xpath = "//a[text()[contains(.,'Home')]]"
  home_link = driver.find_element_by_xpath(home_xpath)
  time.sleep(1)
  driver.execute_script("arguments[0].click();", home_link)
  wait = random.randint(4,9)
  time.sleep(wait)
  subject_page_xpath = "//li[contains(@class, 'react-tabs__tab') and text()[contains(.,'By Subject Area')]]"
  WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,subject_page_xpath)))
  subject_link = driver.find_element_by_xpath(subject_page_xpath)
  subject_link.click()
  wait = random.randint(3,6)
  time.sleep(wait)
  return