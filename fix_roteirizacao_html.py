path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra inicio da pagina roteirizacao
start = content.find('<div class="page" id="page-roteirizacao">')
end   = content.find('<div class="page" id="page-rotas">')

if start == -1 or end == -1:
    print(f'Nao encontrou: start={start}, end={end}')
    exit(1)

print(f'Encontrou secao: start={start}, end={end}')

new_section = '''<div class="page" id="page-roteirizacao">
  <div class="page-header">
    <div>
      <div class="page-title">Motor de Roteirizacao</div>
      <div class="page-sub">Selecione o veiculo e os pedidos para roteirizar</div>
    </div>
    <div style="display:flex;gap:8px;align-items:center">
      <input type="date" id="opt-date" style="padding:8px 12px;border:1px solid var(--border);border-radius:6px;font-size:13px">
      <button class="btn btn-secondary" onclick="loadPreSummary()">&#8635; Atualizar</button>
    </div>
  </div>

  <!-- PASSO 1: VEICULO -->
  <div class="card" style="margin-bottom:16px">
    <div class="card-header">
      <span class="card-title">&#x1F69B; Passo 1 &mdash; Selecione o Veiculo</span>
    </div>
    <div class="card-body" style="padding:16px">
      <div id="lista-veiculos-rot" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px">
        <div style="color:var(--muted);font-size:13px">Carregando veiculos...</div>
      </div>
    </div>
  </div>

  <!-- BARRA DE CAPACIDADE -->
  <div id="barra-capacidade" class="card" style="margin-bottom:16px;display:none">
    <div class="card-body" style="padding:16px">
      <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:12px">
        <span id="veiculo-selecionado-nome" style="font-weight:700;font-size:15px"></span>
        <span id="contador-pedidos-sel" style="background:var(--primary);color:#fff;padding:2px 10px;border-radius:10px;font-size:12px;font-weight:600">0 pedidos</span>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
        <div>
          <div style="display:flex;justify-content:space-between;margin-bottom:4px;font-size:12px">
            <span>Peso</span><span id="peso-usado-txt">0 / 0 kg</span>
          </div>
          <div style="background:#e5e7eb;border-radius:6px;height:12px;overflow:hidden">
            <div id="barra-peso" style="height:100%;background:#e8521a;border-radius:6px;transition:width .3s;width:0%"></div>
          </div>
        </div>
        <div>
          <div style="display:flex;justify-content:space-between;margin-bottom:4px;font-size:12px">
            <span>Volume</span><span id="vol-usado-txt">0 / 0 m3</span>
          </div>
          <div style="background:#e5e7eb;border-radius:6px;height:12px;overflow:hidden">
            <div id="barra-vol" style="height:100%;background:#2563eb;border-radius:6px;transition:width .3s;width:0%"></div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- PASSO 2: PEDIDOS -->
  <div id="card-pedidos-rot" class="card" style="margin-bottom:16px;display:none">
    <div class="card-header">
      <span class="card-title">&#x1F4E6; Passo 2 &mdash; Selecione os Pedidos</span>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <button class="btn btn-secondary btn-sm" onclick="selecionarTodosPedidos()">Selecionar Todos</button>
        <button class="btn btn-secondary btn-sm" onclick="limparSelecao()">Limpar</button>
        <input type="text" id="busca-pedidos-rot" placeholder="Buscar cliente..." onkeyup="filtrarPedidosRot()"
          style="padding:4px 10px;border:1px solid var(--border);border-radius:6px;font-size:12px;width:160px">
      </div>
    </div>
    <div class="card-body" style="padding:0;max-height:420px;overflow-y:auto">
      <table style="width:100%;border-collapse:collapse;font-size:12px">
        <thead style="position:sticky;top:0;z-index:1">
          <tr style="background:#f8fafc;border-bottom:2px solid var(--border)">
            <th style="padding:10px 12px;text-align:center;width:40px"><input type="checkbox" id="chk-todos" onchange="toggleTodos(this)"></th>
            <th style="padding:10px 12px;text-align:left">Pedido</th>
            <th style="padding:10px 12px;text-align:left">Cliente</th>
            <th style="padding:10px 12px;text-align:left">Endereco</th>
            <th style="padding:10px 12px;text-align:right">Peso(kg)</th>
            <th style="padding:10px 12px;text-align:right">Vol(m3)</th>
            <th style="padding:10px 12px;text-align:center">Janela</th>
          </tr>
        </thead>
        <tbody id="tbody-pedidos-rot"></tbody>
      </table>
    </div>
  </div>

  <!-- PASSO 3: ROTEIRIZAR -->
  <div id="card-roteirizar" style="display:none;margin-bottom:16px">
    <button id="btn-optimize" onclick="optimizeRoutes()"
      style="width:100%;padding:16px;background:#e8521a;color:#fff;border:none;border-radius:10px;font-size:16px;font-weight:700;cursor:pointer">
      &#x26A1; Roteirizar Pedidos Selecionados
    </button>
  </div>

  <div id="optimize-result"></div>
</div>

'''

content = content[:start] + new_section + content[end:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('HTML atualizado com sucesso!')
