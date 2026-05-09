path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

opens  = len(re.findall(r'<script[^>]*>', content))
closes = len(re.findall(r'</script>', content))
print(f'<script>: {opens}  </script>: {closes}  Diferença: {opens-closes}')

# Adiciona fechamentos faltando antes do </body>
last_body = content.rfind('</body>')
falta = opens - closes
print(f'Adicionando {falta} </script>...')

insercao = '\n</script>' * falta + '\n'
content = content[:last_body] + insercao + content[last_body:]

# Verifica
opens2  = len(re.findall(r'<script[^>]*>', content))
closes2 = len(re.findall(r'</script>', content))
print(f'Após: <script>: {opens2}  </script>: {closes2}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Salvo! Ctrl+Shift+R.')
