# Packages
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException

# Config
login_time = 30                 # Time for login (in seconds)
new_msg_time = 20               # TTime for a new message (in seconds)
send_msg_time = 5               # Time for sending a message (in seconds)
country_code = 91               # Set your country code
action_time = 5                 # Set time for button click action
image_path = '/Users/parakhagrawal/Downloads/WhatsApp Image 2024-01-01 at 8.09.31 PM.jpeg'        # Absolute path to you image

# Create driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Encode Message Text
#with open('message.txt', 'r') as file:
#    msg = file.read()

# Open browser with default link
link = 'https://web.whatsapp.com'
driver.get(link)
time.sleep(login_time)

# Loop Through Numbers List
with open('numbers.txt', 'r') as numbers_file, open('names.txt', 'r') as names_file:
    for num, name in zip(numbers_file, names_file):
        num = num.rstrip()
        name = name.rstrip()
        link = f'https://web.whatsapp.com/send/?phone={country_code}{num}'
        driver.get(link)
        time.sleep(new_msg_time)
        # Click on button to load the input DOM
        if(image_path):
            try:
                attach_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]')))
                attach_btn.click()
                time.sleep(action_time)
                # Find and send image path to input
                msg_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/ul/div/div[2]/li/div/input')))
                msg_input.send_keys(image_path)
                time.sleep(action_time)
            except TimeoutException:
                print("Timeout occurred while waiting for element.")
            except ElementNotInteractableException:
                print("Element is not interactable. Check element state and adjust interaction method if necessary.")
        # Writing Message
        msg = "HEllo, {} this is auto generated message.".format(name)
        # Start the action chain to write the message
        actions = ActionChains(driver)
        for line in msg.split('\n'):
            actions.send_keys(line)
            # SHIFT + ENTER to create next line
            actions.key_down(Keys.SHIFT).send_keys(Keys.RETURN).key_up(Keys.SHIFT)
        actions.send_keys(Keys.RETURN)
        actions.perform()
        time.sleep(send_msg_time)

# Quit the driver
driver.quit()