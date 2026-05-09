import re

PATH = r'C:\fleet-cloud\gelocrim_v1.html'

with open(PATH, encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Substituir TODAS as ocorrencias de fallback '1000' no order_type
# para preservar o TOP original
replacements = [
    ("return mapa[t]||t||'1000';", "return mapa[t]||t||'';"),
    ('return mapa[t]||t||"1000";', 'return mapa[t]||t||"";'),
    ("||'1000'", "||''"),
]

changes = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        changes += 1
        print(f"OK: '{old}' -> '{new}'")

# Tambem garantir que o mapeamento inclui todos os TOPs
OLD_MAPA = "var mapa={'1100':'1000','1126':'1009','1117':'1007','1118':'1008','1127':'1010'};"
NEW_MAPA = "var mapa={'1000':'1000','1009':'1009','1007':'1007','1008':'1008','1010':'1010','1100':'1000','1126':'1009','1117':'1007','1118':'1008','1127':'1010'};"

if OLD_MAPA in content:
    content = content.replace(OLD_MAPA, NEW_MAPA)
    changes += 1
    print("OK: mapa de TOPs completo!")

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes} correcoes aplicadas!")
print("Ctrl+Shift+R no navegador e reimporte!")
