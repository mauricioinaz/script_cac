import csv, email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

subject = "Informe de diagnósticos sociales"
body = """{}, 

Recibe un cordial saludo del equipo de Horizontes Creativos.

Adjuntamos el informe correspondiente a la sistematización de los resultados de los diagnósticos sociales realizados por tu equipo en las CAC a tu cargo.

Preparamos este video para que puedas leer correctamente el archivo: https://youtu.be/z1FFLeD5Djw

Quedamos atentas/os a cualquier duda."""
sender_email = "diagnosticosocialpsv@gmail.com"
#receiver_email = "horizontescreativos1@gmail.com"
password = input("Type your password and press enter:")
from_address = "diagnosticosocialpsv@gmail.com"


# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(from_address, password)
    with open("listadoFiltrado.csv") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for Nombre, ID, correo in reader:
            Nombre_facilitador = Nombre
            receiver_email = correo
            # Create a multipart message and set headers
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            #message["Bcc"] = receiver_email  # Recommended for mass emails
            # Add body to email
            message.attach(MIMEText(body.format(Nombre_facilitador), "plain"))
            filename = "informe_"+ID+".pdf"  # In same directory as script
            # Open PDF file in binary mode
            with open(filename, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            # Encode file in ASCII characters to send by email    
            encoders.encode_base64(part)
            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
            # Add attachment to message and convert message to string
            message.attach(part)
            text = message.as_string()
            server.sendmail(
                from_address,
                correo,
                text
            )