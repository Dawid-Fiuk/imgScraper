import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from urllib.parse import urljoin


#Enter your credentails for login and desired page url
LOGIN_URL = ""
TARGET_URL = ""
USERNAME = ""
PASSWORD = ""

def login_with_selenium(login_url, username, password):
    driver = webdriver.Chrome()
    driver.get(login_url)
    time.sleep(3)

    driver.find_element(By.ID, "user_login").send_keys(username)
    driver.find_element(By.ID, "user_pass").send_keys(password)
    driver.find_element(By.ID, "rememberme").click()
    driver.find_element(By.ID, "wp-submit").click()
    time.sleep(5)

    if "login" in driver.current_url.lower():
        print("Login failed. Please check your credentials.")
        driver.quit()
        return None

    print("Login successful.")
    return driver

def scrape_images(driver, target_url, folder_name):
    driver.get(target_url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    img_tags = soup.find_all('img')
    for idx, img_tag in enumerate(img_tags, start=1):
        img_url = extract_img_url(img_tag, target_url)
        if img_url:
            save_image(img_url, folder_name, idx)

    print(f"Downloaded all images to folder: {folder_name}")

def extract_img_url(img_tag, base_url):
    return urljoin(base_url, img_tag.get('src') or img_tag.get('data-src') or img_tag.get('data-lazy-src'))

def save_image(img_url, folder_name, idx):
    try:
        response = requests.get(img_url, stream=True)
        response.raise_for_status()
        ext = os.path.splitext(img_url)[1] or ".jpg"
        filename = os.path.join(folder_name, f"{idx}{ext}")
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Could not download {img_url}. Reason: {e}")

def main():
    driver = login_with_selenium(LOGIN_URL, USERNAME, PASSWORD)
    if driver:
        scrape_images(driver, TARGET_URL,
                      "new_folder_name")

        driver.quit()

if __name__ == "__main__":
    main()
