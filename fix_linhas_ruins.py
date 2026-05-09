path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total antes: {len(lines)}')

# Remove linhas problemáticas
linhas_remover = []
for i, line in enumerate(lines):
    if '... outras funções ...' in line:
        linhas_remover.append(i)
        print(f'Removendo linha {i+1}: {repr(line[:60])}')
    # Remove } solto depois do DOMContentLoaded
    
# Remove do final para o início
for i in reversed(linhas_remover):
    del lines[i]

# Verifica e remove linha '}' solta após DOMContentLoaded duplicado
for i in range(len(lines)-1, 0, -1):
    if lines[i].strip() == '}' and i > 0:
        prev = lines[i-1].strip()
        if 'carregarBaseClientes' in prev:
            print(f'Removendo }} solto na linha {i+1}')
            del lines[i]
            break

# Remove DOMContentLoaded duplicado
found_dom = False
for i in range(len(lines)-1, 0, -1):
    if 'carregarBaseClientes' in lines[i]:
        if found_dom:
            print(f'Removendo DOMContentLoaded duplicado linha {i+1}')
            del lines[i]
        else:
            found_dom = True

print(f'Total depois: {len(lines)}')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Salvo! Ctrl+Shift+R.')
