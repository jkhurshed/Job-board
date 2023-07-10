"""
Django admin customization
"""
from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Define the admin pages for company."""
    model = Company
    ordering = ['id']
    list_display = ['id', 'title', 'description', 'website', 'logo', 'location']
    list_display_links = ['title']
    readonly_fields = ['id']
