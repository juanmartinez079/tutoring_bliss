import calendar
from datetime import datetime
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.safari.options import Options
import time
import tutorbird_helper as tb


class ActiveStudentReportGenerator:
    def __init__(self):
        month = datetime.now().month
        day = datetime.now().day
        year = datetime.now().year

        with open('constant_variables.json', 'r') as json_file:
            self.tutoring_constants = json.load(json_file)

        self.home_address = self.tutoring_constants["home_address"]
        self.students = self.tutoring_constants["student_view_address"]
        self.default_save_location = self.tutoring_constants["default_download_location"]
        self.username = self.tutoring_constants["login_username"]
        self.password = self.tutoring_constants["login_password"]

        self.output_file = f"current_student_stats_d{month}_{day}_{year}_.csv"

        # set up autonomous browser and configure base driver
        options = Options()
        options.headless = True

        self.driver = webdriver.Safari(options=options)
        self.driver.maximize_window()

    def run(self):
        self.generate_report()
        time.sleep(5)
        tb.rename_file(self.default_save_location, self.output_file)
        self.output_file = self.default_save_location + "/" + self.output_file

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
        self.driver.get(self.students)
        time.sleep(3)

        check_all = self.driver.find_element(By.ID, 'mat-checkbox-3')
        check_all.click()
        time.sleep(3)

        options_button = self.driver.find_element(By.XPATH, "//lib-menu-button[@tooltiptext='Select 1 or more "
                                                            "students']")
        options_button.click()
        time.sleep(3)

        download_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[p/text()="Download as Excel"]'))
        )
        download_button.click()

        tb.wait_for_download()
        self.driver.quit()


if __name__ == '__main__':
    generator = ActiveStudentReportGenerator()
    generator.run()
