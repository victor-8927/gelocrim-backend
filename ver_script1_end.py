path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== LINHAS 3388-3402 ===')
for i in range(3387, min(3402, len(lines))):
    print(f'{i+1}: {repr(lines[i][:110])}')
