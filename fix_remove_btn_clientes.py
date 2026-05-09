path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove o botão Base Clientes do header de pedidos
old_btn = '<button class="btn btn-secondary" onclick="abrirImportacaoBaseClientes()" title="Importar base de clientes com GPS">👥 Base Clientes</button>\n          '
if old_btn in content:
    content = content.replace(old_btn, '')
    print('Botão Base Clientes removido!')
else:
    # Tenta variação
    import re
    content = re.sub(
        r'<button[^>]*onclick="abrirImportacaoBaseClientes\(\)"[^>]*>.*?</button>\s*',
        '',
        content
    )
    print('Botão removido via regex!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Ctrl+Shift+R.')
