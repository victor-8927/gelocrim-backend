path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_mapa = '''  // Mapeamento Sankhya → campos do app
  const mapa = {
    id:       ['NUNOTA','NUMNOTA','NUMNOT','PEDIDO','NOTA'],
    cliente:  ['NOMEPARC','NOME','NOMECLIENTE','CLIENTE','RAZAOSOCIAL','RAZAOSOC'],
    endereco: ['ENDERECO','ENDCOB','ENDERECOCOB','LOGRADOURO','END'],
    cidade:   ['CIDADE','MUNICIPIO','NOMECIDADE','CIDADECOB'],
    bairro:   ['BAIRRO','BAIRROCOB'],
    peso:     ['PESO','PESOLIQ','PESOBRUTO','PESONOTA'],
    volume:   ['VOLUME','VOL','CUBAGEM','VOLUMETOTAL'],
    data:     ['DTNEG','DTNEGOCIACAO','DATA','DATAPED','DTPED'],
    top:      ['CODTIPOPER','TIPOPER','TOP','TIPOOPER'],
    valor:    ['VLRNOTA','VALOR','VLRTOTAL','TOTALNOTAFISCAL'],
    codparc:  ['CODPARC','CODCLIENTE','CODFORNEC'],
    regiao:   ['ROTA','REGIAO','ZONA','CODREGIAO'],
  };'''

new_mapa = '''  // Mapeamento Sankhya → campos do app (colunas reais do TGFCAB)
  const mapa = {
    id:       ['NRO UNICO','NROUNICO','NRO. UNICO','NUNOTA','NUMNOTA','PEDIDO','NOTA'],
    cliente:  ['NOME PARCEIRO (PARCEIRO)','NOMEPARC','NOME PARCEIRO','NOMECLIENTE','CLIENTE','NOME FANTASIA (EMPRESA)'],
    endereco: ['ENDERECO','ENDCOB','LOGRADOURO','END'],
    cidade:   ['CIDADE','MUNICIPIO','NOMECIDADE'],
    bairro:   ['BAIRRO'],
    peso:     ['PESO','PESOLIQ','PESOBRUTO','PESONOTA'],
    volume:   ['VOLUME','VOL','CUBAGEM'],
    data:     ['DT. NEG.','DTNEG','DTNEGOCIACAO','DATA','DT NEG'],
    top:      ['DESCRICAO (TIPO DE OPERACAO)','TIPO OPERACAO','CODTIPOPER','TIPOPER','TOP','TIPO OPERAÇÃO','DESCRICÃO (TIPO DE OPERAÇÃO)'],
    valor:    ['VLR. NOTA','VLRNOTA','VALOR','VLR NOTA','VLRTOTAL'],
    codparc:  ['PARCEIRO','CODPARC','CODCLIENTE'],
    nronota:  ['NRO. NOTA','NRONOTA','NRO NOTA'],
    regiao:   ['ROTA','REGIAO','ZONA','CENTRO RESULTADO','DESCRICAO (CENTRO DE RESULTADO)'],
  };'''

if old_mapa in content:
    content = content.replace(old_mapa, new_mapa)
    print('Mapeamento atualizado com colunas reais do Sankhya!')
else:
    print('Padrão não encontrado, buscando...')
    idx = content.find("id:       ['NUNOTA'")
    if idx != -1:
        print(content[max(0,idx-100):idx+400])

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Ctrl+Shift+R e teste novamente.')
