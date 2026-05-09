path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Corrige /producao/items -> /producao/itens
content = content.replace('/producao/items', '/producao/itens')
print('URLs corrigidas!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
