path = r'C:\fleet-cloud\app\routers\orders.py'

with open(path, 'r') as f:
    content = f.read()

# Substitui Dict[str, Any] por dict simples (Python 3.9+)
content = content.replace(
    'order: Dict[str, Any] = Body(...)',
    'order: dict = Body(...)'
)

# Remove import typing se foi adicionado
content = content.replace('from typing import Any, Dict\n', '')

print('Corrigido!')

with open(path, 'w') as f:
    f.write(content)

print('Reinicie o servidor agora!')
