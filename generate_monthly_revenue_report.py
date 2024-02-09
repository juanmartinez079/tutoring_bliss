from bs4 import BeautifulSoup
from datetime import datetime
import json
import glob
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.safari.options import Options
import time
import tutorbird_helper as tb
import os

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

        tb.get_current_html(self.driver)

        # # find the revenue and expenses option and click
        # revenue_and_expenses = self.driver.find_element(By.ID, 'mat-option-20')
        # revenue_and_expenses.click()
        # time.sleep(2)


