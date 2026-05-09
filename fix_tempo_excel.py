path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Corrige a conversão do tempo Excel para minutos
old = """      // Converte tempo HH:MM:SS para minutos
      parceiros.forEach(function(p){
        if(p.tempo_entrega && p.tempo_entrega.indexOf(':')>=0){
          var parts = p.tempo_entrega.split(':');
          var h = parseInt(parts[0])||0;
          var m = parseInt(parts[1])||0;
          p.tempo_entrega = String(h*60+m); // em minutos
        }"""

new = """      // Converte tempo Excel para minutos
      parceiros.forEach(function(p){
        if(p.tempo_entrega && p.tempo_entrega !== '') {
          var val = p.tempo_entrega;
          var minutos = 0;
          if(String(val).indexOf(':')>=0){
            // Formato HH:MM:SS
            var parts = String(val).split(':');
            minutos = (parseInt(parts[0])||0)*60 + (parseInt(parts[1])||0);
          } else {
            var num = parseFloat(val);
            if(!isNaN(num)){
              if(num < 1) {
                // Fração de dia do Excel: 0.0625 = 90min
                minutos = Math.round(num * 24 * 60);
              } else {
                // Já em minutos
                minutos = Math.round(num);
              }
            }
          }
          p.tempo_entrega = minutos > 0 ? String(minutos) : '';
        }"""

if old in content:
    content = content.replace(old, new)
    print('Conversão de tempo corrigida!')
else:
    print('Padrão não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Reimporte a planilha.')
