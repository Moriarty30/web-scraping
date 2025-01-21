import os

url = os.getenv("WARENA")
usuario = os.getenv("USERNAME_GRAFANA")
password = os.getenv("PASSWORD_GRAFANA")    


print(f"URL: {url}, usuario: {usuario}, password: {password}")