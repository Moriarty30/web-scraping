import sys
from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import util


class Test(unittest.TestCase):
    """ Demonstration: Get Chrome to generate fullscreen screenshot """

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_fullpage_screenshot(self):
        """ Generate document-height screenshot after login """
        url = "https://data-prod-p.superpay.com.co/d/ddxhbqolrre9se/w-arena?orgId=1&refresh=1m"
        self.driver.get(url)

        # Inicio de sesión
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id=":r0:"]'))
        )

        input_user = self.driver.find_element(By.XPATH, '//*[@id=":r0:"]')
        input_user.send_keys("Cristian.giraldo@superpay.com.co")

        input_password = self.driver.find_element(By.XPATH, '//*[@id=":r1:"]')
        input_password.send_keys("30102000" + Keys.ENTER)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="pageContent"]/div[3]/div/div[1]/div/div/div/div/div/div[7]')
            )
        )

        # Captura de pantalla de página completa
        util.fullpage_screenshot(self.driver, "test.png")


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
