import calendar
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.safari.options import Options
import time
import tutorbird_helper as tb


class RevenueReportGenerator:
    def __init__(self, month, year):
        self.month = month
        self.year = year
        with open('constant_variables.json', 'r') as json_file:
            self.tutoring_constants = json.load(json_file)

        self.home_address = self.tutoring_constants["home_address"]
        self.business_report_address = self.tutoring_constants["business_report_address"]
        self.default_save_location = self.tutoring_constants["default_download_location"]
        self.username = self.tutoring_constants["login_username"]
        self.password = self.tutoring_constants["login_password"]

        self.output_file = f"monthly_revenue_{self.month}_{self.year}.csv"

        # set up autonomous browser and configure base driver
        options = Options()
        options.headless = True

        self.driver = webdriver.Safari(options=options)
        self.driver.maximize_window()

        self.start_date = ''
        self.end_date = ''

    def run(self):
        self.generate_start_end_date()
        self.generate_report()
        time.sleep(5)
        tb.rename_file(self.default_save_location, self.output_file)
        self.output_file = self.default_save_location + "/" + self.output_file

    def generate_start_end_date(self):
        # List of month names
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

        # Initialize an empty list to store key-value pairs
        month_days_list = []

        # Iterate over each month
        for month_idx, month_name in enumerate(months, start=1):
            # Get the number of days in the month
            num_days = calendar.monthrange(self.year, month_idx)[1]

            # Append the key-value pair to the list
            month_days_list.append((month_name, num_days))

        numerical_list = []
        for i, pair in enumerate(month_days_list, start=1):
            numerical_list.append((i, pair[1]))
        print(numerical_list)

        self.start_date = str(self.month) + "/1/" + str(self.year)
        self.end_date = str(self.month) + "/" + str(numerical_list[self.month-1][1]) + "/" + str(self.year)

        print("start date", self.start_date)
        print("end date", self.end_date)

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
        time.sleep(1)

        revenue_and_expenses = self.driver.find_element(By.ID, "mat-option-21")
        revenue_and_expenses.click()

        time.sleep(1)

        # select report format
        first_radio_button = self.driver.find_element(By.XPATH, "//label[@for='radioOptionID-mat-radio-1-input']")
        first_radio_button.click()

        # select report format
        second_radio_button = self.driver.find_element(By.XPATH, "//label[@for='radioOptionID-mat-radio-5-input']")
        second_radio_button.click()

        # select report format
        third_radio_button = self.driver.find_element(By.XPATH, "//label[@for='radioOptionID-mat-radio-12-input']")
        third_radio_button.click()

        start = "[aria-label='" + self.start_date + "']"
        end = "[aria-label='" + self.end_date + "']"

        # select the start date calendar
        calendar_start = self.driver.find_element(By.ID, "mat-input-0")
        calendar_start.click()
        time.sleep(0.5)
        # first check to see if the dates appear on the default calendar or if we need to switch tabs
        tb.switch_to_correct_date(self.driver, start, default_start="last_year_start")

        # select the first date
        first_date = self.driver.find_element(By.CSS_SELECTOR, start)
        first_date.click()
        time.sleep(0.5)

        # select the end date calendar
        calendar_end = self.driver.find_element(By.ID, "mat-input-1")
        calendar_end.click()
        time.sleep(0.5)

        tb.switch_to_correct_date(self.driver, end, default_start="last_year_end")
        # select the end date
        last_date = self.driver.find_element(By.CSS_SELECTOR, end)
        last_date.click()
        time.sleep(0.5)

        # submit the form
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//lib-legacy-button[@label="Create"]/div/button'))
        )
        submit_button.click()
        # wait for report to be created
        time.sleep(10)

        tb.download_most_recent_report(self.driver)

        tb.wait_for_download()
        self.driver.quit()


if __name__ == '__main__':
    month = 9
    year = 2024
    generator = RevenueReportGenerator(month, year)
    generator.run()
