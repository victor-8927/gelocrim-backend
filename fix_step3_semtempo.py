path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove card de tempo do Passo 3
old = '''          <div style="background:#0a1628;border-radius:6px;padding:6px;text-align:center">
            <div id="sug-tempo" style="font-size:15px;font-weight:700;color:#10b981">—</div>
            <div style="font-size:9px;color:#90afd4">TEMPO EST.</div>
          </div>'''

if old in content:
    content = content.replace(old, '')
    print('Card de tempo removido do Passo 3!')

# Muda grid para 3 colunas
content = content.replace(
    'display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:8px',
    'display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;padding:8px'
)

# Remove cálculo de tempo do atualizarSelecaoRot
old2 = "  var tempoTotal= itens.reduce(function(s,x){ return s+(parseInt((x.order||{}).tempo_entrega)||15); }, 0);\n\n  // Pallets estimados: peso_pallet_max = 700kg (gelo 20kg*35un=700kg p/ pallet)\n  var PESO_PALLET = 700;\n  var palletsEst = Math.ceil(pesoTotal / PESO_PALLET) || 0;\n\n  // Tempo estimado em horas e minutos\n  var totalMin = tempoTotal + (itens.length * 10); // +10min deslocamento médio por cliente\n  var horas = Math.floor(totalMin/60);\n  var mins  = totalMin % 60;\n  var tempoStr = horas>0 ? horas+'h '+mins+'min' : mins+'min';"

new2 = "  // Pallets estimados: peso máx por pallet = 700kg\n  var PESO_PALLET = 700;\n  var palletsEst = Math.ceil(pesoTotal / PESO_PALLET) || 0;"

if old2 in content:
    content = content.replace(old2, new2)
    print('Cálculo de tempo removido de atualizarSelecaoRot!')

# Remove referência a sug-tempo
old3 = "    if(el('sug-tempo'))      el('sug-tempo').textContent      = tempoStr;\n"
if old3 in content:
    content = content.replace(old3, '')
    print('sug-tempo removido!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
