path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Mostra linhas 515-545
print('LINHAS 515-545:')
for i, line in enumerate(lines[514:544], start=515):
    print(f'{i}: {line.rstrip()}')

print('\n\nProcurando card-sel-veiculo...')
for i, line in enumerate(lines):
    if 'card-sel-veiculo' in line:
        # Mostra contexto
        start = max(0, i-2)
        end   = min(len(lines), i+20)
        print(f'\nEncontrado na linha {i+1}:')
        for j in range(start, end):
            print(f'  {j+1}: {lines[j].rstrip()}')
        break
