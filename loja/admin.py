from django.contrib import admin
from .models import Vendedor, Produto, Cupom, Pedido, Item

admin.site.register(Vendedor)
admin.site.register(Produto)
admin.site.register(Cupom)

class ItemInline(admin.TabularInline):
    model = Item
    extra = 0
    readonly_fields = ['produto', 'quantidade', 'preco']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'total', 'criado_em']
    readonly_fields = ['cliente', 'cupom', 'subtotal', 'total', 'criado_em']
    inlines = [ItemInline]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
