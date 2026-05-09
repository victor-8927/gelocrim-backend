path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Atualiza accept do input para incluir XLS/XLSX ──────────────
old_input = 'accept=".csv,.txt" style="display:none" onchange="lerArquivoCSV(this)"'
new_input = 'accept=".csv,.txt,.xls,.xlsx" style="display:none" onchange="lerArquivoCSV(this)"'

if old_input in content:
    content = content.replace(old_input, new_input)
    print('Input atualizado para XLS/XLSX!')

# ── 2. Atualiza descrição no modal ─────────────────────────────────
old_desc = 'Clique para selecionar o arquivo CSV'
new_desc = 'Clique para selecionar o arquivo (CSV, XLS ou XLSX)'
content = content.replace(old_desc, new_desc)

old_format = 'Campos: NUNOTA, NOMEPARC, ENDERECO, PESO, VOLUME, CODTIPOPER, VLRNOTA'
new_format = 'Formatos aceitos: CSV, XLS, XLSX (exportação direta do Sankhya)'
content = content.replace(old_format, new_format)
print('Descrição atualizada!')

# ── 3. Adiciona SheetJS para ler XLS/XLSX ─────────────────────────
old_head = '</head>'
sheetjs = '  <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>\n</head>'
if 'xlsx.full.min.js' not in content:
    content = content.replace(old_head, sheetjs)
    print('SheetJS adicionado!')

