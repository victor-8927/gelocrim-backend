caminho = r"C:\fleet-cloud\gelocrim_v1.html"
with open(caminho, encoding="utf-8", errors="ignore") as f:
    data = f.read()

# 1. Adicionar aliases do novo formato Sankhya no mapa
antigo = """    id:['NRO UNICO','NUNOTA','NUMNOTA','NRO NOTA','NUMERO'],
    cliente:['NOME PARCEIRO','NOMEPARC','NOME PARC','CLIENTE','RAZAOSOCIAL'],
    codparc:['PARCEIRO','CODPARC','COD PARC'],
    endereco:['ENDERECO','ENDCLIENTE','LOGRADOURO'],
    cidade:['CIDADE','MUNICIPIO'],
    peso:['PESO','PESOLIQ','PESOBRUTO'],
    volume:['VOLUME','VOL','CUBAGEM'],
    data:['DT NEG','DTNEG','DATA','DATAPED'],
    top:['DESCRICAO TIPO DE OPERACAO','CODTIPOPER','TIPOPER','TOP'],
    valor:['VLR NOTA','VLRNOTA','VALOR'],
    regiao:['CENTRO RESULTADO','ROTA','REGIAO','ZONA'],"""

novo = """    id:['NRO UNICO','NUNOTA','NUMNOTA','NRO NOTA','NUMERO','NRO.','NRO'],
    cliente:['NOME PARCEIRO (PARCEIRO)','NOME PARCEIRO','NOMEPARC','NOME PARC','CLIENTE','RAZAOSOCIAL'],
    codparc:['PARCEIRO','CODPARC','COD PARC'],
    endereco:['ENDERECO','ENDCLIENTE','LOGRADOURO'],
    cidade:['CIDADE','MUNICIPIO'],
    peso:['PESO','PESOLIQ','PESOBRUTO'],
    volume:['VOLUME','VOL','CUBAGEM'],
    data:['DT. NEG.','DT NEG','DTNEG','DATA','DATAPED'],
    top:['TIPO OPERACAO','TIPO OPERA','DESCRICAO TIPO DE OPERACAO','CODTIPOPER','TIPOPER','TOP'],
    valor:['VLR. NOTA','VLR NOTA','VLRNOTA','VALOR'],
    regiao:['CENTRO RESULTADO','ROTA','REGIAO','ZONA'],"""

if antigo in data:
    data = data.replace(antigo, novo)
    print("OK1 - aliases adicionados!")
else:
    print("ERRO1 - nao encontrado")

# 2. Remover prefixo SNK-
antigo2 = "external_id:'SNK-'+nunota,"
novo2   = "external_id:nunota,"

if antigo2 in data:
    data = data.replace(antigo2, novo2)
    print("OK2 - prefixo SNK removido!")
else:
    print("ERRO2")

# 3. Corrigir mapeamento de TOP - novo formato usa numero direto (1000, 1009 etc)
antigo3 = """var mapa={'1100':'1000','1126':'1009','1117':'1007','1118':'1008','1127':'1010'};
        return mapa[t]||t||'1000';"""
novo3   = """var mapa={'1100':'1000','1126':'1009','1117':'1007','1118':'1008','1127':'1010'};
        // Novo formato ja vem com 1000, 1009 etc diretamente
        return mapa[t]||t||'1000';"""

# Nao precisa mudar - ja funciona

with open(caminho, "w", encoding="utf-8") as f:
    f.write(data)
print("Salvo!")
