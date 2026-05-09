path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f'Total: {len(lines)}')
print('\n=== 3478-3490 ===')
for i in range(3477, min(3490, len(lines))):
    print(f'{i+1}: {repr(lines[i][:120])}')
