import csv
import sys
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
import os
import conf as conf

from gtts import gTTS
from playsound import playsound

user = conf.LKD_USERNAME
pwd = conf.LKD_PASS

writer = csv.writer(open('final.csv', 'w'))
writer.writerow(['name', 'linkedin', 'site', 'description', 'phone', 'company_size'])

driver = webdriver.Chrome('chromedriver.exe')

driver.get('https://www.linkedin.com/')

time.sleep(1)

driver.find_element_by_xpath('//a[text()="Sign in"]').click()
time.sleep(1)
username_input = driver.find_element_by_name('session_key')
username_input.send_keys(user)

password_input = driver.find_element_by_name('session_password')
password_input.send_keys(pwd)
time.sleep(1)


driver.find_element_by_xpath('//button[text()="Sign in"]').click()

with open('name_list.csv') as f:

    readCSV = csv.reader(f, delimiter=',')

    for c in readCSV:

        name = str(c[0])
        
        pausa = np.random.randint(3, size=1)[0]+1

        time.sleep(pausa)

        print('Scraping ', name)

        driver.get('https://www.google.com/')

        search_input = driver.find_element_by_name('q')

        search_input.send_keys(f'site:linkedin.com/company/ AND "{name}"')

        search_input.send_keys(Keys.RETURN)

        profiles = driver.find_elements_by_xpath('//*[@class="r"]/a[1]')
        profiles = [profile.get_attribute('href') for profile in profiles]

        try:
            profile = profiles[0] + '/about/'

            pausa = np.random.randint(6, size=1)[0]+1

            time.sleep(pausa)

            driver.get(profile)

            time.sleep(1)
        except: 
            pass

        sel = Selector(text=driver.page_source)

        site = ''
        try:
            site = driver.find_element_by_css_selector("a[data-control-name='page_details_module_website_external_link']")
            site = site.get_attribute('href')
        except:
            pass        
        
        phone = ''
        try:
            phone = driver.find_element_by_css_selector("a[data-control-name='page_details_module_phone_external_link']")
            phone = phone.get_attribute('href')
        except:
            pass

        company_size = ''
        try:
            company_size = driver.find_element_by_tag_name("dd[class*'org-about-company-module__company-size-definition-text']/text()")
        except:
            pass

        text = '' 
        
        row = [name, str(profile), str(site), str(text), str(phone), str(company_size)]

        print('   ', row)

        writer.writerow(row)

driver.quit()