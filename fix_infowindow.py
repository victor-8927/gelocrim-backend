path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = """      mk.addListener('click',function(){
        if(window.rotSelecionados[o.id]){
          delete window.rotSelecionados[o.id];
          mk.setIcon({path:google.maps.SymbolPath.CIRCLE,scale:9,fillColor:getCorRota(o.regiao),fillOpacity:1,strokeColor:'#fff',strokeWeight:2});
          iw.close();
        }else{
          window.rotSelecionados[o.id]={order:o,marker:mk};
          mk.setIcon({path:google.maps.SymbolPath.CIRCLE,scale:12,fillColor:'#10b981',fillOpacity:1,strokeColor:'#fff',strokeWeight:2});
          iw.open(m,mk);
        }
        atualizarSelecaoRot();
      });"""

new = """      mk.addListener('click',function(){
        if(window.rotSelecionados[o.id]){
          delete window.rotSelecionados[o.id];
          mk.setIcon({path:google.maps.SymbolPath.CIRCLE,scale:9,fillColor:getCorRota(o.regiao),fillOpacity:1,strokeColor:'#fff',strokeWeight:2});
        }else{
          window.rotSelecionados[o.id]={order:o,marker:mk};
          mk.setIcon({path:google.maps.SymbolPath.CIRCLE,scale:12,fillColor:'#10b981',fillOpacity:1,strokeColor:'#fff',strokeWeight:2});
        }
        // Sempre mostra InfoWindow ao clicar
        iw.open(m,mk);
        atualizarSelecaoRot();
      });"""

if old in content:
    content = content.replace(old, new)
    print('InfoWindow corrigido!')
else:
    print('Padrão não encontrado!')
    # Busca o addListener no renderRotMapMarkers
    idx = content.find("mk.addListener('click',function(){")
    while idx != -1:
        ln = content[:idx].count('\n')+1
        print(f'  addListener linha {ln}')
        idx = content.find("mk.addListener('click',function(){", idx+1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
