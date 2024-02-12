import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.safari.options import Options
import time
import tutorbird_helper as tb


def report_progress(message):
    print(message)


class PayrollReportGenerator:
    def __init__(self, start, end):
        self.start_date = start
        self.end_date = end
        with open('constant_variables.json', 'r') as json_file:
            self.tutoring_constants = json.load(json_file)

        self.home_address = self.tutoring_constants["home_address"]
        self.business_report_address = self.tutoring_constants["business_report_address"]
        self.default_save_location = self.tutoring_constants["default_download_location"]
        self.username = self.tutoring_constants["login_username"]
        self.password = self.tutoring_constants["login_password"]
        self.output_file = f"tutor_payroll_{self.start_date.replace('/', '_')} to {self.end_date.replace('/', '_')}.csv"

        # set up autonomous browser and configure base driver
        options = Options()
        options.headless = True

        self.driver = webdriver.Safari(options=options)
        self.driver.maximize_window()

    def run(self):
        self.generate_report()
        time.sleep(5)
        tb.rename_file(self.default_save_location, self.output_file)

    def generate_report(self):
        # first go home screen
        self.driver.get(self.home_address)
        # find the HTML elements that relate to log in info
        username_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "ctl00$ctl00$MainContent$contentBody$textboxEmail")))
        password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "ctl00$ctl00$MainContent$contentBody$textboxPassword")))
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'ctl00$ctl00$MainContent$contentBody$buttonLogin')))

        # Input your credentials and click login
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        # username_input.send_keys("crypworld2000@gmail.com")
        # password_input.send_keys("qwertQWERT1")
        submit_button.click()

        # wait for login to proceed, change if necessary
        time.sleep(5)

        # first, navigate to the business report section
        self.driver.get(self.business_report_address)
        time.sleep(2)

        # find the first dropdown to select report type and click
        custom_dropdown1 = self.driver.find_element(By.ID, 'mat-select-value-1')
        custom_dropdown1.click()
        time.sleep(2)

        # find the payroll option and click
        payroll = self.driver.find_element(By.ID, 'mat-option-20')
        payroll.click()
        time.sleep(2)
        # select the start date calendar
        calendar_start = self.driver.find_element(By.ID, "mat-input-0")
        calendar_start.click()
        time.sleep(1)

        # first, check to see if year is in the current year
        # then check if month is in current month

        # first configure stat/end date aria labels
        start = "[aria-label='" + self.start_date + "']"
        end = "[aria-label='" + self.end_date + "']"

        # first check to see if the dates appear on the default calendar or if we need to switch tabs
        tb.switch_to_correct_date(self.driver, start)

        # select the first date
        first_date = self.driver.find_element(By.CSS_SELECTOR, start)
        first_date.click()
        report_progress("selected first date")
        time.sleep(1)

        # select the end date calendar
        calendar_end = self.driver.find_element(By.ID, "mat-input-1")
        calendar_end.click()
        report_progress("selected end date")
        time.sleep(1)

        tb.switch_to_correct_date(self.driver, end)
        # select the end date
        last_date = self.driver.find_element(By.CSS_SELECTOR, end)
        last_date.click()
        time.sleep(1)

        # select the total hours
        # select the payroll details
        total_hours_label = self.driver.find_element(By.XPATH, "//label[@for='mat-checkbox-4-input']")
        total_hours_label.click()
        payroll_label = self.driver.find_element(By.XPATH, "//label[@for='mat-checkbox-5-input']")
        payroll_label.click()

        # select report format
        csv_report_label = self.driver.find_element(By.XPATH, "//label[@for='radioOptionID-mat-radio-2-input']")
        csv_report_label.click()
        time.sleep(0.5)

        # submit the form
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//lib-legacy-button[@label="Create"]/div/button'))
        )
        submit_button.click()
        report_progress("submited report")
        # wait for report to be created
        time.sleep(8)

        tb.download_most_recent_report(self.driver)
        tb.wait_for_download()

        self.driver.quit()


if __name__ == "__main__":
    start_date = '3/4/2021'
    end_date = '4/17/2024'
    generator = PayrollReportGenerator(start_date, end_date)
    generator.run()
