path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Mostra linhas 3485-3498 para ver o que está lá
print('=== LINHAS 3485-3498 ===')
for i in range(3484, min(3498, len(lines))):
    print(f'{i+1}: {repr(lines[i])}')

# Remove as declarações duplicadas no segundo script (linhas após 3488)
variaveis_dup = ['var confOrdem', 'var confMap', 'var rotaConfirmada', 'var rotSelecionados']
removidas = []
for i in range(3487, min(3500, len(lines))):
    for v in variaveis_dup:
        if v in lines[i]:
            print(f'\nRemovendo linha {i+1}: {repr(lines[i])}')
            removidas.append(i)

# Remove de trás para frente para não deslocar índices
for i in sorted(removidas, reverse=True):
    del lines[i]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f'\nTotal: {len(lines)} linhas')
print('Pronto! Ctrl+Shift+R.')
