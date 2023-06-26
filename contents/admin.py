"""
Django admin customization
"""
from django.contrib import admin

from .models import Category, Location, Skill


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Define the admin pages for category."""
    model = Category
    ordering = ['id']
    list_display = ['id', 'title', 'description']
    list_display_links = ['title']
    readonly_fields = ['id']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Define the admin pages for location."""
    model = Location
    ordering = ['country']
    list_display = ['id', 'address', 'country', 'state', 'city']
    list_display_links = ['address']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Define the admin pages for skill."""
    model = Skill
    ordering = ['title']
    list_display = ['id', 'title', 'description', 'proficiency_level']
    list_display_links = ['proficiency_level']
