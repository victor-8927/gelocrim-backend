import os

path = r'C:\fleet-cloud\app\routers\routes.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Corrige importacao errada
content = content.replace(
    'from sqlalchemy.ext.asyncio import Session',
    'from sqlalchemy.orm import Session'
)
content = content.replace(
    'from sqlalchemy.ext.asyncio import AsyncSession',
    'from sqlalchemy.orm import Session'
)
content = content.replace('AsyncSession', 'Session')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('routes.py corrigido!')

# Verifica se ainda tem imports errados
if 'asyncio' in content and 'Session' in content:
    print('AVISO: Ainda pode ter imports asyncio')
else:
    print('OK: Sem imports asyncio')
