path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

idx = content.find('function loadMonitoring')
if idx == -1:
    idx = content.find('async function loadMonitoring')
ln = content[:idx].count('\n')
print(f'loadMonitoring linha {ln+1}:')
for i in range(ln, ln+60):
    print(f'{i+1}: {lines[i]}')
    if i > ln and lines[i].strip() == '}' and lines[i-1].strip() != '':
        break
