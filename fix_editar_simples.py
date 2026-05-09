path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui editarVeiculo por versão simples e direta sem setTimeout
old_start = 'async function editarVeiculo(id){'
idx = content.find(old_start)
if idx == -1:
    print('NAO ENCONTROU editarVeiculo!')
else:
    # Encontra o fim da função
    depth = 0
    i = idx
    while i < len(content):
        if content[i] == '{': depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
        i += 1
    
    print(f'editarVeiculo: linhas {content[:idx].count(chr(10))+1} até {content[:end].count(chr(10))+1}')
    
    new_func = """async function editarVeiculo(id){
  _editVeiculoId = id;
  try{
    var data = await api('GET','/vehicles');
    var v = data.find(function(x){return x.id===id;});
    if(!v){ toast('Veículo não encontrado!','error'); return; }

    console.log('Editando veículo:', v);

    document.getElementById('modal-veiculo-completo').style.display='flex';

    function setVal(eid, val){
      var e = document.getElementById(eid);
      if(e && val!==null && val!==undefined && val!=='') e.value = val;
    }

    setVal('v-vda',         v.vda);
    setVal('v-plate',       v.plate);
    setVal('v-model',       v.model);
    setVal('v-type',        v.type);
    setVal('v-kg',          v.capacity_kg);
    setVal('v-m3',          v.capacity_m3);
    setVal('v-pallets',     v.pallets);
    setVal('v-comp',        v.bau_comp);
    setVal('v-larg',        v.bau_larg);
    setVal('v-alt',         v.bau_alt);
    setVal('v-combustivel', v.fuel_type);
    setVal('v-kml',         v.km_per_liter);
    setVal('v-preco-comb',  v.fuel_price);
    setVal('v-ipva',        v.ipva_anual);
    setVal('v-manut',       v.manut_mes);
    setVal('v-custo-dia',   v.daily_cost);
    setVal('v-ult-oleo',    v.oleo_ult_data);
    setVal('v-prox-oleo',   v.oleo_prox_data);
    setVal('v-custo-oleo',  v.oleo_custo);
    setVal('v-status',      v.status);

    var titulo = document.getElementById('modal-veic-titulo');
    if(titulo) titulo.textContent = 'Editar — ' + (v.vda||v.plate);

    if(v.bau_comp && v.bau_larg && v.bau_alt) calcularCubagem();

  }catch(e){ toast('Erro: '+e.message,'error'); }
}"""
    
    content = content[:idx] + new_func + content[end:]
    print('editarVeiculo substituído!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
