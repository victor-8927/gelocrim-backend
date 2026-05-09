path = r'C:\fleet-cloud\app\routers\orders.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

print('=== ROTAS EXISTENTES ===')
import re
for m in re.finditer(r'@router\.(get|post|put|delete|patch)[^\n]*', content, re.IGNORECASE):
    print(m.group())

print('\n=== POST EXISTS? ===')
print('POST' in content.upper())
