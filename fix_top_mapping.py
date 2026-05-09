HTML_PATH = r'C:\fleet-cloud\gelocrim_v1.html'

with open(HTML_PATH, encoding='utf-8', errors='ignore') as f:
    content = f.read()

changes = 0

# Corrigir o mapeamento do TOP no processarLinhas do CSV
# O problema: estava mapeando TUDO para 1000
OLD_TOP_MAP = """    order_type:(function(){
        var t=get('top')||'';
        // Normaliza TOPs do Sankhya para TOPs do app
        var mapa={'1100':'1000','1126':'1009','1117':'1007','1118':'1008','1127':'1010'};
        return mapa[t]||t||'1000';
      })(),"""

NEW_TOP_MAP = """    order_type:(function(){
        var t=String(get('top')||'').trim();
        // Mapa de codigos Sankhya para TOPs do app
        var mapa={
          '1000':'1000','1009':'1009','1007':'1007','1008':'1008','1010':'1010',
          '1100':'1000','1126':'1009','1117':'1007','1118':'1008','1127':'1010'
        };
        return mapa[t] || t || '1000';
      })(),"""

if OLD_TOP_MAP in content:
    content = content.replace(OLD_TOP_MAP, NEW_TOP_MAP)
    changes += 1
    print("OK: mapeamento TOP corrigido no CSV!")
else:
    import re
    # Tentar corrigir via regex
    pattern = r"order_type:\(function\(\)\{.*?return mapa\[t\]\|\|t\|\|'1000';.*?\}\)\(\),"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        NEW = """    order_type:(function(){
        var t=String(get('top')||'').trim();
        var mapa={'1000':'1000','1009':'1009','1007':'1007','1008':'1008','1010':'1010','1100':'1000','1126':'1009','1117':'1007','1118':'1008','1127':'1010'};
        return mapa[t] || t || '1000';
      })(),"""
        content = content[:match.start()] + NEW + content[match.end():]
        changes += 1
        print("OK: TOP corrigido via regex!")
    else:
        print("AVISO: bloco TOP nao encontrado")

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes} correcoes aplicadas!")
print("Recarregue com Ctrl+Shift+R e reimporte!")
