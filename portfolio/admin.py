from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from portfolio.models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'email', 'first_name', 'last_name', 'phone', 'is_active'
    ]