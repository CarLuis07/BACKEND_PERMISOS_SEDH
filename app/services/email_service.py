from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from app.config.email_config import EmailSettings
import os
from datetime import datetime

class EmailService:
    def __init__(self):
        self.settings = EmailSettings()

    def generar_pdf_permiso(self, datos_permiso):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(190, 10, "CONSTANCIA DE PERMISO", 0, 1, "C")
        
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        
        # Datos del permiso
        pdf.cell(190, 10, f"Número de Permiso: {datos_permiso['id_permiso']}", 0, 1)
        pdf.cell(190, 10, f"Fecha: {datos_permiso['fecha_solicitud']}", 0, 1)
        pdf.cell(190, 10, f"Empleado: {datos_permiso['nombre_completo']}", 0, 1)
        pdf.cell(190, 10, f"Tipo de Permiso: {datos_permiso['tipo_permiso']}", 0, 1)
        pdf.cell(190, 10, f"Hora de Salida: {datos_permiso['hora_salida']}", 0, 1)
        pdf.cell(190, 10, f"Hora de Retorno: {datos_permiso['hora_retorno']}", 0, 1)
        
        # Generar nombre único para el archivo
        filename = f"permiso_{datos_permiso['id_permiso']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        filepath = os.path.join("temp", filename)
        
        # Asegurar que el directorio temp existe
        os.makedirs("temp", exist_ok=True)
        
        pdf.output(filepath)
        return filepath

    def enviar_correo_con_pdf(self, email_destino, archivo_pdf, datos_permiso):
        msg = MIMEMultipart()
        msg['From'] = self.settings.SENDER_EMAIL
        msg['To'] = email_destino
        msg['Subject'] = f"Constancia de Permiso #{datos_permiso['id_permiso']}"

        # Cuerpo del correo
        body = f"""
        Estimado(a) {datos_permiso['nombre_completo']},

        Se adjunta la constancia de su permiso solicitado.

        Detalles del permiso:
        - Tipo de permiso: {datos_permiso['tipo_permiso']}
        - Fecha: {datos_permiso['fecha_solicitud']}
        - Hora de salida: {datos_permiso['hora_salida']}
        - Hora de retorno: {datos_permiso['hora_retorno']}

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