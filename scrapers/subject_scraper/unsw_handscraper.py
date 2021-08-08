from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import os
from traverse_all_unsw_subjects import traverse_all_subjects

def main():
  opts = Options()
  ua = UserAgent()
  user_agent = ua.random
  #print(user_agent)
  opts.add_argument(f'user-agent={user_agent}')
  #opts.add_argument("--headless")
  #opts.add_argument('--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"')
  opts.add_argument("--window-size=1920,1080")
  #assert opts.headless
  chrome_driver = os.getcwd() + '/../chromedriver'
  print(chrome_driver)
  

  driver = Chrome(options=opts, executable_path=chrome_driver)
  driver.get('https://www.handbook.unsw.edu.au')
  traverse_all_subjects(driver)
  driver.quit()

if __name__ == "__main__":
  main()