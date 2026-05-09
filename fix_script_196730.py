path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Insere </script> antes do segundo <script> na pos 196730
pos = 196730
print(f'Contexto antes: {repr(content[pos-50:pos+20])}')

content = content[:pos] + '\n</script>\n' + content[pos:]

import re
opens  = len(re.findall(r'<script[^>]*>', content))
closes = len(re.findall(r'</script>', content))
print(f'Após: {opens} opens / {closes} closes')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Ctrl+Shift+R.')
