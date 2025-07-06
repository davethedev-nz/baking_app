from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from members.models import Member, EmailTemplate
from members.utils import render_template_string

# TEMPLATE_PATH = 'certificate_templates/certificate_template.docx'
# OUTPUT_DIR = 'generated_certificates/'

class Command(BaseCommand):
    help = 'Generate and email certificate PDFs to all members.'

    def handle(self, *args, **kwargs):
        # os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Load the active email template
        try:
            template = EmailTemplate.objects.get(name='Membership Certificate Email', is_active=True)
        except EmailTemplate.DoesNotExist:
            self.stdout.write(self.style.ERROR("No active 'Membership Certificate Email' template found."))
            return
        
        members = Member.objects.all()

        for member in members:
            context = {
                'membership_number': member.membership_number or '',
                'business_name': member.business_name or '',
                'email': member.email or ''
            }
            
            subject = render_template_string(template.subject, context)
            body = render_template_string(template.body, context)


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
            email = EmailMessage(
                subject=subject,
                body=body,
                to=[member.email],
            )

            email.send()

            self.stdout.write(self.style.SUCCESS(f"Sent certificate to {member.email}"))
