path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Corrige o detector de cabeçalho para procurar NUNOTA em mais linhas
old = """  console.log('processarLinhas chamado! rows:', rows.length, 'primeira linha:', rows[0]);
  var headerIdx=0;
  for(var r=0;r<Math.min(5,rows.length);r++){
    var norm=rows[r].map(function(h){return String(h||'').toUpperCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');});
    if(norm.some(function(h){return h.indexOf('NUNOTA')>=0||h.indexOf('NRO')>=0||h.indexOf('NOTA')>=0;})){headerIdx=r;break;}
  }"""

new = """  console.log('processarLinhas chamado! rows:', rows.length, 'primeira linha:', rows[0]);
  var headerIdx=0;
  for(var r=0;r<Math.min(10,rows.length);r++){
    var norm=rows[r].map(function(h){return String(h||'').toUpperCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');});
    if(norm.some(function(h){return h.indexOf('NUNOTA')>=0||h.indexOf('NRO')>=0||h.indexOf('NOTA')>=0||h.indexOf('PARCEIRO')>=0||h.indexOf('PESO')>=0;})){
      headerIdx=r;
      console.log('Cabecalho encontrado na linha', r+1, ':', rows[r]);
      break;
    }
  }
  console.log('headerIdx:', headerIdx, 'header:', rows[headerIdx]);"""

if old in content:
    content = content.replace(old, new)
    print('Detector de cabeçalho corrigido!')
else:
    print('Padrão não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R e reimporte.')
