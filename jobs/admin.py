"""
Django admin customization
"""
from django.contrib import admin

from .models import Job


@admin.register(Job)
class CompanyAdmin(admin.ModelAdmin):
    """Define the admin pages for company."""
    model = Job
    ordering = ['id']
    list_display = ['id', 'user', 'title', 'description', 'location', 'company', 'salary', 'created_at']
    list_display_links = ['title']
    readonly_fields = ['id']
