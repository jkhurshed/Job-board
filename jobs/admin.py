"""
Django admin customization
"""
from django.contrib import admin

from .models import Job, Applicant


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """Define the admin pages for company."""
    model = Job
    ordering = ['id']
    list_display = ['id', 'user', 'title', 'description', 'location', 'company', 'salary', 'created_at']
    list_display_links = ['title']
    readonly_fields = ['id']


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    """Define the admin pages for applicant."""
    model = Applicant
    ordering = ['id']
    list_display = ['id', 'user', 'name', 'skill']
    list_display_links = ['name']
    readonly_fields = ['id']
