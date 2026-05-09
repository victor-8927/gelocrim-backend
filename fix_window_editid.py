path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Usa window.veiculoEditId em vez de qualquer outra abordagem
# 1. No editarVeiculo - seta window.veiculoEditId
content = content.replace(
    "    // Seta o ID no campo hidden\n    var hiddenId = document.getElementById('v-edit-id');\n    if(hiddenId) hiddenId.value = id;",
    "    window.veiculoEditId = id;\n    var hiddenId = document.getElementById('v-edit-id');\n    if(hiddenId) hiddenId.value = id;\n    console.log('veiculoEditId setado:', window.veiculoEditId);"
)

# 2. No salvarVeiculoCompleto - lê window.veiculoEditId
content = content.replace(
    "async function salvarVeiculoCompleto(editId){\n  editId = editId || null;\n  console.log('editId recebido:', editId);",
    "async function salvarVeiculoCompleto(editId){\n  editId = editId || window.veiculoEditId || null;\n  console.log('editId final:', editId, 'window:', window.veiculoEditId);"
)

# 3. No abrirModalVeiculo - limpa window.veiculoEditId
content = content.replace(
    "  _editVeiculoId = null;\n  var h=document.getElementById('v-edit-id'); if(h) h.value='';\n  document.getElementById('modal-veiculo-completo').style.display='flex';",
    "  _editVeiculoId = null;\n  window.veiculoEditId = null;\n  var h=document.getElementById('v-edit-id'); if(h) h.value='';\n  document.getElementById('modal-veiculo-completo').style.display='flex';"
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
