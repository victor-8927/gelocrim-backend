path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '''<button class="btn" onclick="abrirModalItens()" style="background:rgba(16,185,129,.15);border:1px solid #10b981;color:#10b981">📦 Importar Itens</button>'''

new = '''<button class="btn" onclick="abrirModalItens()" style="background:rgba(16,185,129,.15);border:1px solid #10b981;color:#10b981">📦 Importar Itens</button>
          <button class="btn" onclick="abrirModalPlanilha()" style="background:rgba(100,180,255,.15);border:1px solid #64B4FF;color:#64B4FF">📋 Importar Planilha TI</button>'''

if old in content:
    content = content.replace(old, new)
    print('Botão adicionado!')
else:
    print('Não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Ctrl+Shift+R')
