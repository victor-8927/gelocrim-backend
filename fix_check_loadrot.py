path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Ver função loadRotMapData
idx = content.find('function loadRotMapData')
if idx == -1:
    idx = content.find('async function loadRotMapData')
ln = content[:idx].count('\n')
print('loadRotMapData:')
for i in range(ln, ln+60):
    print(f'{i+1}: {lines[i]}')
