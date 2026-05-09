path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
opens  = len(re.findall(r'<script[^>]*>', content))
closes = len(re.findall(r'</script>', content))
print(f'Scripts: {opens} opens / {closes} closes')

# Posição de cada </script>
for m in re.finditer(r'</script>', content):
    line = content[:m.start()].count('\n') + 1
    ctx  = content[max(0,m.start()-40):m.start()]
    print(f'  </script> linha {line}: {repr(ctx[-40:])}')

# Verifica onde loadVehicles foi injetada
idx = content.find('async function loadVehicles')
if idx != -1:
    line = content[:idx].count('\n') + 1
    # Verifica se está dentro de um script aberto
    antes = content[:idx]
    opens_antes  = len(re.findall(r'<script[^>]*>', antes))
    closes_antes = len(re.findall(r'</script>', antes))
    print(f'\nloadVehicles na linha {line}')
    print(f'Scripts antes: {opens_antes} opens / {closes_antes} closes')
    print(f'Status: {"DENTRO de script" if opens_antes > closes_antes else "FORA de script!"}')
