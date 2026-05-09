path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Substitui linhas 841-887 (índices 840-886)
novo_painel = '''        <div style="border-left:1px solid #1e3a5c;overflow-y:auto;padding:14px;background:#061828">
          <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:14px">INDICADORES DA CARGA</div>

          <!-- Cronograma -->
          <div style="margin-bottom:12px">
            <div style="font-size:10px;color:#64B4FF;font-weight:700;margin-bottom:8px">📅 CRONOGRAMA</div>
            <div style="display:grid;gap:6px">
              <div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:11px;color:#90afd4">Data saída</span><input type="date" id="conf-data-saida" style="padding:4px 8px;border:1px solid #1e3a5c;border-radius:4px;font-size:11px;background:#0a1628;color:#e8f0fe;width:130px"></div>
              <div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:11px;color:#90afd4">Hora início</span><input type="time" id="conf-hora-inicio" value="07:30" style="padding:4px 8px;border:1px solid #1e3a5c;border-radius:4px;font-size:11px;background:#0a1628;color:#e8f0fe;width:90px"></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Previsão fim</span><span id="conf-hora-fim" style="font-size:11px;color:#64B4FF;font-weight:600">—</span></div>
            </div>
          </div>

          <!-- Logística com barras de capacidade -->
          <div style="border-top:1px solid #1e3a5c;padding-top:12px;margin-bottom:12px">
            <div style="font-size:10px;color:#64B4FF;font-weight:700;margin-bottom:8px">🚛 LOGÍSTICA</div>
            <div style="display:grid;gap:4px;margin-bottom:10px">
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Veículo</span><span id="conf-veiculo" style="font-size:11px;color:#e8f0fe;font-weight:600">—</span></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Motorista</span><span id="conf-motorista" style="font-size:11px;color:#e8f0fe">—</span></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Entregas</span><span id="conf-entregas" style="font-size:11px;color:#64B4FF;font-weight:600">—</span></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Distância</span><span id="conf-distancia" style="font-size:11px;color:#64B4FF">—</span></div>
              <span id="conf-capacidade" style="display:none"></span>
            </div>
            <!-- Barras de capacidade -->
            <div style="display:grid;gap:8px">
              <div>
                <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:3px">
                  <span style="color:#90afd4">⚖️ Peso</span><span id="conf-peso" style="color:#f59e0b;font-weight:600">—</span>
                </div>
                <div style="background:#1e3a5c;border-radius:3px;height:6px"><div id="conf-bar-peso" style="height:100%;background:#f59e0b;border-radius:3px;width:0%;transition:width .3s"></div></div>
              </div>
              <div>
                <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:3px">
                  <span style="color:#90afd4">📦 Volume</span><span id="conf-volume" style="color:#2dd4bf;font-weight:600">—</span>
                </div>
                <div style="background:#1e3a5c;border-radius:3px;height:6px"><div id="conf-bar-vol" style="height:100%;background:#2dd4bf;border-radius:3px;width:0%;transition:width .3s"></div></div>
              </div>
              <div>
                <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:3px">
                  <span style="color:#90afd4">🪵 Pallets</span><span id="conf-pallets" style="color:#a78bfa;font-weight:600">—</span>
                </div>
                <div style="background:#1e3a5c;border-radius:3px;height:6px"><div id="conf-bar-pallets" style="height:100%;background:#a78bfa;border-radius:3px;width:0%;transition:width .3s"></div></div>
              </div>
            </div>
          </div>

          <!-- Mix de carga por TOP com barras -->
          <div style="border-top:1px solid #1e3a5c;padding-top:12px;margin-bottom:12px">
            <div style="font-size:10px;color:#64B4FF;font-weight:700;margin-bottom:8px">💰 MIX DE CARGA POR TOP</div>
            <div style="display:grid;gap:6px">
              <div>
                <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:2px"><span style="color:#90afd4">1000 Vendas</span><span id="conf-top1000" style="color:#10b981">—</span></div>
                <div style="background:#1e3a5c;border-radius:3px;height:4px"><div id="conf-bar-top1000" style="height:100%;background:#10b981;border-radius:3px;width:0%"></div></div>
              </div>
              <div>
                <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:2px"><span style="color:#90afd4">1009 Trocas</span><span id="conf-top1009" style="color:#64B4FF">—</span></div>
                <div style="background:#1e3a5c;border-radius:3px;height:4px"><div id="conf-bar-top1009" style="height:100%;background:#64B4FF;border-radius:3px;width:0%"></div></div>
              </div>
              <div>
                <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:2px"><span style="color:#90afd4">1007 Bonif.</span><span id="conf-top1007" style="color:#a78bfa">—</span></div>
                <div style="background:#1e3a5c;border-radius:3px;height:4px"><div id="conf-bar-top1007" style="height:100%;background:#a78bfa;border-radius:3px;width:0%"></div></div>
              </div>
              <div>
                <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:2px"><span style="color:#90afd4">1010 Pré-ped.</span><span id="conf-top1010" style="color:#f59e0b">—</span></div>
                <div style="background:#1e3a5c;border-radius:3px;height:4px"><div id="conf-bar-top1010" style="height:100%;background:#f59e0b;border-radius:3px;width:0%"></div></div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:10px"><span style="color:#90afd4">1008 Consig.</span><span id="conf-top1008" style="color:#90afd4">—</span></div>
              <div style="display:flex;justify-content:space-between;border-top:1px solid #1e3a5c;padding-top:5px;margin-top:2px">
                <span style="font-size:11px;color:#e8f0fe;font-weight:700">Total</span>
                <span id="conf-total-pedidos" style="font-size:14px;color:#10b981;font-weight:800">—</span>
              </div>
            </div>
          </div>

          <!-- Margem operacional -->
          <div style="border-top:1px solid #1e3a5c;padding-top:12px">
            <div style="font-size:10px;color:#64B4FF;font-weight:700;margin-bottom:8px">📊 MARGEM OPERACIONAL</div>
            <div style="display:grid;gap:4px;margin-bottom:12px">
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Custo equipe</span><span id="conf-custo-equipe" style="font-size:11px;color:#f87171">—</span></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Combustível</span><span id="conf-custo-diesel" style="font-size:11px;color:#f87171">—</span></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Manutenção/IPVA</span><span id="conf-custo-manut" style="font-size:11px;color:#f87171">—</span></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#e8f0fe;font-weight:600">Total custos</span><span id="conf-custo-total" style="font-size:12px;color:#f87171;font-weight:700">—</span></div>
            </div>
            <div id="conf-semaforo" style="padding:14px;border-radius:10px;text-align:center;background:#1e3a5c;border:1px solid #2563a8">
              <div style="font-size:32px" id="conf-semaforo-emoji">⏳</div>
              <div style="font-size:24px;font-weight:800;margin:4px 0;color:#e8f0fe" id="conf-margem-valor">—</div>
              <div style="font-size:11px;color:#90afd4" id="conf-margem-label">Margem Operacional</div>
            </div>
            <!-- Alerta margem negativa -->
            <div id="conf-alerta-margem" style="display:none;margin-top:8px;padding:10px;background:rgba(248,113,113,.15);border:1px solid #f87171;border-radius:8px">
              <div style="font-size:11px;color:#f87171;font-weight:700;margin-bottom:6px">⚠️ Margem Negativa — Justificativa Obrigatória</div>
              <textarea id="conf-justificativa" rows="2" placeholder="Informe o motivo para gravar com margem negativa..." style="width:100%;background:#0a1628;border:1px solid #f87171;border-radius:4px;color:#e8f0fe;font-size:11px;padding:6px;resize:none"></textarea>
            </div>
            <!-- Romaneio -->
            <button onclick="gerarRomaneio()" style="margin-top:10px;width:100%;padding:8px;background:transparent;border:1px solid #1e3a5c;color:#90afd4;border-radius:6px;font-size:11px;cursor:pointer">
              🖨️ Gerar Romaneio PDF
            </button>
          </div>
        </div>
'''

# Substitui linhas 841-887 (índice 840 a 886 inclusive)
lines[840:887] = [novo_painel]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Painel direito substituído com sucesso!')
print('Faca Ctrl+Shift+R.')
