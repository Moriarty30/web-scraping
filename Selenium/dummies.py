import os
import time
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import tempfile
import shutil

def fullpage_screenshot(driver, file):
    print("Iniciando captura de pantalla de página completa...")

    # 1) Localiza el contenedor que tiene la altura dinámica.
    #    En tu caso, es el div con clase .react-grid-layout
    height_element = driver.find_element(By.CSS_SELECTOR, ".react-grid-layout")

    # 2) Localiza el contenedor que realmente TIENE el scroll.
    scrollable_element = driver.find_element(By.CSS_SELECTOR, ".scrollbar-view")

    # 3) Calcula el ancho total de .react-grid-layout
    total_width = driver.execute_script("return arguments[0].offsetWidth", height_element)

    #    Calcula el alto total (contenido) de .react-grid-layout
    total_height = driver.execute_script("return arguments[0].offsetHeight", height_element)

    # 4) Calcula la altura visible (viewport) de .scrollbar-view
    viewport_height = driver.execute_script("return arguments[0].clientHeight", scrollable_element)

    print(f"Ancho total: {total_width}")
    print(f"Alto total (contenido): {total_height}")
    print(f"Alto visible (viewport): {viewport_height}")

    # 5) Crea una imagen "en blanco" del tamaño total
    stitched_image = Image.new('RGB', (total_width, total_height))

    # 6) Asegura que el scroll arranque en 0 (arriba de todo)
    driver.execute_script("arguments[0].scrollTop = 0;", scrollable_element)
    time.sleep(1)  # Espera para evitar capturas con la página a medio render

    # 7) Variables para recorrer la página
    current_position = 0
    part = 0  # Contador de "partes" o secciones

    # 8) Recorre la página en pasos de "viewport_height" hasta llegar al final
    while current_position < total_height:
        # Calcula hasta dónde cubre esta "rebanada"
        top_height = current_position + viewport_height
        if top_height > total_height:
            top_height = total_height

        # 9) Desplaza el scroll al current_position
        driver.execute_script("arguments[0].scrollTop = arguments[1];", scrollable_element, current_position)
        print(f"Desplazado a scrollTop={current_position}")
        
        # Espera 1 segundo para que el dashboard se refresque
        time.sleep(1)

        # 10) Captura de pantalla
        file_name = f"part_{part}.png"
        driver.get_screenshot_as_file(file_name)
        print(f"Capturando {file_name} ...")

        # 11) Abre la captura y pégala (paste) en la posición que corresponde
        screenshot = Image.open(file_name)
        offset = (0, current_position)  # Va en el eje X=0, Y=current_position

        # Pega la screenshot en la imagen grande
        stitched_image.paste(screenshot, offset)

        # Limpieza de la captura temporal
        screenshot.close()
        os.remove(file_name)

        # 12) Prepara la siguiente sección
        part += 1
        current_position += viewport_height

    # 13) Finalmente, guarda la imagen compuesta
    stitched_image.save(file)
    print(f"Captura completa guardada en: {file}")
    return True


# ---------------------------------------------------------
# EJEMPLO DE USO
# ---------------------------------------------------------
if __name__ == "__main__":

    chromedriver_path = "/var/jenkins_home/workspace/Selenium/Selenium/chromedriver"
    
    # Configurar opciones de Chrome
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    
    # Usar un directorio temporal único para evitar conflictos
    user_data_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    

    try:

        url = os.getenv("WARENA")
        username = os.getenv("USERNAME_GRAFANA")
        password = os.getenv("PASSWORD_GRAFANA")
        
        if not isinstance(url, str) or not url:
            ValueError(f"url: {url}, username: {username}, password: {password}")
            raise ValueError("La variable de entorno 'WARENA' no está definida o no es válida.")
        
        driver.get(url)
        driver.maximize_window()
        time.sleep(2)  # Espera para evitar capturas con la página a medio render
        driver.save_screenshot("pagina_cargada.png")

        # Login de ejemplo
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "input-wrapper"))
        )
        input_user = driver.find_element(By.XPATH, '//*[@id=":r0:"]')
        input_user.send_keys(username)
        input_password = driver.find_element(By.XPATH, '//*[@id=":r1:"]')
        input_password.send_keys(password + Keys.ENTER)
        print("Login exitoso")

        # Esperamos que cargue el dashboard:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'scrollbar-view'))
        )
        time.sleep(5) 
        elemento = driver.find_element(By.CLASS_NAME, 'scrollbar-view')
        print(f"Elemento no encontrado: {elemento}")

        # Llamamos a la función para la screenshot completa
        fullpage_screenshot(driver, "dashboard_fullpage.png")

    except Exception as e:
        print(f"Error durante la ejecución: {str(e)}")
        driver.save_screenshot("error.png")  # Captura el estado en caso de error
    finally:
        driver.quit()
