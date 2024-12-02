from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    # Adiciona campos visíveis na lista
    list_display = ('first_name', 'last_name', 'username', 'birth_date', 'email', 'phone_number')
    
    # Permite busca por alguns campos no admin
    search_fields = ('first_name', 'last_name', 'email')
    
    # Adiciona filtros laterais no admin
    list_filter = ('birth_date',)  # Exemplo de filtro por data de nascimento

    # Torna 'phone_number' como somente leitura (não pode ser editado diretamente)
    readonly_fields = ('phone_number',)

# Registra o modelo CustomUser com a classe CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
