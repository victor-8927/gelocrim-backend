path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui o HTML do dashboard
old_dash_start = '    <!-- ══ DASHBOARD ══ -->'
old_dash_end   = '    <!-- ══ PEDIDOS ══ -->'

idx_start = content.find(old_dash_start)
idx_end   = content.find(old_dash_end)

if idx_start == -1 or idx_end == -1:
    print('Padrao nao encontrado!')
    print(f'start: {idx_start}, end: {idx_end}')
else:
    new_dash = '''    <!-- ══ DASHBOARD ══ -->
    <div class="page active" id="page-dashboard">
      <div class="page-header">
        <div>
          <div class="page-title">Painel Operacional</div>
          <div class="page-sub" id="dash-subtitle">Resumo da operação do dia</div>
        </div>
        <div style="display:flex;gap:10px">
          <button class="btn btn-secondary" onclick="loadDashboard()">↺ Atualizar</button>
          <button class="btn btn-primary" onclick="goTo('roteirizacao',null)">⚡ Roteirizar Agora</button>
        </div>
      </div>

      <div id="dash-alerts"></div>

      <!-- LAYOUT: indicadores à esquerda | mapa à direita -->
      <div style="display:grid;grid-template-columns:1fr 360px;gap:16px;align-items:start">

        <!-- COLUNA ESQUERDA -->
        <div>

          <!-- PEDIDOS -->
          <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px">📦 PEDIDOS</div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:20px" id="dash-kpis-pedidos">
            <div class="loading-state" style="grid-column:1/-1">Carregando...</div>
          </div>

          <!-- OPERAÇÃO -->
          <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px">🚛 OPERAÇÃO</div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:20px" id="dash-kpis-op">
            <div class="loading-state" style="grid-column:1/-1">Carregando...</div>
          </div>

          <!-- FINANCEIRO -->
          <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px">💰 FINANCEIRO</div>
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:20px" id="dash-kpis-fin">
            <div class="loading-state" style="grid-column:1/-1">Carregando...</div>
          </div>

          <!-- RETORNO + ROTAS -->
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
            <div class="card" style="margin-bottom:0">
              <div class="card-header" style="padding:12px 16px">
                <span class="card-title" style="font-size:13px">↩️ Retorno de Produtos</span>
                <button class="btn btn-sm btn-secondary" onclick="abrirModalDash('retorno','↩️ Retorno de Produtos')">Detalhar</button>
              </div>
              <div class="card-body" style="padding:12px 16px;display:flex;align-items:center;gap:16px">
                <div style="text-align:center">
                  <div id="dash-retorno-total" style="font-size:38px;font-weight:800;color:#f59e0b;line-height:1">0</div>
                  <div style="font-size:10px;color:#90afd4;margin-top:2px">itens hoje</div>
                </div>
                <div id="dash-retorno-lista" style="flex:1;font-size:12px;color:#90afd4;line-height:1.8"></div>
              </div>
            </div>
            <div class="card" style="margin-bottom:0">
              <div class="card-header" style="padding:12px 16px">
                <span class="card-title" style="font-size:13px">🗺️ Rotas do Dia</span>
                <button class="btn btn-sm btn-secondary" onclick="abrirModalDash('rotas','🗺️ Rotas do Dia')">Ver todas</button>
              </div>
              <div class="card-body" style="padding:0">
                <table>
                  <thead><tr><th>Veículo</th><th>Paradas</th><th>Status</th></tr></thead>
                  <tbody id="dash-routes-list"></tbody>
                </table>
              </div>
            </div>
          </div>

        </div>

        <!-- COLUNA DIREITA: MAPA FIXO -->
        <div style="position:sticky;top:80px">
          <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px">📍 ROTAS ATIVAS</div>
          <div class="card" style="margin-bottom:0">
            <div class="card-body" style="padding:8px">
              <div id="dash-map" style="height:calc(100vh - 200px);min-height:500px;border-radius:8px;overflow:hidden;"></div>
            </div>
          </div>
        </div>

      </div>

      <!-- MODAL GENÉRICO DO DASHBOARD -->
      <div id="modal-dash" onclick="if(event.target===this)fecharModalDash()" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:2000;align-items:center;justify-content:center;padding:20px">
        <div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:680px;max-width:100%;max-height:85vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,.5)">
          <div style="padding:20px 24px;border-bottom:1px solid #1e3a5c;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;background:#0f2040;border-radius:16px 16px 0 0;z-index:1">
            <span style="font-size:16px;font-weight:700;color:#e8f0fe" id="modal-dash-title">Detalhe</span>
            <button onclick="fecharModalDash()" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer;padding:0 4px">✕</button>
          </div>
          <div id="modal-dash-body" style="padding:20px 24px">Carregando...</div>
        </div>
      </div>

    </div>

    '''

    content = content[:idx_start] + new_dash + content[idx_end:]
    print('HTML do dashboard reorganizado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verifica
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()
print(f'modal-dash no HTML: {c.count("modal-dash")}')
print('Faca Ctrl+Shift+R!')
