from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


Service= Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=Service) 

driver.get("https://data-prod-p.superpay.com.co/d/ddxhbqolrre9se/w-arena?orgId=1&refresh=1m")

WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id=":r0:"]'))
)


input_user = driver.find_element(By.XPATH, '//*[@id=":r0:"]')
input_user.send_keys("Cristian.giraldo@superpay.com.co")

input_password = driver.find_element(By.XPATH, '//*[@id=":r1:"]')
input_password.send_keys("30102000"+Keys.ENTER)
WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="pageContent"]/div[3]/div/div[1]/div/div/div/div/div/div[7]'))
)
time.sleep(5)
bar = driver.find_element(By.CLASS_NAME, 'thumb-vertical')
print("variable var: ver que tiene dentro ---- ",bar)
body = driver.find_element(By.CLASS_NAME, 'main-view')
body.screenshot("captura.png")
#screenshot_path = "captura_visibilidad.png"
#driver.save_screenshot(screenshot_path)
print(f"Captura de pantalla guardada en {body}")

driver.quit()