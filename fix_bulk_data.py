with open(r'C:\fleet-cloud\app\routers\orders.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''                    "id": str(uuid.uuid4()),
                    "codparc": p.codparc,
                    "top_app": p.external_id,
                    "tipo": item.cod,
                    "nome": item.nome,
                    "peso": item.peso_unit,
                    "qtd": item.qtd,
                    "dt": p.data or ""'''

new = '''                    "id": str(uuid.uuid4()),
                    "codparc": p.codparc,
                    "top_app": str(p.top_app or p.external_id),
                    "tipo": str(item.cod),
                    "nome": str(item.nome),
                    "peso": float(item.peso_unit),
                    "qtd": int(item.qtd),
                    "dt": str(p.data or "")[:10]'''

if old in content:
    content = content.replace(old, new)
    print('Tipos corrigidos!')
else:
    print('Padrão não encontrado!')

# Também corrige a data no JS - converte serial Excel para string
with open(r'C:\fleet-cloud\app\routers\orders.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile(r'C:\fleet-cloud\app\routers\orders.py', doraise=True)
    print('VÁLIDO!')
except Exception as e:
    print(f'ERRO: {e}')
