path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Encontra todas as ocorrências de loadRotMapData
matches = list(re.finditer(r'async function loadRotMapData\(\)', content))
print(f'Total loadRotMapData: {len(matches)}')
for m in matches:
    ln = content[:m.start()].count('\n')+1
    antes = content[:m.start()]
    script = antes.count('<script')
    print(f'  Linha {ln}, script {script}')

# Remove a versão do script 4 (a antiga que usa /orders)
# Mantém apenas a do script 3
for m in reversed(matches):
    antes = content[:m.start()]
    opens = antes.count('<script')
    if opens >= 4:  # está no script 4
        # Encontra fim da função
        depth = 0
        i = m.start()
        while i < len(content):
            if content[i] == '{': depth += 1
            elif content[i] == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
            i += 1
        ln = content[:m.start()].count('\n')+1
        print(f'\nRemovendo versão antiga (linha {ln})...')
        content = content[:m.start()] + content[end:]
        print('Removida!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verifica
matches2 = list(re.finditer(r'async function loadRotMapData\(\)', content))
print(f'\nloadRotMapData restantes: {len(matches2)}')
for m in matches2:
    ln = content[:m.start()].count('\n')+1
    print(f'  Linha {ln}')
print('Pronto! Ctrl+Shift+R.')
