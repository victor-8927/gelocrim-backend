path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Corrige loadPallets para ter botão editar funcional
old = '''async function loadPallets(){
  try{
    var data=await api('GET','/producao/pallets');
    var tbody=document.getElementById('pallets-tbody');
    if(!tbody) return;
    tbody.innerHTML=data.length?data.map(function(p){return '<tr>'+
      '<td><b>'+p.nome+'</b></td><td>'+p.comprimento+'</td><td>'+p.largura+'</td>'+
      '<td>'+p.altura+'</td><td style="color:#2dd4bf">'+p.cubagem+'</td>'+
      '<td>'+p.peso_max+' kg</td>'+
      '<td><span class="badge active">Ativo</span></td>'+
      '<td><button class="btn btn-sm btn-secondary">Editar</button></td></tr>';}).join('')
    :'<tr><td colspan="8" class="loading-state">Nenhum pallet</td></tr>';
  }catch(e){toast('Erro: '+e.message,'error');}
}'''

new = '''async function loadPallets(){
  try{
    var data=await api('GET','/producao/pallets');
    var tbody=document.getElementById('pallets-tbody');
    if(!tbody) return;
    tbody.innerHTML=data.length?data.map(function(p){return '<tr>'+
      '<td><b>'+p.nome+'</b></td>'+
      '<td>'+(p.comprimento||0)+'</td>'+
      '<td>'+(p.largura||0)+'</td>'+
      '<td>'+(p.altura||0)+'</td>'+
      '<td style="color:#2dd4bf">'+(p.cubagem||0)+'</td>'+
      '<td>'+(p.peso_max||0)+' kg</td>'+
      '<td><span class="badge active">Ativo</span></td>'+
      '<td><button class="btn btn-sm btn-secondary" data-id="'+p.id+'" onclick="editarPallet(this.dataset.id)">✏️ Editar</button></td>'+
      '</tr>';}).join('')
    :'<tr><td colspan="8" class="loading-state">Nenhum pallet cadastrado</td></tr>';
  }catch(e){toast('Erro: '+e.message,'error');}
}

async function editarPallet(id){
  try{
    var data=await api('GET','/producao/pallets');
    var p=data.find(function(x){return x.id===id;});
    if(!p) return;
    document.getElementById('p-nome').value=p.nome||'';
    document.getElementById('p-comp').value=p.comprimento||'';
    document.getElementById('p-larg').value=p.largura||'';
    document.getElementById('p-alt').value=p.altura||'';
    document.getElementById('p-peso-max').value=p.peso_max||'';
    document.getElementById('p-cubagem').value=p.cubagem||'';
    document.getElementById('p-obs').value=p.observacao||'';
    var titulo=document.getElementById('modal-pallet-titulo');
    if(titulo) titulo.textContent='Editar Pallet';
    // Guarda id para salvar
    document.getElementById('modal-pallet').dataset.editId=id;
    document.getElementById('modal-pallet').style.display='flex';
  }catch(e){toast('Erro: '+e.message,'error');}
}'''

if old in content:
    content = content.replace(old, new)
    print('loadPallets corrigido!')
else:
    print('loadPallets nao encontrado!')

# Corrige loadItens para ter botão editar funcional
old2 = '''async function loadItens(){
  try{
    var data=await api('GET','/producao/itens');
    var tbody=document.getElementById('itens-tbody');
    if(!tbody) return;
    tbody.innerHTML=data.length?data.map(function(it){return '<tr>'+
      '<td><b>'+it.nome+'</b></td><td style="color:#f59e0b">'+it.peso+' kg</td>'+
      '<td style="font-size:11px">'+it.comprimento+'x'+it.largura+'x'+it.altura+'</td>'+
      '<td>'+it.un_pallet+'</td><td>'+it.top+'</td>'+
      '<td style="font-size:11px">'+it.observacao+'</td>'+
      '<td><button class="btn btn-sm btn-secondary">Editar</button></td></tr>';}).join('')
    :'<tr><td colspan="7" class="loading-state">Nenhum item</td></tr>';
  }catch(e){toast('Erro: '+e.message,'error');}
}'''

new2 = '''async function loadItens(){
  try{
    var data=await api('GET','/producao/itens');
    var tbody=document.getElementById('itens-tbody');
    if(!tbody) return;
    tbody.innerHTML=data.length?data.map(function(it){return '<tr>'+
      '<td><b>'+(it.nome||'—')+'</b></td>'+
      '<td style="color:#f59e0b">'+(it.peso||0)+' kg</td>'+
      '<td style="font-size:11px">'+(it.comprimento||0)+'x'+(it.largura||0)+'x'+(it.altura||0)+'</td>'+
      '<td>'+(it.un_pallet||0)+'</td>'+
      '<td>'+(it.top||'—')+'</td>'+
      '<td style="font-size:11px">'+(it.observacao||'—')+'</td>'+
      '<td><button class="btn btn-sm btn-secondary" data-id="'+it.id+'" onclick="editarItem(this.dataset.id)">✏️ Editar</button></td>'+
      '</tr>';}).join('')
    :'<tr><td colspan="7" class="loading-state">Nenhum item cadastrado</td></tr>';
  }catch(e){toast('Erro: '+e.message,'error');}
}

async function editarItem(id){
  try{
    var data=await api('GET','/producao/itens');
    var it=data.find(function(x){return x.id===id;});
    if(!it) return;
    document.getElementById('i-nome').value=it.nome||'';
    document.getElementById('i-peso').value=it.peso||'';
    document.getElementById('i-comp').value=it.comprimento||'';
    document.getElementById('i-larg').value=it.largura||'';
    document.getElementById('i-alt').value=it.altura||'';
    document.getElementById('i-obs').value=it.observacao||'';
    document.getElementById('i-un-pallet').value=it.un_pallet||0;
    document.getElementById('i-top').value=it.top||'1000';
    var titulo=document.getElementById('modal-item-titulo');
    if(titulo) titulo.textContent='Editar Item';
    document.getElementById('modal-item').dataset.editId=id;
    document.getElementById('modal-item').style.display='flex';
  }catch(e){toast('Erro: '+e.message,'error');}
}'''

