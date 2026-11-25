from rest_framework import serializers
from django.db import transaction
from django.db.models import F
from decimal import Decimal, ROUND_HALF_UP
from .models import Vendedor, Produto, Cupom, Pedido, Item

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class CupomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cupom
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    quantidade = serializers.IntegerField(min_value=1)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Item
        fields = ['produto', 'quantidade', 'preco', 'subtotal']
        read_only_fields = ['preco']

class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemSerializer(many=True, allow_empty=False)

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'cupom', 'itens', 'subtotal', 'total', 'criado_em']
        read_only_fields = ['subtotal', 'total', 'criado_em']

    @transaction.atomic
    def create(self, validated_data):
        itens = validated_data.pop('itens')
        cupom = validated_data.get('cupom')
        if cupom and not cupom.ativo:
            raise serializers.ValidationError('Cupom inativo.')
        pedido = Pedido.objects.create(**validated_data)
        subtotal = Decimal('0')
        for item in itens:
            produto = Produto.objects.select_for_update().get(pk=item['produto'].pk)
            quantidade = item['quantidade']
            atualizado = Produto.objects.filter(pk=produto.pk, estoque__gte=quantidade).update(estoque=F('estoque') - quantidade)
            if not atualizado:
                raise serializers.ValidationError(f'Estoque insuficiente: {produto.nome}.')
            Item.objects.create(pedido=pedido, produto=produto, quantidade=quantidade, preco=produto.preco)
            subtotal += produto.preco * quantidade
        desconto = cupom.desconto if cupom else Decimal('0')
        pedido.subtotal = subtotal
        pedido.total = (subtotal * (1 - desconto / 100)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        pedido.save()
        return pedido
