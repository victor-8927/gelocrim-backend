path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Corrige o mapeamento de colunas no lerBaseClientesXLS
old = """      var m = {
        codparc:['CODIGO_ERP','CODPARC','CODIGO'],
        nome:['NOME_FANTASIA','NOMEFANTASIA','NOME'],
        razao_social:['RAZAO_SOCIAL','RAZAOSOCIAL'],
        endereco:['ENDERECO'],cep:['CEP'],bairro:['BAIRRO'],
        cidade:['CIDADEUF','CIDADE'],lat:['LATITUDE','LAT'],lng:['LONGITUDE','LNG'],
        cpf_cnpj:['CPFCNPJ','CPF/CNPJ'],segmento:['SEGMENTO'],
        zona_geo:['ZONA_GEO','ZONAGEO'],comodatos:['COMODATOS'],
        tempo_entrega:['TEMPOMEDIO'],rota:['ROTA'],
      };"""

new = """      var m = {
        codparc:      ['CODIGO_ERP','CODPARC','CODIGO','COD'],
        nome:         ['NOME_FANTASIA','NOMEFANTASIA','NOME FANTASIA','NOME'],
        razao_social: ['RAZAO_SOCIAL','RAZAOSOCIAL','RAZAO SOCIAL'],
        endereco:     ['ENDERECO'],
        cep:          ['CEP'],
        bairro:       ['BAIRRO'],
        cidade:       ['CIDADE/UF','CIDADEUF','CIDADE UF','CIDADE'],
        lat:          ['LATITUDE','LAT'],
        lng:          ['LONGITUDE','LNG'],
        cpf_cnpj:     ['CPF/CNPJ','CPFCNPJ','CPF CNPJ'],
        segmento:     ['SEGMENTO'],
        zona_geo:     ['ZONA_GEO','ZONAGEO','ZONA GEO'],
        comodatos:    ['COMODATOS'],
        tempo_entrega:['TEMPO MEDIO ENTREGA','TEMPOMEDIO','TEMPO MEDIO','TEMPO ENTREGA','TEMPO MEDIOENTREGA'],
        rota:         ['ROTA'],
      };"""

if old in content:
    content = content.replace(old, new)
    print('Mapeamento corrigido!')
else:
    print('Padrao nao encontrado, buscando...')
    # Busca por trecho menor
    idx = content.find("tempo_entrega:['TEMPOMEDIO']")
    if idx != -1:
        print(f'Encontrado em pos {idx}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto!')
