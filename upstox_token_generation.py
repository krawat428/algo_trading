#!/usr/bin/env python3
from upstox_api.api import *
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
import os

#password 2fa is date of year

api_key = ''
api_secret=''
usernam=''
password=''
password_2fa=''

def Code_extractor(code1):
    code1=code1
    code=''

    for i in code1[::-1]:
        if i == '=':
            code=code[::-1]
            break
        code+=i
    return(code)
def code_gen(current_url):
    element_present = EC.visibility_of_element_located((By.XPATH, '/html/body/form/fieldset/div[1]/div[1]/div[2]'))
    WebDriverWait(driver, 5).until(element_present)
    print("clicking ")
    driver.find_element_by_xpath('//*[@id="allow"]').click()
    print("clicked")
    WebDriverWait(driver, 30).until(EC.url_changes(current_url))
    print(driver.current_url)
    current_url=driver.current_url
    return(current_url)





s = Session(api_key)
s.set_redirect_uri('http://upstox.com:3000')
s.set_api_secret(api_secret)

url=s.get_login_url()
print(url)

options = Options()
options.add_argument("--headless")
driver = Chrome(chrome_options=options)
driver.get(url)


username = driver.find_element_by_xpath('//input[@id="name"]')
password = driver.find_element_by_xpath('//*[@id="password"]')
password2fa = driver.find_element_by_xpath('//*[@id="password2fa"]')
username.clear()
username.send_keys(username)
password.send_keys(password)
password2fa.send_keys(password2fa)

driver.find_element_by_xpath('/html/body/form/fieldset/div[3]/div/button').click()

current_url = driver.current_url
try:
    current_url=code_gen(current_url)
    
except TimeoutException:
    print("TimeOut")
    time.sleep(50)
    current_url=code_gen(current_url)
code=Code_extractor(current_url)
print(code)
driver.close()

s.set_code(code)
access_token = s.retrieve_access_token()

print(access_token)
with open('token.txt', 'w') as f:
    f.write(access_token)

#for Linux To free the occupied RAM
#os.system('killall -9 chromedriver')
