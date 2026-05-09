path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f'Total: {len(lines)}')
for i in range(3393, min(3408, len(lines))):
    print(f'{i+1}: {repr(lines[i][:100])}')
