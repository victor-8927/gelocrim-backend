HTML_PATH = r'C:\fleet-cloud\gelocrim_v1.html'

with open(HTML_PATH, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

changes = 0

# O problema: o SheetJS normaliza headers mas nao remove acentos
# Precisamos adicionar normalize NFD no processamento do CSV/XLSX

# Corrigir a funcao que processa headers do XLSX (planilha TI)
OLD_NORM_PLANILHA = "function col(row, nomes) {"
NEW_NORM_PLANILHA = """function removeAcentos(s) {
        return String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toUpperCase().replace(/[^A-Z0-9]/g,'');
      }
      function col(row, nomes) {"""

if OLD_NORM_PLANILHA in content:
    content = content.replace(OLD_NORM_PLANILHA, NEW_NORM_PLANILHA, 1)
    changes += 1
    print("OK: funcao removeAcentos adicionada")

# Corrigir o mapeamento do CSV para usar normalizacao sem acento
OLD_MAPA = """    id:['NRO UNICO','NUNOTA','NUMNOTA','NRO NOTA','NUMERO','NRO.','NRO'],
    cliente:['NOME PARCEIRO (PARCEIRO)','NOME PARCEIRO','NOMEPARC','NOME PARC','CLIENTE','RAZAOSOCIAL'],
    codparc:['PARCEIRO','CODPARC','COD PARC'],
    endereco:['ENDERECO','ENDCLIENTE','LOGRADOURO'],
    cidade:['CIDADE','MUNICIPIO'],
    peso:['PESO','PESOLIQ','PESOBRUTO'],
    volume:['VOLUME','VOL','CUBAGEM'],
    data:['DT. NEG.','DT NEG','DTNEG','DATA','DATAPED'],
    top:['TIPO OPERACAO','TIPO OPERA','DESCRICAO TIPO DE OPERACAO','CODTIPOPER','TIPOPER','TOP'],
    valor:['VLR. NOTA','VLR NOTA','VLRNOTA','VALOR','Vlr. Nota','VLR.NOTA','vlr. nota','vlrnota'],"""

NEW_MAPA = """    id:['NROUNICO','NUNOTA','NUMNOTA','NRONOTA','NUMERO','NRO','NROUNICO'],
    cliente:['NOMEPARCEIRO(PARCEIRO)','NOMEPARCEIRO','NOMEPARC','NOMEPAR','CLIENTE','RAZAOSOCIAL'],
    codparc:['PARCEIRO','CODPARC','CODPAR'],
    endereco:['ENDERECO','ENDCLIENTE','LOGRADOURO'],
    cidade:['CIDADE','MUNICIPIO'],
    peso:['PESO','PESOLIQ','PESOBRUTO'],
    volume:['VOLUME','VOL','CUBAGEM'],
    data:['DTNEG','DTneg','DATA','DATAPED'],
    top:['TIPOOPERACAO','TIPOOPERA','DESCRICAOTIPODEOPERACAO','CODTIPOPER','TIPOPER','TOP'],
    valor:['VLRNOTA','VLRNOTA','VALOR'],"""

if OLD_MAPA in content:
    content = content.replace(OLD_MAPA, NEW_MAPA)
    changes += 1
    print("OK: mapeamento atualizado sem acentos")
else:
    print("AVISO: mapeamento nao encontrado exatamente - tentando parcial")
    import re
    # Substituir apenas o mapeamento de id
    content = re.sub(
        r"id:\['NRO UNICO'.*?\]",
        "id:['NROUNICO','NUNOTA','NUMNOTA','NRONOTA','NUMERO','NRO']",
        content
    )
    content = re.sub(
        r"top:\['TIPO OPERACAO'.*?\]",
        "top:['TIPOOPERACAO','TIPOOPERA','CODTIPOPER','TIPOPER','TOP']",
        content
    )
    content = re.sub(
        r"cliente:\['NOME PARCEIRO.*?\]",
        "cliente:['NOMEPARCEIRO(PARCEIRO)','NOMEPARCEIRO','NOMEPARC','CLIENTE','RAZAOSOCIAL']",
        content
    )
    changes += 1
    print("OK: mapeamentos corrigidos via regex")

# Corrigir a normalizacao do header no processarLinhas
OLD_NORM = "var norm=rows[r].map(function(h){return String(h||'').toUpperCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');"
NEW_NORM = "var norm=rows[r].map(function(h){return String(h||'').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toUpperCase().replace(/[^A-Z0-9]/g,'');"

if OLD_NORM in content:
    content = content.replace(OLD_NORM, NEW_NORM)
    changes += 1
    print("OK: normalizacao de header corrigida (remove acentos E caracteres especiais)")
else:
    # Tentar variacao
    import re
    pattern = r"var norm=rows\[r\]\.map\(function\(h\)\{return String\(h\|"
    if re.search(pattern, content):
        content = re.sub(
            r"(var norm=rows\[r\]\.map\(function\(h\)\{return String\(h\|\|''\))(\.[^;]+;)",
            r"\1.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toUpperCase().replace(/[^A-Z0-9]/g,'');",
            content
        )
        changes += 1
        print("OK: normalizacao corrigida via regex")
    else:
        print("AVISO: normalizacao nao encontrada")

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes} correcoes aplicadas!")
print("Recarregue com Ctrl+Shift+R e reimporte o arquivo!")
