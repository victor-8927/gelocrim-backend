HTML_PATH = r'C:\fleet-cloud\gelocrim_v1.html'

with open(HTML_PATH, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Corrigir mapeamento para incluir variações exatas do Sankhya
OLD = "valor:['VLR. NOTA','VLR NOTA','VLRNOTA','VALOR'],"
NEW = "valor:['VLR. NOTA','VLR NOTA','VLRNOTA','VALOR','Vlr. Nota','VLR.NOTA','VLRNOTA','vlr. nota','vlrnota'],"

if OLD in content:
    content = content.replace(OLD, NEW)
    print("OK! Mapeamento Vlr. Nota corrigido!")
else:
    # Tentar encontrar e mostrar o que existe
    import re
    m = re.search(r'valor:\[.*?\]', content)
    if m:
        print("Encontrado:", m.group())
        print("Substituindo...")
        content = re.sub(r"valor:\[.*?\]", "valor:['VLR. NOTA','VLR NOTA','VLRNOTA','VALOR','Vlr. Nota','VLR.NOTA','vlr. nota','vlrnota']", content)
        print("OK!")
    else:
        print("Nao encontrado — verificar manualmente")

# Corrigir também o mapeamento do TOP/CODTIPOPER
OLD_TOP = "top:['TIPO OPERACAO','CODTIPOPER','TOP','TIPO DE OPERACAO','TIPOPER','DESCRICAO TIPO DE OPERACAO'],"
NEW_TOP = "top:['TIPO OPERACAO','CODTIPOPER','TOP','TIPO DE OPERACAO','TIPOPER','DESCRICAO TIPO DE OPERACAO','Tipo Operação','TIPO OPERACAO','tipo operacao'],"
if OLD_TOP in content:
    content = content.replace(OLD_TOP, NEW_TOP)
    print("OK! Mapeamento TOP corrigido!")

# Corrigir mapeamento do id/NUNOTA
OLD_ID = "id:['NUNOTA','NRO. UNICO','NRO UNICO','NOTA','NUMERO NOTA','NF'],"
NEW_ID = "id:['NUNOTA','NRO. UNICO','NRO UNICO','NOTA','NUMERO NOTA','NF','Nro. Único','Nro. Unico','NRO. ÚNICO'],"
if OLD_ID in content:
    content = content.replace(OLD_ID, NEW_ID)
    print("OK! Mapeamento ID corrigido!")

# Corrigir mapeamento PESO
OLD_PESO = "peso:['PESO','WEIGHT','PESO_KG','PESO KG'],"
NEW_PESO = "peso:['PESO','WEIGHT','PESO_KG','PESO KG','Peso'],"
if OLD_PESO in content:
    content = content.replace(OLD_PESO, NEW_PESO)
    print("OK! Mapeamento PESO corrigido!")

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nRecarregue com Ctrl+Shift+R e reimporte o arquivo!")
