path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = """      // Peso total
      var pesoItens  = cfg.un * cfg.kg;
      var pesoPallet = pPeso;
      var pesoTotal  = pesoItens + pesoPallet;"""

new = """      // Peso total — usa peso REAL do item cadastrado
      var pesoUnitario = item ? parseFloat(item.peso) : cfg.kg;
      var pesoItens    = cfg.un * pesoUnitario;
      var pesoPallet   = pPeso;
      var pesoTotal    = pesoItens + pesoPallet;"""

if old in content:
    content = content.replace(old, new)
    print('Peso real do item aplicado!')
else:
    print('Padrão não encontrado!')

# Corrige também o label que mostra "kg total"
old2 = """              '<div style="font-size:20px;font-weight:800;color:#f87171">'+pesoTotal.toFixed(0)+'</div>'+"""
new2 = """              '<div style="font-size:20px;font-weight:800;color:#f87171">'+(pesoItens+pesoPallet).toFixed(0)+'</div>'+"""
content = content.replace(old2, new2)

# Corrige info de peso unitário no rodapé do card
old3 = """            '<span>⚖️ Peso pallet: '+pesoPallet+' kg</span>'+"""
new3 = """            '<span>⚖️ Peso unit.: '+pesoUnitario+' kg</span>'+"""
content = content.replace(old3, new3)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
