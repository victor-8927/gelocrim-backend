path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== ÚLTIMAS 10 LINHAS ===')
for i in range(len(lines)-10, len(lines)):
    print(f'{i+1}: {repr(lines[i])}')
