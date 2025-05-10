from django.contrib import admin
from .models import Client  # Используйте модель Client вместо UserProfile

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'phone_number')

