path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_page = '''    <!-- ══ PARCEIROS ══ -->
    <div id="page-clientes" class="page">
    <h2>Importar Parceiros</h2>
    <p>Selecione a planilha XLS/XLSX com os dados dos parceiros (codigo_erp, nome fantasia, razão social, zona geo,  endereço, cep, bairro, cidade/uf,  latitude,  longitude, cpf/cnpj, segmento, zona geo, comodatos, tempo medio de entrega, rota).</p>
    <input type="file" id="cliente-file" accept=".xls,.xlsx">
    <button onclick="uploadParceiros()">Enviar</button>
    <div id="cliente-status" style="margin-top:10px; color:#16a34a;"></div>
</div>'''

new_page = '''    <!-- ══ PARCEIROS ══ -->
    <div id="page-clientes" class="page">
      <div class="page-header">
        <div>
          <div class="page-title">🤝 Parceiros</div>
          <div class="page-sub" id="clientes-sub">Base de clientes com geolocalização</div>
        </div>
        <div style="display:flex;gap:8px">
          <button class="btn btn-secondary" onclick="loadClientes()">↺ Atualizar</button>
          <button class="btn btn-primary" onclick="abrirImportacaoBaseClientes()">📥 Importar XLS</button>
        </div>
      </div>

      <!-- KPIs -->
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:16px">
        <div class="card" style="padding:14px;margin-bottom:0;border-left:3px solid #64B4FF">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">Total</div>
          <div style="font-size:28px;font-weight:800;color:#64B4FF" id="cli-total">—</div>
          <div style="font-size:10px;color:#90afd4">parceiros</div>
        </div>
        <div class="card" style="padding:14px;margin-bottom:0;border-left:3px solid #10b981">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">Com GPS</div>
          <div style="font-size:28px;font-weight:800;color:#10b981" id="cli-gps">—</div>
          <div style="font-size:10px;color:#90afd4">geolocalizados</div>
        </div>
        <div class="card" style="padding:14px;margin-bottom:0;border-left:3px solid #f59e0b">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">Ativos</div>
          <div style="font-size:28px;font-weight:800;color:#f59e0b" id="cli-ativos">—</div>
          <div style="font-size:10px;color:#90afd4">parceiros ativos</div>
        </div>
        <div class="card" style="padding:14px;margin-bottom:0;border-left:3px solid #a78bfa">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">Regiões</div>
          <div style="font-size:28px;font-weight:800;color:#a78bfa" id="cli-regioes">—</div>
          <div style="font-size:10px;color:#90afd4">zonas mapeadas</div>
        </div>
      </div>

      <!-- Filtros -->
      <div class="card" style="padding:14px;margin-bottom:16px">
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr auto;gap:10px;align-items:end">
          <div>
            <label class="form-label">Buscar</label>
            <input type="text" class="form-control" id="cli-busca" placeholder="Nome, código, endereço..." oninput="filtrarClientes()">
          </div>
          <div>
            <label class="form-label">Região</label>
            <select class="form-control" id="cli-regiao" onchange="filtrarClientes()">
              <option value="">Todas as regiões</option>
            </select>
          </div>
          <div>
            <label class="form-label">GPS</label>
            <select class="form-control" id="cli-gps-filtro" onchange="filtrarClientes()">
              <option value="">Todos</option>
              <option value="sim">Com GPS</option>
              <option value="nao">Sem GPS</option>
            </select>
          </div>
          <button class="btn btn-secondary" onclick="limparFiltrosClientes()">Limpar</button>
        </div>
      </div>

      <!-- Tabela -->
      <div class="card" style="padding:0">
        <div style="overflow-x:auto;max-height:calc(100vh - 420px);overflow-y:auto">
          <table>
            <thead>
              <tr>
                <th>Cód.</th>
                <th>Nome</th>
                <th>Endereço</th>
                <th>Bairro</th>
                <th>Cidade</th>
                <th>Região</th>
                <th>GPS</th>
                <th>Telefone</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody id="clientes-tbody">
              <tr><td colspan="9" class="loading-state">⏳ Clique em Atualizar para carregar</td></tr>
            </tbody>
          </table>
        </div>
        <div style="padding:10px 16px;border-top:1px solid #1e3a5c;font-size:11px;color:#90afd4" id="clientes-rodape"></div>
      </div>
    </div>'''

if old_page in content:
    content = content.replace(old_page, new_page)
    print('Tela de Parceiros atualizada!')
