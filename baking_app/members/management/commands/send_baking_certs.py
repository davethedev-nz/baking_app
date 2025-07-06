from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from members.models import Member, EmailTemplate, EmailSignature
from members.utils import render_template_string
from email.mime.image import MIMEImage
import os

# TEMPLATE_PATH = 'certificate_templates/certificate_template.docx'
# OUTPUT_DIR = 'generated_certificates/'

class Command(BaseCommand):
    help = 'Generate and email certificate PDFs to all members.'

    def handle(self, *args, **kwargs):
        # os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Load the active email template
        try:
            template = EmailTemplate.objects.get(name='Membership Certificate Email', is_active=True)
            signature = EmailSignature.objects.get(name='Accounts Signature', is_active=True)
        except EmailTemplate.DoesNotExist:
            self.stdout.write(self.style.ERROR("No active 'Membership Certificate Email' template found."))
            return
        except EmailSignature.DoesNotExist:
            self.stdout.write(self.style.ERROR("No active 'Accounts Signature' signature found."))
            return
        
        members = Member.objects.all()

        for member in members:
            context = {
                'membership_number': member.membership_number or '',
                'business_name': member.business_name or '',
                'email': member.email or ''
            }
            
            subject = render_template_string(template.subject, context)
            body_plain = render_template_string(template.body, context)

            signature_cid = "signature-image"
            signature_html = ""
            if signature:
                signature_html = signature.render_cid_html(cid="signature-image")

            html_body = f"<p>{body_plain.replace(chr(10), '<br>')}</p>{signature_html}"

            # doc = Document(TEMPLATE_PATH)

            # # Replace placeholder text in the docx template
            # for p in doc.paragraphs:
            #     if '{{name}}' in p.text:
            #         p.text = p.text.replace('{{name}}', f"{member.first_name} {member.last_name}")
            #     if '{{business}}' in p.text:
            #         p.text = p.text.replace('{{business}}', member.business_name or '')

            # # Save personalized DOCX
            # docx_filename = os.path.join(OUTPUT_DIR, f"{member.id}_cert.docx")
            # doc.save(docx_filename)

            # # Convert to PDF using libreoffice
            # subprocess.run([
            #     'libreoffice', '--headless', '--convert-to', 'pdf', docx_filename,
            #     '--outdir', OUTPUT_DIR
            # ])

            # pdf_filename = docx_filename.replace('.docx', '.pdf')

            # Email the PDF
            email = EmailMultiAlternatives(
                subject=subject,
                body=body_plain,
                to=[member.email],
            )
            email.attach_alternative(html_body, "text/html")

                # Attach signature image as inline
            if signature and signature.image:
                image_path = os.path.join(settings.MEDIA_ROOT, signature.image.name)
                with open(image_path, 'rb') as f:
                    mime_image = MIMEImage(f.read())
                    mime_image.add_header('Content-ID', f'<{signature_cid}>')
                    mime_image.add_header("Content-Disposition", "inline", filename="signature.png")
                    email.attach(mime_image)
            email.send()

            self.stdout.write(self.style.SUCCESS(f"Sent certificate to {member.email}"))
