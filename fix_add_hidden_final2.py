path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona hidden antes do botão Cancelar do modal veículo
old = '              <button onclick="document.getElementById(\'modal-veiculo-completo\').style.display=\'none\'" class="btn btn-secondary">Cancelar</button>\n              <button onclick="salvarVeiculoCompleto()" class="btn btn-primary">'
new = '              <input type="hidden" id="v-edit-id" value="">\n' + old

if old in content:
    content = content.replace(old, new, 1)
    print('Hidden adicionado!')
else:
    print('Padrao nao encontrado!')
    # Busca alternativa
    idx = content.find('salvarVeiculoCompleto()')
    while idx != -1:
        before = content[:idx]
        opens  = before.count('<script')
        closes = before.count('</script>')
        if opens == closes:
            ln = before.count('\n')+1
            print(f'Botao salvar HTML linha {ln}')
            print(repr(content[max(0,idx-150):idx+30]))
            break
        idx = content.find('salvarVeiculoCompleto()', idx+1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

total = content.count('id="v-edit-id"')
print(f'v-edit-id total: {total}')
print('Pronto! Ctrl+Shift+R.')
