path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Ver linhas 4088-4135
print('=== 4088-4135 ===')
for i in range(4087, min(4135, len(lines))):
    print(f'{i+1}: {repr(lines[i][:100])}')