if old2 in content:
    content = content.replace(old2, new2)
    print('loadItens corrigido!')
else:
    print('loadItens nao encontrado!')

# Corrige salvarPallet para suportar edição
old3 = "function salvarPallet(){toast('Pallet salvo!','success');}"
new3 = """async function salvarPallet(){
  var modal=document.getElementById('modal-pallet');
  var editId=modal?modal.dataset.editId:null;
  var body={
    nome:document.getElementById('p-nome').value,
    comprimento:parseFloat(document.getElementById('p-comp').value)||0,
    largura:parseFloat(document.getElementById('p-larg').value)||0,
    altura:parseFloat(document.getElementById('p-alt').value)||0,
    peso_max:parseFloat(document.getElementById('p-peso-max').value)||0,
    cubagem:parseFloat(document.getElementById('p-cubagem').value)||0,
    observacao:document.getElementById('p-obs').value
  };
  if(!body.nome){toast('Nome obrigatório!','error');return;}
  try{
    if(editId){
      await api('PATCH','/producao/pallets/'+editId,body);
      toast('Pallet atualizado!','success');
    } else {
      await api('POST','/producao/pallets',body);
      toast('Pallet criado!','success');
    }
    if(modal){modal.style.display='none';delete modal.dataset.editId;}
    var titulo=document.getElementById('modal-pallet-titulo');
    if(titulo) titulo.textContent='Novo Pallet';
    loadPallets();
  }catch(e){toast('Erro: '+e.message,'error');}
}"""

if old3 in content:
    content = content.replace(old3, new3)
    print('salvarPallet corrigido!')

# Corrige salvarItem para suportar edição
old4 = "function salvarItem(){toast('Item salvo!','success');}"
new4 = """async function salvarItem(){
  var modal=document.getElementById('modal-item');
  var editId=modal?modal.dataset.editId:null;
  var body={
    nome:document.getElementById('i-nome').value,
    peso:parseFloat(document.getElementById('i-peso').value)||0,
    comprimento:parseFloat(document.getElementById('i-comp').value)||0,
    largura:parseFloat(document.getElementById('i-larg').value)||0,
    altura:parseFloat(document.getElementById('i-alt').value)||0,
    observacao:document.getElementById('i-obs').value,
    un_pallet:parseInt(document.getElementById('i-un-pallet').value)||0,
    top:document.getElementById('i-top').value||'1000'
  };
  if(!body.nome){toast('Nome obrigatório!','error');return;}
  try{
    if(editId){
      await api('PATCH','/producao/itens/'+editId,body);
      toast('Item atualizado!','success');
    } else {
      await api('POST','/producao/itens',body);
      toast('Item criado!','success');
    }
    if(modal){modal.style.display='none';delete modal.dataset.editId;}
    var titulo=document.getElementById('modal-item-titulo');
    if(titulo) titulo.textContent='Novo Item';
    loadItens();
  }catch(e){toast('Erro: '+e.message,'error');}
}"""

if old4 in content:
    content = content.replace(old4, new4)
    print('salvarItem corrigido!')

# calcPalletCubagem automático
old5 = "function calcPalletCubagem(){}"
new5 = """function calcPalletCubagem(){
  var c=parseFloat(document.getElementById('p-comp').value)||0;
  var l=parseFloat(document.getElementById('p-larg').value)||0;
  var a=parseFloat(document.getElementById('p-alt').value)||0;
  var cub=document.getElementById('p-cubagem');
  if(cub && c&&l&&a) cub.value=(c*l*a).toFixed(4);
}"""
content = content.replace(old5, new5)

old6 = "function calcItemCubagem(){}"
new6 = """function calcItemCubagem(){
  var c=parseFloat(document.getElementById('i-comp').value)||0;
  var l=parseFloat(document.getElementById('i-larg').value)||0;
  var a=parseFloat(document.getElementById('i-alt').value)||0;
  var cub=document.getElementById('i-cubagem');
  if(cub && c&&l&&a) cub.value=(c*l*a).toFixed(4);
}"""
content = content.replace(old6, new6)
print('calcCubagem adicionado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('\nPronto! Ctrl+Shift+R.')
