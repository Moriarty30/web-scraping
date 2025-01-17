from PIL import Image
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fullpage_screenshot(driver, file):
    print("Starting chrome full page screenshot workaround ...")

    # Encuentra el contenedor principal del canvas
    canvas_element = driver.find_element(By.CLASS_NAME, 'css-1978mzo-canvas-content')

    # Obtener dimensiones del canvas
    total_width = driver.execute_script("return arguments[0].offsetWidth", canvas_element)
    total_height = driver.execute_script("return arguments[0].offsetHeight", canvas_element)
    viewport_height = driver.execute_script("return arguments[0].clientHeight", canvas_element)

    print(f"Total: ({total_width}, {total_height}), Viewport: {viewport_height}")
    rectangles = []

    # Scroll usando `scrollTop`
    current_position = 0
    step = viewport_height  # Tamaño del desplazamiento en cada paso

    while current_position < total_height:
        top_height = current_position + viewport_height

        if top_height > total_height:
            top_height = total_height

        print(f"Appending rectangle (0,{current_position}, {total_width},{top_height})")
        rectangles.append((0, current_position, total_width, top_height))

        # Desplazar el canvas ajustando `scrollTop`
        driver.execute_script(
            f"arguments[0].scrollTop = {current_position};", canvas_element
        )
        print(f"Scrolled To Y: {current_position}")
        time.sleep(1.0)  # Esperar para renderizado

        current_position += step

    # Capturar las secciones de la página
    stitched_image = Image.new('RGB', (total_width, total_height))
    part = 0

    for rectangle in rectangles:
        file_name = f"part_{part}.png"
        print(f"Capturing {file_name} ...")

        driver.get_screenshot_as_file(file_name)
        screenshot = Image.open(file_name)

        offset = (rectangle[0], rectangle[1])
        print(f"Adding to stitched image with offset {offset}")
        stitched_image.paste(screenshot, offset)

        del screenshot
        os.remove(file_name)
        part += 1

    stitched_image.save(file)
    print("Finishing chrome full page screenshot workaround...")
    return True
