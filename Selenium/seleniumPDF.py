import os
import time
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fullpage_screenshot_to_pdf(driver, pdf_file):
    print("Iniciando captura de pantalla de página completa en PDF...")

    # 1) Localiza el contenedor que tiene la altura dinámica
    height_element = driver.find_element(By.CSS_SELECTOR, ".react-grid-layout")

    # 2) Localiza el contenedor que TIENE el scroll
    scrollable_element = driver.find_element(By.CSS_SELECTOR, ".scrollbar-view")

    # 3) Mide el ancho/alto total de .react-grid-layout
    total_width = driver.execute_script("return arguments[0].offsetWidth", height_element)
    total_height = driver.execute_script("return arguments[0].offsetHeight", height_element)

    # 4) Mide la altura visible (viewport) de .scrollbar-view
    viewport_height = driver.execute_script("return arguments[0].clientHeight", scrollable_element)

    print(f"Ancho total: {total_width}")
    print(f"Alto total: {total_height}")
    print(f"Viewport height: {viewport_height}")

    # 5) Creamos una imagen final del tamaño total
    stitched_image = Image.new('RGB', (total_width, total_height))

    # 6) Iniciamos el scroll en 0 (arriba del todo)
    driver.execute_script("arguments[0].scrollTop = 0;", scrollable_element)
    time.sleep(1)

    # 7) Variables para iterar sobre el alto
    current_position = 0
    part = 0

    # 8) Recorremos la página en pasos de 'viewport_height'
    while current_position < total_height:
        # Hasta dónde llegará esta sección
        top_height = current_position + viewport_height
        if top_height > total_height:
            top_height = total_height

        # Hacemos scroll real
        driver.execute_script(
            "arguments[0].scrollTop = arguments[1];", 
            scrollable_element, 
            current_position
        )
        print(f"Desplazado a scrollTop={current_position}")

        # Esperamos 1 segundo para refresco
        time.sleep(1)

        # 9) Capturamos la pantalla
        file_name = f"part_{part}.png"
        print(f"Capturando {file_name} ...")
        driver.get_screenshot_as_file(file_name)

        # 10) Pegamos en la imagen final
        screenshot = Image.open(file_name)
        offset = (0, current_position)  # X=0, Y=current_position
        stitched_image.paste(screenshot, offset)

        # Limpieza
        screenshot.close()
        os.remove(file_name)

        # Avanzamos al siguiente tramo
        part += 1
        current_position += viewport_height

    # 11) Guardamos el resultado final **como PDF**
    #     Convierte a RGB para evitar problemas de perfil de color
    stitched_image = stitched_image.convert("RGB")
    stitched_image.save(pdf_file, "PDF", resolution=100.0)
    print(f"Captura completa guardada en PDF: {pdf_file}")

    return True


# ---------------------------------------------------------
# EJEMPLO DE USO
# ---------------------------------------------------------
if __name__ == "__main__":
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    driver = webdriver.Chrome()
    try:
        driver.get("https://data-prod-p.superpay.com.co/d/ddxhbqolrre9se/w-arena?orgId=1&refresh=1m")
        driver.maximize_window()

        # Login (ajusta según tu caso)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id=":r0:"]'))
        )
        input_user = driver.find_element(By.XPATH, '//*[@id=":r0:"]')
        input_user.send_keys("Cristian.giraldo@superpay.com.co")
        input_password = driver.find_element(By.XPATH, '//*[@id=":r1:"]')
        input_password.send_keys("30102000" + Keys.ENTER)

        # Esperamos que cargue el dashboard
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".scrollbar-view"))
        )

        # Capturamos a PDF
        fullpage_screenshot_to_pdf(driver, "dashboard_fullpage.pdf")

    finally:
        driver.quit()
