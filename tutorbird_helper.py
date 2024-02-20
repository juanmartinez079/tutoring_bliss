from bs4 import BeautifulSoup
from datetime import datetime
import glob
import os
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import tkinter as tk
from tkinter import filedialog


def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename()  # Open file dialog
    return file_path


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


def switch_to_correct_date(driver, date, default_start="current"):
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

    if default_start == "current":
        # Get the current month and year
        current_month = datetime.now().month
        current_year = datetime.now().year
    elif default_start == "last_year_start":
        current_year = datetime.now().year - 1
        current_month = 1
    elif default_start == "last_year_end":
        current_year = datetime.now().year - 1
        current_month = 12

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
                time.sleep(0.1)
        else:
            for i in range(abs(diff)):
                last_year_button.click()
                time.sleep(0.1)

    if date.month != current_month:
        diff = current_month - date.month
        print("difference in months: ", diff)
        # in the case that the input year is in the future
        if diff < 0:
            for i in range(abs(diff)):
                next_month_button.click()
                time.sleep(0.1)
        else:
            for i in range(abs(diff)):
                last_month_button.click()
                time.sleep(0.1)


def download_most_recent_report(driver):
    # select the top option
    top_checkbox = driver.find_element(By.ID, 'checkboxID-selectCheckBox0')
    top_checkbox.click()
    time.sleep(1)

    # click options tab
    options = driver.find_element(By.ID, 'TeacherPortalInstructorsAdminsToolsMenuButton')
    options.click()
    time.sleep(1)

    download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[p/text()="Download"]'))
    )
    download_button.click()


def wait_for_download(timeout=20):
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
