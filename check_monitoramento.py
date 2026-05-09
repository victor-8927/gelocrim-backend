path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Encontra a página de monitoramento
idx = content.find('id="page-monitoramento"')
ln = content[:idx].count('\n')
print(f'page-monitoramento linha {ln+1}:')
for i in range(ln, ln+50):
    print(f'{i+1}: {lines[i]}')
