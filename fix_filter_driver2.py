path = r'C:\fleet-cloud\app\routers\routes.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui apenas a assinatura da funcao e adiciona filtro
# Troca _ por current_user na assinatura
old_sig = '    _=Depends(get_current_user),\n    db: Session = Depends(get_db),\n):\n    q = """'
new_sig = '    current_user=Depends(get_current_user),\n    db: Session = Depends(get_db),\n):\n    q = """'

if old_sig in content:
    content = content.replace(old_sig, new_sig, 1)
    print('Assinatura corrigida!')
else:
    print('Assinatura nao encontrada, tentando alternativa...')
    # Mostra o trecho para debug
    idx = content.find('def list_routes')
    print(repr(content[idx:idx+200]))

# Adiciona filtro apos o WHERE existente
old_where = '''    params = {}
    if date_:
        q += " WHERE r.route_date = :d"
        params["d"] = str(date_)'''

new_where = '''    params = {}
    wheres = []
    if date_:
        wheres.append("r.route_date = :d")
        params["d"] = str(date_)
    # Motorista so ve suas proprias rotas
    if hasattr(current_user, 'role') and current_user.role == 'driver':
        driver_id = getattr(current_user, 'driver_id', None)
        if driver_id:
            wheres.append("r.driver_id = :driver_id")
            params["driver_id"] = str(driver_id)
    if wheres:
        q += " WHERE " + " AND ".join(wheres)'''

if old_where in content:
    content = content.replace(old_where, new_where, 1)
    print('Filtro WHERE adicionado!')
else:
    print('WHERE nao encontrado, tentando...')
    idx = content.find('params = {}')
    print(repr(content[idx:idx+200]))

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Reinicie a API.')
