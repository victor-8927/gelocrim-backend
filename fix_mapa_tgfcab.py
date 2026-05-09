path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = """  var mapa={
    id:       ['NRO UNICO','NUNOTA','NUMNOTA','NRO NOTA','NUMERO'],
    cliente:  ['NOME PARCEIRO','NOMEPARC','NOME PARC','CLIENTE','RAZAOSOCIAL'],
    codparc:  ['PARCEIRO','CODPARC','COD PARC'],
    endereco: ['ENDERECO','ENDCLIENTE','LOGRADOURO'],
    cidade:   ['CIDADE','MUNICIPIO'],
    peso:     ['PESO','PESOLIQ','PESOBRUTO'],
    volume:   ['VOLUME','VOL','CUBAGEM'],
    data:     ['DT NEG','DTNEG','DATA','DATAPED'],
    top:      ['DESCRICAO TIPO DE OPERACAO','CODTIPOPER','TIPOPER','TOP'],
    valor:    ['VLR NOTA','VLRNOTA','VALOR'],
    regiao:   ['CENTRO RESULTADO','ROTA','REGIAO','ZONA'],
  };"""

new = """  var mapa={
    id:       ['NRO UNICO','NRO. UNICO','NUNOTA','NUMNOTA','NRO NOTA','NUMERO'],
    cliente:  ['NOME PARCEIRO PARCEIRO','NOME PARCEIRO (PARCEIRO)','NOMEPARC','NOME PARC','CLIENTE','RAZAOSOCIAL'],
    codparc:  ['PARCEIRO','CODPARC','COD PARC'],
    endereco: ['ENDERECO','ENDCLIENTE','LOGRADOURO'],
    cidade:   ['CIDADE','MUNICIPIO'],
    peso:     ['PESO','PESOLIQ','PESOBRUTO'],
    volume:   ['VOLUME','VOL','CUBAGEM'],
    data:     ['DT. NEG.','DT NEG','DTNEG','DATA','DATAPED'],
    top:      ['DESCRICAO TIPO DE OPERACAO','DESCRICAO (TIPO DE OPERACAO)','CODTIPOPER','TIPOPER','TOP'],
    valor:    ['VLR. NOTA','VLR NOTA','VLRNOTA','VALOR'],
    regiao:   ['CENTRO RESULTADO','DESCRICAO (CENTRO DE RESULTADO)','ROTA','REGIAO','ZONA'],
  };"""

if old in content:
    content = content.replace(old, new)
    print('Mapeamento TGFCAB corrigido!')
else:
    print('Padrão não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R e reimporte.')
