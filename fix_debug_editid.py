path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Adiciona console.log na linha 4133 para ver o valor de _editVeiculoId
old = 'async function salvarVeiculoCompleto(){\n  var editId = _editVeiculoId;\n'
new = 'async function salvarVeiculoCompleto(){\n  var editId = _editVeiculoId;\n  console.log("editId ao salvar:", editId, "| _editVeiculoId:", typeof _editVeiculoId !== "undefined" ? _editVeiculoId : "NAO DEFINIDA");\n'

content = ''.join(lines)
if old in content:
    content = content.replace(old, new)
    print('Log adicionado!')
else:
    print('Padrão não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
