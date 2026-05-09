caminho = r"C:\fleet-cloud\gelocrim_v1.html"
with open(caminho, encoding="utf-8", errors="ignore") as f:
    data = f.read()

# Estrategia: usar o peso_kg do pedido e dividir pelo peso medio ponderado por pallet
# Mais simples: calcular pallets baseado no peso bruto dos itens selecionados
# Peso por pallet: 5kg->180un=1080kg, 10kg->110un=1210kg, 20kg->50un=1150kg, 40kg->27un=1215kg
# Media aproximada: ~1160 kg por pallet

antigo1 = """  // Pallets calculados pelos itens reais (un_pallet do cadastro)
  var UN_PALLET = {'GELO 05KG':180,'GELO 10KG':110,'GELO 20KG':50,'GELO 40KG':27};
  var palletsEst = 0;
  itens.forEach(function(x){
    var mix = (x.order||{}).mix_top || {};
    Object.values(mix).forEach(function(top){
      (top.itens||[]).forEach(function(it){
        var up = UN_PALLET[it.nome] || 180;
        palletsEst += Math.ceil((it.qtd||0) / up);
      });
    });
  });
  if(palletsEst === 0) palletsEst = Math.ceil(pesoTotal / 700) || 0;"""

novo1 = """  // Pallets: peso bruto / 1150 kg por pallet (media ponderada do cadastro)
  var PESO_POR_PALLET = 1150;
  var palletsEst = Math.ceil(pesoTotal / PESO_POR_PALLET) || 0;"""

antigo2 = """  // Pallets calculados pelos itens reais (un_pallet do cadastro)
  var UN_PALLET = {'GELO 05KG':180,'GELO 10KG':110,'GELO 20KG':50,'GELO 40KG':27};
  var palletsUsados = 0;
  itens.forEach(function(x){
    var mix = (x.order||{}).mix_top || {};
    Object.values(mix).forEach(function(top){
      (top.itens||[]).forEach(function(it){
        var up = UN_PALLET[it.nome] || 180;
        palletsUsados += Math.ceil((it.qtd||0) / up);
      });
    });
  });
  if(palletsUsados === 0) palletsUsados = Math.ceil(pesoTotal / 700);"""

novo2 = """  // Pallets: peso bruto / 1150 kg por pallet (media ponderada do cadastro)
  var PESO_POR_PALLET = 1150;
  var palletsUsados = Math.ceil(pesoTotal / PESO_POR_PALLET);"""

if antigo1 in data:
    data = data.replace(antigo1, novo1)
    print("OK1")
else:
    print("ERRO1")

if antigo2 in data:
    data = data.replace(antigo2, novo2)
    print("OK2")
else:
    print("ERRO2")

with open(caminho, "w", encoding="utf-8") as f:
    f.write(data)
print("Salvo!")
