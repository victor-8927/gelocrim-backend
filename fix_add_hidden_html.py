path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona input hidden logo após a abertura do div de conteúdo do modal veículo
# Busca o div de padding que contém o formulário
old = '          <div style="padding:20px 24px">\n            <!-- Identificação -->'
new = '          <div style="padding:20px 24px">\n            <input type="hidden" id="v-edit-id" value="">\n            <!-- Identificação -->'

if old in content:
    content = content.replace(old, new)
    print('Input hidden adicionado no HTML!')
else:
    # Tenta outra variação
    idx = content.find('id="modal-veiculo-completo"')
    if idx != -1:
        # Acha o primeiro div de padding após o modal
        idx2 = content.find('<div style="padding:20px 24px">', idx)
        if idx2 != -1:
            ln = content[:idx2].count('\n')+1
            print(f'Encontrado em linha {ln}')
            print(repr(content[idx2:idx2+80]))
            insert_pos = idx2 + len('<div style="padding:20px 24px">\n')
            content = content[:insert_pos] + '            <input type="hidden" id="v-edit-id" value="">\n' + content[insert_pos:]
            print('Hidden inserido!')

# Verifica
count = content.count('id="v-edit-id"')
print(f'\nTotal de v-edit-id no HTML: {count}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
