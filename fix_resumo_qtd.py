caminho = r"C:\fleet-cloud\gelocrim_v1.html"
with open(caminho, encoding="utf-8", errors="ignore") as f:
    data = f.read()

# 1. Corrigir coluna janela para mostrar tempo_entrega
antigo_janela = """'<td style="font-size:11px;color:#90afd4">'+(o.tempo_entrega?o.tempo_entrega+' min':'—')+'</td>'+"""
novo_janela   = """'<td style="font-size:11px;color:#90afd4">'+(o.tempo_entrega&&o.tempo_entrega!==''?o.tempo_entrega+' min':'—')+'</td>'+"""

if antigo_janela in data:
    data = data.replace(antigo_janela, novo_janela)
    print("OK1 - janela corrigida")

# 2. Adicionar resumo de quantidades antes da tabela de pedidos
# Buscar o elemento orders-sub que mostra "X pedidos carregados"
antigo_sub = """var sub = document.getElementById('orders-sub');
    if(sub) sub.textContent = data.length+' pedidos carregados';"""

novo_sub = """var sub = document.getElementById('orders-sub');
    if(sub) sub.textContent = data.length+' pedidos carregados';
    // Calcular resumo de quantidades
    atualizarResumoQuantidades();"""

if antigo_sub in data:
    data = data.replace(antigo_sub, novo_sub)
    print("OK2 - chamada resumo adicionada")

# 3. Adicionar elemento HTML do resumo antes da tabela
antigo_header = """<th>Nº
                Pedido</th>"""
novo_header = antigo_header  # nao mudar o header

# Adicionar div de resumo antes do filtro de pedidos
antigo_filtro = """<div style="display:flex;gap:12px;align-items:flex-end;flex-wrap:wrap;margin-bottom:16px">
          <div>
            <label class="form-label">STATUS</label>"""

novo_filtro = """<div id="resumo-quantidades" style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;padding:10px 16px;margin-bottom:12px;display:flex;gap:16px;align-items:center;flex-wrap:wrap">
            <span style="font-size:11px;color:#90afd4;font-weight:700;letter-spacing:1px">RESUMO IMPORTADO:</span>
            <span id="resumo-texto" style="font-size:12px;color:#e8f0fe">—</span>
          </div>
          <div style="display:flex;gap:12px;align-items:flex-end;flex-wrap:wrap;margin-bottom:16px">
          <div>
            <label class="form-label">STATUS</label>"""

# Fechar a div extra adicionada
antigo_fim_filtro = """</div>
        </div>

        <!-- MODAL DETALHE PEDIDO -->"""
novo_fim_filtro = """</div>
        </div>
        </div>

        <!-- MODAL DETALHE PEDIDO -->"""

if antigo_filtro in data:
    data = data.replace(antigo_filtro, novo_filtro, 1)
    print("OK3 - div resumo adicionada")
    if antigo_fim_filtro in data:
        data = data.replace(antigo_fim_filtro, novo_fim_filtro, 1)
        print("OK4 - div fechada")

# 4. Adicionar funcao atualizarResumoQuantidades
antigo_func = "function atualizarKpisPedidos(orders) {"
novo_func = """async function atualizarResumoQuantidades() {
  try {
    var rows = await api('GET', '/orders/resumo-itens');
    var txt = rows.map(function(r){ return r.total_qtd+'x '+r.item_nome+' ('+r.total_kg+'kg)'; }).join(' / ');
    var el = document.getElementById('resumo-texto');
    if(el) el.textContent = txt || '—';
  } catch(e) {
    var el = document.getElementById('resumo-texto');
    if(el) el.textContent = '—';
  }
}
function atualizarKpisPedidos(orders) {"""

if antigo_func in data:
    data = data.replace(antigo_func, novo_func, 1)
    print("OK5 - funcao resumo adicionada")

with open(caminho, "w", encoding="utf-8") as f:
    f.write(data)
print("Salvo!")
