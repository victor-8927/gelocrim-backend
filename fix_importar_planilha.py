caminho = r"C:\fleet-cloud\importar_planilha.py"
with open(caminho, encoding="utf-8") as f:
    data = f.read()

# Corrigir para usar NOMEFANTASIA em vez de NOMEPARC
antigo = """        nome = str(row.get('NOMEPARC', '') or '').strip()"""
novo   = """        nome_fantasia = str(row.get('NOMEFANTASIA', '') or '').strip()
        nome_parceiro = str(row.get('NOMEPARC', '') or '').strip()
        nome = nome_fantasia if nome_fantasia and nome_fantasia != 'nan' else nome_parceiro"""

if antigo in data:
    data = data.replace(antigo, novo)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(data)
    print("OK - usando NOMEFANTASIA!")
else:
    # Buscar onde NOMEPARC e usado
    idx = data.find("NOMEPARC")
    print("Nao encontrado, verificando...")
    print(data[max(0,idx-100):idx+200])
