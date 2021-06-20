from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import os
from traverse_all_unsw_subjects import traverse_all_subjects

def main():
  opts = Options()
  #opts.add_argument("--headless")
  opts.add_argument("--window-size=1920,1080")
  #assert opts.headless
  chrome_driver = os.getcwd() + '/chromedriver'

  driver = Chrome(options=opts, executable_path=chrome_driver)
  driver.get('https://www.handbook.unsw.edu.au')
  traverse_all_subjects(driver)
  driver.quit()

if __name__ == "__main__":
  main()