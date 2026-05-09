caminho = r"C:\fleet-cloud\gelocrim_v1.html"
with open(caminho, encoding="utf-8", errors="ignore") as f:
    data = f.read()

# Corrigir a funcao atualizarResumoQuantidades para adicionar cores
antigo = """    var txt = rows.map(function(r){ return r.total_qtd+'x '+r.item_nome+' ('+r.total_kg+'kg)'; }).join(' / ');"""

novo = """    var cores = {'GELO 05KG':'#00d4aa','GELO 10KG':'#64B4FF','GELO 20KG':'#f59e0b','GELO 40KG':'#f87171'};
    var txt = rows.map(function(r){
      var cor = cores[r.item_nome] || '#e8f0fe';
      return '<span style="color:'+cor+';font-weight:700">'+r.total_qtd+'x '+r.item_nome+'</span> <span style="color:#90afd4;font-size:11px">('+r.total_kg+'kg)</span>';
    }).join('<span style="color:#1e3a5c;margin:0 6px">|</span>');"""

if antigo in data:
    data = data.replace(antigo, novo)
    # Corrigir textContent para innerHTML
    data = data.replace("if(el) el.textContent = txt || '—';", "if(el) el.innerHTML = txt || '—';")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(data)
    print("OK - cores neon adicionadas!")
else:
    print("Trecho nao encontrado")
