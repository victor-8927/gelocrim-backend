path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona painel de sugestão após o card de veículo selecionado
old = '''          <div id="card-sel-veiculo"'''

new = '''          <!-- PAINEL SUGESTÃO -->
          <div id="rot-sugestao-veiculo" style="display:none;background:#0f2040;border:1px solid #10b981;border-radius:8px;padding:10px;margin-bottom:8px">
            <div style="font-size:11px;font-weight:700;color:#10b981;margin-bottom:6px">📊 RESUMO DA SELEÇÃO</div>
            <div style="display:flex;gap:12px;flex-wrap:wrap">
              <div style="text-align:center">
                <div style="font-size:18px;font-weight:700;color:#e8f0fe" id="sug-clientes">0</div>
                <div style="font-size:10px;color:#90afd4">clientes</div>
              </div>
              <div style="text-align:center">
                <div style="font-size:18px;font-weight:700;color:#f59e0b" id="sug-peso-total">0 kg</div>
                <div style="font-size:10px;color:#90afd4">peso total</div>
              </div>
              <div style="text-align:center">
                <div style="font-size:18px;font-weight:700;color:#64B4FF" id="sug-pallets">—</div>
                <div style="font-size:10px;color:#90afd4">pallets est.</div>
              </div>
              <div style="text-align:center">
                <div style="font-size:18px;font-weight:700;color:#a78bfa" id="sug-tempo">—</div>
                <div style="font-size:10px;color:#90afd4">tempo est.</div>
              </div>
            </div>
          </div>
          <div id="card-sel-veiculo"'''

if old in content:
    content = content.replace(old, new, 1)
    print('Painel de sugestão adicionado!')
else:
    print('Âncora não encontrada!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto!')
