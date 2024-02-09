from bs4 import BeautifulSoup
from datetime import datetime
import glob
import os
import re
from selenium.webdriver.common.by import By
import time


def get_current_html(driver):
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    print(soup.prettify())


def rename_file(save_location, output_name):
    # Specify the directory where the files are located
    directory = save_location

    # Get a list of all files in the directory
    files = glob.glob(os.path.join(directory, "*"))

    if not files:
        print("No files found in the directory.")
        return

    # Sort files by modification time to get the most recent one
    latest_file = max(files, key=os.path.getmtime)

    # Extract the file name
    file_name = os.path.basename(latest_file)

    # Rename the most recent file
    os.rename(latest_file, os.path.join(directory, output_name))

    print(f"File '{file_name}' has been renamed to '{output_name}'.")


def switch_to_correct_date(driver, date):
    # Regular expression pattern to match the date
    pattern = r"\d+/\d+/\d+"

    # Find all matches of the pattern in the input string
    matches = re.findall(pattern, date)

    # If there are matches, extract the first one
    if matches:
        date = matches[0]
        print("Extracted date:", date)
    else:
        print("No date found in the input string")
    date = datetime.strptime(date, "%m/%d/%Y")

    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year
    next_year_button = driver.find_element(By.ID, "iconButtonID-datePickerHeaderNextYearButton")
    last_year_button = driver.find_element(By.ID, "iconButtonID-datePickerHeaderPreviousYearButton")
    next_month_button = driver.find_element(By.ID, "iconButtonID-datePickerHeaderNextMonthButton")
    last_month_button = driver.find_element(By.ID, "iconButtonID-datePickerHeaderPreviousMonthButton")

    if date.year != current_year:
        diff = current_year - date.year
        print("difference in years: ", diff)
        # in the case that the input year is in the future
        if diff < 0:
            for i in range(abs(diff)):
                next_year_button.click()
                time.sleep(1)
        else:
            for i in range(abs(diff)):
                last_year_button.click()
                time.sleep(1)

    if date.month != current_month:
        diff = current_month - date.month
        print("difference in months: ", diff)
        # in the case that the input year is in the future
        if diff < 0:
            for i in range(abs(diff)):
                next_month_button.click()
                time.sleep(1)
        else:
            for i in range(abs(diff)):
                last_month_button.click()
                time.sleep(1)
