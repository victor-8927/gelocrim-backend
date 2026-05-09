path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica se já existe
if 'function abrirImportacaoCSV' in content:
    print('Função já existe!')
else:
    print('Função não encontrada, injetando...')

importacao_js = '''
// ── IMPORTAÇÃO CSV SANKHYA ────────────────────────────────────────
let _csvDados = [];

function abrirImportacaoCSV() {
  _csvDados = [];
  document.getElementById('csv-nome-arquivo').textContent = 'Nenhum arquivo selecionado';
  document.getElementById('csv-preview').style.display = 'none';
  document.getElementById('csv-opcoes').style.display = 'none';
  document.getElementById('csv-resultado').style.display = 'none';
  const btn = document.getElementById('btn-importar-csv');
  if (btn) { btn.disabled=true; btn.style.opacity='.5'; btn.textContent='📥 Importar Pedidos'; }
  document.getElementById('csv-file-input').value = '';
  document.getElementById('modal-importacao-csv').style.display = 'flex';
}

function lerArquivoCSV(input) {
  const file = input.files[0];
  if (!file) return;
  document.getElementById('csv-nome-arquivo').textContent = file.name + ' (' + (file.size/1024).toFixed(1) + ' KB)';

  const reader = new FileReader();
  reader.onload = e => {
    let text = e.target.result;
    const sep = text.includes(';') ? ';' : ',';
    const linhas = text.split(/\r?\n/).filter(l => l.trim());
    if (linhas.length < 2) { toast('Arquivo vazio!', 'error'); return; }

    const header = linhas[0].split(sep).map(h => h.trim().toUpperCase().replace(/["\u0000-\u001f]/g,''));
    console.log('Colunas CSV:', header);

    // Mapeamento Sankhya → campos do app
    const mapa = {
      id:       ['NUNOTA','NUMNOTA','NUM_NOTA','PEDIDO'],
      cliente:  ['NOMEPARC','NOME_PARC','NOMECLIENTE','CLIENTE','RAZAOSOCIAL'],
      endereco: ['ENDERECO','ENDEREÇO','ENDCLIENTE','LOGRADOURO'],
      cidade:   ['CIDADE','MUNICIPIO','NOMECIDADE'],
      peso:     ['PESO','PESOLIQ','PESO_LIQ','PESOBRUTO'],
      volume:   ['VOLUME','VOL','CUBAGEM'],
      data:     ['DTNEG','DT_NEG','DATANEG','DATA'],
      top:      ['CODTIPOPER','COD_TIPO_OPER','TOP','TIPOPER'],
      valor:    ['VLRNOTA','VLR_NOTA','VALOR','VLRTOTAL'],
      codparc:  ['CODPARC','COD_PARC'],
    };

    const idx = {};
    for (const [campo, opcoes] of Object.entries(mapa)) {
      idx[campo] = opcoes.map(o => header.indexOf(o)).find(i => i !== -1) ?? -1;
    }
    console.log('Mapeamento:', idx);

    _csvDados = [];
    let erros = 0;

    for (let i = 1; i < linhas.length; i++) {
      const cols = linhas[i].split(sep).map(c => c.trim().replace(/^"|"$/g,''));
      if (cols.length < 2) continue;
      const get = (campo) => idx[campo] !== -1 ? (cols[idx[campo]]||'').trim() : '';

      const nunota = get('id');
      const pesoStr = get('peso').replace(',','.').replace(/[^\d.]/g,'');
      const peso = parseFloat(pesoStr) || 0;

      if (!nunota || peso === 0) { erros++; continue; }

      const endereco = get('endereco');
      const cidade   = get('cidade') || 'Manaus';
      const endFull  = endereco ? `${endereco}, ${cidade} - AM` : 'Manaus - AM';

      // Apenas campos usados pelo app matriz
      _csvDados.push({
        external_id:       'SNK-' + nunota,
        recipient_name:    get('cliente') || 'CODPARC ' + get('codparc'),
        address:           endFull,
        weight_kg:         peso,
        volume_m3:         parseFloat(get('volume').replace(',','.').replace(/[^\d.]/g,'')) || 0,
        total_value:       parseFloat(get('valor').replace(',','.').replace(/[^\d.]/g,'')) || 0,
        order_type:        get('top') || '1000',
        delivery_date:     get('data') || new Date().toISOString().slice(0,10),
        status:            'pending',
        priority:          1,
        lat:               null,
        lng:               null,
        time_window_start: '07:30',
        time_window_end:   '18:00',
      });
    }

    document.getElementById('csv-total-linhas').textContent = linhas.length - 1;
    document.getElementById('csv-validos').textContent = _csvDados.length;
    document.getElementById('csv-erros').textContent = erros;

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
    document.getElementById('csv-opcoes').style.display = 'block';

    const btn = document.getElementById('btn-importar-csv');
    if (_csvDados.length > 0) {
      btn.disabled=false; btn.style.opacity='1'; btn.style.cursor='pointer';
      toast(`${_csvDados.length} pedidos encontrados! Verifique a prévia.`, 'success');
    } else {
      toast('Nenhum pedido válido! Verifique o CSV.', 'error');
    }
  };
  reader.readAsText(file, 'latin1');
}

async function importarCSV() {
  if (_csvDados.length === 0) { toast('Nenhum dado!', 'error'); return; }
  const btn = document.getElementById('btn-importar-csv');
  btn.disabled=true; btn.textContent='⏳ Importando...';

  const ignorarDup = document.getElementById('csv-opt-duplicados').checked;
  const usarHoje   = document.getElementById('csv-opt-data-hoje').checked;
  const hoje       = new Date().toISOString().slice(0,10);

  let existentes = [];
  if (ignorarDup) {
    try { const ords=await api('GET','/orders'); existentes=ords.map(o=>o.external_id); } catch(e) {}
  }

  let importados=0, duplicados=0, erros=0;

  for (const pedido of _csvDados) {
    if (ignorarDup && existentes.includes(pedido.external_id)) { duplicados++; continue; }
    if (usarHoje) pedido.delivery_date = hoje;
    try {
      await api('POST', '/orders', pedido);
      importados++;
    } catch(e) { erros++; console.log('Erro:', pedido.external_id, e.message); }
    btn.textContent = `⏳ ${importados+duplicados+erros}/${_csvDados.length}...`;
  }

  const res = document.getElementById('csv-resultado');
  res.style.display='block';
  res.style.background=erros>0?'rgba(248,113,113,.1)':'rgba(16,185,129,.1)';
  res.style.border=`1px solid ${erros>0?'#f87171':'#10b981'}`;
  res.innerHTML=`
    <div style="font-size:13px;font-weight:700;color:${erros>0?'#f87171':'#10b981'};margin-bottom:8px">
      ${erros>0?'⚠️':'✅'} Importação ${erros>0?'com alertas':'concluída'}
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;font-size:12px">
      <div style="text-align:center"><div style="font-size:22px;font-weight:800;color:#10b981">${importados}</div><div style="color:#90afd4">Importados</div></div>
      <div style="text-align:center"><div style="font-size:22px;font-weight:800;color:#f59e0b">${duplicados}</div><div style="color:#90afd4">Duplicados</div></div>
      <div style="text-align:center"><div style="font-size:22px;font-weight:800;color:#f87171">${erros}</div><div style="color:#90afd4">Erros</div></div>
    </div>`;

  btn.textContent='✅ Concluído';
  toast(`${importados} pedidos importados!`, 'success');
  setTimeout(()=>{ loadOrders(); document.getElementById('modal-importacao-csv').style.display='none'; }, 2000);
}
'''

# Injeta antes de </script>
content = content.replace('</script>\n</body>', importacao_js + '\n</script>\n</body>')
print('JS injetado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Ctrl+Shift+R.')
