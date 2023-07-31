from configparser import ConfigParser
import sys, os, time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def get_variables(group,variable):
    config = ConfigParser()
    current_os = os.getcwd()
    config.read(f"{current_os}\config.ini")
    return config.get(group, variable)

def get_chrome_driver():
    result = os.listdir(os.getcwd())
    return [word for word in result if 'hrome' in word][0]

def select_date_range(driver,date_picker,day,month,year):
    
    while f"{month} {year}" not in date_picker:
        driver.find_element(By.XPATH, '//button[contains(@aria-label,"Previous Month")]').click()
        date_picker =  driver.find_element(By.XPATH, '(//div[@class="react-datepicker__current-month"])[1]').text
    driver.find_element(By.XPATH, f'//div[contains(@aria-label,"{month} {day}")]').click()

def is_element_present(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return True
    except Exception as e:
        print("Element isn't present")

def click_element(driver,selector,path):
    element = driver.find_element(selector,path)
    driver.execute_script("arguments[0].click();", element)