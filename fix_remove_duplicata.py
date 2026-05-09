path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Remove linhas 3714-3729 (índices 3713-3728) que têm a versão corrompida
print('Removendo linhas 3714-3729...')
for i in range(3713, min(3729, len(lines))):
    print(f'  Removendo {i+1}: {lines[i][:60]}')

del lines[3713:3729]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f'\nTotal linhas agora: {len(lines)}')
print('Pronto! Ctrl+Shift+R.')
