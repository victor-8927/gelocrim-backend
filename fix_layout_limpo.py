path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove elementos duplicados inseridos anteriormente
import re

# Remove o bloco PASSO 3 duplicado que foi inserido fora da sidebar
for bloco in [
    '      <!-- PASSO 3 -->\n      <div class="card" style="flex-shrink:0">\n        <div class="card-header" style="padding:8px 12px">\n          <span class="card-title" style="font-size:11px;color:#e8521a">📊 PASSO 3 — CARGA ESTIMADA</span>\n        </div>',
    '      <!-- LISTA CLIENTES -->\n      <div class="card" style="flex:1;overflow:hidden;display:flex;flex-direction:column">\n        <div class="card-header" style="flex-shrink:0;padding:10px 12px">\n          <span class="card-title" style="font-size:11px;color:#64B4FF">CLIENTES SELECIONADOS (<span id="rot-count">0</span>)</span>',
]:
    if bloco in content:
        # Encontra e remove o bloco inteiro
        idx = content.find(bloco)
        # Acha o fechamento do div
        depth = 0
        i = idx
        while i < len(content):
            if content[i:i+4] == '<div': depth += 1
            elif content[i:i+6] == '</div': 
                depth -= 1
                if depth == 0:
                    end = content.find('>', i) + 1
                    content = content[:idx] + content[end:]
                    print(f'Bloco duplicado removido!')
                    break
            i += 1

# 2. Adiciona pallets no card CARGA SELECIONADA existente
old_carga = '''          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px">
            <div style="background:#0a1628;border:1px solid #1e3a5c;padding:8px;border-radius:6px;text-align:center">
              <div id="rot-total-peso" style="font-size:18px;font-weight:700;color:#f59e0b">0 kg</div>
              <div style="font-size:10px;color:#90afd4">PESO TOTAL</div>
            </div>
            <div style="background:#0a1628;border:1px solid #1e3a5c;padding:8px;border-radius:6px;text-align:center">
              <div id="rot-total-vol" style="font-size:18px;font-weight:700;color:#2dd4bf">0 m3</div>
              <div style="font-size:10px;color:#90afd4">VOLUME TOTAL</div>
            </div>
        </div>
      </div>'''

new_carga = '''          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin-bottom:4px">
            <div style="background:#0a1628;border:1px solid #1e3a5c;padding:6px;border-radius:6px;text-align:center">
              <div id="rot-total-peso" style="font-size:16px;font-weight:700;color:#f59e0b">0 kg</div>
              <div style="font-size:9px;color:#90afd4">PESO</div>
            </div>
            <div style="background:#0a1628;border:1px solid #1e3a5c;padding:6px;border-radius:6px;text-align:center">
              <div id="rot-total-vol" style="font-size:16px;font-weight:700;color:#2dd4bf">0 m³</div>
              <div style="font-size:9px;color:#90afd4">CUBAGEM</div>
            </div>
            <div style="background:#0a1628;border:1px solid #1e3a5c;padding:6px;border-radius:6px;text-align:center">
              <div id="sug-pallets" style="font-size:16px;font-weight:700;color:#a78bfa">—</div>
              <div style="font-size:9px;color:#90afd4">PALLETS</div>
            </div>
          </div>
        </div>
      </div>'''

if old_carga in content:
    content = content.replace(old_carga, new_carga)
    print('Card CARGA atualizado com pallets!')
else:
    print('Card CARGA não encontrado!')

# 3. Adiciona rot-count no header da lista (se não existir)
old_lista_header = '<span class="card-title" style="font-size:11px;color:#64B4FF">CLIENTES SELECIONADOS</span>'
new_lista_header = '<span class="card-title" style="font-size:11px;color:#64B4FF">CLIENTES SELECIONADOS (<span id="rot-count">0</span>)</span>'
if old_lista_header in content:
    content = content.replace(old_lista_header, new_lista_header)
    print('rot-count adicionado na lista!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
