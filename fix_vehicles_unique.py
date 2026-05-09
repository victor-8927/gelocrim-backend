path = r'C:\fleet-cloud\app\routers\vehicles.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica se tem check de placa duplicada no POST
print('Buscando check de placa...')
idx = content.find('plate')
while idx != -1:
    ctx = content[max(0,idx-30):idx+60]
    if 'already' in ctx.lower() or 'duplicate' in ctx.lower() or 'existe' in ctx.lower() or 'UNIQUE' in ctx:
        print(f'Check encontrado: {repr(ctx)}')
    idx = content.find('plate', idx+1)

# Mostra o endpoint POST completo
idx_post = content.find('@router.post')
if idx_post != -1:
    print('\nEndpoint POST:')
    print(content[idx_post:idx_post+800])
