path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_parse = '''    // Parse das linhas
    _csvDados = [];
    let erros = 0;
    for (let i = 1; i < linhas.length; i++) {
      const cols = linhas[i].split(sep).map(c => c.trim().replace(/^["\']|["\']$/g,\'\'));
      if (cols.length < 2) continue;
      const get = (campo) => idx[campo] !== -1 ? cols[idx[campo]] || \'\' : \'\';
      const peso = parseFloat(get(\'peso\').replace(\',\',\'.\')) || 0;
      if (!get(\'id\') || peso === 0) { erros++; continue; }
      _csvDados.push({
        external_id:     \'SNK-\' + get(\'id\'),
        codparc:         get(\'codparc\'),
        recipient_name:  get(\'cliente\') || \'Cliente \' + get(\'codparc\'),
        address:         get(\'endereco\') ? get(\'endereco\') + (get(\'cidade\') ? \', \' + get(\'cidade\') + \' - AM\' : \', Manaus - AM\') : \'Manaus - AM\',
        weight_kg:       peso,
        volume_m3:       parseFloat(get(\'volume\').replace(\',\',\'.\')) || 0,
        delivery_date:   get(\'data\') || new Date().toISOString().slice(0,10),
        order_type:      get(\'top\') || \'1000\',
        total_value:     parseFloat(get(\'valor\').replace(\',\',\'.\')) || 0,
        status:          \'pending\',
        priority:        1,
      });
    }'''

new_parse = '''    // Parse das linhas — apenas campos usados pelo app
    _csvDados = [];
    let erros = 0;
    for (let i = 1; i < linhas.length; i++) {
      const cols = linhas[i].split(sep).map(c => c.trim().replace(/^["\'"]|["\'"]$/g,''));
      if (cols.length < 2) continue;
      const get = (campo) => idx[campo] !== -1 ? (cols[idx[campo]] || '').trim() : '';

      const nunota = get('id');
      const peso   = parseFloat(get('peso').replace(',','.').replace(/[^0-9.]/g,'')) || 0;

      // Ignora linha se não tiver NUNOTA ou peso
      if (!nunota || peso === 0) { erros++; continue; }

      // Monta endereço completo para Manaus
      const endereco = get('endereco');
      const cidade   = get('cidade') || 'Manaus';
      const endFull  = endereco
        ? `${endereco}, ${cidade} - AM`
        : 'Manaus - AM';

      // Apenas os campos que o app usa
      _csvDados.push({
        external_id:        'SNK-' + nunota,
        recipient_name:     get('cliente') || 'CODPARC ' + get('codparc'),
        address:            endFull,
        weight_kg:          peso,
        volume_m3:          parseFloat(get('volume').replace(',','.').replace(/[^0-9.]/g,'')) || 0,
        total_value:        parseFloat(get('valor').replace(',','.').replace(/[^0-9.]/g,'')) || 0,
        order_type:         get('top') || '1000',
        delivery_date:      get('data') || new Date().toISOString().slice(0,10),
        status:             'pending',
        priority:           1,
        // GPS vazio — será geocodificado
        lat:                null,
        lng:                null,
        // Janela padrão Gelocrim
        time_window_start:  '07:30',
        time_window_end:    '18:00',
      });
    }'''

if old_parse in content:
    content = content.replace(old_parse, new_parse)
    print('Parse do CSV atualizado com campos corretos!')
else:
    # Tenta localizar pelo trecho único
    idx2 = content.find("_csvDados.push({")
    if idx2 != -1:
        print(f'Encontrado em posição {idx2}, verificando...')
        print(content[idx2:idx2+400])
    else:
        print('ERRO: padrão não encontrado')

# Atualiza também a prévia para mostrar campos corretos
old_preview_html = '''      <thead><tr style="background:#1e3a5c">
        <th style="padding:6px 10px;font-size:10px;color:#64B4FF">NUNOTA</th>
        <th style="padding:6px 10px;font-size:10px;color:#64B4FF">Cliente</th>
        <th style="padding:6px 10px;font-size:10px;color:#64B4FF">Endereço</th>
        <th style="padding:6px 10px;font-size:10px;color:#64B4FF">Peso (kg)</th>
        <th style="padding:6px 10px;font-size:10px;color:#64B4FF">Volume (m³)</th>
        <th style="padding:6px 10px;font-size:10px;color:#64B4FF">TOP</th>
      </tr></thead>
      <tbody>
        ${preview.map(p=>`<tr>
          <td style="padding:5px 10px;font-family:monospace;font-size:11px;color:#64B4FF">${p.external_id}</td>
          <td style="padding:5px 10px;font-size:11px">${p.recipient_name}</td>
          <td style="padding:5px 10px;font-size:10px;color:#90afd4;max-width:150px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${p.address}</td>
          <td style="padding:5px 10px;font-size:11px;color:#f59e0b;font-weight:600">${p.weight_kg} kg</td>
          <td style="padding:5px 10px;font-size:11px;color:#2dd4bf">${p.volume_m3} m³</td>
          <td style="padding:5px 10px;font-size:11px;color:#a78bfa">${p.order_type}</td>
        </tr>`).join('')}'''

new_preview_html = '''      <thead><tr style="background:#1e3a5c">
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
        </tr>`).join('')}'''

if old_preview_html in content:
    content = content.replace(old_preview_html, new_preview_html)
    print('Prévia atualizada com campos corretos!')

# Atualiza instruções do modal
old_instrucoes = '''              Colunas obrigatórias: <span style="color:#10b981">NUNOTA, CODPARC, DTNEG, PESO, VOLUME</span><br>
              Colunas opcionais: <span style="color:#f59e0b">NOMEPARC, ENDERECO, CIDADE, CODTIPOPER, VLRNOTA</span><br>'''

new_instrucoes = '''              Colunas obrigatórias: <span style="color:#10b981">NUNOTA, PESO</span><br>
              Colunas usadas: <span style="color:#f59e0b">NOMEPARC, ENDERECO, CIDADE, VOLUME, DTNEG, CODTIPOPER, VLRNOTA</span><br>
              Demais colunas da planilha: <span style="color:#90afd4">ignoradas automaticamente</span><br>'''

if old_instrucoes in content:
    content = content.replace(old_instrucoes, new_instrucoes)
    print('Instruções atualizadas!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Ctrl+Shift+R.')
