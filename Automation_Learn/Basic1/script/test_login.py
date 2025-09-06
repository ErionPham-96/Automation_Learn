from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import pytest
import csv

# Reading login data from CSV file by pandas
def read_login_data(file_path):
    credentials = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            credentials.append((row['username'], row['password']))
    return credentials

# Creating test case for login function
@pytest.mark.parametrize("username,password", read_login_data("./Automation_Learn/Basic1/data/login_data.csv"))

def test_login(username,password):
    #get the driver
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.google.com/")   # Getting the URL
        wait = WebDriverWait(driver, 10)  # Explicit wait to check the element is displayed or not to execute next step
        driver.maximize_window()  # Maximizing the window
        
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login") # Practice
        driver.back()  # Navigate back to the previous page
        driver.forward()  # Navigate forward to the next page
        
        username_input = wait.until(ec.presence_of_element_located((By.NAME, "username")))   # Selecting locator for username
        username_input.send_keys(username)  
        password_input = wait.until(ec.presence_of_element_located((By.NAME, "password")))   # Selecting locator for password
        password_input.send_keys(password)

        login = wait.until(ec.presence_of_element_located((By.XPATH, "//button[@type = 'submit']")))   # Selecting locator before enter login button
        login.click()

        # Ensure a successful login by checking an element that consistently appears and is unlikely to change or move in the future
        check_login = wait.until(ec.presence_of_element_located((By.XPATH, "//button[contains(@class,'orangehrm-upgrade-button')]")))  
        print("Login Succssful: Upgrade button is displayed", check_login.is_displayed())
    except Exception as e:
        print("Error: ", e)
    finally:
        driver.quit()