import sys, os, time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from functions import get_variables,get_chrome_driver,select_date_range,is_element_present,click_element

user = get_variables("JANEAPP.COM","user")
password = get_variables("JANEAPP.COM","password")
##FROM
from_day = get_variables("INF-TO-PROCESS","from_day")
from_month = get_variables("INF-TO-PROCESS","from_month")
from_year = get_variables("INF-TO-PROCESS","from_year")

##TO
to_day = get_variables("INF-TO-PROCESS","to_day")
to_month = get_variables("INF-TO-PROCESS","to_month")
to_year = get_variables("INF-TO-PROCESS","to_year")

##Account to process
account = get_variables("INF-TO-PROCESS","account")
screen = get_variables("SCREEN","available_to_view")

service = Service(executable_path=get_chrome_driver())
options = webdriver.ChromeOptions()

if (screen=="no"):options.add_argument('--headless=new')

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://mountainviewmassageandwellness.janeapp.com/admin")
driver.find_element(By.ID,'auth_key').send_keys(user)
driver.find_element(By.ID,'password').send_keys(password)
driver.find_element(By.ID,'log_in').click()
driver.get("https://mountainviewmassageandwellness.janeapp.com/admin#reports/accounts_receivable")
WebDriverWait(driver,timeout=10).until(lambda d: d.find_element(By.CLASS_NAME, "table-report"))

driver.find_element(By.XPATH, f'//a[text()="{account}"]').click()
WebDriverWait(driver,timeout=10).until(lambda d: d.find_element(By.XPATH, """//a[@class="toggle-filters"]"""))

time.sleep(5)
driver.find_element(By.XPATH, """//a[@class="toggle-filters"]""").click()
time.sleep(2)
driver.find_element(By.XPATH, '//a[text()="Select a Date Range..."]').click()
time.sleep(2)
driver.find_element(By.XPATH, '//div[@class="react-datepicker__current-month"]').click()

driver.find_element(By.XPATH, '//button[contains(@aria-label,"Next Month")]').click()
date_picker1 =  driver.find_element(By.XPATH, '(//div[@class="react-datepicker__current-month"])[1]').text
select_date_range(driver,date_picker1,to_day,to_month,to_year)
date_picker1 =  driver.find_element(By.XPATH, '(//div[@class="react-datepicker__current-month"])[1]').text
select_date_range(driver,date_picker1,from_day,from_month,from_year)

WebDriverWait(driver,timeout=10).until(lambda d: d.find_element(By.XPATH, '//div[@id="insurer_content"]/div'))

time.sleep(5)
payments_to_aprobe = 0
while 1==1:
    print(1)
    WebDriverWait(driver,timeout=10).until(lambda d: d.find_element(By.XPATH, '//div[@id="insurer_content"]/div'))
    time.sleep(1)
    print(2)
    if is_element_present(driver,By.XPATH,'//button[@class="btn btn-link hide-old load-more" and @style="display: inline-block;"]'):
        click_element(driver,By.XPATH,'//button[@class="btn btn-link hide-old load-more" and @style="display: inline-block;"]')
    print(3)
    if is_element_present(driver,By.XPATH,'//button[@class="btn btn-link hide-old load-more" and @style="display: none;"]'):
        payments_to_aprobe = len(driver.find_elements(By.XPATH,'//tbody[@class="purchases"]/tr'))
        break

print("payments =>",payments_to_aprobe)
for payment in range (payments_to_aprobe):
    if is_element_present(driver,By.XPATH,f'(//tbody[@class="purchases"]/tr)[{payment+1}]//strong[@class="submitted"]'):
        print(f"number {payment+1}" + driver.find_element(By.XPATH,f'(//tbody[@class="purchases"]/tr)[{payment+1}]//a[@class="sensitive"]').text)
        for diff_payment in range(len(driver.find_elements(By.XPATH,f'(//tbody[@class="purchases"]/tr)[{payment+1}]//a[@class="pay-and-approve"]'))):
            print(diff_payment+1)
            if is_element_present(driver,By.XPATH,f'(//tbody[@class="purchases"]/tr)[{payment+1}]//a[@class="pay-and-approve"]',1):
                print("click ")
                click_element(driver,By.XPATH,f'(//tbody[@class="purchases"]/tr)[{payment+1}]//a[@class="pay-and-approve"]')
                time.sleep(1)

    print("==============")

print("PROCESS FINISHED SUCCESSFULLY")