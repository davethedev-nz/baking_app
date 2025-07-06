from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from members.models import Member, EmailTemplate, EmailSignature
from members.utils import render_template_string
from email.mime.image import MIMEImage
from PIL import Image, ImageDraw, ImageFont
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

            # Create output directory if it doesn't exist
            output_dir = os.path.join(settings.BASE_DIR, 'output_certs')
            os.makedirs(output_dir, exist_ok=True)

            filename = f"Membership_Certificate_{member.membership_number}.pdf"
            output_path = os.path.join(output_dir, filename)
            self.generate_certificate(member, output_path)

            # Email the PDF
            email = EmailMultiAlternatives(
                subject=subject,
                body=body_plain,
                to=[member.email],
            )

            with open(output_path, "rb") as pdf_file:
                email.attach(f"Membership_Certificate_{member.membership_number}.pdf", pdf_file.read(), "application/pdf")

            welcome_pack_path = os.path.join(settings.BASE_DIR, 'static/welcome_pack/BakingNZ_WelcomePack.pdf')
            with open(welcome_pack_path, "rb") as pdf_file:
                email.attach("BakingNZ_WelcomePack.pdf", pdf_file.read(), "application/pdf")

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

    def generate_certificate(self, member, output_path):

        template_path = os.path.join(settings.BASE_DIR, 'certificate_templates/BakingCert.png')
        background = Image.open(template_path).convert("RGB")
        draw = ImageDraw.Draw(background)

        # Load a font
        font_path = os.path.join(settings.BASE_DIR, 'static/fonts/GothicB.ttf')  # Optional
        
        line_height = 30

        # Generate the business name text
        font = ImageFont.truetype(font_path, size=line_height)
        # business_name_text = f"{member.business_name}"
        business_name_text = "Gluten Free Holdings Ltd T/A Gluten Free Choice"
        column_x_start = 505          
        max_width = 1080 - 505
        start_y = 480 
        wrapped_lines = self.wrap_text(draw, business_name_text, font, max_width)
        for i, line in enumerate(wrapped_lines):
            text_width, _ = draw.textsize(line, font=font)
            x = column_x_start + (max_width - text_width) // 2
            y = start_y + i * line_height
            draw.text((x, y), line, font=font, fill="black")

        font = ImageFont.truetype(font_path, size=24)
        membership_number_text = f"{member.membership_number}"
        draw.text((600, 600), membership_number_text, font=font, fill="black")

        # Save to PDF
        background.save(output_path, "PDF", resolution=100.0)

    def wrap_text(self, draw, text, font, max_width):
        words = text.strip().split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            text_width, _ = draw.textsize(test_line, font=font)
            if text_width > max_width and current_line:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line

        if current_line:
            lines.append(current_line)

        return lines
