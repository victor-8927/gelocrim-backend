path = r'C:\fleet-cloud\app\main.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove a classe duplicada e usa a definição correta
old = """class OrderItemBulk(BaseModel):
    items: list"""

# Verifica se já existe outra classe BaseModel
if 'from pydantic import BaseModel' in content or 'BaseModel' in content[:500]:
    print('BaseModel já importado!')
else:
    print('BaseModel NÃO importado!')

# Mostra as primeiras linhas para ver imports
print('\nPrimeiras 20 linhas:')
lines = content.split('\n')
for i,l in enumerate(lines[:20]):
    print(f'{i+1}: {l}')

# Mostra onde foi inserido o endpoint
idx = content.find('class OrderItemBulk')
ln = content[:idx].count('\n')+1
print(f'\nOrderItemBulk linha {ln}')
print(repr(content[max(0,idx-100):idx+50]))
