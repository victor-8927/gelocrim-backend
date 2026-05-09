path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Corrige calcularCubagem para calcular cubagem E pallets
old = "function calcularCubagem(){}"
new = """async function calcularCubagem(){
  var comp = parseFloat(document.getElementById('v-comp').value)||0;
  var larg = parseFloat(document.getElementById('v-larg').value)||0;
  var alt  = parseFloat(document.getElementById('v-alt').value)||0;
  var elInfo = document.getElementById('v-cubagem-calc');

  if(!comp || !larg || !alt){
    if(elInfo) elInfo.textContent = 'Cubagem calculada: — m³ (preencha as dimensões)';
    return;
  }

  var cubagem = comp * larg * alt;

  // Calcula quantos pallets cabem — busca pallets carregados
  try{
    var pallets = await api('GET','/producao/pallets');
    var itens   = await api('GET','/producao/itens');

    var pallet = pallets.length > 0 ? pallets[0] : null;
    var pComp  = pallet ? parseFloat(pallet.comprimento)||1.20 : 1.20;
    var pLarg  = pallet ? parseFloat(pallet.largura)||1.00    : 1.00;

    // Quantos pallets cabem no comprimento e largura do baú
    var colsComp = Math.floor(comp / pComp);
    var colsLarg = Math.floor(larg / pLarg);
    var totalPallets = colsComp * colsLarg;

    // Atualiza campo de pallets
    var elPallets = document.getElementById('v-pallets');
    if(elPallets && totalPallets > 0) elPallets.value = totalPallets;

    // Atualiza capacity_m3
    var elM3 = document.getElementById('v-m3');
    if(elM3) elM3.value = cubagem.toFixed(2);

    // Monta tabela de tipos de gelo x pallets
    var configs = [
      {nome:'Gelo 5kg',  kg:5,  un:180},
      {nome:'Gelo 10kg', kg:10, un:110},
      {nome:'Gelo 20kg', kg:20, un:50},
      {nome:'Gelo 40kg', kg:40, un:27},
    ];

    var linhas = configs.map(function(cfg){
      var item = itens.find(function(it){
        var n = (it.nome||'').toLowerCase().replace(/\s/g,'');
        return n.indexOf(cfg.kg+'kg')>=0;
      });
      var pesoUnit = item ? parseFloat(item.peso) : cfg.kg;
      var pesoTotal = (cfg.un * pesoUnit * totalPallets) + (6 * totalPallets); // +6kg tara/pallet
      return '<tr style="border-bottom:1px solid #1e3a5c">'+
        '<td style="padding:4px 8px;color:#64B4FF">'+cfg.nome+'</td>'+
        '<td style="padding:4px 8px;text-align:center;color:#f59e0b">'+cfg.un+' un/pallet</td>'+
        '<td style="padding:4px 8px;text-align:center;color:#a78bfa">'+totalPallets+' pallets</td>'+
        '<td style="padding:4px 8px;text-align:center;color:#10b981">'+cfg.un*totalPallets+' un total</td>'+
        '<td style="padding:4px 8px;text-align:center;color:#f87171">'+pesoTotal.toFixed(0)+' kg</td>'+
        '</tr>';
    }).join('');

    if(elInfo) elInfo.innerHTML =
      '<div style="margin-bottom:8px">'+
        '<b style="color:#64B4FF">Cubagem do baú: '+cubagem.toFixed(3)+' m³</b> &nbsp;|&nbsp; '+
        '<b style="color:#f59e0b">'+totalPallets+' pallets</b> ('+pComp+'x'+pLarg+'m cada)'+
      '</div>'+
      '<table style="width:100%;font-size:11px">'+
        '<thead><tr style="background:#1e3a5c">'+
          '<th style="padding:4px 8px;text-align:left;color:#90afd4">Tipo</th>'+
          '<th style="padding:4px 8px;color:#90afd4">Un/Pallet</th>'+
          '<th style="padding:4px 8px;color:#90afd4">Pallets</th>'+
          '<th style="padding:4px 8px;color:#90afd4">Total Un.</th>'+
          '<th style="padding:4px 8px;color:#90afd4">Peso Total</th>'+
        '</tr></thead>'+
        '<tbody>'+linhas+'</tbody>'+
      '</table>';

  } catch(e) {
    if(elInfo) elInfo.textContent = 'Cubagem: '+cubagem.toFixed(3)+' m³ | Erro ao calcular pallets: '+e.message;
  }
}"""

