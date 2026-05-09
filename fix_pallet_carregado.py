path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = """async function loadPalletsCarregados(){
  var grid=document.getElementById('pallets-carregados-grid');
  if(grid) grid.innerHTML='<div class="loading-state">Nenhum pallet carregado configurado</div>';
}"""

new = """async function loadPalletsCarregados(){
  var grid=document.getElementById('pallets-carregados-grid');
  if(!grid) return;

  try{
    var pallets = await api('GET','/producao/pallets');
    var itens   = await api('GET','/producao/itens');

    // Configurações fixas: tipo gelo -> qtd unidades por pallet
    var configs = [
      {kg:5,  un:180, cor:'#64B4FF',  emoji:'🧊'},
      {kg:10, un:110, cor:'#2dd4bf',  emoji:'🧊'},
      {kg:20, un:50,  cor:'#a78bfa',  emoji:'🧊'},
      {kg:40, un:27,  cor:'#f59e0b',  emoji:'🧊'},
    ];

    // Pallet base padrão (usa o primeiro cadastrado ou default)
    var palletBase = pallets.length > 0 ? pallets[0] : {
      nome:'Padrão', comprimento:1.20, largura:1.00, altura:0.15,
      cubagem:0.18, peso_max:1000
    };

    var cards = configs.map(function(cfg){
      // Encontra item correspondente ao kg
      var item = itens.find(function(it){ return parseFloat(it.peso)=== cfg.kg; });

      // Dimensões do pallet base
      var pComp = parseFloat(palletBase.comprimento)||1.20;
      var pLarg = parseFloat(palletBase.largura)||1.00;
      var pAlt  = parseFloat(palletBase.altura)||0.15;
      var pPeso = parseFloat(palletBase.peso_max)||25;

      // Dimensões do item
      var iComp = item ? parseFloat(item.comprimento)||0.30 : 0.30;
      var iLarg = item ? parseFloat(item.largura)||0.20    : 0.20;
      var iAlt  = item ? parseFloat(item.altura)||0.10     : 0.10;

      // Calcula empilhamento
      // Quantos itens cabem por camada (área do pallet / área do item)
      var itensPorCamada = Math.floor((pComp/iComp)) * Math.floor((pLarg/iLarg));
      // Quantas camadas cabem na altura útil (considera 1.50m altura total - pallet base)
      var alturaUtil = 1.50 - pAlt;
      var camadas = Math.floor(alturaUtil / iAlt);
      var totalUn = itensPorCamada * camadas;

      // Usa a qtd padrão da config se o cálculo der muito diferente
      var unFinal = totalUn > 0 ? Math.min(totalUn, cfg.un*2) : cfg.un;
      // Para simplificar, usa a configuração padrão
      unFinal = cfg.un;

      // Peso total
      var pesoItens  = cfg.un * cfg.kg;
      var pesoPallet = pPeso;
      var pesoTotal  = pesoItens + pesoPallet;

      // Cubagem total do pallet carregado
      // Pallet base + volume ocupado pelos itens empilhados
      var altTotal   = pAlt + (Math.ceil(cfg.un / Math.max(1, Math.floor((pComp/iComp)*Math.floor((pLarg/iLarg))))) * iAlt);
      var cubTotal   = pComp * pLarg * Math.min(altTotal, 1.80);

      // Pct capacidade (peso)
      var pctPeso = Math.min(100, Math.round(pesoItens/1000*100));

      return '<div class="card" style="padding:0;margin-bottom:0;border:1px solid '+cfg.cor+';border-radius:12px;overflow:hidden">'+
        '<div style="background:'+cfg.cor+'22;padding:14px;border-bottom:1px solid '+cfg.cor+'44;display:flex;align-items:center;gap:10px">'+
          '<span style="font-size:28px">'+cfg.emoji+'</span>'+
          '<div>'+
            '<div style="font-size:16px;font-weight:800;color:'+cfg.cor+'">Gelo '+cfg.kg+' kg</div>'+
            '<div style="font-size:11px;color:#90afd4">'+palletBase.nome+' + '+cfg.un+' unidades</div>'+
          '</div>'+
        '</div>'+
        '<div style="padding:14px;display:grid;gap:8px">'+
          '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px">'+
            '<div style="background:#0a1628;border-radius:8px;padding:10px;text-align:center">'+
              '<div style="font-size:20px;font-weight:800;color:'+cfg.cor+'">'+cfg.un+'</div>'+
              '<div style="font-size:10px;color:#90afd4">un/pallet</div>'+
            '</div>'+
            '<div style="background:#0a1628;border-radius:8px;padding:10px;text-align:center">'+
              '<div style="font-size:20px;font-weight:800;color:#f87171">'+pesoTotal.toFixed(0)+'</div>'+
              '<div style="font-size:10px;color:#90afd4">kg total</div>'+
            '</div>'+
            '<div style="background:#0a1628;border-radius:8px;padding:10px;text-align:center">'+
              '<div style="font-size:20px;font-weight:800;color:#2dd4bf">'+cubTotal.toFixed(3)+'</div>'+
              '<div style="font-size:10px;color:#90afd4">m³ total</div>'+
            '</div>'+
          '</div>'+
          '<div>'+
            '<div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:3px">'+
              '<span style="color:#90afd4">Peso da carga</span>'+
              '<span style="color:'+cfg.cor+'">'+pesoItens+' kg</span>'+
            '</div>'+
            '<div style="background:#1e3a5c;border-radius:4px;height:6px">'+
              '<div style="height:100%;background:'+cfg.cor+';border-radius:4px;width:'+pctPeso+'%"></div>'+
            '</div>'+
          '</div>'+
          '<div style="font-size:10px;color:#90afd4;display:grid;grid-template-columns:1fr 1fr;gap:4px">'+
            '<span>📦 Pallet: '+pComp+'x'+pLarg+'x'+pAlt+' m</span>'+
            '<span>🧊 Item: '+iComp+'x'+iLarg+'x'+iAlt+' m</span>'+
            '<span>⚖️ Peso pallet: '+pesoPallet+' kg</span>'+
            '<span>📐 Alt total: '+Math.min(altTotal,1.80).toFixed(2)+' m</span>'+
          '</div>'+
        '</div>'+
      '</div>';
    });

    grid.innerHTML = cards.join('');

  }catch(e){
    grid.innerHTML='<div class="loading-state" style="grid-column:1/-1">Erro: '+e.message+'<br><small>Cadastre pallets e itens primeiro</small></div>';
  }
}"""

if old in content:
    content = content.replace(old, new)
    print('loadPalletsCarregados implementado!')
else:
    print('Padrão não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
