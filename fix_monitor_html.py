path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra a tela de monitoramento atual
idx_mon_start = content.find('    <!-- ══ MONITORAMENTO ══ -->')
idx_mon_end   = content.find('    <!-- ══ OCORRÊNCIAS ══ -->')
if idx_mon_end == -1:
    idx_mon_end = content.find('<div class="page" id="page-ocorrencias">')

if idx_mon_start == -1 or idx_mon_end == -1:
    print(f'ERRO: start={idx_mon_start}, end={idx_mon_end}')
else:
    new_monitor = '''    <!-- ══ MONITORAMENTO ══ -->
    <div class="page" id="page-monitoramento">
      <div class="page-header">
        <div>
          <div class="page-title">🗼 Torre de Controle</div>
          <div class="page-sub" id="mon-subtitle">Monitoramento ativo em tempo real</div>
        </div>
        <div style="display:flex;gap:8px;align-items:center">
          <span id="mon-auto-badge" style="font-size:10px;background:#10b981;color:#fff;padding:3px 8px;border-radius:10px">● AUTO 30s</span>
          <input type="date" id="mon-date" style="padding:6px 10px;border:1px solid var(--border);border-radius:6px;font-size:12px;background:#0a1628;color:#e8f0fe">
          <button class="btn btn-secondary" onclick="loadMonitoring()">↺ Atualizar</button>
        </div>
      </div>

      <!-- KPIs Torre de Controle -->
      <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-bottom:16px" id="mon-kpis"></div>

      <!-- Layout: lista rotas | mapa | timeline -->
      <div style="display:grid;grid-template-columns:280px 1fr 280px;gap:12px;height:calc(100vh - 260px);min-height:500px">

        <!-- COL 1: Lista de rotas do dia -->
        <div style="display:flex;flex-direction:column;gap:8px;overflow-y:auto">
          <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px">ROTAS DO DIA</div>
          <div id="mon-rotas-lista" style="display:flex;flex-direction:column;gap:6px">
            <div class="loading-state">Carregando...</div>
          </div>
        </div>

        <!-- COL 2: Mapa satélite -->
        <div style="display:flex;flex-direction:column;gap:8px">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px">MAPA EM TEMPO REAL</div>
            <div style="display:flex;gap:6px">
              <button onclick="toggleMapaTipo()" id="btn-mapa-tipo" style="font-size:10px;padding:3px 8px;background:#1e3a5c;border:none;color:#64B4FF;border-radius:4px;cursor:pointer">🛰️ Satélite</button>
              <button onclick="toggleTrafegoMon()" style="font-size:10px;padding:3px 8px;background:#1e3a5c;border:none;color:#64B4FF;border-radius:4px;cursor:pointer">🚦 Tráfego</button>
            </div>
          </div>
          <div id="mon-map" style="flex:1;border-radius:10px;overflow:hidden;border:1px solid #1e3a5c;min-height:400px"></div>
        </div>

        <!-- COL 3: Timeline da rota selecionada -->
        <div style="display:flex;flex-direction:column;gap:8px;overflow-y:auto">
          <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px">LINHA DO TEMPO</div>
          <div id="mon-timeline" style="font-size:12px;color:#90afd4;text-align:center;padding:20px">
            Selecione uma rota para ver a timeline
          </div>
        </div>

      </div>
    </div>

    '''

    content = content[:idx_mon_start] + new_monitor + content[idx_mon_end:]
    print('Torre de Controle atualizada!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Parte 3 OK.')
