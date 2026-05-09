path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Muda o botão salvar para passar o ID direto
# Troca onclick="salvarVeiculoCompleto()" por onclick="salvarVeiculoCompleto(document.getElementById('v-edit-id').value)"
old_btn = """              <button onclick="salvarVeiculoCompleto()" class="btn btn-primary">💾 Salvar Veículo</button>"""
new_btn = """              <button onclick="salvarVeiculoCompleto(document.getElementById('v-edit-id').value)" class="btn btn-primary">💾 Salvar Veículo</button>"""

if old_btn in content:
    content = content.replace(old_btn, new_btn)
    print('Botão salvar atualizado!')

# Atualiza salvarVeiculoCompleto para receber o id como parâmetro
old_fn = "async function salvarVeiculoCompleto(){\n  var hiddenEl = document.getElementById('v-edit-id');\n  var editId = (hiddenEl && hiddenEl.value) ? hiddenEl.value : _editVeiculoId;\n  console.log('editId:', editId);"
new_fn = "async function salvarVeiculoCompleto(editId){\n  editId = editId || null;\n  console.log('editId recebido:', editId);"

if old_fn in content:
    content = content.replace(old_fn, new_fn)
    print('salvarVeiculoCompleto atualizado!')
else:
    # Tenta versão mais simples
    old_fn2 = "async function salvarVeiculoCompleto(){"
    new_fn2 = "async function salvarVeiculoCompleto(editId){\n  editId = editId || null;"
    # Só substitui a primeira ocorrência que é a função real
    idx = content.find(old_fn2)
    if idx != -1:
        # Verifica se está no segundo script (após linha 3400)
        ln = content[:idx].count('\n')+1
        print(f'salvarVeiculoCompleto na linha {ln}')
        content = content[:idx] + new_fn2 + content[idx+len(old_fn2):]
        # Remove a linha antiga de leitura do editId
        content = content.replace(
            "  var hiddenEl = document.getElementById('v-edit-id');\n  var editId = (hiddenEl && hiddenEl.value) ? hiddenEl.value : _editVeiculoId;\n  console.log('editId:', editId);\n",
            "  console.log('editId recebido:', editId);\n"
        )
        print('Substituído!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
