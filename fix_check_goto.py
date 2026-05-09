path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
idx = content.find('function goTo(')
ln = content[:idx].count('\n')
print('goTo função:')
for i in range(ln, ln+20):
    print(f'{i+1}: {lines[i]}')
