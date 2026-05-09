path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

clientes_js = '''
// ── BASE DE CLIENTES ─────────────────────────────────────────────
let _clientesCache = {};

async function carregarBaseClientes() {
  try {
    const lista = await api('GET', '/clientes');
    _clientesCache = {};
    lista.forEach(c => { _clientesCache[c.codparc] = c; });
    console.log(`Base de clientes carregada: ${lista.length} registros`);
    return lista.length;
  } catch(e) {
    console.log('Base de clientes não disponível:', e.message);
    return 0;
  }
}

function buscarClientePorCodparc(codparc) {
  return _clientesCache[parseInt(codparc)] || null;
}

// ── IMPORTAÇÃO DA BASE DE CLIENTES (XLS do Sankhya Parceiro) ─────
function abrirImportacaoBaseClientes() {
  const modal = document.getElementById('modal-base-clientes');
  if (modal) modal.style.display = 'flex';
}

function lerBaseClientesXLS(input) {
  const file = input.files[0];
  if (!file) return;
  document.getElementById('base-clientes-nome').textContent = file.name;

  const reader = new FileReader();
  reader.onload = e => {
    try {
      const wb   = XLSX.read(e.target.result, {type:'binary'});
      const ws   = wb.Sheets[wb.SheetNames[0]];
      const rows = XLSX.utils.sheet_to_json(ws, {header:1, defval:''});

      // Encontra linha de cabeçalho
      let headerIdx = 0;
      for (let r = 0; r < Math.min(5, rows.length); r++) {
        const norm = rows[r].map(h => String(h||'').toUpperCase());
        if (norm.some(h => h.includes('PARCEIRO') || h.includes('COD'))) {
          headerIdx = r; break;
        }
      }

      const header = rows[headerIdx].map(h =>
        String(h||'').trim().toUpperCase().normalize('NFD')
          .replace(/[\u0300-\u036f]/g,'').replace(/[^A-Z0-9 ().+]/g,'').trim()
      );
      console.log('Colunas base clientes:', header);

      // Mapeamento das colunas da base de parceiros Sankhya
      const m = {
        codparc:  ['COD. PARCEIRO','CODPARCEIRO','COD PARCEIRO','CODIGO'],
        nome:     ['NOME PARCEIRO','NOME','NOMEPARCEIRO'],
        bairro:   ['NOME (BAIRRO)','BAIRRO','NOME BAIRRO'],
        cidade:   ['NOME + UF (CIDADE)','CIDADE','NOME CIDADE'],
        regiao:   ['NOME (REGIAO)','REGIAO','NOME REGIAO','NOME (REGIÃO)'],
        cep:      ['CEP'],
        endereco: ['NOME (ENDERECO)','ENDERECO','NOME ENDERECO','NOME (ENDERE+O)','NOME (ENDERE O)'],
        numero:   ['NUMERO','NÚMERO'],
        telefone: ['TELEFONE','CELULAR/FAX'],
        lat:      ['LATITUDE'],
        lng:      ['LONGITUDE'],
      };

      const idx = {};
      for (const [campo, opcoes] of Object.entries(m)) {
        idx[campo] = opcoes.map(o => header.indexOf(o)).find(i => i !== -1) ?? -1;
      }
      console.log('Mapeamento base clientes:', idx);

      const clientes = [];
      let sem_gps = 0;

      for (let i = headerIdx + 1; i < rows.length; i++) {
        const cols = rows[i].map(c => String(c||'').trim());
        if (cols.join('').length === 0) continue;
        const get = (campo) => idx[campo] !== -1 ? cols[idx[campo]] || '' : '';

        const codparc = parseInt(get('codparc'));
        if (!codparc || isNaN(codparc)) continue;

        // Lat/lng — aceita vírgula ou ponto
        const parseCoorд = (v) => parseFloat(String(v).replace(',','.').replace(/[^\d.\-]/g,'')) || null;
        const lat = parseCoorд(get('lat'));
        const lng = parseCoorд(get('lng'));
        if (!lat || !lng) sem_gps++;

        // Monta endereço legível
        const rua    = get('endereco');
        const num    = get('numero');
        const bairro = get('bairro');
        const cidade = get('cidade').replace(/ - AM$/, '') || 'Manaus';
        const endFull = [rua, num].filter(Boolean).join(', ')
          + (bairro ? ', ' + bairro : '')
          + ', ' + cidade + ' - AM';

        clientes.push({
          codparc,
          nome:     get('nome'),
          bairro:   bairro,
          cidade:   get('cidade'),
          regiao:   get('regiao'),
          cep:      get('cep'),
          endereco: endFull,
          numero:   num,
          lat,
          lng,
          telefone: get('telefone'),
          ativo:    'S',
        });
      }

      document.getElementById('base-clientes-count').textContent =
        `${clientes.length} clientes encontrados (${sem_gps} sem GPS)`;
      document.getElementById('btn-importar-base').disabled = false;
      document.getElementById('btn-importar-base').style.opacity = '1';
      window._clientesParaImportar = clientes;
      toast(`${clientes.length} clientes prontos para importar!`, 'success');

    } catch(err) {
      toast('Erro ao ler XLS: ' + err.message, 'error');
      console.error(err);
    }
  };
  reader.readAsBinaryString(file);
}

async function importarBaseClientes() {
  const clientes = window._clientesParaImportar;
  if (!clientes || clientes.length === 0) { toast('Nenhum dado!','error'); return; }

  const btn = document.getElementById('btn-importar-base');
  btn.disabled = true; btn.textContent = '⏳ Importando...';

  try {
    // Envia em lotes de 500
    const loteSize = 500;
    let totalImport = 0;
    for (let i = 0; i < clientes.length; i += loteSize) {
      const lote = clientes.slice(i, i + loteSize);
      const res = await api('POST', '/clientes/bulk', lote);
      totalImport += res.inserted + res.updated;
      btn.textContent = `⏳ ${totalImport}/${clientes.length}...`;
    }
    // Recarrega cache
    await carregarBaseClientes();
    toast(`✅ ${totalImport} clientes importados! GPS disponível para cruzamento.`, 'success');
    btn.textContent = '✅ Importado';
    setTimeout(()=>{ document.getElementById('modal-base-clientes').style.display='none'; }, 2000);
  } catch(e) {
    toast('Erro: ' + e.message, 'error');
    btn.textContent = '📥 Importar Base';
    btn.disabled = false;
  }
}

// Carrega cache ao iniciar
document.addEventListener('DOMContentLoaded', () => {
  carregarBaseClientes();
});
'''

