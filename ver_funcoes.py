path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
funcs = re.findall(r'(?:async\s+)?function\s+(\w+)\s*\(', content)
print(f'Total funções: {len(funcs)}')

# Funções críticas que devem existir
criticas = ['doLogin','loadOrders','loadVehicles','loadDrivers','loadRoutes',
            'loadDashboard','gerarRomaneio','abrirImportacaoCSV','lerArquivoCSV',
            'importarCSV','loadClientes','abrirImportacaoBaseClientes',
            'lerBaseClientesXLS','importarBaseClientes','loadProducao',
            'loadRotMapData','loadOcorrencias','loadMonitoring','loadReports']

print('\n=== FUNÇÕES CRÍTICAS ===')
for f in criticas:
    status = '✅' if f in funcs else '❌ FALTANDO'
    print(f'  {status} {f}')
