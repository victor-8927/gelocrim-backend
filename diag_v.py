with open(r'C:\fleet-cloud\gelocrim_v1.html', encoding='utf-8') as f:
    c = f.read()
import re
for m in re.finditer('modal-veiculo-completo', c):
    ln = c[:m.start()].count('\n')+1
    print(ln, repr(c[max(0,m.start()-20):m.start()+50]))
