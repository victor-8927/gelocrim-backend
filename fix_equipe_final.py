path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Insere logo apos o select de veiculo
old = '''          <select id="rot-veiculo-select" onchange="rotVeiculoChanged()"
            style="width:100%;padding:8px;border:1px solid var(--border);border-radius:6px;font-size:12px">
            <option value="">-- Selecione --</option>
          </select>
          <div id="rot-cap-info"'''

new = '''          <select id="rot-veiculo-select" onchange="rotVeiculoChanged()"
            style="width:100%;padding:8px;border:1px solid var(--border);border-radius:6px;font-size:12px">
            <option value="">-- Selecione --</option>
          </select>
          <div style="margin-top:10px;padding-top:10px;border-top:1px solid var(--border)">
            <div style="font-weight:700;font-size:11px;color:var(--muted);margin-bottom:8px">EQUIPE DA ROTA</div>
            <div style="margin-bottom:6px">
              <div style="font-size:11px;color:var(--muted);margin-bottom:4px">&#x1F468;&#x200D;&#x1F4BC; Motorista</div>
              <select id="sel-motorista" style="width:100%;padding:8px;border:1px solid var(--border);border-radius:6px;font-size:12px;background:var(--bg)">
                <option value="">-- Selecione --</option>
              </select>
            </div>
            <div style="margin-bottom:6px">
              <div style="font-size:11px;color:var(--muted);margin-bottom:4px">&#x1F477; Ajudante 1</div>
              <select id="sel-ajudante1" style="width:100%;padding:8px;border:1px solid var(--border);border-radius:6px;font-size:12px;background:var(--bg)">
                <option value="">-- Nenhum --</option>
              </select>
            </div>
            <div>
              <div style="font-size:11px;color:var(--muted);margin-bottom:4px">&#x1F477; Ajudante 2</div>
              <select id="sel-ajudante2" style="width:100%;padding:8px;border:1px solid var(--border);border-radius:6px;font-size:12px;background:var(--bg)">
                <option value="">-- Nenhum --</option>
              </select>
            </div>
          </div>
          <div id="rot-cap-info"'''

if old in content:
    content = content.replace(old, new, 1)
    print('Campos inseridos com sucesso!')
else:
    print('Padrao nao encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verifica
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()
print(f'sel-motorista no HTML: {c.count("id=\"sel-motorista\"")}')
print('Faca Ctrl+Shift+R no navegador!')
