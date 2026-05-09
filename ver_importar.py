data = open(r'C:\fleet-cloud\gelocrim_v1.html', encoding='utf-8', errors='ignore').read()
idx = data.find("var mapa={")
# Pegar o mapa completo
idx2 = data.rfind("var mapa={", 0, data.find("external_id:'SNK-'"))
print(data[idx2:idx2+1000])
