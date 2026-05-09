path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra e substitui o HTML do dashboard
idx_start = content.find('    <!-- ══ DASHBOARD ══ -->')
idx_end   = content.find('    <!-- ══ PEDIDOS ══ -->')

if idx_start == -1 or idx_end == -1:
    print(f'ERRO: start={idx_start}, end={idx_end}')
else:
    new_dash = '''    <!-- ══ DASHBOARD ══ -->
    <div class="page active" id="page-dashboard">
      <div class="page-header" style="margin-bottom:12px">
        <div>
          <div class="page-title">Painel Operacional</div>
          <div class="page-sub" id="dash-subtitle">Resumo da operação do dia</div>
        </div>
        <div style="display:flex;gap:10px;align-items:center">
          <div id="dash-clock" style="font-family:monospace;font-size:14px;color:#64B4FF;font-weight:700"></div>
          <button class="btn btn-secondary" onclick="loadDashboard()">↺ Atualizar</button>
          <button class="btn btn-primary" onclick="goTo('roteirizacao',null)">⚡ Roteirizar Agora</button>
        </div>
      </div>

      <!-- BARRA DE PROGRESSO DO DIA -->
      <div class="card" style="margin-bottom:14px;padding:14px 20px">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
          <div style="font-size:12px;font-weight:700;color:#e8f0fe">📊 Progresso da Operação do Dia</div>
          <div style="font-size:13px;font-weight:800;color:#64B4FF" id="dash-progresso-pct">—</div>
        </div>
        <div style="background:#1e3a5c;border-radius:6px;height:10px;overflow:hidden">
          <div id="dash-progresso-bar" style="height:100%;background:linear-gradient(90deg,#10b981,#64B4FF);border-radius:6px;width:0%;transition:width .5s"></div>
        </div>
        <div style="display:flex;justify-content:space-between;margin-top:6px;font-size:11px;color:#90afd4">
          <span id="dash-prog-entregues">0 entregues</span>
          <span id="dash-prog-total">0 total</span>
        </div>
      </div>

      <!-- ALERTAS -->
      <div id="dash-alerts" style="margin-bottom:12px"></div>

      <!-- LAYOUT: indicadores esquerda | mapa direita -->
      <div style="display:grid;grid-template-columns:1fr 380px;gap:16px;align-items:start">

        <!-- COLUNA ESQUERDA -->
        <div>

          <!-- SEÇÃO PEDIDOS -->
          <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px">📦 PEDIDOS</div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:18px" id="dash-kpis-pedidos">
            <div class="loading-state" style="grid-column:1/-1">Carregando...</div>
          </div>

          <!-- SEÇÃO OPERAÇÃO -->
          <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px">🚛 OPERAÇÃO</div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:18px" id="dash-kpis-op">
            <div class="loading-state" style="grid-column:1/-1">Carregando...</div>
          </div>

          <!-- SEÇÃO FINANCEIRO -->
          <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px">💰 FINANCEIRO</div>
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:18px" id="dash-kpis-fin">
            <div class="loading-state" style="grid-column:1/-1">Carregando...</div>
          </div>

          <!-- ALERTAS PREDITIVOS -->
          <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px">⚡ ALERTAS PREDITIVOS</div>
          <div id="dash-alertas-preditivos" class="card" style="margin-bottom:18px;padding:12px">
            <div class="loading-state">Analisando operação...</div>
          </div>

          <!-- RETORNO + ROTAS -->
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
            <div class="card" style="margin-bottom:0">
              <div class="card-header" style="padding:12px 16px">
                <span class="card-title" style="font-size:13px">↩️ Retorno de Produtos</span>
                <button class="btn btn-sm btn-secondary" onclick="abrirModalDash('retorno','↩️ Retorno de Produtos')">Detalhar</button>
              </div>
              <div class="card-body" style="padding:12px 16px">
                <div style="display:flex;align-items:center;gap:16px">
                  <div style="text-align:center">
                    <div id="dash-retorno-total" style="font-size:38px;font-weight:800;color:#f59e0b;line-height:1">0</div>
                    <div style="font-size:10px;color:#90afd4;margin-top:2px">itens hoje</div>
                  </div>
                  <div id="dash-retorno-lista" style="flex:1;font-size:12px;color:#90afd4;line-height:1.8"></div>
                </div>
                <div id="dash-retorno-motivo" style="margin-top:8px;font-size:11px;color:#f87171"></div>
              </div>
            </div>
            <div class="card" style="margin-bottom:0">
              <div class="card-header" style="padding:12px 16px">
                <span class="card-title" style="font-size:13px">🗺️ Rotas do Dia</span>
                <button class="btn btn-sm btn-secondary" onclick="abrirModalDash('rotas','🗺️ Rotas do Dia')">Ver todas</button>
              </div>
              <div class="card-body" style="padding:0">
                <table>
                  <thead><tr><th>Veículo</th><th>Paradas</th><th>⏱️</th><th>Status</th></tr></thead>
                  <tbody id="dash-routes-list"></tbody>
                </table>
              </div>
            </div>
          </div>

        </div>

        <!-- COLUNA DIREITA: MAPA FIXO -->
        <div style="position:sticky;top:80px">
          <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center">
            <span>📍 ROTAS ATIVAS</span>
            <button onclick="expandirMapa()" style="font-size:10px;background:transparent;border:1px solid #1e3a5c;color:#64B4FF;padding:3px 8px;border-radius:4px;cursor:pointer">⛶ Expandir</button>
          </div>
          <div class="card" style="margin-bottom:0">
            <div class="card-body" style="padding:8px">
              <div id="dash-map" style="height:calc(100vh - 260px);min-height:400px;border-radius:8px;overflow:hidden;"></div>
            </div>
          </div>
          <!-- Canhotos pendentes -->
          <div class="card" style="margin-top:8px;padding:12px;margin-bottom:0">
            <div style="display:flex;justify-content:space-between;align-items:center">
              <div>
                <div style="font-size:11px;color:#90afd4">📋 Canhotos Pendentes</div>
                <div style="font-size:22px;font-weight:800;color:#f59e0b" id="dash-canhotos">—</div>
              </div>
              <div>
                <div style="font-size:11px;color:#90afd4">⏰ Rotas +8h em campo</div>
                <div style="font-size:22px;font-weight:800;color:#f87171" id="dash-risco-perecivel">—</div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- MODAL MAPA EXPANDIDO -->
      <div id="modal-mapa-full" onclick="if(event.target===this)this.style.display='none'" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.9);z-index:5000;align-items:center;justify-content:center">
        <div style="width:95vw;height:90vh;border-radius:12px;overflow:hidden;position:relative">
          <button onclick="document.getElementById('modal-mapa-full').style.display='none'" style="position:absolute;top:10px;right:10px;z-index:10;background:#0f2040;border:1px solid #1e3a5c;color:#e8f0fe;padding:6px 12px;border-radius:6px;cursor:pointer">✕ Fechar</button>
          <div id="dash-map-full" style="width:100%;height:100%"></div>
        </div>
      </div>

      <!-- MODAL GENÉRICO -->
      <div id="modal-dash" onclick="if(event.target===this)fecharModalDash()" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:2000;align-items:center;justify-content:center;padding:20px">
        <div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:680px;max-width:100%;max-height:85vh;overflow-y:auto">
          <div style="padding:20px 24px;border-bottom:1px solid #1e3a5c;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;background:#0f2040;border-radius:16px 16px 0 0;z-index:1">
            <span style="font-size:16px;font-weight:700;color:#e8f0fe" id="modal-dash-title">Detalhe</span>
            <button onclick="fecharModalDash()" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer">✕</button>
          </div>
          <div id="modal-dash-body" style="padding:20px 24px">Carregando...</div>
        </div>
      </div>

    </div>

    '''

    content = content[:idx_start] + new_dash + content[idx_end:]
    print('Dashboard HTML atualizado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Parte 1 concluída! Execute fix_dashboard_js.py em seguida.')
