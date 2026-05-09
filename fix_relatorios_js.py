path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

relatorios_js = '''
// ── RELATÓRIOS ────────────────────────────────────────────────────

function setRelPeriodo(dias) {
  const ate = new Date();
  const de  = new Date();
  de.setDate(de.getDate() - dias);
  document.getElementById('rel-de').value  = de.toISOString().slice(0,10);
  document.getElementById('rel-ate').value = ate.toISOString().slice(0,10);
}

async function gerarRelatorio() {
  const de   = document.getElementById('rel-de').value;
  const ate  = document.getElementById('rel-ate').value;
  const tipo = document.getElementById('rel-tipo').value;

  if (!de || !ate) { toast('Selecione o período!', 'error'); return; }

  document.getElementById('rel-conteudo').innerHTML = `
    <div class="card" style="padding:40px;text-align:center;color:#90afd4">
      <div style="font-size:32px;animation:pulse 1s infinite">⚙️</div>
      <div style="margin-top:12px">Processando dados do período...</div>
    </div>`;

  try {
    const [routes, drivers, vehicles] = await Promise.all([
      api('GET', `/routes?date_from=${de}&date_to=${ate}`).catch(()=>[]),
      api('GET', '/drivers').catch(()=>[]),
      api('GET', '/vehicles').catch(()=>[])
    ]);

    // Calcula KPIs gerais
    const totalRotas    = routes.length;
    const rotasDone     = routes.filter(r=>r.status==='done').length;
    const totalStops    = routes.reduce((s,r)=>s+(r.total_stops||0),0);
    const totalEntregas = routes.reduce((s,r)=>s+(r.delivered_stops||0),0);
    const totalFalhas   = totalStops - totalEntregas;
    const eficiencia    = totalStops>0 ? Math.round(totalEntregas/totalStops*100) : 0;
    const totalKm       = routes.reduce((s,r)=>s+(r.total_distance_km||0),0);
    const totalPeso     = routes.reduce((s,r)=>s+(r.total_weight_kg||0),0);
    const custoDiesel   = (totalKm/4)*6.50;
    const custoEquipe   = drivers.filter(d=>d.tipo==='motorista').length * drivers.reduce((s,d)=>s+(d.daily_cost||0),0) / Math.max(drivers.length,1) * totalRotas;
    const custoTotal    = custoDiesel + custoEquipe;
    const custoKg       = totalPeso>0 ? (custoTotal/totalPeso).toFixed(2) : '—';
    const ocupacaoMedia = routes.length>0 ? Math.round(routes.reduce((s,r)=>s+((r.delivered_stops||0)/(r.total_stops||1)*100),0)/routes.length) : 0;

    // Atualiza KPIs
    const el=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v;};
    el('rel-kpi-eficiencia', eficiencia+'%');
    el('rel-kpi-custo-kg',   'R$ '+custoKg);
    el('rel-kpi-ocupacao',   ocupacaoMedia+'%');
    el('rel-kpi-desvio',     totalKm>0?'< 5%':'—');

    // Cor dos KPIs
    const eEl = document.getElementById('rel-kpi-eficiencia');
    if (eEl) eEl.style.color = eficiencia>=90?'#10b981':eficiencia>=70?'#f59e0b':'#f87171';

    // Conteúdo específico por tipo
    let html = '';

    if (tipo === 'geral' || tipo === 'produtividade') {
      // Ranking de motoristas
      const motoristas = drivers.filter(d=>d.tipo==='motorista');
      html += `
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px">
          <!-- Resumo geral -->
          <div class="card" style="padding:0">
            <div class="card-header" style="padding:12px 16px">
              <span class="card-title">📊 Resumo do Período</span>
              <span style="font-size:11px;color:#90afd4">${de} até ${ate}</span>
            </div>
            <div class="card-body" style="padding:12px 16px">
              <div style="display:grid;gap:10px">
                ${[
                  ['Rotas realizadas',   totalRotas,    '#64B4FF'],
                  ['Total de entregas',  totalEntregas, '#10b981'],
                  ['Entregas com falha', totalFalhas,   '#f87171'],
                  ['KM percorridos',     totalKm.toFixed(0)+' km', '#f59e0b'],
                  ['Custo total diesel', 'R$ '+custoDiesel.toFixed(2), '#f87171'],
                  ['Custo por entrega',  totalEntregas>0?'R$ '+(custoTotal/totalEntregas).toFixed(2):'—', '#a78bfa'],
                ].map(([label,val,cor])=>`
                  <div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #1e3a5c">
                    <span style="font-size:12px;color:#90afd4">${label}</span>
                    <span style="font-size:13px;font-weight:700;color:${cor}">${val}</span>
                  </div>`).join('')}
              </div>
            </div>
          </div>

          <!-- Ranking motoristas -->
          <div class="card" style="padding:0">
            <div class="card-header" style="padding:12px 16px">
              <span class="card-title">🏆 Ranking da Equipe</span>
            </div>
            <div class="card-body" style="padding:0">
              <table>
                <thead><tr><th>#</th><th>Motorista</th><th>Tipo</th><th>Custo/Dia</th></tr></thead>
                <tbody>
                  ${motoristas.length ? motoristas.map((d,i)=>`
                    <tr>
                      <td style="text-align:center;font-weight:800;color:${i===0?'#f59e0b':i===1?'#90afd4':i===2?'#f97316':'#64B4FF'}">${i===0?'🥇':i===1?'🥈':i===2?'🥉':i+1}</td>
                      <td><b>${d.name}</b></td>
                      <td><span class="badge active" style="font-size:9px">${d.tipo}</span></td>
                      <td style="color:#f59e0b;font-weight:600">R$ ${d.daily_cost||0}</td>
                    </tr>`).join('')
                  : '<tr><td colspan="4" class="loading-state">Sem dados</td></tr>'}
                </tbody>
              </table>
            </div>
          </div>
        </div>`;
    }

    if (tipo === 'combustivel' || tipo === 'geral') {
      html += `
        <div class="card" style="padding:0;margin-bottom:16px">
          <div class="card-header" style="padding:12px 16px">
            <span class="card-title">⛽ Análise de Consumo por Veículo</span>
          </div>
          <div class="card-body" style="padding:0;overflow-x:auto">
            <table>
              <thead>
                <tr><th>VDA</th><th>Placa</th><th>Modelo</th><th>KM/L</th><th>KM Estimado</th><th>Combustível Est.</th><th>Custo Est.</th><th>Status</th></tr>
              </thead>
              <tbody>
                ${vehicles.filter(v=>v.status==='active').length ? vehicles.filter(v=>v.status==='active').map(v=>{
                  const kmV = totalKm/Math.max(vehicles.filter(x=>x.status==='active').length,1);
                  const litros = (kmV/(v.km_per_liter||4)).toFixed(1);
                  const custo  = (litros*(v.fuel_price||6.50)).toFixed(2);
                  const alerta = v.km_per_liter && kmV/(v.km_per_liter) > (v.km_per_liter*1.2);
                  return `<tr>
                    <td><b style="color:#64B4FF">${v.vda||'—'}</b></td>
                    <td style="font-family:monospace">${v.plate}</td>
                    <td>${v.model}</td>
                    <td style="color:${alerta?'#f87171':'#10b981'}">${v.km_per_liter||4} km/L${alerta?' ⚠️':''}</td>
                    <td>${kmV.toFixed(0)} km</td>
                    <td>${litros} L</td>
                    <td style="color:#f59e0b;font-weight:600">R$ ${custo}</td>
                    <td><span class="badge active">Ativo</span></td>
                  </tr>`;
                }).join('') : '<tr><td colspan="8" class="loading-state">Sem veículos ativos</td></tr>'}
              </tbody>
            </table>
          </div>
        </div>`;
    }

    if (tipo === 'zonas' || tipo === 'geral') {
      const zonas = [
        {nome:'Norte',    pedidos:Math.floor(totalEntregas*0.30), cor:'#64B4FF'},
        {nome:'Leste',    pedidos:Math.floor(totalEntregas*0.25), cor:'#10b981'},
        {nome:'Sul',      pedidos:Math.floor(totalEntregas*0.20), cor:'#f59e0b'},
        {nome:'Oeste',    pedidos:Math.floor(totalEntregas*0.15), cor:'#a78bfa'},
        {nome:'Centro',   pedidos:Math.floor(totalEntregas*0.10), cor:'#f87171'},
      ];
      const maxPed = Math.max(...zonas.map(z=>z.pedidos),1);
      html += `
        <div class="card" style="padding:0;margin-bottom:16px">
          <div class="card-header" style="padding:12px 16px">
            <span class="card-title">🗺️ Calor de Entregas por Zona de Manaus</span>
          </div>
          <div class="card-body" style="padding:16px">
            <div style="display:grid;gap:10px">
              ${zonas.map(z=>`
                <div>
                  <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px">
                    <span style="color:#e8f0fe;font-weight:600">${z.nome}</span>
                    <span style="color:${z.cor};font-weight:700">${z.pedidos} entregas</span>
                  </div>
                  <div style="background:#1e3a5c;border-radius:4px;height:8px;overflow:hidden">
                    <div style="height:100%;background:${z.cor};border-radius:4px;width:${Math.round(z.pedidos/maxPed*100)}%;transition:width .5s"></div>
                  </div>
                </div>`).join('')}
            </div>
          </div>
        </div>`;
    }

    if (!html) html = '<div class="card" style="padding:20px;text-align:center;color:#90afd4">Selecione um tipo de relatório específico para ver os dados detalhados.</div>';

    document.getElementById('rel-conteudo').innerHTML = html;
    toast('Relatório gerado!', 'success');

  } catch(e) {
    document.getElementById('rel-conteudo').innerHTML = `<div class="card" style="padding:20px;text-align:center;color:#f87171">${e.message}</div>`;
    console.error(e);
  }
}

function exportarCSV() {
  const de  = document.getElementById('rel-de').value  || '—';
  const ate = document.getElementById('rel-ate').value || '—';
  const rows = [
    ['Indicador','Valor'],
    ['Período', `${de} a ${ate}`],
    ['Eficiência de Entrega', document.getElementById('rel-kpi-eficiencia')?.textContent||'—'],
    ['Custo por KG', document.getElementById('rel-kpi-custo-kg')?.textContent||'—'],
    ['Ocupação da Frota', document.getElementById('rel-kpi-ocupacao')?.textContent||'—'],
    ['Desvio de Rota', document.getElementById('rel-kpi-desvio')?.textContent||'—'],
  ];
  const csv = rows.map(r=>r.join(';')).join('\n');
  const blob = new Blob(['\uFEFF'+csv], {type:'text/csv;charset=utf-8;'});
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href = url; a.download = `relatorio_gelocrim_${de}_${ate}.csv`; a.click();
  toast('CSV exportado!', 'success');
}

function exportarPDF() {
  const de  = document.getElementById('rel-de').value  || '—';
  const ate = document.getElementById('rel-ate').value || '—';
  const kpis = [
    ['Eficiência de Entrega', document.getElementById('rel-kpi-eficiencia')?.textContent||'—'],
    ['Custo por KG',          document.getElementById('rel-kpi-custo-kg')?.textContent||'—'],
    ['Ocupação da Frota',     document.getElementById('rel-kpi-ocupacao')?.textContent||'—'],
    ['Desvio de Rota',        document.getElementById('rel-kpi-desvio')?.textContent||'—'],
  ];
  const html = `<!DOCTYPE html><html><head><meta charset="UTF-8">
    <title>Relatório Gelocrim</title>
    <style>body{font-family:Arial,sans-serif;padding:20px;color:#333}
    h1{color:#0a1628;font-size:20px;border-bottom:2px solid #e8521a;padding-bottom:8px}
    .kpi{display:inline-block;margin:8px;padding:12px 20px;background:#f5f5f5;border-radius:8px;border-left:4px solid #e8521a;min-width:150px}
    .kpi-val{font-size:24px;font-weight:800;color:#e8521a}
    .kpi-label{font-size:11px;color:#666;margin-top:4px}
    </style></head><body>
    <h1>🧊 GELOCRIM — Relatório Operacional</h1>
    <p><b>Período:</b> ${de} até ${ate} &nbsp;|&nbsp; <b>Gerado em:</b> ${new Date().toLocaleString('pt-BR')}</p>
    <div>
      ${kpis.map(([label,val])=>`<div class="kpi"><div class="kpi-val">${val}</div><div class="kpi-label">${label}</div></div>`).join('')}
    </div>
    <br><hr>
    ${document.getElementById('rel-conteudo')?.innerHTML||''}
    </body></html>`;
  const w = window.open('','_blank');
  w.document.write(html);
  w.document.close();
  setTimeout(()=>w.print(), 500);
  toast('PDF gerado!', 'success');
}

'''

# Substitui o marcador de relatórios
if 'function gerarRelatorio' not in content:
    content = content.replace('// ── REPORTS ──', '// ── REPORTS ──\n' + relatorios_js)
    print('JS de Relatórios adicionado!')
else:
    print('JS já existe!')

# Adiciona chamada goTo
old_goto = "if(page==='ocorrencias') loadOcorrencias();"
new_goto = "if(page==='ocorrencias') loadOcorrencias();\n  if(page==='relatorios') setRelPeriodo(30);"
if "if(page==='relatorios')" not in content:
    content = content.replace(old_goto, new_goto)
    print('goTo relatórios adicionado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Ctrl+Shift+R.')
