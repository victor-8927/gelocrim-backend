path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = """    // Abre o modal PRIMEIRO para garantir que os elementos existem no DOM
    document.getElementById('modal-veiculo-completo').style.display='flex';

    // Aguarda o modal renderizar
    setTimeout(function(){"""

new = """    // Seta o ID ANTES do setTimeout
    _editVeiculoId = id;

    // Abre o modal PRIMEIRO para garantir que os elementos existem no DOM
    document.getElementById('modal-veiculo-completo').style.display='flex';

    // Aguarda o modal renderizar
    setTimeout(function(){"""

if old in content:
    content = content.replace(old, new)
    print('_editVeiculoId movido para antes do setTimeout!')
else:
    print('Padrão não encontrado!')

# Remove a linha duplicada dentro do setTimeout
old2 = "      _editVeiculoId = id;\n\n      // Recalcula cubagem"
new2 = "      // Recalcula cubagem"
if old2 in content:
    content = content.replace(old2, new2)
    print('Linha duplicada removida!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
