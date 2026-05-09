path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Encontra as duas ocorrências de page-relatorios
ocorrencias = [m.start() for m in re.finditer('id="page-relatorios"', content)]
print(f'Ocorrências: {len(ocorrencias)}')
for o in ocorrencias:
    ln = content[:o].count('\n')+1
    print(f'  linha {ln}')

# A segunda é a duplicata
# Encontra o <div que contém a segunda ocorrência (volta ~100 chars)
idx2 = ocorrencias[1]
# Procura o <div mais próximo antes do idx2
inicio_dup = content.rfind('<div', 0, idx2)
# Mas pode ter um </div> colado - vamos pegar desde o \n antes
inicio_linha = content.rfind('\n', 0, inicio_dup) + 1
ln_ini = content[:inicio_linha].count('\n')+1
print(f'Início duplicata: linha {ln_ini}: {repr(content[inicio_linha:inicio_linha+80])}')

# Encontra o fim - próximo fechamento que deixa depth=0
depth = 0
i = inicio_linha
started = False
fim_dup = None
while i < len(content):
    if content[i:i+4] == '<div':
        depth += 1
        started = True
    elif content[i:i+6] == '</div>':
        if started:
            depth -= 1
            if depth == 0:
                fim_dup = i + 6
                break
    i += 1

ln_fim = content[:fim_dup].count('\n')+1
print(f'Fim duplicata: linha {ln_fim}')
print(f'Removendo {fim_dup - inicio_linha} chars')

# Remove a duplicata
content = content[:inicio_linha] + content[fim_dup:]

opens  = len(re.findall(r'<div[\s>]', content))
closes = len(re.findall(r'</div>', content))
print(f'<div>: {opens} opens, {closes} closes')
print(f'page-relatorios: {content.count("id=\"page-relatorios\"")} vez/vezes')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R')
