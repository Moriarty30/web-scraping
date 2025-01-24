import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# Configuración
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
to = os.getenv("TO").split(',')

asunto = "mensaje de prueba desde python"
message = "Este correo tiene los pantallazos de los dashboards de WARENA y SGMOVIL"

# Función para adjuntar archivos
def attach_file(msg, filepath):
    filename = filepath.split('/')[-1]
    with open(filepath, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(part)

# Crear el mensaje de correo
msg = MIMEMultipart()
msg['From'] = username
msg['To'] = ', '.join(to)
msg['Subject'] = asunto
msg.attach(MIMEText(message, 'plain'))

# Adjuntar archivos
ruta_sg = '../dashboard_fullpage_sg.png'
ruta_warena = '../dashboard_fullpage_warena.png'

print(f"Ruta SG: {ruta_sg}, Ruta Warena: {ruta_warena}")
attach_file(msg, ruta_sg)
attach_file(msg, ruta_warena)

# Enviar el correo
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(username, password)
    server.sendmail(username, to, msg.as_string())

print('Email sent')
