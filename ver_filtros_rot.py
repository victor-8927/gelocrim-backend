path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica se os filtros HTML existem
for el in ['rot-filtro-rota','rot-filtro-top','rot-filtro-busca']:
    count = content.count('id="'+el+'"')
    print(f'{el}: {count} ocorrências')
    idx = content.find('id="'+el+'"')
    if idx != -1:
        ln = content[:idx].count('\n')+1
        print(f'  linha {ln}: {repr(content[max(0,idx-20):idx+80])}')
