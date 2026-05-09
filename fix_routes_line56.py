path = r'C:\fleet-cloud\app\routers\routes.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Corrige o erro na linha 56
content = content.replace(
    'rows = db.execute(text(q).fetchall, params).fetchall',
    'rows = db.execute(text(q), params).fetchall()'
)
# Corrige outros padrões similares
content = content.replace(
    '.fetchall, ', ', '
)
import re
content = re.sub(r'db\.execute\(text\((\w+)\)\.fetchall,\s*(\w+)\)\.fetchall', 
                 r'db.execute(text(\1), \2).fetchall()', content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('routes.py corrigido!')
