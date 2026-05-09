path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Atualiza tela de Gestão de Rotas ───────────────────────────
old_rotas = '''    <div class="page" id="page-rotas">
      <div class="page-header">
        <div>
          <div class="page-title">Gestão de Rotas</div>
          <div class="page-sub">Visualize, ajuste e libere as rotas geradas</div>
        </div>
        <button class="btn btn-secondary" onclick="loadRoutes()">↺ Atualizar</button>
      </div>
      <div class="filters-bar">
        <div class="filter-group">
          <span class="filter-label">Data</span>
          <input type="date" class="filter-input" id="routes-date" onchange="loadRoutes()">
        </div>
        <div class="filter-sep"></div>
        <div class="filter-group">
          <span class="filter-label">Status</span>
          <select class="filter-input" id="routes-status" onchange="loadRoutes()">
            <option value="">Todos</option>
            <option value="draft">Rascunho</option>
            <option value="optimized">Otimizada</option>
            <option value="released">Liberada</option>
            <option value="executing">Em Execução</option>
            <option value="done">Concluída</option>
            <option value="cancelled">Cancelada</option>
          </select>
        </div>
      </div>
      <div class="card">
        <div class="card-body">
          <table>
            <thead>
              <tr><th>Veículo</th><th>Motorista</th><th>Data</th><th>Paradas</th><th>Distância</th><th>Início Prev.</th><th>Fim Prev.</th><th>Status</th><th>Ações</th></tr>
            </thead>
            <tbody id="routes-tbody"></tbody>
          </table>
        </div>
      </div>
    </div>'''

new_rotas = '''    <div class="page" id="page-rotas">
      <div class="page-header">
        <div>
          <div class="page-title">Gestão de Rotas</div>
          <div class="page-sub">Visão panorâmica da execução do dia</div>
        </div>
        <div style="display:flex;gap:8px">
          <button class="btn btn-secondary" onclick="loadRoutes()">↺ Atualizar</button>
          <button class="btn btn-secondary" onclick="imprimirRomaneiosSelecionados()">🖨️ Imprimir Selecionados</button>
        </div>
      </div>

      <!-- KPIs de alta performance -->
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:16px" id="rotas-kpis">
        <div class="card" style="padding:12px;margin-bottom:0;border-left:3px solid #10b981">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">📊 Taxa de Sucesso (SLA)</div>
          <div style="font-size:24px;font-weight:800;color:#10b981" id="kpi-sla">—</div>
          <div style="font-size:10px;color:#90afd4">entregas no prazo</div>
        </div>
        <div class="card" style="padding:12px;margin-bottom:0;border-left:3px solid #64B4FF">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">🚛 Saúde da Frota</div>
          <div style="font-size:24px;font-weight:800;color:#64B4FF" id="kpi-saude">—</div>
          <div style="font-size:10px;color:#90afd4" id="kpi-saude-sub">veículos ativos</div>
        </div>
        <div class="card" style="padding:12px;margin-bottom:0;border-left:3px solid #f59e0b">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">📍 KM Real vs Planejado</div>
          <div style="font-size:24px;font-weight:800;color:#f59e0b" id="kpi-km-desvio">—</div>
          <div style="font-size:10px;color:#90afd4">desvio médio</div>
        </div>
        <div class="card" style="padding:12px;margin-bottom:0;border-left:3px solid #a78bfa">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">✅ Progresso Geral</div>
          <div style="font-size:24px;font-weight:800;color:#a78bfa" id="kpi-progresso">—</div>
          <div style="font-size:10px;color:#90afd4">do dia concluído</div>
        </div>
      </div>

      <!-- Filtros -->
      <div class="filters-bar" style="margin-bottom:12px">
        <div class="filter-group">
          <span class="filter-label">Data</span>
          <input type="date" class="filter-input" id="routes-date" onchange="loadRoutes()">
        </div>
        <div class="filter-sep"></div>
        <div class="filter-group">
          <span class="filter-label">Status</span>
          <select class="filter-input" id="routes-status" onchange="loadRoutes()">
            <option value="">Todos</option>
            <option value="draft">Rascunho</option>
            <option value="optimized">Otimizada</option>
            <option value="released">Liberada</option>
            <option value="executing">Em Execução</option>
            <option value="done">Concluída</option>
            <option value="cancelled">Cancelada</option>
          </select>
        </div>
      </div>

      <!-- Tabela com barras de progresso -->
      <div class="card">
        <div class="card-body" style="padding:0;overflow-x:auto">
          <table>
            <thead>
              <tr>
                <th style="width:30px"><input type="checkbox" id="chk-all-rotas" onchange="toggleTodasRotas(this.checked)"></th>
                <th>Veículo</th>
                <th>Motorista</th>
                <th>Data</th>
                <th>Progresso</th>
                <th>Distância</th>
                <th>Início Prev.</th>
                <th>Fim Prev. / Real</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody id="routes-tbody"></tbody>
          </table>
        </div>
      </div>
    </div>'''

if old_rotas in content:
    content = content.replace(old_rotas, new_rotas)
    print('Tela de Gestão de Rotas atualizada!')
else:
    print('ERRO: padrão rotas não encontrado')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Parte 1 OK. Execute fix_monitor_js.py em seguida.')
