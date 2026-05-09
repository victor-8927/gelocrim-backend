path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
calls = re.findall(r'.{50}carregarFrota\(\).{50}', content)
print('Chamadas de carregarFrota:')
for c in calls:
    print(' ', c)

# Verifica se é chamada quando roteirização abre
idx = content.find("if(page==='roteirizacao')")
print('\ngoTo roteirizacao:')
print(content[idx:idx+200])
