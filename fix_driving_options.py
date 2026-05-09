HTML_PATH = r'C:\fleet-cloud\gelocrim_v1.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Linha 3367 (index 3366)
target_idx = 3366
print(f"Linha atual: {lines[target_idx].rstrip()}")

OLD = "        optimizeWaypoints: false // mant"
if OLD in lines[target_idx]:
    lines[target_idx] = """        optimizeWaypoints: false, // mantém a ordem do analista
        drivingOptions: {
          departureTime: (function(){ var h=new Date(); return h.getHours()>=8?h:new Date(h.getFullYear(),h.getMonth(),h.getDate(),8,0,0); })(),
          trafficModel: 'bestGuess'
        }
"""
    print("✅ drivingOptions com tráfego real adicionado!")
else:
    print("⚠️ Linha diferente do esperado:")
    print(lines[target_idx])

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Salvo! Recarregue com Ctrl+Shift+R")
