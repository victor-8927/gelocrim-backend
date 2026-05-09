path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f'Total: {len(lines)}')

print('\n=== LINHAS 3395-3405 ===')
for i in range(3394, min(3405, len(lines))):
    print(f'{i+1}: {repr(lines[i][:120])}')

print('\n=== LINHAS 3732-3742 ===')
for i in range(3731, min(3742, len(lines))):
    print(f'{i+1}: {repr(lines[i][:120])}')
