from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'email', 'membership_number', 'joined_at')
    search_fields = ('business_name', 'email')
    ordering = ('business_name',)
