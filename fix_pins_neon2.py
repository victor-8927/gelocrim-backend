PATH = r'C:\fleet-cloud\gelocrim_v1.html'

with open(PATH, encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Adicionar funcao getCorSegmento antes do forEach
OLD = "    var openIW = null; // InfoWindow atualmente aberto\n    var fixedIW = null; // InfoWindow fixo (duplo"

NEW = """    var openIW = null; // InfoWindow atualmente aberto
    var fixedIW = null; // InfoWindow fixo (duplo"""

# Adicionar funcao de cor por segmento antes do loop
FUNC_SEG = """
    // Cores neon por segmento
    function getCorSegmento(o) {
      var seg = (o.segmento||o.segment||'').toUpperCase();
      if (seg.indexOf('POSTO') >= 0 || seg.indexOf('COMBUST') >= 0) return '#FF6B35';
      if (seg.indexOf('ILHA') >= 0 || seg.indexOf('GELAD') >= 0)    return '#00FFEA';
      if (seg.indexOf('FABRIC') >= 0 || seg.indexOf('INDUST') >= 0) return '#BF5FFF';
      if (seg.indexOf('REFEIT') >= 0 || seg.indexOf('RESTAUR') >= 0) return '#FFD700';
      if (seg.indexOf('DISTRIB') >= 0 || seg.indexOf('ATACAD') >= 0) return '#00FF88';
      if (seg.indexOf('SUPERM') >= 0 || seg.indexOf('MERCED') >= 0) return '#FF3355';
      if (seg.indexOf('BAR') >= 0 || seg.indexOf('BOATE') >= 0)     return '#FF8C00';
      if (seg.indexOf('CONV') >= 0)                                   return '#FF6B35';
      return getCorRota(o.rota||o.regiao);
    }
"""

# Substituir cor no marker
OLD_COR = "      var sel = !!window.rotSelecionados[o.id];\n      var cor = sel ? '#10b981' : getCorRota(o.rota||o.regiao);"
NEW_COR = "      var sel = !!window.rotSelecionados[o.id];\n      var cor = sel ? '#00FF88' : getCorSegmento(o);"

# Melhorar o icone do marker
OLD_ICON = """          fillColor: cor,
          fillOpacity: 1,
          strokeColor: '#ffffff',
          strokeWeight: 1,
          scale: sel ? 2.2 : 1.7,
          anchor: new google.maps.Point(12, 22),
          rotation: 0"""

NEW_ICON = """          fillColor: cor,
          fillOpacity: 1,
          strokeColor: sel ? '#ffffff' : '#001020',
          strokeWeight: sel ? 2.5 : 1.5,
          scale: sel ? 2.5 : 1.8,
          anchor: new google.maps.Point(12, 22)"""

changes = 0

if OLD in content:
    content = content.replace(OLD, FUNC_SEG + NEW, 1)
    changes += 1
    print("OK: funcao getCorSegmento adicionada!")

if OLD_COR in content:
    content = content.replace(OLD_COR, NEW_COR, 1)
    changes += 1
    print("OK: cor por segmento aplicada!")

if OLD_ICON in content:
    content = content.replace(OLD_ICON, NEW_ICON, 1)
    changes += 1
    print("OK: icone melhorado!")

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"{changes} correcoes! Ctrl+Shift+R!")
