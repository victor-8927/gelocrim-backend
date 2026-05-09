path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra todos os kpiCard com goTo
import re
matches = re.findall(r"kpiCard\([^)]+goTo[^)]+\)", content)
print('kpiCards com goTo:')
for m in matches:
    print(' ', m[:100])
