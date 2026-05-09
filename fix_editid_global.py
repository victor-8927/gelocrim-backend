path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Usa variável global em vez de dataset
# 1. Adiciona variável global
old_vars = "var rotSelecionados = {};"
new_vars = "var rotSelecionados = {};\nvar _editVeiculoId = null;"
content = content.replace(old_vars, new_vars, 1)

# 2. Na editarVeiculo, seta a variável global
old = "    document.getElementById('modal-veiculo-completo').dataset.editId = id;"
new = "    _editVeiculoId = id;"
content = content.replace(old, new)

# 3. Na abrirModalVeiculo, limpa a variável
old2 = "  delete document.getElementById('modal-veiculo-completo').dataset.editId;"
new2 = "  _editVeiculoId = null;"
content = content.replace(old2, new2)

# 4. No salvarVeiculoCompleto, usa a variável global
old3 = "  var editId = document.getElementById('modal-veiculo-completo').dataset.editId||null;"
new3 = "  var editId = _editVeiculoId;"
content = content.replace(old3, new3)

# 5. Na hora de limpar após salvar
old4 = "    modal.removeAttribute('data-edit-id');"
new4 = "    _editVeiculoId = null;"
content = content.replace(old4, new4)

print('Variável global _editVeiculoId implementada!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
