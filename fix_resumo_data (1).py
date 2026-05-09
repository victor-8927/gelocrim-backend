caminho = r"C:\fleet-cloud\gelocrim_v1.html"
with open(caminho, encoding="utf-8", errors="ignore") as f:
    data = f.read()

# Verificar se o div resumo existe
if 'resumo-quantidades' in data:
    idx = data.find('resumo-quantidades')
    print("DIV encontrado:")
    print(data[max(0,idx-50):idx+200])
else:
    print("DIV nao encontrado - adicionando...")
    # Adicionar antes dos filtros
    antigo = """<div style="display:flex;gap:12px;align-items:flex-end;flex-wrap:wrap;margin-bottom:16px">
          <div>
            <label class="form-label">STATUS</label>"""
    novo = """<div id="resumo-quantidades" style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;padding:10px 16px;margin-bottom:12px;display:flex;gap:16px;align-items:center;flex-wrap:wrap">
            <span style="font-size:11px;color:#90afd4;font-weight:700;letter-spacing:1px">📦 RESUMO:</span>
            <span id="resumo-texto" style="font-size:12px;color:#e8f0fe;font-weight:600">carregando...</span>
          </div>
          <div style="display:flex;gap:12px;align-items:flex-end;flex-wrap:wrap;margin-bottom:16px">
          <div>
            <label class="form-label">STATUS</label>"""
    if antigo in data:
        data = data.replace(antigo, novo, 1)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(data)
        print("OK - div adicionado!")
    else:
        print("Nao encontrou o filtro STATUS - buscando alternativa...")
        idx2 = data.find('class="form-label">STATUS</label>')
        print(repr(data[max(0,idx2-200):idx2+50]))
