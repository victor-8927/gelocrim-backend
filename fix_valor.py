caminho = r"C:\fleet-cloud\importar_planilha.py"
with open(caminho, encoding="utf-8") as f:
    data = f.read()

antigo = """        try:
            vlr = float(str(row.get('VLRNOTA','0') or '0').strip().replace(',','.'))
        except:
            vlr = 0"""

novo = """        try:
            vlr_raw = str(row.get('VLRNOTA','0') or '0').strip()
            # Formato brasileiro: 1.737,50 -> remover ponto de milhar, trocar virgula por ponto
            vlr_raw = vlr_raw.replace('.','').replace(',','.')
            vlr = float(vlr_raw) if vlr_raw else 0
        except:
            vlr = 0"""

if antigo in data:
    data = data.replace(antigo, novo)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(data)
    print("OK - conversao de valor corrigida!")
else:
    print("Trecho nao encontrado, verificando formato atual...")
    idx = data.find("VLRNOTA")
    print(data[max(0,idx-100):idx+300])
