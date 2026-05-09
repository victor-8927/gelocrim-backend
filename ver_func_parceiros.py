path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica quantas vezes aparece
import re
ocorr = [m.start() for m in re.finditer('abrirImportacaoBaseClientes', content)]
print(f'Total ocorrências: {len(ocorr)}')
for pos in ocorr:
    print(f'  Pos {pos}: {content[max(0,pos-30):pos+60]}')

# Verifica se a função está definida
if 'function abrirImportacaoBaseClientes' in content:
    print('\nFunção EXISTE!')
    idx = content.find('function abrirImportacaoBaseClientes')
    print(content[idx:idx+200])
else:
    print('\nFunção NAO EXISTE — precisa ser adicionada!')
