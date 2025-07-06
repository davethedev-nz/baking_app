from django.db import models
from django.conf import settings

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
    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=200)
    body = models.TextField(help_text="Use $membership_number, $business_name, $email")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class EmailSignature(models.Model):
    name = models.CharField(max_length=100)
    sign_off_text = models.TextField(blank=True)
    signer_name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='signatures/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def render_html(self):
        html = "<p style='margin-top: 30px;'>"
        if self.sign_off_text:
            html += self.sign_off_text.replace("\n", "<br>") + "<br>"
        if self.signer_name:
            html += f"<strong>{self.signer_name}</strong><br>"
        if self.image:
            full_url = f"{settings.MEDIA_FULL_URL}{self.image.name}"
            html += f"<img src='{full_url}' width='200' alt='Signature'>"
        html += "</p>"
        return html