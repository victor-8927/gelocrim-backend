path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Corrige aspas simples dentro de strings no detalharParceiro
old = """    div.innerHTML = '<div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:680px;max-height:85vh;overflow-y:auto">'+
      '<div style="padding:16px 24px;border-bottom:1px solid #1e3a5c;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;background:#0f2040;border-radius:16px 16px 0 0">'+
      '<span style="font-size:15px;font-weight:700;color:#e8f0fe" id="modal-parc-titulo">Parceiro</span>'+
      '<button onclick="document.getElementById('modal-parceiro-detalhe').style.display='none'" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer">✕</button>'+
      '</div><div id="modal-parc-body" style="padding:20px 24px"></div></div>';"""

new = """    div.innerHTML = '<div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:680px;max-height:85vh;overflow-y:auto">'+
      '<div style="padding:16px 24px;border-bottom:1px solid #1e3a5c;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;background:#0f2040;border-radius:16px 16px 0 0">'+
      '<span style="font-size:15px;font-weight:700;color:#e8f0fe" id="modal-parc-titulo">Parceiro</span>'+
      '<button onclick="document.getElementById(&quot;modal-parceiro-detalhe&quot;).style.display=&quot;none&quot;" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer">&#x2715;</button>'+
      '</div><div id="modal-parc-body" style="padding:20px 24px"></div></div>';"""

if old in content:
    content = content.replace(old, new)
    print('Aspas corrigidas!')
else:
    # Busca a linha problemática e corrige
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if "getElementById('modal-parceiro-detalhe').style.display='none'" in line:
            print(f'Linha {i+1}: {repr(line[:100])}')
            lines[i] = line.replace(
                "getElementById('modal-parceiro-detalhe').style.display='none'",
                'getElementById(&quot;modal-parceiro-detalhe&quot;).style.display=&quot;none&quot;'
            )
            print(f'Corrigida!')
    content = '\n'.join(lines)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Valida novamente
import subprocess
start = content.find('<script>\nvar _clientesCache')
end   = content.find('</script>', start)
script2 = content[start+8:end]
with open(r'C:\fleet-cloud\test_script2.js', 'w', encoding='utf-8') as f:
    f.write('var XLSX={};var google={maps:{Marker:function(){this.addListener=function(){};this.setIcon=function(){};},SymbolPath:{CIRCLE:0},event:{trigger:function(){}}}};function api(){}function toast(){}function initMap(){return null;}function addMarker(){}\n')
    f.write(script2)
result = subprocess.run(['node','--check',r'C:\fleet-cloud\test_script2.js'],capture_output=True,text=True)
if result.returncode==0:
    print('Script VALIDO!')
else:
    print('Ainda com erro:')
    print(result.stderr[:1000])
