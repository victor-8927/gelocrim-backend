path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Busca loadVehicles no segundo script
idx = content.find('async function loadVehicles()')
if idx != -1:
    ln = content[:idx].count('\n')+1
    print(f'loadVehicles na linha {ln}')
    print(content[idx:idx+600])
