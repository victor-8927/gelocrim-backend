path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adiciona input hidden no modal de veículo
old = '<div style="padding:20px 24px">\n            <!-- Identificação -->'
new = '<div style="padding:20px 24px">\n            <input type="hidden" id="v-edit-id" value="">\n            <!-- Identificação -->'
if old in content:
    content = content.replace(old, new)
    print('Input hidden adicionado!')
else:
    print('Padrão não encontrado para hidden!')

# 2. editarVeiculo seta o hidden
old2 = """    var titulo = document.getElementById('modal-veic-titulo');
    if(titulo) titulo.textContent = 'Editar — ' + (v.vda||v.plate);

    if(v.bau_comp && v.bau_larg && v.bau_alt) calcularCubagem();

  }catch(e){ toast('Erro: '+e.message,'error'); }
}"""
new2 = """    var titulo = document.getElementById('modal-veic-titulo');
    if(titulo) titulo.textContent = 'Editar — ' + (v.vda||v.plate);

    // Seta o ID no campo hidden
    var hiddenId = document.getElementById('v-edit-id');
    if(hiddenId) hiddenId.value = id;

    if(v.bau_comp && v.bau_larg && v.bau_alt) calcularCubagem();

  }catch(e){ toast('Erro: '+e.message,'error'); }
}"""
if old2 in content:
    content = content.replace(old2, new2)
    print('editarVeiculo seta hidden!')

# 3. abrirModalVeiculo limpa o hidden
old3 = "  _editVeiculoId = null;\n  document.getElementById('modal-veiculo-completo').style.display='flex';"
new3 = "  _editVeiculoId = null;\n  var h=document.getElementById('v-edit-id'); if(h) h.value='';\n  document.getElementById('modal-veiculo-completo').style.display='flex';"
if old3 in content:
    content = content.replace(old3, new3)
    print('abrirModalVeiculo limpa hidden!')

# 4. salvarVeiculoCompleto lê do hidden
old4 = "  var editId = _editVeiculoId;\n  console.log"
new4 = "  var hiddenEl = document.getElementById('v-edit-id');\n  var editId = (hiddenEl && hiddenEl.value) ? hiddenEl.value : _editVeiculoId;\n  console.log('editId:', editId);"
if old4 in content:
    content = content.replace(old4, new4)
    print('salvarVeiculoCompleto lê hidden!')
else:
    old4b = "  var editId = _editVeiculoId;\n"
    new4b = "  var hiddenEl = document.getElementById('v-edit-id');\n  var editId = (hiddenEl && hiddenEl.value) ? hiddenEl.value : _editVeiculoId;\n  console.log('editId:', editId);\n"
    if old4b in content:
        content = content.replace(old4b, new4b, 1)
        print('salvarVeiculoCompleto lê hidden (v2)!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
