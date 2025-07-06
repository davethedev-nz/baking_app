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
    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=200)
    body = models.TextField(help_text="Use {{ membership_number }}, {{ business_name }}, etc.")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
