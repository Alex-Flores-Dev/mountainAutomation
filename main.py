import sys, os, time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from functions import get_variables,get_chrome_driver,select_date_range,is_element_present,click_element,get_element_text_safely
from selenium.webdriver.support.ui import Select

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

service = Service(executable_path='chromedriver')
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
driver.find_element(By.XPATH, '//select[@name="invoice_state"]/option[text()="Submitted"]').click()

WebDriverWait(driver,timeout=10).until(lambda d: d.find_element(By.XPATH, '//div[@id="insurer_content"]/div'))

payments_to_aprobe = 0
while 1==1:
    WebDriverWait(driver,timeout=10).until(lambda d: d.find_element(By.XPATH, '//div[@id="insurer_content"]/div'))
    time.sleep(1)
    if is_element_present(driver,By.XPATH,'//button[@class="btn btn-link hide-old load-more" and @style="display: inline-block;"]'):
        click_element(driver,By.XPATH,'//button[@class="btn btn-link hide-old load-more" and @style="display: inline-block;"]')
    if is_element_present(driver,By.XPATH,'//button[@class="btn btn-link hide-old load-more" and @style="display: none;"]'):
        payments_to_aprobe = len(driver.find_elements(By.XPATH,'//tbody[@class="purchases"]/tr'))
        break
row=1
print("payments =>",payments_to_aprobe)
try:
    for payment in range (payments_to_aprobe):

        if get_element_text_safely(WebDriverWait(driver,timeout=10).until(lambda d: d.find_element(By.XPATH,f'((//tbody[@class="purchases"]/tr)[{row}]/td)[8]'))) == "$0.00":
            row = row + 1

        if is_element_present(driver,By.XPATH,f'(//tbody[@class="purchases"]/tr)[{row}]//strong[@class="submitted"]'):
            print(f"number {payment+1} " + get_element_text_safely(WebDriverWait(driver,timeout=10).until(lambda d: d.find_element(By.XPATH,f'(//tbody[@class="purchases"]/tr)[{row}]//a[@class="sensitive"]'))))
            for diff_payment in range(len(driver.find_elements(By.XPATH,f'(//tbody[@class="purchases"]/tr)[{row}]//a[@class="pay-and-approve"]'))):
                if is_element_present(driver,By.XPATH,f'(//tbody[@class="purchases"]/tr)[{row}]//a[@class="pay-and-approve"]',1):
                    click_element(driver,By.XPATH,f'(//tbody[@class="purchases"]/tr)[{row}]//a[@class="pay-and-approve"]')
                    time.sleep(5)
                    print("payed and approved")
                else:
                    time.sleep(5)
                    click_element(driver,By.XPATH,f'(//tbody[@class="purchases"]/tr)[{row+1}]//a[@class="pay-and-approve"]')
                    time.sleep(5)

        print("==============")
except Exception as e:
    print("PROCESS FINISHED WITH ERRORS")
print("PROCESS FINISHED SUCCESSFULLY")