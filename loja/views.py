from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from rest_framework import viewsets, mixins
from .models import Vendedor, Produto, Cupom, Pedido
from .serializers import VendedorSerializer, ProdutoSerializer, CupomSerializer, PedidoSerializer

class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class CupomViewSet(viewsets.ModelViewSet):
    queryset = Cupom.objects.all()
    serializer_class = CupomSerializer

class PedidoViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Pedido.objects.prefetch_related('itens').order_by('-id')
    serializer_class = PedidoSerializer

@staff_member_required
def dashboard(request):
    return render(request, 'loja/dashboard.html', {'produtos': Produto.objects.count(), 'vendedores': Vendedor.objects.count(), 'pedidos': Pedido.objects.count(), 'receita': Pedido.objects.aggregate(valor=Sum('total'))['valor'] or 0, 'recentes': Pedido.objects.order_by('-id')[:10]})

def loja(request):
    carrinho = request.session.get('carrinho', {})
    if request.method == 'POST':
        acao = request.POST.get('acao')
        if acao == 'limpar':
            request.session['carrinho'] = {}
            return redirect('loja')
        if acao == 'adicionar':
            produto = Produto.objects.filter(pk=request.POST.get('produto')).first()
            if produto:
                chave = str(produto.pk)
                carrinho[chave] = min(carrinho.get(chave, 0) + 1, produto.estoque)
                request.session['carrinho'] = carrinho
            return redirect('loja')
        if acao == 'comprar':
            cupom = request.POST.get('cupom', '').strip()
            codigo = Cupom.objects.filter(codigo=cupom, ativo=True).first() if cupom else None
            if cupom and not codigo:
                erro = 'Cupom inválido.'
            else:
                serializer = PedidoSerializer(data={'cliente': request.POST.get('cliente'), 'cupom': codigo.pk if codigo else None, 'itens': [{'produto': k, 'quantidade': v} for k, v in carrinho.items() if v > 0]})
                if serializer.is_valid():
                    from rest_framework.exceptions import ValidationError
                    try:
                        pedido = serializer.save()
                        request.session['carrinho'] = {}
                        return render(request, 'loja/sucesso.html', {'pedido': pedido})
                    except ValidationError as exc:
                        erro = exc.detail
                else:
                    erro = serializer.errors
    linhas = [{'produto': p, 'quantidade': carrinho[str(p.pk)], 'subtotal': p.preco * carrinho[str(p.pk)]} for p in Produto.objects.filter(pk__in=carrinho) if carrinho[str(p.pk)] > 0]
    return render(request, 'loja/index.html', {'produtos': Produto.objects.select_related('vendedor'), 'linhas': linhas, 'total': sum(l['subtotal'] for l in linhas), 'erro': locals().get('erro')})
