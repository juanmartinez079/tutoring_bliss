import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.safari.options import Options
import time
import os


def generate_report(start_date, end_date):
    url = "https://app.tutorbird.com/Teacher/v2/en/home"
    # set up autonomous browser and configure base driver
    options = Options()
    options.headless = True

    driver = webdriver.Safari(options=options)
    driver.get(url)

    # find the HTML elements that relate to log in info
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "ctl00$ctl00$MainContent$contentBody$textboxEmail")))
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "ctl00$ctl00$MainContent$contentBody$textboxPassword")))
    submit_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'ctl00$ctl00$MainContent$contentBody$buttonLogin')))

    # Input your credentials
    username_input.send_keys('crypworld2000@gmail.com')
    password_input.send_keys('qwertQWERT1')

    submit_button.click()
    # wait for login to proceed, change if necessary
    time.sleep(5)

    # first, navigate to the business report section
    business_report_link = "https://app.tutorbird.com/Teacher/v2/en/reports/add"
    driver.get(business_report_link)
    time.sleep(2)

    # find the first dropdown to select report type and click
    custom_dropdown1 = driver.find_element(By.ID, 'mat-select-value-1')
    custom_dropdown1.click()
    time.sleep(2)

    # find the payroll option and click
    payroll = driver.find_element(By.ID, 'mat-option-20')
    payroll.click()
    time.sleep(2)
    # select the start date calendar
    calendar_start = driver.find_element(By.ID, "mat-input-0")
    calendar_start.click()
    time.sleep(1)

    # first, check to see if year is in the current year
    # then check if month is in current month

    # first configure stat/end date aria labels
    start = "[aria-label='" + start_date + "']"
    end = "[aria-label='" + end_date + "']"

    # select the first date
    first_date = driver.find_element(By.CSS_SELECTOR, start)
    first_date.click()
    report_progress("selected first date")
    time.sleep(1)

    # select the end date calendar
    calendar_start = driver.find_element(By.ID, "mat-input-1")
    calendar_start.click()
    report_progress("selected end date")
    time.sleep(1)
    # select the end date
    last_date = driver.find_element(By.CSS_SELECTOR, end)
    last_date.click()
    time.sleep(1)

    # select the total hours
    # select the payroll details
    total_hours_label = driver.find_element(By.XPATH, "//label[@for='mat-checkbox-4-input']")
    total_hours_label.click()
    payroll_label = driver.find_element(By.XPATH, "//label[@for='mat-checkbox-5-input']")
    payroll_label.click()

    # select report format
    csv_report_label = driver.find_element(By.XPATH, "//label[@for='radioOptionID-mat-radio-2-input']")
    csv_report_label.click()
    time.sleep(0.5)

    # submit the form
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//lib-legacy-button[@label="Create"]/div/button'))
    )
    submit_button.click()
    report_progress("submited report")
    # wait for report to be created
    time.sleep(8)

    # select the top option
    top_checkbox = driver.find_element(By.ID, 'checkboxID-selectCheckBox0')
    report_progress("got here")
    top_checkbox.click()
    time.sleep(1)

    # click options tab
    options = driver.find_element(By.ID, 'TeacherPortalInstructorsAdminsToolsMenuButton')
    options.click()
    time.sleep(3)

    # click download
    download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//lib-legacy-menu-item[@label="Download"]/div'))
    )
    download_button.click()

    wait_for_download()

    driver.quit()


def wait_for_download(timeout=60):

    start_time = time.time()
    downloads_dir = os.path.expanduser('~/Downloads')
    initial_files = set(os.listdir(downloads_dir))
    while time.time() - start_time < timeout:
        print("waiting for file to download...")
        current_files = set(os.listdir(downloads_dir))
        new_files = current_files - initial_files

        if new_files:
            return True

        time.sleep(1)  # Adjust the sleep duration based on your needs

    return False


def parse_HTML(script, keywords):
    pattern = r"<(.*?)>"
    str_html = str(script)
    substrings = re.findall(pattern, str_html)
    output = []
    for i, line in enumerate(substrings):
        if keywords in line:
            output.append(line)
    for line in output:
        print("<", line, ">")


def report_progress(message):
    print(message)


def get_current_html(driver):
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    parse_HTML(soup, 'Download')
    print(soup)


if __name__ == "__main__":
    # start_date = input("Enter start date: ")
    # end_date = input("Enter end date: ")
    start_date = '2/2/2024'
    end_date = '2/14/2024'
    generate_report(start_date, end_date)
