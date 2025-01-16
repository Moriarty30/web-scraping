import os
import time

from PIL import Image


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fullpage_screenshot(driver, file):

        print("Starting chrome full page screenshot workaround ...")


        print("Logica para ingresar a grafana...")

        
        Service= Service(executable_path="chromedriver.exe")
        driver = webdriver.Chrome(service=Service) 

        driver.get("https://data-prod-p.superpay.com.co/d/ddxhbqolrre9se/w-arena?orgId=1&refresh=1m")

        WebDriverWait(driver,5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id=":r0:"]'))
        )


        input_user = driver.find_element(By.XPATH, '//*[@id=":r0:"]')
        input_user.send_keys("xxxx")

        input_password = driver.find_element(By.XPATH, '//*[@id=":r1:"]')
        input_password.send_keys("xxxx"+Keys.ENTER)
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="pageContent"]/div[3]/div/div[1]/div/div/div/div/div/div[7]'))
        )
        time.sleep(5)
        print("fin de logica...")
        total_width = driver.execute_script("return document.body.offsetWidth")
        total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        viewport_width = driver.execute_script("return document.body.clientWidth")
        viewport_height = driver.execute_script("return window.innerHeight")
        print("Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height,viewport_width,viewport_height))
        rectangles = []

        i = 0
        while i < total_height:
            ii = 0
            top_height = i + viewport_height

            if top_height > total_height:
                top_height = total_height

            while ii < total_width:
                top_width = ii + viewport_width

                if top_width > total_width:
                    top_width = total_width

                print("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
                rectangles.append((ii, i, top_width,top_height))

                ii = ii + viewport_width

            i = i + viewport_height

        stitched_image = Image.new('RGB', (total_width, total_height))
        previous = None
        part = 0

        for rectangle in rectangles:
            if not previous is None:
                driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
                print("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
                time.sleep(0.2)

            file_name = "part_{0}.png".format(part)
            print("Capturing {0} ...".format(file_name))

            driver.get_screenshot_as_file(file_name)
            screenshot = Image.open(file_name)

            if rectangle[1] + viewport_height > total_height:
                offset = (rectangle[0], total_height - viewport_height)
            else:
                offset = (rectangle[0], rectangle[1])

            print("Adding to stitched image with offset ({0}, {1})".format(offset[0],offset[1]))
            stitched_image.paste(screenshot, offset)

            del screenshot
            os.remove(file_name)
            part = part + 1
            previous = rectangle

        stitched_image.save(file)
        print("Finishing chrome full page screenshot workaround...")
        return True