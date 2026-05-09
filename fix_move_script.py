path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Linha 3483 tem </script> no meio do HTML do modal
# Remove esse </script> (índice 3482)
print(f'Removendo linha 3483: {repr(lines[3482])}')
del lines[3482]

# Agora o script de clientes começa na linha 3483 (era 3484)
# Precisa que o HTML do modal fique FORA do script
# Verifica o que ficou
print('Linha 3480-3486 após remoção:')
for i in range(3479, min(3486, len(lines))):
    print(f'{i+1}: {repr(lines[i][:80])}')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f'\nTotal: {len(lines)}')
print('Pronto! Ctrl+Shift+R.')
