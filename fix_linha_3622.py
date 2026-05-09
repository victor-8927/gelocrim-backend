path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== LINHAS 3618-3628 ===')
for i in range(3617, min(3628, len(lines))):
    print(f'{i+1}: {repr(lines[i][:100])}')

# Corrige todas as template literals problemáticas na região
for i in range(3610, min(3640, len(lines))):
    if '`' in lines[i]:
        original = lines[i]
        lines[i] = lines[i].replace(
            '`${API}/clientes/upload`',
            "API + '/clientes/upload'"
        ).replace(
            '`Bearer ${token}`',
            "'Bearer ' + token"
        ).replace(
            '`${API}/', 
            "API + '/"
        )
        if lines[i] != original:
            print(f'Linha {i+1} corrigida: {repr(lines[i][:80])}')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('\nSalvo! Ctrl+Shift+R.')
