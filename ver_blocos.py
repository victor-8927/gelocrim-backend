path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f'Total: {len(lines)}')
print('\n=== 3440-3462 ===')
for i in range(3439, min(3462, len(lines))):
    print(f'{i+1}: {repr(lines[i][:100])}')
print('\n=== 3490-3510 ===')
for i in range(3489, min(3510, len(lines))):
    print(f'{i+1}: {repr(lines[i][:100])}')
