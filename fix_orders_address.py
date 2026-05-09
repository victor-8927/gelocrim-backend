with open(r'C:\fleet-cloud\app\routers\orders.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui todas as ocorrências de address na query de clientes
content = content.replace(
    '"SELECT lat, lng, address, regiao FROM clientes WHERE codparc = :c"',
    '"SELECT lat, lng, bairro, cidade, regiao FROM clientes WHERE codparc = :c"'
)
content = content.replace(
    'address = cli["address"] if cli and cli.get("address") else ""',
    'bairro = cli["bairro"] if cli and cli.get("bairro") else ""\n        cidade = cli["cidade"] if cli and cli.get("cidade") else "Manaus"\n        address = (bairro + ", " + cidade).strip(", ") if bairro else cidade'
)

with open(r'C:\fleet-cloud\app\routers\orders.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile(r'C:\fleet-cloud\app\routers\orders.py', doraise=True)
    print('VALIDO! Reinicie o servidor.')
except Exception as e:
    print(f'ERRO: {e}')
