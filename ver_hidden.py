path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica se hidden existe
idx = content.find('v-edit-id')
while idx != -1:
    ln = content[:idx].count('\n')+1
    print(f'Linha {ln}: {repr(content[max(0,idx-20):idx+60])}')
    idx = content.find('v-edit-id', idx+1)
