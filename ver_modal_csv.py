path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica se o modal existe
if 'modal-importacao-csv' in content:
    idx = content.find('modal-importacao-csv')
    print(f'Encontrado na posição {idx}')
    print(content[idx:idx+200])
else:
    print('modal-importacao-csv NAO EXISTE no HTML!')

# Quantas vezes aparece
import re
ocorrencias = [m.start() for m in re.finditer('modal-importacao-csv', content)]
print(f'\nTotal de ocorrências: {len(ocorrencias)}')
for pos in ocorrencias:
    print(f'  Pos {pos}: {content[max(0,pos-20):pos+50]}')
