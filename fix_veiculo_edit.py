data = open(r'C:\fleet-cloud\gelocrim_v1.html', encoding='utf-8', errors='ignore').read()

# Ver funcao de importar CSV
idx = data.find('importarCSV\|importPlanilha\|parseCsvSankhya\|bulk_planilha')
import re
for termo in ['parseCsvSankhya', 'importarCSV', 'bulk_planilha', 'NUNOTA', 'SNK-']:
    idx = data.find(termo)
    if idx >= 0:
        print(f"\n=== '{termo}' pos {idx} ===")
        print(data[max(0,idx-100):idx+400])
        break