if old in content:
    content = content.replace(old, new)
    print('calcularCubagem implementado!')
else:
    print('Padrão não encontrado!')

# 2. Corrige salvarVeiculoCompleto para realmente salvar no banco
old2 = "function salvarVeiculoCompleto(){toast('Veiculo salvo!','success');}"
new2 = """async function salvarVeiculoCompleto(){
  var editId = document.getElementById('modal-veiculo-completo').dataset.editId||null;
  var body = {
    vda:          document.getElementById('v-vda').value,
    plate:        document.getElementById('v-plate').value,
    model:        document.getElementById('v-model').value,
    type:         document.getElementById('v-type').value,
    capacity_kg:  parseFloat(document.getElementById('v-kg').value)||0,
    capacity_m3:  parseFloat(document.getElementById('v-m3').value)||0,
    pallets:      parseInt(document.getElementById('v-pallets').value)||0,
    bau_comp:     parseFloat(document.getElementById('v-comp').value)||0,
    bau_larg:     parseFloat(document.getElementById('v-larg').value)||0,
    bau_alt:      parseFloat(document.getElementById('v-alt').value)||0,
    fuel_type:    document.getElementById('v-combustivel').value,
    km_per_liter: parseFloat(document.getElementById('v-kml').value)||0,
    fuel_price:   parseFloat(document.getElementById('v-preco-comb').value)||0,
    ipva_anual:   parseFloat(document.getElementById('v-ipva').value)||0,
    manut_mes:    parseFloat(document.getElementById('v-manut').value)||0,
    daily_cost:   parseFloat(document.getElementById('v-custo-dia').value)||0,
    oleo_ult_data: document.getElementById('v-ult-oleo').value||null,
    oleo_prox_data:document.getElementById('v-prox-oleo').value||null,
    oleo_custo:   parseFloat(document.getElementById('v-custo-oleo').value)||0,
    status:       document.getElementById('v-status').value,
  };
  if(!body.plate||!body.model){toast('Placa e modelo obrigatórios!','error');return;}
  try{
    if(editId){
      await api('PATCH','/vehicles/'+editId, body);
      toast('Veículo atualizado!','success');
    } else {
      await api('POST','/vehicles', body);
      toast('Veículo cadastrado!','success');
    }
    document.getElementById('modal-veiculo-completo').style.display='none';
    delete document.getElementById('modal-veiculo-completo').dataset.editId;
    loadVehicles();
  }catch(e){toast('Erro: '+e.message,'error');}
}"""

if old2 in content:
    content = content.replace(old2, new2)
    print('salvarVeiculoCompleto implementado!')

# 3. Corrige loadVehicles para ter botão editar funcional
old3 = """    tbody.innerHTML=data.map(function(v){return '<tr>'+
      '<td><b style="color:#64B4FF">'+(v.vda||'—')+'</b></td>'+
      '<td style="font-family:monospace">'+v.plate+'</td>'+
      '<td>'+v.model+'</td>'+
      '<td>'+v.type+'</td>'+
      '<td>'+v.capacity_kg+'kg</td>'+
      '<td>'+(v.fuel_type||'diesel')+'</td>'+
      '<td>'+(v.km_per_liter||'—')+' km/L</td>'+
      '<td>'+(v.daily_cost?'R$'+v.daily_cost:'—')+'</td>'+
      '<td><span class="badge '+(v.status||'active')+'">'+(v.status||'active')+'</span></td>'+
      '<td><button class="btn btn-sm btn-secondary" data-id="'+v.id+'" onclick="abrirModalVeiculo(this.dataset.id)">Editar</button></td>'+
      '</tr>';}).join('');"""

