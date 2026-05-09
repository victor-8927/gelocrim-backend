path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Mostra as linhas ao redor de 3393-3400
print('=== LINHAS 3390-3402 ===')
for i in range(3389, min(3402, len(lines))):
    print(f'{i+1}: {repr(lines[i][:100])}')

# Mostra também o que vem antes — últimas linhas de JS antes do modal
print('\n=== LINHAS 3380-3398 ===')
for i in range(3379, min(3398, len(lines))):
    if any(kw in lines[i] for kw in ['function', '}', 'var ', 'const ', 'let ', '//', '/*', '</script>', '<!--']):
        print(f'{i+1}: {repr(lines[i][:100])}')
