path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
total = len(lines)
print(f'Total linhas: {total}')
print(f'Total chars: {len(content)}')
print('\nÚltimas 10 linhas:')
for i in range(max(0,total-10), total):
    print(f'{i+1}: {repr(lines[i])}')
