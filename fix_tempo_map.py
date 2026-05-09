path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Corrige o mapeamento de tempo_entrega para pegar variações com acento
old = "        tempo_entrega:['TEMPO MEDIO ENTREGA','TEMPOMEDIO','TEMPO MEDIO','TEMPO ENTREGA','TEMPO MEDIOENTREGA'],"
new = "        tempo_entrega:['TEMPO MEDIO ENTREGA','TEMPO MDIO ENTREGA','TEMPOMEDIO','TEMPO MEDIO','TEMPO ENTREGA','TEMPO MEDIOENTREGA','TEMPOMEDIOENTREGA','TEMPO'],"

if old in content:
    content = content.replace(old, new)
    print('Mapeamento atualizado!')
else:
    print('Nao encontrado, buscando...')
    idx = content.find('tempo_entrega:[')
    if idx != -1:
        end = content.find(']', idx)
        print(f'Atual: {repr(content[idx:end+1])}')

# Adiciona log de debug no processamento
old2 = "      console.log('Cabeçalho encontrado na linha '+(headerIdx+1)+':', header);"
new2 = """      console.log('Cabecalho encontrado na linha '+(headerIdx+1)+':', header);
      console.log('Mapeamento idx:', JSON.stringify(idx));"""

content = content.replace(old2, new2) if old2 in content else content

# Também garante que a normalização remove acentos corretamente
# O header é normalizado com NFD mas 'Tempo Médio' vira 'Tempo Medio' após NFD
# Vamos garantir que busca por substring também
old3 = """        mapa[campo].forEach(function(o){
      if(idx[campo]===-1){
        var found=header.findIndex(function(h){return h===o||h.indexOf(o)>=0;});
        if(found!==-1) idx[campo]=found;
      }
    });"""

new3 = """        mapa[campo].forEach(function(o){
      if(idx[campo]===-1){
        var found=header.findIndex(function(h){
          return h===o || h.indexOf(o)>=0 || o.indexOf(h)>=0;
        });
        if(found!==-1) idx[campo]=found;
      }
    });"""

if old3 in content:
    content = content.replace(old3, new3)
    print('Busca por substring bidirecional adicionada!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Reimporte a planilha.')
