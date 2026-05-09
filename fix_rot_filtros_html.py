path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona filtros e legenda de cores no mapa de roteirização
old = '''        <span id="rot-map-status" style="margin-left:auto;color:#90afd4;font-size:11px">Clique em Atualizar</span>
      </div>
      <div id="rot-map" style="flex:1;border-radius:10px;overflow:hidden;border:1px solid #1e3a5c;min-height:400px"></div>'''

new = '''        <span id="rot-map-status" style="margin-left:auto;color:#90afd4;font-size:11px">Clique em Atualizar</span>
      </div>
      <!-- FILTROS DO MAPA -->
      <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;background:#0f2040;border:1px solid #1e3a5c;border-radius:8px;padding:8px 12px">
        <select id="rot-filtro-rota" onchange="filtrarRotMapa()" style="padding:6px 10px;border:1px solid #1e3a5c;border-radius:6px;font-size:12px;background:#0a1628;color:#e8f0fe">
          <option value="">Todas as rotas</option>
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
        <button onclick="rotLimparTudo()" style="padding:6px 12px;background:transparent;border:1px solid #f87171;color:#f87171;border-radius:6px;font-size:11px;cursor:pointer">✕ Limpar</button>
        <!-- Legenda cores -->
        <div style="display:flex;gap:8px;margin-left:auto;flex-wrap:wrap">
          <span style="display:flex;align-items:center;gap:3px;font-size:10px;color:#90afd4"><span style="width:10px;height:10px;background:#e8521a;border-radius:50%;display:inline-block"></span>801</span>
          <span style="display:flex;align-items:center;gap:3px;font-size:10px;color:#90afd4"><span style="width:10px;height:10px;background:#64B4FF;border-radius:50%;display:inline-block"></span>802</span>
          <span style="display:flex;align-items:center;gap:3px;font-size:10px;color:#90afd4"><span style="width:10px;height:10px;background:#10b981;border-radius:50%;display:inline-block"></span>803</span>
          <span style="display:flex;align-items:center;gap:3px;font-size:10px;color:#90afd4"><span style="width:10px;height:10px;background:#f59e0b;border-radius:50%;display:inline-block"></span>804</span>
          <span style="display:flex;align-items:center;gap:3px;font-size:10px;color:#90afd4"><span style="width:10px;height:10px;background:#a78bfa;border-radius:50%;display:inline-block"></span>805</span>
          <span style="display:flex;align-items:center;gap:3px;font-size:10px;color:#90afd4"><span style="width:10px;height:10px;background:#f87171;border-radius:50%;display:inline-block"></span>811</span>
          <span style="display:flex;align-items:center;gap:3px;font-size:10px;color:#90afd4"><span style="width:10px;height:10px;background:#2dd4bf;border-radius:50%;display:inline-block"></span>822</span>
          <span style="display:flex;align-items:center;gap:3px;font-size:10px;color:#90afd4"><span style="width:10px;height:10px;background:#10b981;border-radius:50%;display:inline-block;border:2px solid #fff"></span>Selecionado</span>
        </div>
      </div>
      <div id="rot-map" style="flex:1;border-radius:10px;overflow:hidden;border:1px solid #1e3a5c;min-height:400px"></div>'''

if old in content:
    content = content.replace(old, new)
    print('Filtros HTML adicionados!')
else:
    print('Padrão não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')

# Corrige mapeamento TOP no processarLinhas
path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona normalização de TOP após o processamento
old = "      order_type:get('top')||'1000',"
new = """      order_type:(function(){
        var t=get('top')||'';
        // Normaliza TOPs do Sankhya para TOPs do app
        var mapa={'1100':'1000','1126':'1009','1117':'1007','1118':'1008','1127':'1010'};
        return mapa[t]||t||'1000';
      })(),"""

if old in content:
    content = content.replace(old, new)
    print('Mapeamento TOP corrigido!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
