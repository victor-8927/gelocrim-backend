orders_path = r'C:\fleet-cloud\app\routers\orders.py'

with open(orders_path, 'r') as f:
    content = f.read()

print('=== INICIO ===')
print(content[:300])

# Verifica se text está importado
if 'from sqlalchemy.sql import text' not in content and 'from sqlalchemy import' in content:
    import re
    content = re.sub(
        r'from sqlalchemy import ([^\n]+)',
        r'from sqlalchemy import \1\nfrom sqlalchemy.sql import text',
        content, count=1
    )
    print('text importado!')
elif 'from sqlalchemy.sql import text' in content:
    print('text já importado!')
else:
    # Adiciona no topo
    content = 'from sqlalchemy.sql import text\n' + content
    print('text adicionado no topo!')

# Agora substitui o INSERT no POST
import re

# Encontra o POST e substitui o execute
old_exec = '"INSERT INTO orders (" + ",".join(cols) + ") VALUES (" +\n            ",".join(["?"]*len(cols)) + ")"'
new_exec = 'text("INSERT INTO orders (" + ",".join(cols) + ") VALUES (" + ",".join([":"+c for c in cols]) + ")")'

if '"INSERT INTO orders' in content:
    # Substitui qualquer INSERT orders sem text()
    content = re.sub(
        r'(?<!text\()("INSERT INTO orders \(" \+ ",".join\(cols\) \+ "\) VALUES \(" \+\s*",".join\(\["\\?"\]\*len\(cols\)\) \+ "\)")',
        r'text("INSERT INTO orders (" + ",".join(cols) + ") VALUES (" + ",".join([":"+c for c in cols]) + ")")',
        content
    )
    
    # Muda vals de lista para dict se necessário
    content = content.replace(
        'vals = [order.get(c) for c in cols]',
        'vals = {c: order.get(c) for c in cols}'
    )
    print('INSERT corrigido!')

print('\n=== POST RESULTANTE ===')
m = re.search(r'@router\.post\(""\).*?(?=@router)', content, re.DOTALL)
if m:
    print(m.group()[:500])

with open(orders_path, 'w') as f:
    f.write(content)

print('\nSalvo! Reinicie o servidor.')
