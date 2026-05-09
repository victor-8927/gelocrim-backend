path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona função de conversão HH:MM:SS -> minutos
# e aplica no mapeamento da planilha de parceiros

old = "      window._clientesParaImportar=parceiros;\n      toast(parceiros.length+' parceiros prontos!','success');"

new = """      // Converte tempo HH:MM:SS para minutos
      parceiros.forEach(function(p){
        if(p.tempo_entrega && p.tempo_entrega.indexOf(':')>=0){
          var parts = p.tempo_entrega.split(':');
          var h = parseInt(parts[0])||0;
          var m = parseInt(parts[1])||0;
          p.tempo_entrega = String(h*60+m); // em minutos
        }
        // Extrai só a cidade antes de /UF
        if(p.cidade && p.cidade.indexOf('/')>=0){
          p.cidade = p.cidade.split('/')[0].trim();
        }
        if(p.cidade && p.cidade.indexOf('-')>=0 && p.cidade.length < 6){
          p.cidade = 'Manaus';
        }
        if(!p.cidade || p.cidade.trim()==='') p.cidade = 'Manaus';
      });
      window._clientesParaImportar=parceiros;
      toast(parceiros.length+' parceiros prontos! ('+parceiros.filter(function(p){return p.tempo_entrega&&p.tempo_entrega!=='0';}).length+' com tempo médio)','success');"""

if old in content:
    content = content.replace(old, new)
    print('Conversão de tempo adicionada!')
else:
    print('Padrão não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto!')
