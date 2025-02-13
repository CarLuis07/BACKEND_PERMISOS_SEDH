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

    def generar_pdf_permiso(self, datos_permiso: SolicitudesAgenteCargarDatos):
        pdf = FPDF()
        pdf.add_page()
        
        # Configuración de la página
        pdf.set_font("Arial", "B", 16)
        pdf.cell(190, 10, "CONSTANCIA DE PERMISO", 0, 1, "C")
        pdf.ln(10)
        
        # Configuración para datos
        pdf.set_font("Arial", size=12)
        
        # Datos del permiso
        datos = [
            ("Tipo de Permiso:", datos_permiso.nom_tipo_solicitud),
            ("Nombre del Empleado:", f"{datos_permiso.pri_nombre} {datos_permiso.seg_nombre} {datos_permiso.pri_apellido} {datos_permiso.seg_apellido}"),
            ("Dependencia:", datos_permiso.nom_dependencia),
            ("Cargo:", datos_permiso.nom_cargo),
            ("Fecha de Solicitud:", datos_permiso.fec_solicitud.strftime("%d/%m/%Y")),
            ("Hora de Salida:", datos_permiso.hor_salida if datos_permiso.hor_salida else "N/A"),
            ("Hora de Retorno:", datos_permiso.hor_retorno if datos_permiso.hor_retorno else "N/A"),
            ("Tiempo de Permiso:", datos_permiso.hor_solicitadas if datos_permiso.hor_solicitadas else "N/A")
        ]

        # Imprimir datos
        for label, value in datos:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(60, 10, label, 0, 0)
            pdf.set_font("Arial", "", 12)
            pdf.cell(130, 10, str(value), 0, 1)
            pdf.ln(2)

        # Espacio para firmas
        pdf.ln(20)
        pdf.cell(95, 10, "____________________", 0, 0, "C")
        pdf.cell(95, 10, "____________________", 0, 1, "C")
        pdf.cell(95, 10, "Firma Jefe Inmediato", 0, 0, "C")
        pdf.cell(95, 10, "Firma Recursos Humanos", 0, 1, "C")
        
        # Generar nombre único para el archivo
        filename = f"permiso_{datos_permiso.id_permiso}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
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