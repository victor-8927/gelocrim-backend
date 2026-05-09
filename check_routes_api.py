path = r'C:\fleet-cloud\app\routers\routes.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica se o filtro de motorista ja foi aplicado
if 'current_user.role' in content:
    print('Filtro de motorista ja existe!')
    # Apenas garante que motorista nao precisa de data obrigatoria
else:
    print('Adicionando filtro...')

# Verifica a query atual
idx = content.find('def list_routes')
print('Query atual:')
print(content[idx:idx+600])
