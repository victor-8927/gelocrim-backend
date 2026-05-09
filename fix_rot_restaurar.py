path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

idx_start = content.find('    <!-- ══ ROTEIRIZAÇÃO ══ -->')
idx_end   = content.find('<div class="page" id="page-rotas">')

print(f'start={idx_start}, end={idx_end}')

if idx_start != -1 and idx_end != -1:
    new_rot = '''    <!-- ══ ROTEIRIZAÇÃO ══ -->
    <div class="page" id="page-roteirizacao">
  <div class="page-header" style="margin-bottom:12px">
    <div>
      <div class="page-title">&#x26A1; Roteirização Visual</div>
      <div class="page-sub">Selecione clientes no mapa, escolha o veículo e roteirize</div>
    </div>
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
      <input type="date" id="opt-date" style="padding:8px 12px;border:1px solid var(--border);border-radius:6px;font-size:13px;background:#0a1628;color:#e8f0fe">
      <button class="btn btn-secondary" onclick="loadRotMapData()">&#8635; Atualizar</button>
    </div>
  </div>

  <div style="display:flex;gap:12px;height:calc(100vh - 200px);min-height:500px">

    <!-- SIDEBAR -->
    <div style="width:320px;flex-shrink:0;display:flex;flex-direction:column;gap:8px">

      <div class="card" style="flex-shrink:0">
        <div class="card-body" style="padding:12px">
          <div style="font-weight:700;font-size:11px;color:#64B4FF;margin-bottom:8px">PASSO 1 — SELECIONE CLIENTES NO MAPA</div>
          <div style="display:flex;gap:6px">
            <button id="btn-modo-click" onclick="setModoSelecao('click')"
              style="flex:1;padding:8px;border:2px solid #e8521a;background:rgba(232,82,26,.15);color:#e8521a;border-radius:6px;font-size:11px;font-weight:700;cursor:pointer">
              &#x1F4CC; Individual
            </button>
            <button id="btn-modo-area" onclick="setModoSelecao('area')"
              style="flex:1;padding:8px;border:2px solid #1e3a5c;background:transparent;color:#90afd4;border-radius:6px;font-size:11px;font-weight:700;cursor:pointer">
              &#x270F;&#xFE0F; Desenhar Área
            </button>
          </div>
          <div id="dica-modo" style="font-size:10px;color:#90afd4;margin-top:6px;text-align:center">
            Clique nos pins laranjos para selecionar clientes
          </div>
        </div>
      </div>

      <div class="card" style="flex-shrink:0">
        <div class="card-body" style="padding:12px">
          <div style="font-weight:700;font-size:11px;color:#64B4FF;margin-bottom:8px">CARGA SELECIONADA</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px">
            <div style="background:#0a1628;border:1px solid #1e3a5c;padding:8px;border-radius:6px;text-align:center">
              <div id="rot-total-peso" style="font-size:18px;font-weight:700;color:#f59e0b">0 kg</div>
              <div style="font-size:10px;color:#90afd4">PESO TOTAL</div>
            </div>
            <div style="background:#0a1628;border:1px solid #1e3a5c;padding:8px;border-radius:6px;text-align:center">
              <div id="rot-total-vol" style="font-size:18px;font-weight:700;color:#2dd4bf">0 m3</div>
              <div style="font-size:10px;color:#90afd4">VOLUME TOTAL</div>
            </div>
          </div>
          <div style="font-size:11px;color:#90afd4;text-align:center">
            <span id="rot-count">0</span> cliente(s) selecionado(s)
          </div>
        </div>
      </div>

      <div id="card-sel-veiculo" class="card" style="flex-shrink:0;display:none">
        <div class="card-body" style="padding:12px">
          <div style="font-weight:700;font-size:11px;color:#64B4FF;margin-bottom:8px">PASSO 2 — VEÍCULO E EQUIPE</div>
          <select id="rot-veiculo-select" onchange="rotVeiculoChanged()"
            style="width:100%;padding:8px;border:1px solid #1e3a5c;border-radius:6px;font-size:12px;background:#0a1628;color:#e8f0fe">
            <option value="">-- Selecione o veículo --</option>
          </select>
          <div style="margin-top:10px;padding-top:10px;border-top:1px solid #1e3a5c">
            <div style="font-weight:700;font-size:11px;color:#64B4FF;margin-bottom:8px">EQUIPE DA ROTA</div>
            <div style="margin-bottom:6px">
              <div style="font-size:11px;color:#90afd4;margin-bottom:4px">&#x1F468;&#x200D;&#x1F4BC; Motorista</div>
              <select id="sel-motorista" style="width:100%;padding:8px;border:1px solid #1e3a5c;border-radius:6px;font-size:12px;background:#0a1628;color:#e8f0fe">
                <option value="">-- Selecione --</option>
              </select>
            </div>
            <div style="margin-bottom:6px">
              <div style="font-size:11px;color:#90afd4;margin-bottom:4px">&#x1F477; Ajudante 1</div>
              <select id="sel-ajudante1" style="width:100%;padding:8px;border:1px solid #1e3a5c;border-radius:6px;font-size:12px;background:#0a1628;color:#e8f0fe">
                <option value="">-- Nenhum --</option>
              </select>
            </div>
            <div>
              <div style="font-size:11px;color:#90afd4;margin-bottom:4px">&#x1F477; Ajudante 2</div>
              <select id="sel-ajudante2" style="width:100%;padding:8px;border:1px solid #1e3a5c;border-radius:6px;font-size:12px;background:#0a1628;color:#e8f0fe">
                <option value="">-- Nenhum --</option>
              </select>
            </div>
          </div>
          <div id="rot-cap-info" style="margin-top:8px;display:none">
            <div style="margin-bottom:6px">
              <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px">
                <span style="color:#90afd4">&#x2696;&#xFE0F; Peso</span><span id="rot-peso-txt" style="font-weight:600;color:#e8f0fe">0 kg</span>
              </div>
              <div style="background:#1e3a5c;border-radius:4px;height:8px;overflow:hidden">
                <div id="rot-barra-peso" style="height:100%;background:#e8521a;border-radius:4px;transition:width .3s;width:0%"></div>
              </div>
            </div>
            <div>
              <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px">
                <span style="color:#90afd4">&#x1F4E6; Volume</span><span id="rot-vol-txt" style="font-weight:600;color:#e8f0fe">0 m3</span>
              </div>
              <div style="background:#1e3a5c;border-radius:4px;height:8px;overflow:hidden">
                <div id="rot-barra-vol" style="height:100%;background:#2563eb;border-radius:4px;transition:width .3s;width:0%"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card" style="flex:1;overflow:hidden;display:flex;flex-direction:column">
        <div class="card-header" style="flex-shrink:0;padding:10px 12px">
          <span class="card-title" style="font-size:11px;color:#64B4FF">CLIENTES SELECIONADOS</span>
          <button onclick="rotLimparTudo()" style="font-size:10px;color:#f87171;background:none;border:none;cursor:pointer">Limpar</button>
        </div>
        <div id="rot-lista-sel" style="flex:1;overflow-y:auto;padding:8px">
          <div style="color:#90afd4;font-size:12px;text-align:center;padding:20px">
            Clique nos pins laranjos no mapa para selecionar clientes.
          </div>
        </div>
      </div>

      <button id="btn-rot-map" onclick="abrirConferenciaMaster()" disabled
        style="padding:14px;background:#e8521a;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:700;cursor:pointer;opacity:0.5">
        &#x26A1; Roteirizar &#x2014; Conferência Master
      </button>
    </div>

    <!-- MAPA -->
    <div style="flex:1;display:flex;flex-direction:column;gap:8px">
      <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;font-size:12px;background:#0f2040;border:1px solid #1e3a5c;border-radius:8px;padding:8px 12px">
        <span style="display:flex;align-items:center;gap:4px"><span style="width:10px;height:10px;background:#e8521a;border-radius:50%;display:inline-block"></span><span style="color:#90afd4">Pendente</span></span>
        <span style="display:flex;align-items:center;gap:4px"><span style="width:10px;height:10px;background:#10b981;border-radius:50%;display:inline-block"></span><span style="color:#90afd4">Selecionado</span></span>
        <span style="display:flex;align-items:center;gap:4px"><span style="width:10px;height:10px;background:#2563eb;border-radius:50%;display:inline-block"></span><span style="color:#90afd4">Roteirizado</span></span>
        <span id="rot-map-status" style="margin-left:auto;color:#90afd4;font-size:11px">Clique em Atualizar</span>
      </div>
      <div id="rot-map" style="flex:1;border-radius:10px;overflow:hidden;border:1px solid #1e3a5c;min-height:400px"></div>
    </div>
  </div>

  <div id="optimize-result" style="margin-top:16px"></div>

  <!-- SUBTELA CONFERÊNCIA MASTER -->
  <div id="painel-conferencia" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:3000;align-items:stretch">
    <div style="background:#0a1628;width:100%;display:flex;flex-direction:column;height:100vh;overflow:hidden">
      <div style="background:#061020;border-bottom:2px solid #1e3a5c;padding:14px 20px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0">
        <div>
          <div style="font-size:18px;font-weight:800;color:#e8f0fe">&#x1F4CB; Conferência Master &#x2014; Validação da Carga</div>
          <div style="font-size:12px;color:#90afd4;margin-top:2px" id="conf-subtitulo">Revise todos os dados antes de gravar</div>
        </div>
        <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
          <select id="conf-modelo" style="padding:7px 10px;border:1px solid #1e3a5c;border-radius:6px;font-size:11px;background:#0a1628;color:#e8f0fe">
            <option value="padrao">&#x1F4CD; Padrão</option>
            <option value="cidade">&#x1F3D9;&#xFE0F; Cidade</option>
            <option value="praca">&#x1F3EA; Praça</option>
            <option value="bairro">&#x1F3D8;&#xFE0F; Bairro</option>
            <option value="analista">&#x1F4BB; Opção Analista</option>
          </select>
          <select id="conf-sequencia" style="padding:7px 10px;border:1px solid #1e3a5c;border-radius:6px;font-size:11px;background:#0a1628;color:#e8f0fe">
            <option value="otimizado">Otimizado</option>
            <option value="proximidade">Proximidade</option>
            <option value="distancia">Menor Distância</option>
            <option value="agrupamento">Agrupamento</option>
          </select>
          <button onclick="inverterOrdemConf()" style="padding:7px 12px;background:#1e3a5c;border:none;color:#64B4FF;border-radius:6px;font-size:11px;cursor:pointer">&#x2195;&#xFE0F; Inverter</button>
          <button onclick="fecharConferencia()" style="padding:7px 14px;background:transparent;border:1px solid #1e3a5c;color:#90afd4;border-radius:6px;font-size:11px;cursor:pointer">&#x2715; Fechar</button>
          <button onclick="gravarCarga()" style="padding:7px 20px;background:#10b981;border:none;color:#fff;border-radius:6px;font-size:14px;font-weight:700;cursor:pointer">&#x1F4BE; GRAVAR CARGA</button>
        </div>
      </div>
      <div style="flex:1;display:grid;grid-template-columns:260px 1fr 280px;overflow:hidden">
        <div style="border-right:1px solid #1e3a5c;display:flex;flex-direction:column;overflow:hidden;background:#061828">
          <div style="padding:12px;border-bottom:1px solid #1e3a5c;flex-shrink:0">
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px">SEQUÊNCIA DE ENTREGAS</div>
            <div style="font-size:10px;color:#90afd4;margin-top:2px">Arraste para reordenar</div>
          </div>
          <div id="conf-lista-clientes" style="flex:1;overflow-y:auto;padding:8px"></div>
          <div style="padding:8px;border-top:1px solid #1e3a5c;flex-shrink:0">
            <button onclick="reprocessarSequencia()" style="width:100%;padding:8px;background:#1e3a5c;border:none;color:#64B4FF;border-radius:6px;font-size:11px;cursor:pointer;font-weight:600">&#x1F504; Reprocessar Sequência</button>
          </div>
        </div>
        <div style="display:flex;flex-direction:column;overflow:hidden">
          <div style="padding:8px 14px;border-bottom:1px solid #1e3a5c;flex-shrink:0;background:#061828">
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px">MAPA DE VERIFICAÇÃO — verifique cruzamentos e bate-volta</div>
          </div>
          <div id="conf-mapa" style="flex:1;min-height:300px"></div>
        </div>
        <div style="border-left:1px solid #1e3a5c;overflow-y:auto;padding:14px;background:#061828">
          <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:14px">INDICADORES DA CARGA</div>
          <div style="margin-bottom:12px">
            <div style="font-size:10px;color:#64B4FF;font-weight:700;margin-bottom:8px">&#x1F4C5; CRONOGRAMA</div>
            <div style="display:grid;gap:6px">
              <div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:11px;color:#90afd4">Data saída</span><input type="date" id="conf-data-saida" style="padding:4px 8px;border:1px solid #1e3a5c;border-radius:4px;font-size:11px;background:#0a1628;color:#e8f0fe;width:130px"></div>
              <div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:11px;color:#90afd4">Hora início</span><input type="time" id="conf-hora-inicio" value="07:30" style="padding:4px 8px;border:1px solid #1e3a5c;border-radius:4px;font-size:11px;background:#0a1628;color:#e8f0fe;width:90px"></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Previsão fim</span><span id="conf-hora-fim" style="font-size:11px;color:#64B4FF;font-weight:600">—</span></div>
            </div>
          </div>
          <div style="border-top:1px solid #1e3a5c;padding-top:12px;margin-bottom:12px">
            <div style="font-size:10px;color:#64B4FF;font-weight:700;margin-bottom:8px">&#x1F69B; LOGÍSTICA</div>
            <div style="display:grid;gap:4px">
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Veículo</span><span id="conf-veiculo" style="font-size:11px;color:#e8f0fe;font-weight:600">—</span></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Motorista</span><span id="conf-motorista" style="font-size:11px;color:#e8f0fe">—</span></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Capacidade</span><span id="conf-capacidade" style="font-size:11px;color:#e8f0fe">—</span></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Peso carga</span><span id="conf-peso" style="font-size:11px;color:#f59e0b;font-weight:600">—</span></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Entregas</span><span id="conf-entregas" style="font-size:11px;color:#64B4FF;font-weight:600">—</span></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Distância est.</span><span id="conf-distancia" style="font-size:11px;color:#64B4FF">—</span></div>
            </div>
          </div>
          <div style="border-top:1px solid #1e3a5c;padding-top:12px;margin-bottom:12px">
            <div style="font-size:10px;color:#64B4FF;font-weight:700;margin-bottom:8px">&#x1F4B0; POR TOP (SANKHYA)</div>
            <div style="display:grid;gap:4px">
              <div style="display:flex;justify-content:space-between"><span style="font-size:10px;color:#90afd4">1000 Vendas</span><span id="conf-top1000" style="font-size:11px;color:#10b981">—</span></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:10px;color:#90afd4">1009 Trocas</span><span id="conf-top1009" style="font-size:11px;color:#64B4FF">—</span></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:10px;color:#90afd4">1007 Bonif.</span><span id="conf-top1007" style="font-size:11px;color:#a78bfa">—</span></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:10px;color:#90afd4">1010 Pré-ped.</span><span id="conf-top1010" style="font-size:11px;color:#f59e0b">—</span></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:10px;color:#90afd4">1008 Consig.</span><span id="conf-top1008" style="font-size:11px;color:#90afd4">—</span></div>
              <div style="display:flex;justify-content:space-between;border-top:1px solid #1e3a5c;padding-top:5px;margin-top:4px"><span style="font-size:11px;color:#e8f0fe;font-weight:700">Total</span><span id="conf-total-pedidos" style="font-size:14px;color:#10b981;font-weight:800">—</span></div>
            </div>
          </div>
          <div style="border-top:1px solid #1e3a5c;padding-top:12px">
            <div style="font-size:10px;color:#64B4FF;font-weight:700;margin-bottom:8px">&#x1F4CA; MARGEM OPERACIONAL</div>
            <div style="display:grid;gap:4px;margin-bottom:12px">
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Custo equipe</span><span id="conf-custo-equipe" style="font-size:11px;color:#f87171">—</span></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Combustível</span><span id="conf-custo-diesel" style="font-size:11px;color:#f87171">—</span></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Manutenção/IPVA</span><span id="conf-custo-manut" style="font-size:11px;color:#f87171">—</span></div>
              <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#e8f0fe;font-weight:600">Total custos</span><span id="conf-custo-total" style="font-size:12px;color:#f87171;font-weight:700">—</span></div>
            </div>
            <div id="conf-semaforo" style="padding:14px;border-radius:10px;text-align:center;background:#1e3a5c;border:1px solid #2563a8">
              <div style="font-size:32px" id="conf-semaforo-emoji">&#x23F3;</div>
              <div style="font-size:24px;font-weight:800;margin:4px 0;color:#e8f0fe" id="conf-margem-valor">—</div>
              <div style="font-size:11px;color:#90afd4" id="conf-margem-label">Margem Operacional</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</div>

    '''

    content = content[:idx_start] + new_rot + content[idx_end:]
    print('Roteirização atualizada com subtela de conferência!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Faca Ctrl+Shift+R!')
