path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontra a linha 3400 com </script> (índice 3399)
print(f'Linha 3400: {repr(lines[3399][:80])}')
print(f'Linha 3399: {repr(lines[3398][:80])}')

# Remove o </script> da linha 3400
del lines[3399]
print('</script> da linha 3400 removido!')

# Agora encontra o último </script> (linha ~4459 após remoção)
last_script = None
for i in range(len(lines)-1, 0, -1):
    if '</script>' in lines[i]:
        last_script = i
        print(f'Último </script> na linha {i+1}: {repr(lines[i][:60])}')
        break

import re
content = ''.join(lines)
opens  = len(re.findall(r'<script[^>]*>', content))
closes = len(re.findall(r'</script>', content))
print(f'Scripts: {opens} opens / {closes} closes')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f'Total: {len(lines)} linhas')
print('Pronto! Ctrl+Shift+R.')
