path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona as funções de veículo no primeiro script, antes do </script>
# Encontra o fechamento do primeiro script (linha ~3399)
primeiro_close = content.find('</script>\n  <!-- MODAL IMPORTAÇÃO CSV')

if primeiro_close == -1:
    print('Fechamento do primeiro script não encontrado!')
else:
    ln = content[:primeiro_close].count('\n')+1
    print(f'Primeiro </script> na linha {ln}')

    novo_codigo = """
// ── VEÍCULOS EDIÇÃO ──────────────────────────────────────────────
async function editarVeiculo(id){
  window.veiculoEditId = id;
  console.log('editarVeiculo chamado com id:', id);
  try{
    var data = await api('GET','/vehicles');
    var v = data.find(function(x){return x.id===id;});
    if(!v){ toast('Veículo não encontrado!','error'); return; }
    var modal = document.getElementById('modal-veiculo-completo');
    if(!modal){ toast('Modal não encontrado!','error'); return; }
    modal.style.display='flex';
    setTimeout(function(){
      function setV(eid,val){ var e=document.getElementById(eid); if(e&&val!=null&&val!==undefined&&val!=='') e.value=val; }
      setV('v-vda',v.vda); setV('v-plate',v.plate); setV('v-model',v.model);
      setV('v-type',v.type); setV('v-kg',v.capacity_kg); setV('v-m3',v.capacity_m3);
      setV('v-pallets',v.pallets); setV('v-comp',v.bau_comp); setV('v-larg',v.bau_larg);
      setV('v-alt',v.bau_alt); setV('v-combustivel',v.fuel_type||'diesel');
      setV('v-kml',v.km_per_liter); setV('v-preco-comb',v.fuel_price);
      setV('v-ipva',v.ipva_anual); setV('v-manut',v.manut_mes);
      setV('v-custo-dia',v.daily_cost); setV('v-status',v.status||'active');
      var h=document.getElementById('v-edit-id'); if(h) h.value=id;
      var t=document.getElementById('modal-veic-titulo'); if(t) t.textContent='Editar — '+(v.vda||v.plate);
      console.log('Campos preenchidos, v-edit-id:', document.getElementById('v-edit-id')?.value);
    },200);
  }catch(e){ toast('Erro: '+e.message,'error'); }
}

async function salvarVeiculoCompleto(editId){
  var h = document.getElementById('v-edit-id');
  editId = editId || (h?h.value:null) || window.veiculoEditId || null;
  console.log('Salvando veiculo, editId:', editId);
  var body={
    vda:document.getElementById('v-vda').value,
    plate:document.getElementById('v-plate').value,
    model:document.getElementById('v-model').value,
    type:document.getElementById('v-type').value,
    capacity_kg:parseFloat(document.getElementById('v-kg').value)||0,
    capacity_m3:parseFloat(document.getElementById('v-m3').value)||0,
    pallets:parseInt(document.getElementById('v-pallets').value)||0,
    bau_comp:parseFloat(document.getElementById('v-comp').value)||0,
    bau_larg:parseFloat(document.getElementById('v-larg').value)||0,
    bau_alt:parseFloat(document.getElementById('v-alt').value)||0,
    fuel_type:document.getElementById('v-combustivel').value,
    km_per_liter:parseFloat(document.getElementById('v-kml').value)||0,
    fuel_price:parseFloat(document.getElementById('v-preco-comb').value)||0,
    ipva_anual:parseFloat(document.getElementById('v-ipva').value)||0,
    manut_mes:parseFloat(document.getElementById('v-manut').value)||0,
    daily_cost:parseFloat(document.getElementById('v-custo-dia').value)||0,
    status:document.getElementById('v-status').value,
  };
  if(!body.plate||!body.model){toast('Placa e modelo obrigatórios!','error');return;}
  try{
    if(editId){
      await api('PATCH','/vehicles/'+editId,body);
      toast('Veículo atualizado!','success');
    } else {
      await api('POST','/vehicles',body);
      toast('Veículo cadastrado!','success');
    }
    window.veiculoEditId=null;
    if(h) h.value='';
    document.getElementById('modal-veiculo-completo').style.display='none';
    loadVehicles();
  }catch(e){toast('Erro: '+e.message,'error');}
}
"""
    content = content[:primeiro_close] + novo_codigo + content[primeiro_close:]
    print('Funções adicionadas no primeiro script!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
