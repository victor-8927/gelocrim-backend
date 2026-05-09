path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('<div class="page" id="page-roteirizacao">')
end   = content.find('<div class="page" id="page-rotas">')

if start == -1 or end == -1:
    print(f'Secao nao encontrada!')
    exit(1)

new_section = '''<div class="page" id="page-roteirizacao">
  <div class="page-header" style="margin-bottom:12px">
    <div>
      <div class="page-title">&#x26A1; Roteirizacao Visual</div>
      <div class="page-sub">Selecione clientes no mapa, escolha o veiculo e roteirize</div>
    </div>
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
      <input type="date" id="opt-date" style="padding:8px 12px;border:1px solid var(--border);border-radius:6px;font-size:13px">
      <button class="btn btn-secondary" onclick="loadRotMapData()">&#8635; Atualizar</button>
    </div>
  </div>

  <div style="display:flex;gap:12px;height:calc(100vh - 200px);min-height:500px">

    <!-- SIDEBAR ESQUERDA -->
    <div style="width:320px;flex-shrink:0;display:flex;flex-direction:column;gap:8px">

      <!-- PASSO 1: Modo de selecao -->
      <div class="card" style="flex-shrink:0">
        <div class="card-body" style="padding:12px">
          <div style="font-weight:700;font-size:11px;color:var(--muted);margin-bottom:8px">PASSO 1 &mdash; SELECIONE CLIENTES NO MAPA</div>
          <div style="display:flex;gap:6px">
            <button id="btn-modo-click" onclick="setModoSelecao('click')"
              style="flex:1;padding:8px;border:2px solid #e8521a;background:#fff7ed;color:#e8521a;border-radius:6px;font-size:11px;font-weight:700;cursor:pointer">
              &#x1F4CC; Individual
            </button>
            <button id="btn-modo-area" onclick="setModoSelecao('area')"
              style="flex:1;padding:8px;border:2px solid var(--border);background:#fff;color:var(--muted);border-radius:6px;font-size:11px;font-weight:700;cursor:pointer">
              &#x270F;&#xFE0F; Desenhar Area
            </button>
          </div>
          <div id="dica-modo" style="font-size:10px;color:var(--muted);margin-top:6px;text-align:center">
            Clique nos pins laranjos para selecionar clientes
          </div>
        </div>
      </div>

      <!-- Resumo da selecao -->
      <div class="card" style="flex-shrink:0">
        <div class="card-body" style="padding:12px">
          <div style="font-weight:700;font-size:11px;color:var(--muted);margin-bottom:8px">CARGA SELECIONADA</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px">
            <div style="background:#fff7ed;padding:8px;border-radius:6px;text-align:center">
              <div id="rot-total-peso" style="font-size:18px;font-weight:700;color:#d97706">0 kg</div>
              <div style="font-size:10px;color:#d97706">PESO TOTAL</div>
            </div>
            <div style="background:#eff6ff;padding:8px;border-radius:6px;text-align:center">
              <div id="rot-total-vol" style="font-size:18px;font-weight:700;color:#2563eb">0 m3</div>
              <div style="font-size:10px;color:#2563eb">VOLUME TOTAL</div>
            </div>
          </div>
          <div style="font-size:11px;color:var(--muted);text-align:center">
            <span id="rot-count">0</span> cliente(s) selecionado(s)
          </div>
        </div>
      </div>

      <!-- PASSO 2: Selecionar veiculo -->
      <div id="card-sel-veiculo" class="card" style="flex-shrink:0;display:none">
        <div class="card-body" style="padding:12px">
          <div style="font-weight:700;font-size:11px;color:var(--muted);margin-bottom:8px">PASSO 2 &mdash; SELECIONE O VEICULO</div>
          <select id="rot-veiculo-select" onchange="rotVeiculoChanged()"
            style="width:100%;padding:8px;border:1px solid var(--border);border-radius:6px;font-size:12px">
            <option value="">-- Selecione --</option>
          </select>
          <div id="rot-cap-info" style="margin-top:8px;display:none">
            <div style="margin-bottom:6px">
              <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px">
                <span>&#x2696;&#xFE0F; Peso</span><span id="rot-peso-txt" style="font-weight:600">0 kg</span>
              </div>
              <div style="background:#e5e7eb;border-radius:4px;height:8px;overflow:hidden">
                <div id="rot-barra-peso" style="height:100%;background:#e8521a;border-radius:4px;transition:width .3s;width:0%"></div>
              </div>
            </div>
            <div>
              <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px">
                <span>&#x1F4E6; Volume</span><span id="rot-vol-txt" style="font-weight:600">0 m3</span>
              </div>
              <div style="background:#e5e7eb;border-radius:4px;height:8px;overflow:hidden">
                <div id="rot-barra-vol" style="height:100%;background:#2563eb;border-radius:4px;transition:width .3s;width:0%"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Lista de selecionados -->
      <div class="card" style="flex:1;overflow:hidden;display:flex;flex-direction:column">
        <div class="card-header" style="flex-shrink:0;padding:10px 12px">
          <span class="card-title" style="font-size:11px">CLIENTES SELECIONADOS</span>
          <button onclick="rotLimparTudo()" style="font-size:10px;color:var(--danger);background:none;border:none;cursor:pointer">Limpar</button>
        </div>
        <div id="rot-lista-sel" style="flex:1;overflow-y:auto;padding:8px">
          <div style="color:var(--muted);font-size:12px;text-align:center;padding:20px">
            Clique nos pins laranjos no mapa para selecionar clientes.
          </div>
        </div>
      </div>

      <!-- Botao roteirizar -->
      <button id="btn-rot-map" onclick="roteirizarDoMapa()" disabled
        style="padding:14px;background:#e8521a;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:700;cursor:pointer;opacity:0.5">
        &#x26A1; Roteirizar
      </button>
    </div>

    <!-- MAPA -->
    <div style="flex:1;display:flex;flex-direction:column;gap:8px">
      <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;font-size:12px">
        <span style="display:flex;align-items:center;gap:4px">
          <span style="width:12px;height:12px;background:#e8521a;border-radius:50%;display:inline-block"></span>Pendente
        </span>
        <span style="display:flex;align-items:center;gap:4px">
          <span style="width:12px;height:12px;background:#16a34a;border-radius:50%;display:inline-block"></span>Selecionado
        </span>
        <span style="display:flex;align-items:center;gap:4px">
          <span style="width:12px;height:12px;background:#2563eb;border-radius:50%;display:inline-block"></span>Roteirizado
        </span>
        <span id="rot-map-status" style="margin-left:auto;color:var(--muted);font-size:11px">Clique em Atualizar</span>
      </div>
      <div id="rot-map" style="flex:1;border-radius:10px;overflow:hidden;border:1px solid var(--border);min-height:400px"></div>
    </div>
  </div>

  <div id="optimize-result" style="margin-top:16px"></div>
</div>

'''

content = content[:start] + new_section + content[end:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('HTML atualizado!')
print('Faca Ctrl+Shift+R no navegador.')
