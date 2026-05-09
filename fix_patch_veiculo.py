path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica se o hidden foi adicionado no HTML
count = content.count('id="v-edit-id"')
print(f'v-edit-id no HTML: {count} ocorrências')

# Se não existe, adiciona antes do botão salvar
if count == 0:
    old = '              <button onclick="salvarVeiculoCompleto()" class="btn btn-primary">💾 Salvar Veículo</button>'
    new = '              <input type="hidden" id="v-edit-id" value="">\n              <button onclick="salvarVeiculoCompleto()" class="btn btn-primary">💾 Salvar Veículo</button>'
    if old in content:
        content = content.replace(old, new)
        print('Hidden adicionado antes do botão salvar!')
    else:
        print('Botão salvar não encontrado!')
else:
    print('Hidden já existe!')

# Verifica onde hidden é setado no editarVeiculo
idx = content.find("hiddenId.value = id")
if idx != -1:
    ln = content[:idx].count('\n')+1
    print(f'hiddenId.value = id na linha {ln}')
else:
    print('hiddenId.value não encontrado!')
    # Adiciona no editarVeiculo antes do calcularCubagem
    old2 = "    if(v.bau_comp && v.bau_larg && v.bau_alt) calcularCubagem();\n\n  }catch(e){ toast('Erro: '+e.message,'error'); }\n}"
    new2 = "    // Seta hidden com ID\n    var h = document.getElementById('v-edit-id');\n    if(h) h.value = id;\n    console.log('Setando v-edit-id:', id, 'hidden:', h);\n\n    if(v.bau_comp && v.bau_larg && v.bau_alt) calcularCubagem();\n\n  }catch(e){ toast('Erro: '+e.message,'error'); }\n}"
    if old2 in content:
        content = content.replace(old2, new2)
        print('Hidden setado no editarVeiculo!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