else:
    print('Padrão não encontrado!')
    # Busca por posição
    idx = content.find('id="page-clientes"')
    end = content.find('<!-- ══ INTEGRAÇÃO', idx)
    print(f'Encontrado entre {idx} e {end}')
    content = content[:idx-30] + new_page + '\n    ' + content[end:]
    print('Substituído por posição!')

# Adiciona JS se não existir
if 'function loadClientes' not in content:
    js = '''
<script>
let _todosClientes = [];

function uploadParceiros() { abrirImportacaoBaseClientes(); }

async function loadClientes() {
  try {
    const lista = await api('GET', '/clientes');
    _todosClientes = lista;
    const comGps  = lista.filter(c => c.lat && c.lng).length;
    const ativos  = lista.filter(c => c.ativo === 'S').length;
    const regioes = new Set(lista.map(c => c.regiao).filter(Boolean)).size;
    const el = (id,v) => { const e=document.getElementById(id); if(e) e.textContent=v; };
    el('cli-total', lista.length);
    el('cli-gps', comGps);
    el('cli-ativos', ativos);
    el('cli-regioes', regioes);
    el('clientes-sub', lista.length + ' parceiros cadastrados');
    const sel = document.getElementById('cli-regiao');
    if (sel) {
      const regs = [...new Set(lista.map(c=>c.regiao).filter(Boolean))].sort();
      sel.innerHTML = '<option value="">Todas as regiões</option>' +
        regs.map(r=>`<option value="${r}">${r}</option>`).join('');
    }
    renderClientes(lista);
  } catch(e) { toast('Erro: '+e.message,'error'); }
}

function filtrarClientes() {
  const busca  = (document.getElementById('cli-busca')?.value||'').toLowerCase();
  const regiao = document.getElementById('cli-regiao')?.value||'';
  const gps    = document.getElementById('cli-gps-filtro')?.value||'';
  const filtrados = _todosClientes.filter(c => {
    const mb = !busca || (c.nome||'').toLowerCase().includes(busca) ||
               (c.endereco||'').toLowerCase().includes(busca) ||
               String(c.codparc||'').includes(busca);
    const mr = !regiao || c.regiao === regiao;
    const mg = !gps || (gps==='sim' ? (c.lat&&c.lng) : !(c.lat&&c.lng));
    return mb && mr && mg;
  });
  renderClientes(filtrados);
}

function limparFiltrosClientes() {
  ['cli-busca','cli-regiao','cli-gps-filtro'].forEach(id => {
    const e = document.getElementById(id); if(e) e.value='';
  });
  renderClientes(_todosClientes);
}

function renderClientes(lista) {
  const tbody = document.getElementById('clientes-tbody');
  const rodape = document.getElementById('clientes-rodape');
  if (!tbody) return;
  if (!lista.length) {
    tbody.innerHTML = '<tr><td colspan="9" class="loading-state">Nenhum parceiro encontrado</td></tr>';
    return;
  }
  tbody.innerHTML = lista.map(c => `
    <tr>
      <td style="font-family:monospace;color:#64B4FF;font-weight:700">${c.codparc||'—'}</td>
      <td><b>${c.nome||'—'}</b></td>
      <td style="font-size:11px;color:#90afd4;max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="${c.endereco||''}">${c.endereco||'—'}</td>
      <td style="font-size:11px">${c.bairro||'—'}</td>
      <td style="font-size:11px">${(c.cidade||'').replace(' - AM','')}</td>
      <td><span class="badge active" style="font-size:9px">${c.regiao||'—'}</span></td>
      <td style="text-align:center">${c.lat&&c.lng?'<span style="color:#10b981;font-size:12px">✓</span>':'<span style="color:#f87171;font-size:12px">✗</span>'}</td>
      <td style="font-size:11px">${c.telefone||'—'}</td>
      <td><span class="badge ${c.ativo==='S'?'active':'inactive'}">${c.ativo==='S'?'Ativo':'Inativo'}</span></td>
    </tr>`).join('');
  if (rodape) rodape.textContent = lista.length + ' parceiros exibidos';
}
</script>'''
    last_body = content.rfind('\n</body>')
    content = content[:last_body] + js + content[last_body:]
    print('JS adicionado!')

# goTo
if "if(page==='clientes') loadClientes();" not in content:
    content = content.replace(
        "if(page==='relatorios') setRelPeriodo(30);",
        "if(page==='relatorios') setRelPeriodo(30);\n  if(page==='clientes') loadClientes();"
    )
    print('goTo adicionado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Ctrl+Shift+R.')
