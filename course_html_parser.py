from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

#page = requests.get("https://www.handbook.unsw.edu.au/undergraduate/courses/2021/COMP9243")
#soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())

driver = webdriver.Chrome()
driver.get("https://www.handbook.unsw.edu.au/undergraduate/courses/2021/COMP9243")
Wait(driver, 10).until(EC.visibility_of_element_located((By.ID,"handbook")))
overview = driver.find_element_by_css_selector('div.css-9lgwr7-Box-Container-SContainer.el608uh0')
print(overview.get_attribute('outerHTML'))

time.sleep(5)
#html_source = driver.page_source
#print(html_source)

#handbook > div.css-9lgwr7-Box-Container-SContainer.el608uh0