path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra o botão Importar CSV na toolbar de pedidos
old = '''<button class="btn btn-primary" onclick="abrirImportacaoCSV()">📥 Importar CSV</button>'''

if old in content:
    new = old + '\n          <button class="btn" onclick="abrirModalItens()" style="background:rgba(16,185,129,.15);border:1px solid #10b981;color:#10b981">📦 Importar Itens</button>'
    content = content.replace(old, new, 1)
    print('Botão Importar Itens adicionado!')
else:
    print('Padrão não encontrado! Buscando variações...')
    import re
    m = re.search(r'<button[^>]+abrirImportacaoCSV[^>]+>[^<]+</button>', content)
    if m:
        print(f'Encontrado: {repr(m.group(0))}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
