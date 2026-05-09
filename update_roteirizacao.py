"""
update_roteirizacao.py
Atualiza a tela de roteirização para mostrar score, horário 07:30 e agrupamento.
Execute: python update_roteirizacao.py
"""

html_path = r"C:\fleet-cloud\gelocrim_v1.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Substitui a função optimizeRoutes para mostrar mais informações
old_func = """async function optimizeRoutes() {
  const btn = document.getElementById('btn-optimize');
  const result = document.getElementById('optimize-result');
  btn.disabled = true; btn.textContent = '⏳ Roteirizando...';
  result.innerHTML = `<div class="alert info">⏳ O solver VRP está calculando as melhores rotas. Aguarde...</div>`;
  try {
    const d = await api('POST', '/routes/optimize', {
      route_date: document.getElementById('opt-date').value,
      time_limit_sec: +document.getElementById('opt-time').value||30,
      reoptimize: document.getElementById('opt-reoptimize').checked,
    });
    result.innerHTML = `
      <div class="card">
        <div class="card-header" style="background:var(--success-bg)">
          <span class="card-title" style="color:var(--success)">✅ Roteirização Concluída</span>
          <span style="font-size:12px;color:var(--muted)">Status: ${d.status} · ${(d.wall_time_ms/1000).toFixed(1)}s</span>
        </div>
        <div class="card-body" style="padding:16px">
          <div style="display:flex;gap:16px;margin-bottom:16px;flex-wrap:wrap">
            <div style="background:var(--success-bg);padding:12px 20px;border-radius:8px;text-align:center"><b style="font-size:24px;color:var(--success)">${d.routes_created}</b><br><span style="font-size:11px;color:var(--success);font-weight:600">ROTAS CRIADAS</span></div>
            <div style="background:var(--info-bg);padding:12px 20px;border-radius:8px;text-align:center"><b style="font-size:24px;color:var(--info)">${d.total_stops}</b><br><span style="font-size:11px;color:var(--info);font-weight:600">PARADAS</span></div>
            <div style="background:${d.unassigned_orders.length?'var(--danger-bg)':'var(--success-bg)'};padding:12px 20px;border-radius:8px;text-align:center"><b style="font-size:24px;color:${d.unassigned_orders.length?'var(--danger)':'var(--success)'}">${d.unassigned_orders.length}</b><br><span style="font-size:11px;font-weight:600;color:${d.unassigned_orders.length?'var(--danger)':'var(--success)'}">NÃO ALOCADOS</span></div>
          </div>
          ${d.routes.map(r=>`
            <div style="background:var(--bg);border-radius:8px;padding:16px;margin-bottom:12px;border:1px solid var(--border)">
              <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
                <span style="background:var(--primary);color:#fff;padding:4px 12px;border-radius:6px;font-family:'DM Mono',monospace;font-size:13px;font-weight:600">${r.vehicle_plate}</span>
                <span style="font-size:13px;color:var(--text2)">${r.total_stops} paradas · ${r.total_distance_km} km · ${r.planned_start} → ${r.planned_end}</span>
                <button class="btn btn-secondary btn-sm" style="margin-left:auto" onclick="verDetalhesRota('${r.route_id||''}')">Ver Detalhes</button>
              </div>
              <table style="width:100%;font-size:12px">
                <thead><tr><th style="padding:6px 8px;text-align:left;color:var(--muted);font-size:10px">Seq</th><th style="padding:6px 8px;text-align:left;color:var(--muted);font-size:10px">ETA</th><th style="padding:6px 8px;text-align:left;color:var(--muted);font-size:10px">Cliente</th><th style="padding:6px 8px;text-align:left;color:var(--muted);font-size:10px">Endereço</th></tr></thead>
                <tbody>${r.stops.map(s=>`<tr><td style="padding:5px 8px;font-family:'DM Mono',monospace;color:var(--muted)">${s.sequence+1}</td><td style="padding:5px 8px;font-family:'DM Mono',monospace;color:var(--secondary)">${s.eta}</td><td style="padding:5px 8px"><b>${s.recipient_name}</b></td><td style="padding:5px 8px;color:var(--text2)">${s.address}</td></tr>`).join('')}</tbody>
              </table>
            </div>`).join('')}
          ${d.unassigned_orders.length?`<div class="alert warn"><span>⚠️</span><div><b>${d.unassigned_orders.length} pedido(s) não alocado(s)</b> — verifique capacidade dos veículos e janelas de entrega.</div></div>`:''}
        </div>
      </div>`;
    toast(`${d.routes_created} rotas criadas!`); loadRoutes();
  } catch(e) { result.innerHTML = `<div class="alert danger">❌ ${e.message}</div>`; toast(e.message,'error'); }
  btn.disabled = false; btn.textContent = '⚡ Executar Roteirização Automática';
}"""

