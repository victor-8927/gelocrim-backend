path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra e substitui a tela de relatórios
idx_start = content.find('    <div class="page" id="page-relatorios">')
idx_end   = content.find('    </div>', idx_start)
# Pega o bloco completo da div
depth = 0; i = idx_start
for i in range(idx_start, len(content)):
    if content[i:i+4] == '<div': depth += 1
    elif content[i:i+6] == '</div': depth -= 1
    if depth == 0 and i > idx_start: break

print(f'Tela relatórios: {idx_start} até {i+6}')

new_page = '''    <div class="page" id="page-relatorios">
      <div class="page-header">
        <div>
          <div class="page-title">📊 Relatórios e Business Intelligence</div>
          <div class="page-sub">Análise estratégica da operação de Manaus</div>
        </div>
        <div style="display:flex;gap:8px">
          <button class="btn btn-secondary" onclick="exportarCSV()">📥 Exportar CSV</button>
          <button class="btn btn-secondary" onclick="exportarPDF()">📄 Exportar PDF</button>
          <button class="btn btn-primary" onclick="gerarRelatorio()">⚡ Gerar Relatório</button>
        </div>
      </div>

      <!-- Filtros -->
      <div class="card" style="padding:16px;margin-bottom:16px">
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr auto;gap:12px;align-items:end">
          <div>
            <label class="form-label">Período — De</label>
            <input type="date" class="form-control" id="rel-de" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
          </div>
          <div>
            <label class="form-label">Período — Até</label>
            <input type="date" class="form-control" id="rel-ate" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
          </div>
          <div>
            <label class="form-label">Tipo de Relatório</label>
            <select class="form-control" id="rel-tipo" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              <option value="geral">📊 Visão Geral</option>
              <option value="produtividade">👥 Produtividade da Equipe</option>
              <option value="combustivel">⛽ Consumo de Combustível</option>
              <option value="clientes">🏪 Performance por Cliente</option>
              <option value="zonas">📍 Calor por Zona de Manaus</option>
            </select>
          </div>
          <div style="display:flex;gap:8px">
            <button class="btn btn-secondary" onclick="setRelPeriodo(7)">7d</button>
            <button class="btn btn-secondary" onclick="setRelPeriodo(30)">30d</button>
            <button class="btn btn-secondary" onclick="setRelPeriodo(90)">90d</button>
          </div>
        </div>
      </div>

      <!-- KPIs do relatório -->
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:16px" id="rel-kpis">
        <div class="card" style="padding:14px;margin-bottom:0;border-left:3px solid #10b981">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">✅ Eficiência de Entrega</div>
          <div style="font-size:28px;font-weight:800;color:#10b981" id="rel-kpi-eficiencia">—</div>
          <div style="font-size:10px;color:#90afd4">entregas no prazo</div>
        </div>
        <div class="card" style="padding:14px;margin-bottom:0;border-left:3px solid #f59e0b">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">💲 Custo por KG</div>
          <div style="font-size:28px;font-weight:800;color:#f59e0b" id="rel-kpi-custo-kg">—</div>
          <div style="font-size:10px;color:#90afd4">R$ por kg transportado</div>
        </div>
        <div class="card" style="padding:14px;margin-bottom:0;border-left:3px solid #64B4FF">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">🚛 Ocupação da Frota</div>
          <div style="font-size:28px;font-weight:800;color:#64B4FF" id="rel-kpi-ocupacao">—</div>
          <div style="font-size:10px;color:#90afd4">aproveitamento médio</div>
        </div>
        <div class="card" style="padding:14px;margin-bottom:0;border-left:3px solid #a78bfa">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">📍 Desvio de Rota</div>
          <div style="font-size:28px;font-weight:800;color:#a78bfa" id="rel-kpi-desvio">—</div>
          <div style="font-size:10px;color:#90afd4">KM real vs planejado</div>
        </div>
      </div>

      <!-- Conteúdo dinâmico -->
      <div id="rel-conteudo">
        <div class="card" style="padding:40px;text-align:center;color:#90afd4">
          <div style="font-size:48px;margin-bottom:12px">📊</div>
          <div style="font-size:16px;font-weight:600;margin-bottom:8px">Selecione o período e clique em Gerar Relatório</div>
          <div style="font-size:12px">Os dados serão calculados com base nas rotas finalizadas no período selecionado</div>
        </div>
      </div>
    </div>'''

if idx_start != -1:
    content = content[:idx_start] + new_page + content[i+6:]
    print('Tela de Relatórios substituída!')
else:
    print('ERRO: tela não encontrada')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('HTML salvo!')
