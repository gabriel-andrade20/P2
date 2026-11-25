# VendeHub

Mini marketplace desenvolvido com Python, Django, Django REST Framework e SQLite. Permite cadastrar vendedores, produtos e cupons, montar um carrinho e finalizar pedidos com baixa de estoque.

## Como executar

É necessário ter Python 3.10 ou superior instalado. Abra o terminal na pasta do projeto e execute:

```bash
python -m venv .venv
```

No Windows, ative com `.venv\Scripts\activate`. No Linux ou macOS, use `source .venv/bin/activate`.

```bash
pip install -r requirements.txt
python manage.py makemigrations loja
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse http://127.0.0.1:8000/ para abrir a loja. Entre em `/admin/` com o superusuário e cadastre vendedores, produtos e cupons. O desconto do cupom é percentual. O dashboard está em `/dashboard/`.

## API

Acesse `/api/` após entrar como administrador. Os endpoints são `/api/vendedores/`, `/api/produtos/`, `/api/cupons/` e `/api/pedidos/`. Pedidos permitem criação e consulta, mas não edição ou exclusão.

Exemplo de POST para `/api/pedidos/`, considerando produtos já cadastrados com IDs 1 e 2:

```json
{"cliente":"Maria","cupom":null,"itens":[{"produto":1,"quantidade":2},{"produto":2,"quantidade":1}]}
```

O servidor calcula os preços e o desconto, verifica o estoque e registra o pedido em uma transação. Se faltar estoque, o pedido inteiro é desfeito.

## Escopo

Projeto acadêmico local, com administração centralizada, carrinho por sessão e vendedores associados aos produtos. Não inclui pagamentos reais, frete ou contas individuais de vendedores.
