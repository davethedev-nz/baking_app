from django.db import models

class Member(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    business_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    membership_number = models.IntegerField()
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.business_name}"

class EmailTemplate(models.Model):
    name = models.CharField(
        max_length=100, 
        unique=True,
        help_text="The send_baking_certs command looks for a template named 'Membership Certificate Email'"
    )
    subject = models.CharField(max_length=200)
    body = models.TextField(help_text="Use $membership_number, $business_name, $email, $cert_year as placeholders for dynamic content.")
    is_active = models.BooleanField(default=True, help_text="Only one template should be active at a time")

    def __str__(self):
        return self.name

class EmailSignature(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="The send_baking_certs command looks for a signature named 'Accounts Signature'"
    )
    sign_off_text = models.TextField(blank=True)
    signer_name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='signatures/', blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text="Only one signature should be active at a time")

    def __str__(self):
        return self.name
    

    def render_cid_html(self, cid="signature-image"):
        html = "<p style='margin-top: 15px;'>"
        if self.sign_off_text:
            html += self.sign_off_text.replace("\n", "<br>") + "<br>" +"<br>"
        if self.signer_name:
            html += f"<strong>{self.signer_name}</strong><br>"
        if self.image:
            html += f"<img src='cid:{cid}' width='200' alt='Signature'>"
        html += "</p>"
        return html
