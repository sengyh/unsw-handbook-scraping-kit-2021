from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import os
from traverse_all_unsw_subjects import traverse_all_subjects

def main():
  opts = Options()
  opts.add_argument("--headless")
  opts.add_argument("--start-maximized")
  #assert opts.headless
  chrome_driver = os.getcwd() + '/chromedriver'

  browser = Chrome(options=opts, executable_path=chrome_driver)
  browser.get('https://www.handbook.unsw.edu.au')
  traverse_all_subjects(browser)

if __name__ == "__main__":
  main()