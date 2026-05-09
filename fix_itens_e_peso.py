path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove TOP e Unidade da tabela de itens
old_thead = '''              <tr>
                  <th>Item</th>
                  <th>Peso (kg)</th>
                  <th>Dimensões</th>
                  <th>Un./Pallet</th>
                  <th>TOP</th>
                  <th>Observação</th>
                  <th>Ações</th>
                </tr>'''
new_thead = '''              <tr>
                  <th>Item</th>
                  <th>Peso (kg)</th>
                  <th>Dimensões (m)</th>
                  <th>Observação</th>
                  <th>Ações</th>
                </tr>'''
if old_thead in content:
    content = content.replace(old_thead, new_thead)
    print('Cabeçalho itens corrigido!')

# 2. Corrige loadItens para não mostrar TOP e UN
old_row = """      '<td><b>'+(it.nome||'—')+'</b></td>'+
      '<td style="color:#f59e0b">'+(it.peso||0)+' kg</td>'+
      '<td style="font-size:11px">'+(it.comprimento||0)+'x'+(it.largura||0)+'x'+(it.altura||0)+'</td>'+
      '<td>'+(it.un_pallet||0)+'</td>'+
      '<td>'+(it.top||'—')+'</td>'+
      '<td style="font-size:11px">'+(it.observacao||'—')+'</td>'+
      '<td><button class="btn btn-sm btn-secondary" data-id="'+it.id+'" onclick="editarItem(this.dataset.id)">✏️ Editar</button></td>'+"""
new_row = """      '<td><b>'+(it.nome||'—')+'</b></td>'+
      '<td style="color:#f59e0b">'+(it.peso||0)+' kg</td>'+
      '<td style="font-size:11px">'+(it.comprimento||0)+'x'+(it.largura||0)+'x'+(it.altura||0)+' m</td>'+
      '<td style="font-size:11px">'+(it.observacao||'—')+'</td>'+
      '<td><button class="btn btn-sm btn-secondary" data-id="'+it.id+'" onclick="editarItem(this.dataset.id)">✏️ Editar</button></td>'+"""
if old_row in content:
    content = content.replace(old_row, new_row)
    print('Linha de item corrigida!')

# 3. Corrige loadPalletsCarregados — usa peso real do item
old_peso = """      // Peso total — usa peso REAL do item cadastrado
      var pesoUnitario = item ? parseFloat(item.peso) : cfg.kg;
      var pesoItens    = cfg.un * pesoUnitario;
      var pesoPallet   = pPeso;
      var pesoTotal    = pesoItens + pesoPallet;"""
new_peso = """      // Peso total — usa peso REAL do item cadastrado
      var pesoUnitario = item ? parseFloat(item.peso) : cfg.kg;
      var pesoItens    = cfg.un * pesoUnitario;
      var pesoPallet   = parseFloat(palletBase.peso_max)||25;
      var pesoTotal    = pesoItens + pesoPallet;"""
if old_peso in content:
    content = content.replace(old_peso, new_peso)
    print('Peso real aplicado no pallet carregado!')
else:
    # Tenta versão anterior
    old_peso2 = """      // Peso total
      var pesoItens  = cfg.un * cfg.kg;
      var pesoPallet = pPeso;
      var pesoTotal  = pesoItens + pesoPallet;"""
    new_peso2 = """      // Peso total — usa peso REAL do item cadastrado
      var pesoUnitario = item ? parseFloat(item.peso) : cfg.kg;
      var pesoItens    = cfg.un * pesoUnitario;
      var pesoPallet   = parseFloat(palletBase.peso_max)||25;
      var pesoTotal    = pesoItens + pesoPallet;"""
    if old_peso2 in content:
        content = content.replace(old_peso2, new_peso2)
        print('Peso real aplicado (versão 2)!')
    else:
        print('Padrão de peso não encontrado — buscando...')
        idx = content.find('pesoItens  = cfg.un')
        if idx != -1:
            print(repr(content[idx-10:idx+80]))

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('\nPronto! Ctrl+Shift+R.')