new3 = """    tbody.innerHTML=data.map(function(v){return '<tr>'+
      '<td><b style="color:#64B4FF">'+(v.vda||'—')+'</b></td>'+
      '<td style="font-family:monospace">'+v.plate+'</td>'+
      '<td>'+v.model+'</td>'+
      '<td style="font-size:11px">'+v.type+'</td>'+
      '<td style="color:#a78bfa;font-weight:700">'+v.capacity_kg+' kg</td>'+
      '<td style="color:#2dd4bf">'+(v.fuel_type||'diesel')+'</td>'+
      '<td>'+(v.km_per_liter||'—')+' km/L</td>'+
      '<td style="color:#f59e0b">'+(v.daily_cost?'R$ '+v.daily_cost:'—')+'</td>'+
      '<td><span class="badge '+(v.status||'active')+'">'+(v.status||'active')+'</span></td>'+
      '<td><button class="btn btn-sm btn-secondary" data-id="'+v.id+'" onclick="editarVeiculo(this.dataset.id)">✏️ Editar</button></td>'+
      '</tr>';}).join('');"""

if old3 in content:
    content = content.replace(old3, new3)
    print('loadVehicles corrigido!')

# 4. Adiciona função editarVeiculo
old4 = "function abrirModalVeiculo(id){document.getElementById('modal-veiculo-completo').style.display='flex';}"
new4 = """function abrirModalVeiculo(id){
  // Limpa form
  ['v-vda','v-plate','v-model','v-kg','v-m3','v-pallets','v-comp','v-larg','v-alt',
   'v-kml','v-preco-comb','v-ipva','v-manut','v-custo-dia','v-custo-oleo'].forEach(function(id){
    var e=document.getElementById(id); if(e) e.value='';
  });
  var titulo=document.getElementById('modal-veic-titulo');
  if(titulo) titulo.textContent='Novo Veículo';
  delete document.getElementById('modal-veiculo-completo').dataset.editId;
  document.getElementById('modal-veiculo-completo').style.display='flex';
}

async function editarVeiculo(id){
  try{
    var data = await api('GET','/vehicles');
    var v = data.find(function(x){return x.id===id;});
    if(!v) return;
    var set = function(eid, val){ var e=document.getElementById(eid); if(e) e.value=val||''; };
    set('v-vda',        v.vda);
    set('v-plate',      v.plate);
    set('v-model',      v.model);
    set('v-type',       v.type);
    set('v-kg',         v.capacity_kg);
    set('v-m3',         v.capacity_m3);
    set('v-pallets',    v.pallets);
    set('v-comp',       v.bau_comp);
    set('v-larg',       v.bau_larg);
    set('v-alt',        v.bau_alt);
    set('v-combustivel',v.fuel_type||'diesel');
    set('v-kml',        v.km_per_liter);
    set('v-preco-comb', v.fuel_price);
    set('v-ipva',       v.ipva_anual);
    set('v-manut',      v.manut_mes);
    set('v-custo-dia',  v.daily_cost);
    set('v-ult-oleo',   v.oleo_ult_data);
    set('v-prox-oleo',  v.oleo_prox_data);
    set('v-custo-oleo', v.oleo_custo);
    set('v-status',     v.status);
    var titulo=document.getElementById('modal-veic-titulo');
    if(titulo) titulo.textContent='Editar Veículo — '+v.vda;
    document.getElementById('modal-veiculo-completo').dataset.editId = id;
    document.getElementById('modal-veiculo-completo').style.display='flex';
    // Recalcula cubagem se tiver dimensões
    if(v.bau_comp && v.bau_larg && v.bau_alt) calcularCubagem();
  }catch(e){toast('Erro: '+e.message,'error');}
}"""

if old4 in content:
    content = content.replace(old4, new4)
    print('editarVeiculo adicionado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('\nPronto! Ctrl+Shift+R.')
