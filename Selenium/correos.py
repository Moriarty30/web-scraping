import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# Configuración
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
to = (lambda x: x.split(',') if x else [])(os.getenv("TO"))

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
ruta_actual = os.path.dirname(os.path.abspath(__file__))

# Construir las rutas absolutas de las imágenes
ruta_sg = os.path.join(ruta_actual, '../dashboard_fullpage_sg.png')
ruta_warena = os.path.join(ruta_actual, '../dashboard_fullpage_warena.png')

print(f"Ruta SG: {ruta_sg}, Ruta Warena: {ruta_warena}")
attach_file(msg, ruta_sg)
attach_file(msg, ruta_warena)

print(f'Credenciales: {username}, {password}')
# Enviar el correo
try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.set_debuglevel(1)  # Depuración habilitada
        server.starttls()
        server.login(username, password)
        server.sendmail(username, to, msg.as_string())
        print("Correo enviado exitosamente.")
except Exception as e:
    print(f"Error enviando correo: {e}")
