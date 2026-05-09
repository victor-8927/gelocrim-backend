path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra a área de importação de parceiros
idx = content.find('_clientesParaImportar=parceiros')
if idx != -1:
    print(repr(content[idx-100:idx+100]))
else:
    print('NAO ENCONTRADO')
    # Busca alternativa
    idx2 = content.find('clientesParaImportar')
    print(f'clientesParaImportar em: {idx2}')
    if idx2 != -1:
        print(repr(content[idx2-50:idx2+150]))
