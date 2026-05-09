path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Corrige o find para buscar pelo nome em vez do peso exato
old = "      var item = itens.find(function(it){ return parseFloat(it.peso)=== cfg.kg; });"
new = """      // Busca item pelo nome (ex: 'Gelo 5kg', 'Gelo 5 kg')
      var item = itens.find(function(it){
        var nome = (it.nome||'').toLowerCase().replace(/\s/g,'');
        return nome.indexOf(cfg.kg+'kg')>=0 || nome.indexOf(cfg.kg+' kg')>=0;
      });
      // Fallback: busca pelo índice da config
      if(!item && itens[configs.indexOf(cfg)]) item = itens[configs.indexOf(cfg)];"""

if old in content:
    content = content.replace(old, new)
    print('Match por nome corrigido!')
else:
    print('Padrão não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