# Adiciona JS antes do fechamento do script
if 'function carregarBaseClientes' not in content:
    content = content.replace('</script>\n</body>', clientes_js + '\n</script>\n</body>')
    print('JS da base de clientes adicionado!')

# Atualiza processarLinhas para cruzar com base de clientes
old_push = '''        clientes.push({
          codparc,
          nome:     get(\'nome\'),'''

if old_push not in content:
    # Encontra o ponto onde o _csvDados.push acontece e adiciona cruzamento
    old_crossref = "      // Apenas campos usados pelo app\n      _csvDados.push({"
    new_crossref = """      // Cruza com base de clientes para pegar endereço e GPS
      const codparcNum = parseInt(get('codparc'));
      const clienteBase = codparcNum ? buscarClientePorCodparc(codparcNum) : null;

      // Endereço: prioriza base de clientes (tem GPS preciso)
      const enderecoFinal = clienteBase?.endereco || endFull;
      const latFinal  = clienteBase?.lat || null;
      const lngFinal  = clienteBase?.lng || null;
      const nomeCliente = clienteBase?.nome || get('cliente') || 'CODPARC ' + get('codparc');
      const regiaoFinal = clienteBase?.regiao || get('regiao') || null;

      // Apenas campos usados pelo app
      _csvDados.push({"""

    new_crossref2 = """        external_id:       'SNK-' + nunota,
        recipient_name:    nomeCliente,
        address:           enderecoFinal,
        weight_kg:         peso,
        volume_m3:         parseFloat(get('volume').replace(',','.').replace(/[^\\d.]/g,'')) || 0,
        total_value:       parseFloat(get('valor').replace(',','.').replace(/[^\\d.]/g,'')) || 0,
        order_type:        get('top') || '1000',
        delivery_date:     get('data') || new Date().toISOString().slice(0,10),
        regiao:            regiaoFinal,
        status:            'pending',
        priority:          1,
        lat:               latFinal,
        lng:               lngFinal,
        time_window_start: '07:30',
        time_window_end:   '18:00',"""

    if old_crossref in content:
        content = content.replace(old_crossref, new_crossref)
        print('Cruzamento com base de clientes adicionado!')

        # Substitui os campos do push para usar as variáveis corretas
        old_fields = """        external_id:       'SNK-' + nunota,
        recipient_name:    get('cliente') || 'CODPARC ' + get('codparc'),
        address:           endFull,"""
        if old_fields in content:
            content = content.replace(old_fields, new_crossref2.split('\n')[:3])

