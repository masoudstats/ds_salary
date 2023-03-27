from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

option = Options()
option.headless = True
driver = webdriver.Firefox(executable_path="D://projects//ds_salary//geckodriver", options=option)

driver.get("https://www.glassdoor.com/Job/")

search_element = driver.find_element(By.ID, 'sc.keyword')
search_element.send_keys('data science')
search_element.send_keys(Keys.ENTER)
time.sleep(6)

number_pages = driver.find_element(By.XPATH, "//div[@class = 'paginationFooter']").text
idx = number_pages.find('f')
pages = int(number_pages[idx+1:])
time.sleep(5)

name = []
job_title = []
salary_est = []
location = []
year = []
revenue = []
employee = []
sector = []

page = 1
while page <= pages:
   
    list_item = driver.find_elements(By.XPATH, "//div/ul[@class='hover p-0 my-0  css-7ry9k1 exy0tjh5']/li")
    time.sleep(3)

    for item in list_item:
        try:
            name.append(item.find_element(By.XPATH, ".//div[2]/div[1]/a").text)
        except NoSuchElementException:
            name.append("NaN")

        try:        
            job_title.append(item.find_element(By.XPATH, ".//div[2]/a").text)
        except NoSuchElementException:
            job_title.append("NaN")    

        try:
            salary_est.append(item.find_element(By.XPATH, ".//div[2]/div[3]/div[1]/span").text)
        except NoSuchElementException:
            salary_est.append("NaN") 

        try:
            location.append(item.find_element(By.XPATH, ".//div[contains(@class, 'e1rrn5ka2')]/span").text)
        except NoSuchElementException:
            location.append("NaN") 


        item.click()
        time.sleep(3)

        #close pop-up
        try:
            driver.find_element(By.XPATH, "//span[@class='SVGInline modal_closeIcon']").click()
        except NoSuchElementException:
            pass


        try:
            year.append(driver.find_element(By.XPATH, ".//div[contains(@class, 'e1pvx6aw0')]/span[text()='Founded']/following-sibling::span").text)
        except NoSuchElementException:
            year.append("NaN")

        try:
            revenue.append(driver.find_element(By.XPATH, ".//div[contains(@class, 'e1pvx6aw0')]/span[text()='Revenue']/following-sibling::span").text)
        except NoSuchElementException:
            revenue.append("NaN")

        try:
            employee.append(driver.find_element(By.XPATH, ".//div[contains(@class, 'e1pvx6aw0')]/span[text()='Size']/following-sibling::span").text)
        except NoSuchElementException:
            employee.append("NaN")
        
        try:
            sector.append(driver.find_element(By.XPATH, ".//div[contains(@class, 'e1pvx6aw0')]/span[text()='Sector']/following-sibling::span").text)
        except NoSuchElementException:
            sector.append("NaN")

    
    
    #next page
    print('page ' + str(page) + ' is done!')
    driver.find_element(By.XPATH, "//span[@alt='next-icon']").click()
    time.sleep(6)

    page+=1

driver.close()

df = pd.DataFrame({ 
    'name': name,
    'year': year,
    'revenue': revenue,
    'employee': employee,
    'sector': sector,
    'job_title': job_title,
    'location': location,
    'salary_est': salary_est,
})

df.to_csv('ds_salary_2023.csv', index=False)
