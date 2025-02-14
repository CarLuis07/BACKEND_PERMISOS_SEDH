from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from app.config.email_config import EmailSettings
import os
from datetime import datetime
# Agregar esta importación
from app.schemas.aprobarSolicitudesAgenteSchema import SolicitudesAgenteCargarDatos

class EmailService:
    def __init__(self):
        self.settings = EmailSettings()

    def generar_pdf_permiso(self, datos_permiso: SolicitudesAgenteCargarDatos):
        pdf = FPDF()
        pdf.add_page()
        
        # Agregar imagen de fondo
        pdf.image('app/static/background.jpg', x=0, y=0, w=210)  # Tamaño A4
        
        # Aumentar el espacio superior antes de comenzar con los datos
        pdf.ln(40)  # Aumentado de 10 a 40 para dar más espacio
        
        # Configuración para datos
        pdf.set_font("Helvetica", size=12)
        
        # Datos del permiso
        datos = [
            ("Tipo de Permiso:", datos_permiso.nom_tipo_solicitud),
            ("Nombre del Empleado:", f"{datos_permiso.pri_nombre} {datos_permiso.seg_nombre} {datos_permiso.pri_apellido} {datos_permiso.seg_apellido}"),
            ("Dependencia:", datos_permiso.nom_dependencia),
            ("Cargo:", datos_permiso.nom_cargo),
            ("Fecha de Solicitud:", datos_permiso.fec_solicitud.strftime("%d/%m/%Y")),
            ("Hora de Salida:", datos_permiso.hor_salida if datos_permiso.hor_salida else "N/A"),
            ("Hora de Retorno:", datos_permiso.hor_retorno if datos_permiso.hor_retorno else "N/A")
        ]

        # Imprimir datos
        for label, value in datos:
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(60, 10, label, 0, 0)
            pdf.set_font("Helvetica", "", 12)
            pdf.cell(130, 10, str(value), 0, 1)
            pdf.ln(2)

        # Espacio para firma de RRHH (alineada a la derecha)
        pdf.ln(20)
        
        # Espacio para la imagen de la huella (tamaño aumentado)
        x_huella = 140  # Ajustado la posición X para centrar mejor la huella más grande
        y_huella = pdf.get_y()  # Obtener posición Y actual
        pdf.image('app/static/huella.png', x=x_huella, y=y_huella, w=45, h=45)  # Aumentado de 30x30 a 45x45
        
        # Mover el cursor después de la imagen
        pdf.set_y(y_huella + 50)  # Aumentado para ajustar al nuevo tamaño de la huella
        
        # Línea y texto de firma (alineado a la derecha)
        pdf.cell(190, 10, "____________________", 0, 1, "R")
        pdf.cell(190, 10, "Huella Jefe Recursos Humanos", 0, 1, "R")
        
        # Generar nombre único para el archivo
        filename = f"permiso_{datos_permiso.id_permiso}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        filepath = os.path.join("temp", filename)
        
        # Asegurar que el directorio temp existe
        os.makedirs("temp", exist_ok=True)
        
        pdf.output(filepath)
        return filepath

    def enviar_correo_con_pdf(self, email_destino, archivo_pdf, datos_permiso: SolicitudesAgenteCargarDatos):
        msg = MIMEMultipart()
        msg['From'] = self.settings.SMTP_USERNAME  # El correo que envía (gmail)
        msg['To'] = self.settings.SENDER_EMAIL    # El correo institucional que recibe
        msg['Subject'] = f"Constancia de Permiso #{datos_permiso.id_permiso}"

        # Cuerpo del correo
        nombre_completo = f"{datos_permiso.pri_nombre} {datos_permiso.seg_nombre} {datos_permiso.pri_apellido} {datos_permiso.seg_apellido}"
        body = f"""
        Estimado(a) {nombre_completo},

        Se adjunta la constancia de su permiso solicitado.

        Saludos cordiales.
        """
        msg.attach(MIMEText(body, 'plain'))

        # Adjuntar PDF
        with open(archivo_pdf, "rb") as f:
            pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
            pdf_attachment.add_header(
                'Content-Disposition', 
                'attachment', 
                filename=os.path.basename(archivo_pdf)
            )
            msg.attach(pdf_attachment)

        # Enviar correo
        with smtplib.SMTP(self.settings.SMTP_SERVER, self.settings.SMTP_PORT) as server:
            server.starttls()
            server.login(self.settings.SMTP_USERNAME, self.settings.SMTP_PASSWORD)
            server.send_message(msg)

        # Eliminar archivo temporal
        os.remove(archivo_pdf)