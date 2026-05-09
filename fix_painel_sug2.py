path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Localiza card-sel-veiculo
idx = content.find('card-sel-veiculo')
if idx != -1:
    ln = content[:idx].count('\n')+1
    print(f'card-sel-veiculo linha {ln}')
    print(repr(content[max(0,idx-100):idx+100]))

# Localiza rot-total-peso para saber onde inserir
idx2 = content.find('rot-total-peso')
if idx2 != -1:
    ln2 = content[:idx2].count('\n')+1
    print(f'\nrot-total-peso linha {ln2}')
    print(repr(content[max(0,idx2-50):idx2+150]))

# Insere painel após rot-count / rot-total-peso
old = '''<span id="rot-count">0</span> selecionados'''
if old in content:
    new = old + '''
          <div id="rot-sugestao-veiculo" style="display:none;background:#0a2040;border:1px solid #10b981;border-radius:8px;padding:10px;margin-top:8px">
            <div style="font-size:11px;font-weight:700;color:#10b981;margin-bottom:6px">📊 RESUMO DA SELEÇÃO</div>
            <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:center">
              <div style="text-align:center"><div style="font-size:20px;font-weight:700;color:#e8f0fe" id="sug-clientes">0</div><div style="font-size:10px;color:#90afd4">clientes</div></div>
              <div style="text-align:center"><div style="font-size:20px;font-weight:700;color:#f59e0b" id="sug-peso-total">0 kg</div><div style="font-size:10px;color:#90afd4">peso total</div></div>
              <div style="text-align:center"><div style="font-size:20px;font-weight:700;color:#64B4FF" id="sug-pallets">—</div><div style="font-size:10px;color:#90afd4">pallets est.</div></div>
              <div style="text-align:center"><div style="font-size:20px;font-weight:700;color:#a78bfa" id="sug-tempo">—</div><div style="font-size:10px;color:#90afd4">tempo est.</div></div>
            </div>
          </div>'''
    content = content.replace(old, new, 1)
    print('Painel inserido após rot-count!')
else:
    # Tenta outra âncora
    idx3 = content.find('"rot-count"')
    if idx3 != -1:
        ln3 = content[:idx3].count('\n')+1
        print(f'\nrot-count linha {ln3}:')
        print(repr(content[max(0,idx3-80):idx3+200]))

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
