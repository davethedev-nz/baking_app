from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from members.models import Member, EmailTemplate, EmailSignature
from members.utils import render_template_string
from email.mime.image import MIMEImage
from django.conf import settings
from members.certs import generate_certificate

import os


class Command(BaseCommand):
    help = 'Generate and email certificate PDFs to all members.'

    def handle(self, *args, **kwargs):
        
        # Load the active email template and signature
        try:
            template = EmailTemplate.objects.get(name='Membership Certificate Email', is_active=True)
            signature = EmailSignature.objects.get(name='Accounts Signature', is_active=True)
        except EmailTemplate.DoesNotExist:
            self.stdout.write(self.style.ERROR("No active 'Membership Certificate Email' template found."))
            return
        except EmailSignature.DoesNotExist:
            self.stdout.write(self.style.ERROR("No active 'Accounts Signature' signature found."))
            return
        
        members = Member.objects.all().order_by('business_name')

        for member in members:
            context = {
                'membership_number': member.membership_number or '',
                'business_name': member.business_name or '',
                'email': member.email or ''
            }
            
            subject = render_template_string(template.subject, context)
            body_plain = render_template_string(template.body, context)

            # Generate Signature from db
            signature_cid = "signature-image"
            signature_html = ""
            if signature:
                signature_html = signature.render_cid_html(cid="signature-image")

            html_body = f"<p>{body_plain.replace(chr(10), '<br>')}</p>{signature_html}"

            # Create output directory if it doesn't exist
            output_dir = os.path.join(settings.BASE_DIR, 'output_certs')
            os.makedirs(output_dir, exist_ok=True)

            # Generate the certificate
            filename = f"Membership_Certificate_{member.membership_number}.pdf"
            output_path = os.path.join(output_dir, filename)
            generate_certificate(member, output_path)

            # Initialise the email
            email = EmailMultiAlternatives(
                subject=subject,
                body=body_plain,
                to=[member.email],
            )

            # Attach the cert
            with open(output_path, "rb") as pdf_file:
                email.attach(f"Membership_Certificate_{member.membership_number}.pdf", pdf_file.read(), "application/pdf")

            # Attach the Welcome Pack
            welcome_pack_path = os.path.join(settings.BASE_DIR, f'static/welcome_pack/{settings.WELCOME_PACK_FILE}')
            with open(welcome_pack_path, "rb") as pdf_file:
                email.attach("BakingNZ_WelcomePack.pdf", pdf_file.read(), "application/pdf")

            # Attach HTML signature
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

