path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Linha 3395 (índice 3394) tem '    \n' — é onde o template literal deve fechar
# Precisa adicionar: `; const w = window.open('','_blank'); w.document.write(html); w.document.close(); }
# E remover o </script> da linha 3396

print('Linha 3394:', repr(lines[3394]))
print('Linha 3395:', repr(lines[3395]))  # </script> errado

# Substitui linha 3395 (índice 3394) — fecha o template literal e a função
lines[3394] = "    </div>\`;\n  const w = window.open('','_blank'); w.document.write(html); w.document.close();\n}\n"

# Remove o </script> da linha 3396 (índice 3395)
print('Linha 3396 antes:', repr(lines[3395]))
if '</script>' in lines[3395]:
    del lines[3395]
    print('</script> removido!')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

import re
content = ''.join(lines)
opens  = len(re.findall(r'<script[^>]*>', content))
closes = len(re.findall(r'</script>', content))
print(f'\nScripts: {opens} opens / {closes} closes')
print(f'Total: {len(lines)} linhas')
print('Pronto! Ctrl+Shift+R.')
