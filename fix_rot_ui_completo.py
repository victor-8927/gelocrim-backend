path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Substitui toda a barra de filtros HTML
old = '''      <!-- FILTROS DO MAPA -->
      <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;background:#0f2040;border:1px solid #1e3a5c;border-radius:8px;padding:8px 12px">
        <select id="rot-filtro-rota" onchange="filtrarRotMapa()" style="padding:6px 10px;border:1px solid #1e3a5c;border-radius:6px;font-size:12px;background:#0a1628;color:#e8f0fe">
          <option value="">Todas as rotas</option>
          <option value="801">Rota 801</option>
          <option value="802">Rota 802</option>
          <option value="803">Rota 803</option>
          <option value="804">Rota 804</option>
          <option value="805">Rota 805</option>
          <option value="811">Rota 811</option>
          <option value="821">Rota 821</option>
          <option value="822">Rota 822</option>
        </select>
        <select id="rot-filtro-top" onchange="filtrarRotMapa()" style="padding:6px 10px;border:1px solid #1e3a5c;border-radius:6px;font-size:12px;background:#0a1628;color:#e8f0fe">
          <option value="">Todos TOP</option>
          <option value="1000">TOP 1000 — Venda</option>
          <option value="1007">TOP 1007 — Bonif.</option>
          <option value="1009">TOP 1009 — Troca</option>
          <option value="1010">TOP 1010 — Pré-ped.</option>
        </select>
        <input id="rot-filtro-busca" placeholder="Buscar cliente..." oninput="filtrarRotMapa()" style="padding:6px 10px;border:1px solid #1e3a5c;border-radius:6px;font-size:12px;background:#0a1628;color:#e8f0fe;width:160px">
        <button onclick="selecionarTodaRota()" style="padding:6px 12px;background:#e8521a;border:none;color:#fff;border-radius:6px;font-size:11px;font-weight:700;cursor:pointer">⚡ Selecionar Rota</button>
        <button onclick="rotLimparTudo()" style="padding:6px 12px;background:transparent;border:1px solid #f87171;color:#f87171;border-radius:6px;font-size:11px;cursor:pointer">✕ Limpar</button>'''

new = '''      <!-- FILTROS DO MAPA -->
      <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;background:#0f2040;border:1px solid #1e3a5c;border-radius:8px;padding:8px 12px">
        <select id="rot-filtro-rota" onchange="filtrarRotMapa()" style="padding:6px 10px;border:1px solid #1e3a5c;border-radius:6px;font-size:12px;background:#0a1628;color:#e8f0fe">
          <option value="">🗺️ Todas as rotas</option>
          <option value="801">Rota 801</option>
          <option value="802">Rota 802</option>
          <option value="803">Rota 803</option>
          <option value="804">Rota 804</option>
          <option value="805">Rota 805</option>
          <option value="811">Rota 811</option>
          <option value="821">Rota 821</option>
          <option value="822">Rota 822</option>
        </select>
        <select id="rot-filtro-regiao" onchange="filtrarRotMapa()" style="padding:6px 10px;border:1px solid #1e3a5c;border-radius:6px;font-size:12px;background:#0a1628;color:#e8f0fe">
          <option value="">📍 Todas regiões</option>
        </select>
        <select id="rot-filtro-bairro" onchange="filtrarRotMapa()" style="padding:6px 10px;border:1px solid #1e3a5c;border-radius:6px;font-size:12px;background:#0a1628;color:#e8f0fe">
          <option value="">🏘️ Todos bairros</option>
        </select>
        <input id="rot-filtro-busca" placeholder="🔍 Nome do cliente..." oninput="filtrarRotMapa()" style="padding:6px 10px;border:1px solid #1e3a5c;border-radius:6px;font-size:12px;background:#0a1628;color:#e8f0fe;width:180px">
        <button onclick="buscarFiltrados()" style="padding:6px 16px;background:#e8521a;border:none;color:#fff;border-radius:6px;font-size:12px;font-weight:700;cursor:pointer">🔍 Buscar</button>
        <button onclick="rotLimparTudo()" style="padding:6px 12px;background:transparent;border:1px solid #f87171;color:#f87171;border-radius:6px;font-size:11px;cursor:pointer">✕ Limpar</button>'''

if old in content:
    content = content.replace(old, new)
    print('Filtros HTML atualizados!')
else:
    print('Padrão filtros não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('HTML OK!')
