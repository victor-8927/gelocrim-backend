path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona botão após "Importar Itens"
old = '''<button class="btn btn-primary btn-sm" onclick="abrirModalItens()">📦 Importar Itens</button>'''
new = '''<button class="btn btn-primary btn-sm" onclick="abrirModalItens()">📦 Importar Itens</button>
              <button class="btn btn-sm" style="background:rgba(100,180,255,.15);border:1px solid #64B4FF;color:#64B4FF" onclick="abrirModalPlanilha()">📋 Importar Planilha TI</button>'''

if old in content:
    content = content.replace(old, new)
    print('Botão adicionado!')
else:
    print('Padrão não encontrado! Buscando...')
    idx = content.find('abrirModalItens')
    ln = content[:idx].count('\n')+1
    lines = content.split('\n')
    for i in range(max(0,ln-2), ln+3):
        print(f'{i+1}: {lines[i]}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Ctrl+Shift+R → tela Pedidos')
