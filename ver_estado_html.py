path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total linhas: {len(lines)}')
print('\n=== ÚLTIMAS 20 LINHAS ===')
for i in range(max(0,len(lines)-20), len(lines)):
    print(f'{i+1}: {lines[i].rstrip()[:100]}')

# Verifica funções importantes
content = ''.join(lines)
funcs = ['doLogin', 'loadOrders', 'gerarRelatorio', 'abrirImportacaoCSV', 
         'abrirImportacaoBaseClientes', 'loadClientes', 'loadVeiculos']
print('\n=== FUNÇÕES PRESENTES ===')
for f in funcs:
    print(f'  {f}: {"✅" if f in content else "❌ FALTANDO"}')
