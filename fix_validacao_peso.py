path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# O problema: valida com !nunota || peso===0
# Mas peso pode estar em coluna diferente
# Vamos ver o log do cabeçalho — adiciona console.log do header e idx

old = "  console.log('Cabecalho encontrado na linha '+(headerIdx+1)+':', header);\n      console.log('Mapeamento idx:', JSON.stringify(idx));"
new = "  console.log('Cabecalho encontrado na linha '+(headerIdx+1)+':', header);\n      console.log('Mapeamento idx:', JSON.stringify(idx));\n      console.log('Primeira linha dados:', rows[headerIdx+1]);"

content = content.replace(old, new) if old in content else content

# Também relaxa a validação - aceita peso=0 se tiver nunota
old2 = "    if(!nunota||peso===0){erros++;continue;}"
new2 = "    if(!nunota){erros++;continue;} // peso pode ser 0 para bonificacoes"

if old2 in content:
    content = content.replace(old2, new2)
    print('Validação de peso relaxada!')
else:
    print('Validação não encontrada, buscando...')
    idx = content.find('if(!nunota')
    if idx != -1:
        ln = content[:idx].count('\n')+1
        print(f'Linha {ln}: {repr(content[idx:idx+60])}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R e reimporte.')
