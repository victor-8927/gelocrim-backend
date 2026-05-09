path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui editarVeiculo completo com log de debug
old = """async function editarVeiculo(id){
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

new = """async function editarVeiculo(id){
  try{
    var data = await api('GET','/vehicles');
    var v = data.find(function(x){return x.id===id;});
    if(!v){ toast('Veículo não encontrado!','error'); return; }

    // Abre o modal PRIMEIRO para garantir que os elementos existem no DOM
    document.getElementById('modal-veiculo-completo').style.display='flex';

    // Aguarda o modal renderizar
    setTimeout(function(){
      var set = function(eid, val){
        var e = document.getElementById(eid);
        if(e){ e.value = (val!==null && val!==undefined) ? val : ''; }
      };
      set('v-vda',         v.vda);
      set('v-plate',       v.plate);
      set('v-model',       v.model);
      set('v-type',        v.type||'caminhao_truck');
      set('v-kg',          v.capacity_kg);
      set('v-m3',          v.capacity_m3);
      set('v-pallets',     v.pallets);
      set('v-comp',        v.bau_comp);
      set('v-larg',        v.bau_larg);
      set('v-alt',         v.bau_alt);
      set('v-combustivel', v.fuel_type||'diesel');
      set('v-kml',         v.km_per_liter);
      set('v-preco-comb',  v.fuel_price);
      set('v-ipva',        v.ipva_anual);
      set('v-manut',       v.manut_mes);
      set('v-custo-dia',   v.daily_cost);
      set('v-ult-oleo',    v.oleo_ult_data);
      set('v-prox-oleo',   v.oleo_prox_data);
      set('v-custo-oleo',  v.oleo_custo);
      set('v-status',      v.status||'active');

      var titulo = document.getElementById('modal-veic-titulo');
      if(titulo) titulo.textContent = 'Editar — ' + (v.vda||v.plate);

      _editVeiculoId = id;

      // Recalcula cubagem
      if(v.bau_comp && v.bau_larg && v.bau_alt) calcularCubagem();
    }, 100);

  }catch(e){ toast('Erro: '+e.message,'error'); }
}"""

if old in content:
    content = content.replace(old, new)
    print('editarVeiculo corrigido!')
else:
    print('Padrão não encontrado — substituindo por busca parcial')
    idx = content.find('async function editarVeiculo(id){')
    if idx != -1:
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
        content = content[:idx] + new + content[end:]
        print('Substituído por posição!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
