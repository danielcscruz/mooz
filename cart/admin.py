from django.contrib import admin
from .models import Cart




class CartAdmin(admin.ModelAdmin):
    readonly_fields = ['user']
    list_display = ('id','user', 'total_value', 'status', 'created_at', 'updated_at')

admin.site.register(Cart, CartAdmin)