# ── Adiciona modal da base de clientes ────────────────────────────
modal_clientes = '''
  <!-- MODAL BASE DE CLIENTES -->
  <div id="modal-base-clientes" onclick="if(event.target===this)this.style.display='none'" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:3000;align-items:center;justify-content:center;padding:20px">
    <div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:560px">
      <div style="padding:16px 20px;border-bottom:1px solid #1e3a5c;display:flex;justify-content:space-between;align-items:center">
        <div>
          <div style="font-size:15px;font-weight:700;color:#e8f0fe">👥 Importar Base de Clientes</div>
          <div style="font-size:11px;color:#90afd4">Relatório de Parceiros do Sankhya (com GPS)</div>
        </div>
        <button onclick="document.getElementById('modal-base-clientes').style.display='none'" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer">✕</button>
      </div>
      <div style="padding:20px">
        <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;padding:12px;margin-bottom:16px;font-size:11px;color:#90afd4;line-height:1.8">
          📋 Exporte o relatório <b style="color:#64B4FF">Parceiro</b> do Sankhya com as colunas:<br>
          <span style="color:#10b981">Cód. Parceiro, Nome Parceiro, Bairro, Cidade, Endereço, Número, Latitude, Longitude</span><br>
          Após importar, os pedidos do CSV terão <b style="color:#f59e0b">endereço e GPS automáticos</b>!
        </div>
        <div onclick="document.getElementById('base-clientes-input').click()" style="border:2px dashed #1e3a5c;border-radius:8px;padding:24px;text-align:center;cursor:pointer;margin-bottom:16px">
          <div style="font-size:28px;margin-bottom:6px">👥</div>
          <div style="font-size:13px;color:#e8f0fe;font-weight:600">Clique para selecionar o XLS de Parceiros</div>
          <div style="font-size:11px;color:#90afd4;margin-top:4px" id="base-clientes-nome">Nenhum arquivo</div>
          <div style="font-size:12px;color:#64B4FF;margin-top:6px" id="base-clientes-count"></div>
        </div>
        <input type="file" id="base-clientes-input" accept=".xls,.xlsx,.csv" style="display:none" onchange="lerBaseClientesXLS(this)">
        <div style="display:flex;gap:8px;justify-content:flex-end">
          <button onclick="document.getElementById('modal-base-clientes').style.display='none'" class="btn btn-secondary">Cancelar</button>
          <button id="btn-importar-base" onclick="importarBaseClientes()" disabled class="btn btn-primary" style="opacity:.5;cursor:not-allowed">📥 Importar Base</button>
        </div>
      </div>
    </div>
  </div>
'''

if 'modal-base-clientes' not in content:
    content = content.replace('</body>', modal_clientes + '\n</body>')
    print('Modal base de clientes adicionado!')

# Adiciona botão na navbar ou header de pedidos
old_btn = '<button class="btn btn-primary" onclick="abrirImportacaoCSV()">📥 Importar CSV</button>'
new_btn = '<button class="btn btn-secondary" onclick="abrirImportacaoBaseClientes()" title="Importar base de clientes com GPS">👥 Base Clientes</button>\n          <button class="btn btn-primary" onclick="abrirImportacaoCSV()">📥 Importar CSV</button>'
if old_btn in content and 'abrirImportacaoBaseClientes' not in content:
    content = content.replace(old_btn, new_btn)
    print('Botão Base Clientes adicionado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nConcluído! Execute os dois scripts e reinicie o servidor.')