new_func = """async function optimizeRoutes() {
  const btn = document.getElementById('btn-optimize');
  const result = document.getElementById('optimize-result');
  btn.disabled = true; btn.textContent = '⏳ Roteirizando...';
  result.innerHTML = `<div class="alert info" style="margin-top:16px">⏳ Motor V2 calculando rotas — Agrupamento Tipo 4 + Sequenciamento Tipo K. Aguarde...</div>`;
  try {
    const d = await api('POST', '/routes/optimize', {
      route_date: document.getElementById('opt-date').value,
      time_limit_sec: +document.getElementById('opt-time').value||30,
      reoptimize: document.getElementById('opt-reoptimize').checked,
    });

    // Calcula distância total
    const totalKm = d.routes.reduce((s,r) => s + (r.total_distance_km||0), 0).toFixed(1);
    const avgScore = d.routes.length ? (d.routes.reduce((s,r) => s + (r.score||0), 0) / d.routes.length).toFixed(1) : 0;

    // Cores por cluster/rota
    const routeColors = ['#e8521a','#2563eb','#16a34a','#d97706','#7c3aed','#db2777','#0891b2','#65a30d'];

    result.innerHTML = `
      <div class="card" style="margin-top:16px">
        <div class="card-header" style="background:#f0fdf4">
          <span class="card-title" style="color:#16a34a">✅ Roteirização V2 Concluída</span>
          <span style="font-size:12px;color:var(--muted)">Status: <b>${d.status}</b> · Tempo: ${(d.wall_time_ms/1000).toFixed(1)}s</span>
        </div>
        <div class="card-body" style="padding:16px">

          <!-- KPIs da Roteirização -->
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-bottom:20px">
            <div style="background:#f0fdf4;padding:14px;border-radius:8px;text-align:center;border:1px solid #bbf7d0">
              <div style="font-size:28px;font-weight:700;color:#16a34a">${d.routes_created}</div>
              <div style="font-size:11px;font-weight:600;color:#16a34a">ROTAS CRIADAS</div>
            </div>
            <div style="background:#eff6ff;padding:14px;border-radius:8px;text-align:center;border:1px solid #bfdbfe">
              <div style="font-size:28px;font-weight:700;color:#2563eb">${d.total_stops}</div>
              <div style="font-size:11px;font-weight:600;color:#2563eb">PARADAS</div>
            </div>
            <div style="background:#fff7ed;padding:14px;border-radius:8px;text-align:center;border:1px solid #fed7aa">
              <div style="font-size:28px;font-weight:700;color:#d97706">${totalKm} km</div>
              <div style="font-size:11px;font-weight:600;color:#d97706">DISTÂNCIA TOTAL</div>
            </div>
            <div style="background:#fef9c3;padding:14px;border-radius:8px;text-align:center;border:1px solid #fef08a">
              <div style="font-size:28px;font-weight:700;color:#ca8a04">${avgScore}/10</div>
              <div style="font-size:11px;font-weight:600;color:#ca8a04">SCORE MÉDIO</div>
            </div>
            <div style="background:${d.unassigned_orders.length?'#fef2f2':'#f0fdf4'};padding:14px;border-radius:8px;text-align:center;border:1px solid ${d.unassigned_orders.length?'#fecaca':'#bbf7d0'}">
              <div style="font-size:28px;font-weight:700;color:${d.unassigned_orders.length?'#dc2626':'#16a34a'}">${d.unassigned_orders.length}</div>
              <div style="font-size:11px;font-weight:600;color:${d.unassigned_orders.length?'#dc2626':'#16a34a'}">NÃO ALOCADOS</div>
            </div>
          </div>

          <!-- Info do algoritmo -->
          <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:12px;margin-bottom:16px;display:flex;gap:20px;flex-wrap:wrap;font-size:12px">
            <span>🕐 <b>Saída:</b> 07:30</span>
            <span>📍 <b>Depósito:</b> Início e fim obrigatório</span>
            <span>🗂️ <b>Agrupamento:</b> Tipo 4 (K-Means geográfico)</span>
            <span>🔀 <b>Sequência:</b> Tipo K (Nearest Neighbor + 2-opt)</span>
          </div>

          <!-- Rotas -->
          ${d.routes.map((r, idx) => {
            const color = routeColors[idx % routeColors.length];
            const scoreColor = r.score >= 8 ? '#16a34a' : r.score >= 6 ? '#d97706' : '#dc2626';
            const scoreBg = r.score >= 8 ? '#f0fdf4' : r.score >= 6 ? '#fffbeb' : '#fef2f2';
            return `
            <div style="border:2px solid ${color}20;border-radius:10px;margin-bottom:16px;overflow:hidden">
              <!-- Header da rota -->
              <div style="background:${color}10;padding:12px 16px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;border-bottom:1px solid ${color}20">
                <span style="background:${color};color:#fff;padding:4px 14px;border-radius:6px;font-family:monospace;font-size:13px;font-weight:700">${r.vehicle_plate}</span>
                <div style="display:flex;gap:8px;flex-wrap:wrap;font-size:12px">
                  <span style="background:#fff;padding:3px 10px;border-radius:4px;border:1px solid ${color}30">🕐 Saída: <b>07:30</b></span>
                  <span style="background:#fff;padding:3px 10px;border-radius:4px;border:1px solid ${color}30">🏁 Chegada: <b>${r.planned_end}</b></span>
                  <span style="background:#fff;padding:3px 10px;border-radius:4px;border:1px solid ${color}30">📍 <b>${r.total_stops}</b> paradas</span>
                  <span style="background:#fff;padding:3px 10px;border-radius:4px;border:1px solid ${color}30">🛣️ <b>${r.total_distance_km}</b> km</span>
                  <span style="background:${scoreBg};padding:3px 10px;border-radius:4px;border:1px solid ${scoreColor}30;color:${scoreColor}">⭐ Score: <b>${r.score||'—'}/10</b></span>
                </div>
                <button class="btn btn-secondary btn-sm" style="margin-left:auto" onclick="verDetalhesRota('${r.route_id||''}')">Ver Detalhes</button>
              </div>
              <!-- Paradas -->
              <table style="width:100%;font-size:12px">
                <thead><tr style="background:#f8fafc">
                  <th style="padding:8px 12px;text-align:left;color:var(--muted);font-size:10px;font-weight:600">SEQ</th>
                  <th style="padding:8px 12px;text-align:left;color:var(--muted);font-size:10px;font-weight:600">ETA</th>
                  <th style="padding:8px 12px;text-align:left;color:var(--muted);font-size:10px;font-weight:600">CLIENTE</th>
                  <th style="padding:8px 12px;text-align:left;color:var(--muted);font-size:10px;font-weight:600">ENDEREÇO</th>
                  <th style="padding:8px 12px;text-align:left;color:var(--muted);font-size:10px;font-weight:600">PESO</th>
                </tr></thead>
                <tbody>${r.stops.map((s,si) => `
                  <tr style="${si%2===0?'background:#fff':'background:#fafafa'}">
                    <td style="padding:8px 12px"><span style="background:${color};color:#fff;width:22px;height:22px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:700">${s.sequence+1}</span></td>
                    <td style="padding:8px 12px;font-family:monospace;color:#2563eb;font-weight:600">${s.eta}</td>
                    <td style="padding:8px 12px"><b>${s.recipient_name}</b></td>
                    <td style="padding:8px 12px;color:var(--text2);font-size:11px">${s.address}</td>
                    <td style="padding:8px 12px;font-size:11px;color:var(--muted)">${s.weight_kg||0} kg</td>
                  </tr>`).join('')}
                </tbody>
              </table>
            </div>`;
          }).join('')}

          ${d.unassigned_orders.length ? `
          <div class="alert warn">
            <span>⚠️</span>
            <div><b>${d.unassigned_orders.length} pedido(s) não alocado(s)</b> — verifique capacidade dos veículos e janelas de entrega.<br>
            <span style="font-size:11px">IDs: ${d.unassigned_orders.slice(0,5).join(', ')}${d.unassigned_orders.length>5?'...':''}</span></div>
          </div>` : '<div class="alert" style="background:#f0fdf4;border:1px solid #bbf7d0;color:#16a34a">✅ Todos os pedidos foram alocados com sucesso!</div>'}
        </div>
      </div>`;

    toast(`✅ ${d.routes_created} rotas criadas — Score médio: ${avgScore}/10`);
    loadRoutes();
  } catch(e) {
    result.innerHTML = `<div class="alert danger" style="margin-top:16px">❌ ${e.message}</div>`;
    toast(e.message, 'error');
  }
  btn.disabled = false;
  btn.textContent = '⚡ Executar Roteirização Automática';
}"""

if "async function optimizeRoutes()" in content:
    content = content.replace(old_func, new_func)
    print("✅ Função optimizeRoutes atualizada!")
else:
    print("⚠️  Função não encontrada exatamente — verifique o arquivo")

# Salva
with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("🎉 gelocrim_v1.html atualizado!")
print("Recarregue o navegador com Ctrl+Shift+R")
