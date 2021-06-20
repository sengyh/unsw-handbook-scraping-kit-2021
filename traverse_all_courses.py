from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def traverse_all_courses(browser, subject, codename):
  print(codename)
  subject_xpath = "//h4[contains(text(),'" + codename + "')]"
  subject_link = browser.find_element_by_xpath(subject_xpath)
  subject.click()
  #ActionChains(browser).move_to_element(subject_link).perform().click()
  Wait(browser, 5).until(EC.presence_of_element_located((By.ID, 'subject-Courses')))
  #subject-Courses

  # loop through with flag
  # get all courses first
  # if cant click on next button, break loop
  next_ten = True
  
  while next_ten:
    next_page_button = browser.find_element_by_id('pagination-page-next')
    print(next_page_button.get_attribute('outerHTML'))
    next_tens = next_page_button.is_enabled()

    course_link_xpath = "//a[@class='cs-list-item css-ubozre-StyledLink-StyledAILink exq3dcx2']"
    course_list = browser.find_elements_by_xpath(course_link_xpath)
    for course in course_list:
      course_code = course.find_element_by_css_selector('div.css-1161ecq-StyledAILinkHeaderSection.exq3dcx4').text
      print(course_code)
      #print(course.get_attribute('innerHTML'))
      print("\n")
    
    print(next_tens)
    if next_tens:
      #browser.execute_script("arguments[0].click();", next_page_button)
      #WebDriverWait(browser,1).until(EC.element_to_be_clickable((By.ID, 'pagination-page-next')))
      ActionChains(browser).move_to_element(next_page_button).click().perform()
      Wait(browser, 5).until(EC.visibility_of_element_located((By.ID, 'pagination-page-next')))
      print('bonk')
    else:
      break
    #break
      

  return