path = r'C:\fleet-cloud\app\routers\routes.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Corrige a query que busca rotas por data
old_query = "WHERE date(r.created_at) = :d"
new_query = "WHERE r.route_date = :d"

if old_query in content:
    content = content.replace(old_query, new_query)
    print('Query corrigida: route_date!')
else:
    print('Padrao nao encontrado, tentando alternativa...')
    old2 = "WHERE date(created_at) = :d"
    new2 = "WHERE route_date = :d"
    if old2 in content:
        content = content.replace(old2, new2)
        print('Query alternativa corrigida!')
    else:
        # Mostra todas as queries com date para debug
        import re
        matches = re.findall(r'.{50}date\(.{50}', content)
        for m in matches:
            print('Encontrado:', m)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Reinicie a API!')
