from django.contrib import admin
from .models import Foto, Fotografo, Album


class AlbumAdmin(admin.ModelAdmin):
    # Adiciona album_cod como somente leitura no Admin
    readonly_fields = ['album_cod']
    
    # Outras configurações do Admin
    list_display = ('id','album_cod', 'album_nome', 'album_data', 'album_local')
    search_fields = ('album_cod', 'album_nome')
    filter_horizontal = ("edit_permissions",)  # Interface amigável para gerenciar permissões

# Registra o modelo com a configuração personalizada
admin.site.register(Album, AlbumAdmin)

admin.site.register(Fotografo)

@admin.register(Foto)
class FotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_arquivo','foto_id', 'album', 'fotografo',  'tamanho_arquivo')
    list_filter = ('album', 'fotografo')
    search_fields = ('foto_desc', 'album__album_nome')
    ordering = ('album', 'foto_id')

    # Método para exibir o nome do arquivo
    def nome_arquivo(self, obj):
        return obj.imagem.name.split('/')[-1]  # Extrai o nome do arquivo (sem o caminho)
    nome_arquivo.short_description = 'Nome do Arquivo'  # Descrição para a coluna no admin

    # Método para exibir o tamanho do arquivo
    def tamanho_arquivo(self, obj):
        return f"{obj.imagem.size / 1024:.2f} KB"  # Exibe o tamanho em KB, arredondado a 2 casas decimais
    tamanho_arquivo.short_description = 'Tamanho do Arquivo'  # Descrição para a coluna no admin