# ── 4. Atualiza função lerArquivoCSV para detectar XLS/XLSX ────────
idx = content.find('function lerArquivoCSV(input)')
if idx != -1:
    depth=0; started=False; i=idx
    for i in range(idx, len(content)):
        if content[i]=='{': depth+=1; started=True
        elif content[i]=='}': depth-=1
        if started and depth==0: break

    new_ler = '''function lerArquivoCSV(input) {
  const file = input.files[0];
  if (!file) return;
  const ext = file.name.split('.').pop().toLowerCase();
  document.getElementById('csv-nome-arquivo').textContent = file.name + ' (' + (file.size/1024).toFixed(1) + ' KB)';

  if (ext === 'xls' || ext === 'xlsx') {
    // Lê XLS/XLSX com SheetJS
    const reader = new FileReader();
    reader.onload = e => {
      try {
        const workbook = XLSX.read(e.target.result, {type:'binary'});
        const sheetName = workbook.SheetNames[0];
        const sheet = workbook.Sheets[sheetName];
        const rows  = XLSX.utils.sheet_to_json(sheet, {header:1, defval:''});
        if (rows.length < 2) { toast('Arquivo vazio!','error'); return; }
        processarLinhas(rows);
      } catch(err) {
        toast('Erro ao ler XLS: ' + err.message, 'error');
        console.error(err);
      }
    };
    reader.readAsBinaryString(file);
  } else {
    // Lê CSV
    const reader = new FileReader();
    reader.onload = e => {
      const text = e.target.result;
      const sep  = text.includes(';') ? ';' : ',';
      const linhas = text.split('\\n').filter(l => l.trim());
      if (linhas.length < 2) { toast('Arquivo vazio!','error'); return; }
      const rows = linhas.map(l => l.split(sep).map(c => c.trim().replace(/^"|"$/g,'')));
      processarLinhas(rows);
    };
    reader.readAsText(file, 'latin1');
  }
}

function processarLinhas(rows) {
  // Normaliza header
  const header = rows[0].map(h => String(h).trim().toUpperCase().replace(/[^A-Z0-9_]/g,''));
  console.log('Colunas encontradas:', header);

  // Mapeamento Sankhya → campos do app
  const mapa = {
    id:       ['NUNOTA','NUMNOTA','NUMNOT','PEDIDO','NOTA'],
    cliente:  ['NOMEPARC','NOME','NOMECLIENTE','CLIENTE','RAZAOSOCIAL','RAZAOSOC'],
    endereco: ['ENDERECO','ENDCOB','ENDERECOCOB','LOGRADOURO','END'],
    cidade:   ['CIDADE','MUNICIPIO','NOMECIDADE','CIDADECOB'],
    bairro:   ['BAIRRO','BAIRROCOB'],
    peso:     ['PESO','PESOLIQ','PESOBRUTO','PESONOTA'],
    volume:   ['VOLUME','VOL','CUBAGEM','VOLUMETOTAL'],
    data:     ['DTNEG','DTNEGOCIACAO','DATA','DATAPED','DTPED'],
    top:      ['CODTIPOPER','TIPOPER','TOP','TIPOOPER'],
    valor:    ['VLRNOTA','VALOR','VLRTOTAL','TOTALNOTAFISCAL'],
    codparc:  ['CODPARC','CODCLIENTE','CODFORNEC'],
    regiao:   ['ROTA','REGIAO','ZONA','CODREGIAO'],
  };

  const idx = {};
  for (const [campo, opcoes] of Object.entries(mapa)) {
    idx[campo] = opcoes.map(o => header.indexOf(o)).find(i => i !== -1) ?? -1;
  }
  console.log('Mapeamento:', idx);

  _csvDados = [];
  let erros = 0;

  for (let i = 1; i < rows.length; i++) {
    const cols = rows[i].map(c => String(c||'').trim());
    if (cols.join('').length === 0) continue;
    const get = (campo) => idx[campo] !== -1 ? cols[idx[campo]] || '' : '';

    const nunota = get('id');
    const pesoStr = get('peso').replace(',','.').replace(/[^\\d.]/g,'');
    const peso = parseFloat(pesoStr) || 0;

    if (!nunota || peso === 0) { erros++; continue; }

    const endereco = get('endereco');
    const bairro   = get('bairro');
    const cidade   = get('cidade') || 'Manaus';
    const endParts = [endereco, bairro].filter(Boolean);
    const endFull  = endParts.length > 0
      ? `${endParts.join(', ')}, ${cidade} - AM`
      : 'Manaus - AM';

    _csvDados.push({
      external_id:       'SNK-' + nunota,
      recipient_name:    get('cliente') || 'CODPARC ' + get('codparc'),
      address:           endFull,
      weight_kg:         peso,
      volume_m3:         parseFloat(get('volume').replace(',','.').replace(/[^\\d.]/g,'')) || 0,
      total_value:       parseFloat(get('valor').replace(',','.').replace(/[^\\d.]/g,'')) || 0,
      order_type:        get('top') || '1000',
      delivery_date:     get('data') || new Date().toISOString().slice(0,10),
      regiao:            get('regiao') || null,
      status:            'pending',
      priority:          1,
      lat:               null,
      lng:               null,
      time_window_start: '07:30',
      time_window_end:   '18:00',
    });
  }

  // Atualiza contadores
  document.getElementById('csv-total-linhas').textContent = rows.length - 1;
  document.getElementById('csv-validos').textContent = _csvDados.length;
  document.getElementById('csv-erros').textContent = erros;

  // Prévia
  const preview = _csvDados.slice(0,5);
  document.getElementById('csv-preview-table').innerHTML = `
    <thead><tr style="background:#1e3a5c">
      <th style="padding:6px 10px;font-size:10px;color:#64B4FF">Nº Pedido</th>
      <th style="padding:6px 10px;font-size:10px;color:#64B4FF">Cliente</th>
      <th style="padding:6px 10px;font-size:10px;color:#64B4FF">Endereço</th>
      <th style="padding:6px 10px;font-size:10px;color:#64B4FF">Peso</th>
      <th style="padding:6px 10px;font-size:10px;color:#64B4FF">Volume</th>
      <th style="padding:6px 10px;font-size:10px;color:#64B4FF">TOP</th>
      <th style="padding:6px 10px;font-size:10px;color:#64B4FF">Valor</th>
    </tr></thead>
    <tbody>
      ${preview.map(p=>`<tr>
        <td style="padding:5px 10px;font-family:monospace;font-size:11px;color:#64B4FF">${p.external_id}</td>
        <td style="padding:5px 10px;font-size:11px;font-weight:600">${p.recipient_name}</td>
        <td style="padding:5px 10px;font-size:10px;color:#90afd4;max-width:140px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="${p.address}">${p.address}</td>
        <td style="padding:5px 10px;font-size:11px;color:#f59e0b;font-weight:600">${p.weight_kg} kg</td>
        <td style="padding:5px 10px;font-size:11px;color:#2dd4bf">${p.volume_m3} m³</td>
        <td style="padding:5px 10px;font-size:11px;color:#a78bfa">TOP ${p.order_type}</td>
        <td style="padding:5px 10px;font-size:11px;color:#10b981">${p.total_value>0?'R$ '+p.total_value.toFixed(2):'—'}</td>
      </tr>`).join('')}
      ${_csvDados.length>5?`<tr><td colspan="7" style="padding:5px 10px;font-size:10px;color:#90afd4;text-align:center">... e mais ${_csvDados.length-5} pedidos</td></tr>`:''}
    </tbody>`;

  document.getElementById('csv-preview').style.display = 'block';
  document.getElementById('csv-opcoes').style.display  = 'block';

  const btn = document.getElementById('btn-importar-csv');
  if (_csvDados.length > 0) {
    btn.disabled=false; btn.style.opacity='1'; btn.style.cursor='pointer';
    toast(`${_csvDados.length} pedidos encontrados!`, 'success');
  } else {
    toast('Nenhum pedido válido! Verifique o arquivo.', 'error');
  }
}'''

    content = content[:idx] + new_ler + content[i+1:]
    print('lerArquivoCSV atualizado para XLS/XLSX/CSV!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Ctrl+Shift+R.')
