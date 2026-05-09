path = r'C:\fleet-cloud\app\main.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Remove linhas 62 até o fim do bloco order_items (linha 62 em diante até fechar)
new_lines = []
skip = False
for i, line in enumerate(lines):
    if '# ── ORDER ITEMS' in line:
        skip = True
    if skip and line.strip().startswith('@app.include_router'):
        skip = False
    if not skip:
        new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f'Linhas antes: {len(lines)}, depois: {len(new_lines)}')

# Verifica se include_router de order_items já está
content = open(path).read()
if 'order_items_router' not in content:
    # Adiciona após clientes_router
    content = content.replace(
        'app.include_router(clientes_router)',
        'app.include_router(clientes_router)\napp.include_router(order_items_router)'
    )
    content = content.replace(
        'from app.routers.clientes import router as clientes_router\n',
        'from app.routers.clientes import router as clientes_router\nfrom app.routers.order_items import router as order_items_router\n'
    )
    with open(path, 'w') as f:
        f.write(content)
    print('Router order_items adicionado!')
else:
    print('Router order_items já registrado!')

print('Pronto! Reinicie o servidor.')
