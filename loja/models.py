from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Vendedor(models.Model):
    nome = models.CharField(max_length=120)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    vendedor = models.ForeignKey(Vendedor, on_delete=models.PROTECT, related_name='produtos')
    nome = models.CharField(max_length=120)
    preco = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    estoque = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome

class Cupom(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))])
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.codigo

class Pedido(models.Model):
    cliente = models.CharField(max_length=120)
    cupom = models.ForeignKey(Cupom, null=True, blank=True, on_delete=models.PROTECT)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido {self.pk}'

class Item(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.preco * self.quantidade
