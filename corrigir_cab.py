caminho = r"C:\fleet-cloud\importar_cab.py"
with open(caminho, encoding="utf-8") as f:
    data = f.read()

# Substituir a linha problematica
antigo = "    df = pd.read_excel(xlsx_path, header=2, dtype=str)\n    df = df.dropna(subset=['Nro. Unico' if 'Nro. Unico' in df.columns else 'Nro. \u00danico'])"

novo = """    # Detectar header automaticamente
    header_row = 0
    for h in [0, 1, 2, 3]:
        try:
            df_test = pd.read_excel(xlsx_path, header=h, nrows=1, dtype=str)
            if any('nico' in str(c).lower() or 'nunota' in str(c).lower() for c in df_test.columns):
                header_row = h
                break
        except: pass
    df = pd.read_excel(xlsx_path, header=header_row, dtype=str)
    # Detectar coluna NUNOTA
    col_nunota = next((c for c in df.columns if 'nico' in str(c).lower() or 'nunota' in str(c).lower()), None)
    if not col_nunota:
        print(f'ERRO: Coluna NUNOTA nao encontrada. Colunas: {list(df.columns)[:10]}')
        return
    df = df.dropna(subset=[col_nunota])
    df = df.rename(columns={col_nunota: 'Nro. Unico'})"""

if antigo in data:
    data = data.replace(antigo, novo)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(data)
    print("OK!")
else:
    # Mostrar o trecho atual
    idx = data.find("read_excel")
    print("ERRO - trecho atual:")
    print(repr(data[idx:idx+200]))
