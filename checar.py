import re
data = open(r'C:\fleet-cloud\gelocrim_v1.html', encoding='utf-8', errors='ignore').read()
idx = data.find('modal-motorista-completo')
trecho = data[idx:idx+8000]
campos = re.findall(r'id="(d-[^"]+)"', trecho)
print("Campos do modal motorista:", campos)
