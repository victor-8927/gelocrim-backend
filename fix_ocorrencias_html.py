path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

content = ''.join(lines)

# Encontra início e fim da tela de ocorrências
idx_start = content.find('    <div class="page" id="page-ocorrencias">')
idx_end   = content.find('    <!-- ══ VEÍCULOS ══ -->')
if idx_end == -1:
    idx_end = content.find('    <div class="page" id="page-veiculos">')

print(f'start={idx_start}, end={idx_end}')

new_page = '''    <div class="page" id="page-ocorrencias">
      <div class="page-header">
        <div>
          <div class="page-title">Gestão de Ocorrências</div>
          <div class="page-sub">Auditoria e suporte operacional em tempo real</div>
        </div>
        <div style="display:flex;gap:8px">
          <button class="btn btn-secondary" onclick="loadOcorrencias()">↺ Atualizar</button>
          <button class="btn btn-primary" onclick="abrirModalOcorrencia()">+ Nova Ocorrência</button>
        </div>
      </div>

      <!-- KPIs de ocorrências -->
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:16px">
        <div class="card" onclick="filtrarOcorrencia('pendente')" style="padding:12px;margin-bottom:0;border-left:3px solid #f59e0b;cursor:pointer">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">⏳ Pendentes</div>
          <div style="font-size:24px;font-weight:800;color:#f59e0b" id="oc-kpi-pendentes">—</div>
          <div style="font-size:10px;color:#90afd4">aguardando tratamento</div>
        </div>
        <div class="card" onclick="filtrarOcorrencia('em_tratamento')" style="padding:12px;margin-bottom:0;border-left:3px solid #64B4FF;cursor:pointer">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">🔧 Em Tratamento</div>
          <div style="font-size:24px;font-weight:800;color:#64B4FF" id="oc-kpi-tratamento">—</div>
          <div style="font-size:10px;color:#90afd4">sendo resolvidas</div>
        </div>
        <div class="card" onclick="filtrarOcorrencia('critica')" style="padding:12px;margin-bottom:0;border-left:3px solid #f87171;cursor:pointer">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px;animation:pulse 1.5s infinite">🚨 Críticas</div>
          <div style="font-size:24px;font-weight:800;color:#f87171" id="oc-kpi-criticas">—</div>
          <div style="font-size:10px;color:#90afd4">exigem ação imediata</div>
        </div>
        <div class="card" onclick="filtrarOcorrencia('resolvida')" style="padding:12px;margin-bottom:0;border-left:3px solid #10b981;cursor:pointer">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">✅ Resolvidas</div>
          <div style="font-size:24px;font-weight:800;color:#10b981" id="oc-kpi-resolvidas">—</div>
          <div style="font-size:10px;color:#90afd4">hoje</div>
        </div>
      </div>

      <!-- Filtros -->
      <div class="filters-bar" style="margin-bottom:12px">
        <div class="filter-group">
          <span class="filter-label">Tipo</span>
          <select class="filter-input" id="oc-tipo" onchange="loadOcorrencias()">
            <option value="">Todos</option>
            <option value="avaria">🧊 Avaria de Carga</option>
            <option value="recusa">🚫 Recusa do Cliente</option>
            <option value="atraso">⏰ Atraso Logístico</option>
            <option value="faturamento">💰 Erro de Faturamento</option>
            <option value="localizacao">📍 Ocorrência de Localização</option>
            <option value="veiculo">🚛 Problema com Veículo</option>
            <option value="outros">📋 Outros</option>
          </select>
        </div>
        <div class="filter-sep"></div>
        <div class="filter-group">
          <span class="filter-label">Gravidade</span>
          <select class="filter-input" id="oc-gravidade" onchange="loadOcorrencias()">
            <option value="">Todas</option>
            <option value="critica">🔴 Crítica</option>
            <option value="alta">🟠 Alta</option>
            <option value="media">🟡 Média</option>
            <option value="info">🟢 Informativa</option>
          </select>
        </div>
        <div class="filter-sep"></div>
        <div class="filter-group">
          <span class="filter-label">Data</span>
          <input type="date" class="filter-input" id="oc-date">
        </div>
        <div class="filter-sep"></div>
        <div class="filter-group">
          <span class="filter-label">Status</span>
          <select class="filter-input" id="oc-status" onchange="loadOcorrencias()">
            <option value="">Todos</option>
            <option value="pendente">Pendente</option>
            <option value="em_tratamento">Em Tratamento</option>
            <option value="resolvida">Resolvida</option>
            <option value="critica">Crítica</option>
          </select>
        </div>
        <button class="btn btn-secondary btn-sm" style="align-self:flex-end" onclick="loadOcorrencias()">Filtrar</button>
      </div>

      <!-- Tabela -->
      <div class="card">
        <div class="card-body" style="padding:0;overflow-x:auto">
          <table>
            <thead>
              <tr>
                <th>Gravidade</th>
                <th>Data/Hora</th>
                <th>Tipo</th>
                <th>Cliente / Pedido</th>
                <th>Veículo</th>
                <th>Descrição</th>
                <th>⏱️ Tempo</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody id="oc-tbody">
              <tr><td colspan="9" class="loading-state">Nenhuma ocorrência registrada</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- MODAL NOVA OCORRÊNCIA -->
      <div id="modal-ocorrencia" onclick="if(event.target===this)this.style.display='none'" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:2000;align-items:center;justify-content:center;padding:20px">
        <div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:660px;max-height:90vh;overflow-y:auto">
          <div style="padding:18px 24px;border-bottom:1px solid #1e3a5c;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;background:#0f2040;border-radius:16px 16px 0 0">
            <span style="font-size:16px;font-weight:700;color:#e8f0fe" id="modal-oc-titulo">Nova Ocorrência</span>
            <button onclick="document.getElementById('modal-ocorrencia').style.display='none'" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer">✕</button>
          </div>
          <div style="padding:20px 24px">

            <!-- Gravidade (seleção visual) -->
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:10px">🎯 GRAVIDADE</div>
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:20px">
              <div onclick="selecionarGravidade('info')" id="grav-info"
                style="padding:10px;border:2px solid #10b981;background:rgba(16,185,129,.1);border-radius:8px;text-align:center;cursor:pointer">
                <div style="font-size:18px">🟢</div>
                <div style="font-size:11px;color:#10b981;font-weight:700">Informativa</div>
              </div>
              <div onclick="selecionarGravidade('media')" id="grav-media"
                style="padding:10px;border:2px solid #1e3a5c;background:transparent;border-radius:8px;text-align:center;cursor:pointer">
                <div style="font-size:18px">🟡</div>
                <div style="font-size:11px;color:#90afd4;font-weight:700">Média</div>
              </div>
              <div onclick="selecionarGravidade('alta')" id="grav-alta"
                style="padding:10px;border:2px solid #1e3a5c;background:transparent;border-radius:8px;text-align:center;cursor:pointer">
                <div style="font-size:18px">🟠</div>
                <div style="font-size:11px;color:#90afd4;font-weight:700">Alta</div>
              </div>
              <div onclick="selecionarGravidade('critica')" id="grav-critica"
                style="padding:10px;border:2px solid #1e3a5c;background:transparent;border-radius:8px;text-align:center;cursor:pointer">
                <div style="font-size:18px">🔴</div>
                <div style="font-size:11px;color:#90afd4;font-weight:700">Crítica</div>
              </div>
            </div>
            <input type="hidden" id="oc-gravidade-sel" value="info">

            <!-- Tipo e dados -->
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:10px">📋 DADOS DA OCORRÊNCIA</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px">
              <div>
                <label class="form-label">Tipo de Ocorrência *</label>
                <select class="form-control" id="oc-tipo-novo" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
                  <option value="">— Selecione —</option>
                  <option value="avaria">🧊 Avaria de Carga</option>
                  <option value="recusa">🚫 Recusa do Cliente</option>
                  <option value="atraso">⏰ Atraso Logístico</option>
                  <option value="faturamento">💰 Erro de Faturamento</option>
                  <option value="localizacao">📍 Ocorrência de Localização</option>
                  <option value="veiculo">🚛 Problema com Veículo</option>
                  <option value="outros">📋 Outros</option>
                </select>
              </div>
              <div>
                <label class="form-label">Veículo</label>
                <select class="form-control" id="oc-veiculo-novo" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
                  <option value="">— Selecione —</option>
                </select>
              </div>
              <div>
                <label class="form-label">Nº do Pedido</label>
                <input class="form-control" id="oc-pedido" placeholder="SNK-000000" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Cliente</label>
                <input class="form-control" id="oc-cliente" placeholder="Nome do cliente" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
            </div>
            <div style="margin-bottom:16px">
              <label class="form-label">Descrição Detalhada *</label>
              <textarea class="form-control" id="oc-descricao" rows="3" placeholder="Descreva o que aconteceu..." style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c;resize:vertical"></textarea>
            </div>

            <!-- Evidências -->
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:10px">📷 EVIDÊNCIAS</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px">
              <div>
                <label class="form-label">Foto da Ocorrência</label>
                <div onclick="document.getElementById('oc-foto-input').click()" style="border:2px dashed #1e3a5c;border-radius:8px;padding:16px;text-align:center;cursor:pointer">
                  <img id="oc-foto-preview" style="display:none;max-width:100%;max-height:120px;border-radius:4px;margin-bottom:8px">
                  <div id="oc-foto-placeholder" style="color:#90afd4;font-size:12px">📷 Clique para adicionar foto</div>
                </div>
                <input type="file" id="oc-foto-input" accept="image/*" style="display:none" onchange="previewFoto('oc-foto-input','oc-foto-preview','oc-foto-placeholder','oc-foto-base64')">
                <input type="hidden" id="oc-foto-base64">
              </div>
              <div>
                <label class="form-label">Assinatura Digital</label>
                <div style="border:2px dashed #1e3a5c;border-radius:8px;padding:8px;text-align:center">
                  <canvas id="oc-assinatura" width="220" height="100" style="background:#0a1628;border-radius:4px;cursor:crosshair;touch-action:none"></canvas>
                  <div style="display:flex;gap:6px;justify-content:center;margin-top:6px">
                    <button onclick="limparAssinatura()" style="font-size:10px;padding:3px 8px;background:#1e3a5c;border:none;color:#90afd4;border-radius:4px;cursor:pointer">Limpar</button>
                    <span style="font-size:10px;color:#90afd4;padding:3px">Assine acima</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Ações Sankhya -->
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:10px">⚡ AÇÕES AUTOMÁTICAS (SANKHYA)</div>
            <div style="display:grid;gap:8px;margin-bottom:20px">
              <label style="display:flex;align-items:center;gap:8px;cursor:pointer;font-size:12px;color:#e8f0fe">
                <input type="checkbox" id="oc-gerar-devolucao" style="accent-color:#64B4FF">
                Gerar nota de devolução no Sankhya automaticamente
              </label>
              <label style="display:flex;align-items:center;gap:8px;cursor:pointer;font-size:12px;color:#e8f0fe">
                <input type="checkbox" id="oc-atualizar-estoque" style="accent-color:#64B4FF">
                Atualizar estoque (retornar item ou dar baixa em avaria)
              </label>
            </div>

            <div style="display:flex;gap:10px;justify-content:flex-end;padding-top:12px;border-top:1px solid #1e3a5c">
              <button onclick="document.getElementById('modal-ocorrencia').style.display='none'" class="btn btn-secondary">Cancelar</button>
              <button onclick="salvarOcorrencia()" class="btn btn-primary">💾 Registrar Ocorrência</button>
            </div>
          </div>
        </div>
      </div>

    </div>

    '''

content = content[:idx_start] + new_page + content[idx_end:]
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Tela de Ocorrências implementada!')
