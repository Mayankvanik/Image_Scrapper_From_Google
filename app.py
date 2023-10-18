from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
import requests
from PIL import Image
import base64

# Define constants
CHROME_DRIVER_PATH = 'C:/Users/mayan/Desktop/New folder/chromedriver.exe'
IMAGE_FOLDER = 'image_data'
search_query = 'green line on mobile screen'
image_size_filter = 'isz:l'
search_url = f"https://www.google.com/search?q={search_query}&tbm=isch&{image_size_filter}"
max_scroll_attempts = 20  # Set the maximum number of scroll attempts

# Create the image folder if it doesn't exist
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# Set up ChromeOptions and ChromeService
chrome_options = Options()
chrome_service = Service(CHROME_DRIVER_PATH)

# Create a Chrome driver with the service and options
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

try:
    driver.get(f'https://www.google.com/search?q={search_query}&tbm=isch')

    # Scroll down the page to load more images
    for _ in range(max_scroll_attempts):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(2)

    # Find image elements using XPath
    image_elements = driver.find_elements(By.XPATH, "//img[contains(@src, 'http')]")

    # Download and save images
    for count, image_element in enumerate(image_elements, start=1):
        src = image_element.get_attribute('src')
        if 'http' in src:
            image_name = f'{count}_{search_query.replace(" ", "_")}.jpeg'
            file_path = os.path.join(IMAGE_FOLDER, image_name)
            try:
                response = requests.get(src, timeout=10)
                if response.status_code == 200:
                    with open(file_path, 'wb') as image_file:
                        image_file.write(response.content)
                    img = Image.open(file_path)
                    img = img.convert('RGB')
                    img.save(file_path, 'JPEG')
                    print(f'Image saved: {file_path}')
                else:
                    print(f'Failed to download image: {src}')
            except Exception as e:
                print(f'Error while downloading image: {e}')
        else:
            print(f'Skipped invalid image source: {src}')

finally:
    # Close the WebDriver
    driver.quit()
