path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== LINHAS 3742-3752 ===')
for i in range(3741, min(3752, len(lines))):
    print(f'{i+1}: {repr(lines[i][:120])}')
