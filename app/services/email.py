from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from datetime import datetime
from ..core.email import EmailConfig

class EmailService:
    def __init__(self):
        self.config = EmailConfig()

    def generate_permission_pdf(self, permission_data):
        pdf = FPDF(format='Letter')
        pdf.add_page()
        
        # Configurar PDF
        pdf.image('app/static/background.jpg', x=0, y=0, w=216)
        pdf.ln(50)
        pdf.set_font("Helvetica", size=12)
        
        # Generar contenido
        self._add_permission_data(pdf, permission_data)
        self._add_signature(pdf)
        
        # Guardar PDF
        filename = self._generate_filename(permission_data.id_permiso)
        return self._save_pdf(pdf, filename)

    def send_email_with_pdf(self, to_email, pdf_file, permission_data):
        msg = self._create_email_message(to_email, permission_data)
        self._attach_pdf(msg, pdf_file)
        self._send_email(msg)
        self._cleanup(pdf_file)

    def _add_permission_data(self, pdf, data):
        # Implementar lógica para agregar datos al PDF
        pass

    def _add_signature(self, pdf):
        # Implementar lógica para agregar firma
        pass

    def _generate_filename(self, permission_id):
        return f"permiso_{permission_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"

    def _save_pdf(self, pdf, filename):
        filepath = os.path.join("temp", filename)
        os.makedirs("temp", exist_ok=True)
        pdf.output(filepath)
        return filepath

    def _create_email_message(self, to_email, permission_data):
        msg = MIMEMultipart()
        msg['From'] = self.config.SMTP_USERNAME
        msg['To'] = to_email
        msg['Subject'] = f"Constancia de Permiso #{permission_data.id_permiso}"
        
        body = self._generate_email_body(permission_data)
        msg.attach(MIMEText(body, 'plain'))
        return msg

    def _generate_email_body(self, permission_data):
        return f"""
        Estimado(a) {permission_data.nombre_completo},

        Se adjunta la constancia de su permiso solicitado, saludos cordiales.
        *Cuidemos el Medio Ambiente y nuestros recursos en la SEDH, por favor, no imprima el PDF si no es necesario.
        """

    def _attach_pdf(self, msg, pdf_file):
        with open(pdf_file, "rb") as f:
            attachment = MIMEApplication(f.read(), _subtype="pdf")
            attachment.add_header(
                'Content-Disposition', 
                'attachment', 
                filename=os.path.basename(pdf_file)
            )
            msg.attach(attachment)

    def _send_email(self, msg):
        with smtplib.SMTP(self.config.SMTP_SERVER, self.config.SMTP_PORT) as server:
            server.starttls()
            server.login(self.config.SMTP_USERNAME, self.config.SMTP_PASSWORD)
            server.send_message(msg)

    def _cleanup(self, pdf_file):
        if os.path.exists(pdf_file):
            os.remove(pdf_file)