import py_compile
try:
    py_compile.compile(r'C:\fleet-cloud\app\routers\orders.py', doraise=True)
    print('orders.py VALIDO')
except Exception as e:
    print(f'ERRO: {e}')

# Ver o endpoint bulk_planilha
with open(r'C:\fleet-cloud\app\routers\orders.py', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('bulk_planilha')
ln = content[:idx].count('\n')
lines = content.split('\n')
print('\nbulk_planilha:')
for i in range(ln, ln+60):
    print(f'{i+1}: {lines[i]}')
