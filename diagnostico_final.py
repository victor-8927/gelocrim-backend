import re

# Lê o arquivo atual
path = r'C:\fleet-cloud\gelocrim_v1.html'

# O problema está no arquivo gerado — o HTML do projeto tem problemas:
# 1. Tem um </body></html> no meio (dentro do gerarRomaneio)
# 2. Scripts duplicados

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica estrutura
opens  = len(re.findall(r'<script[^>]*>', content))
closes = len(re.findall(r'</script>', content))
bodies = content.count('</body>')
htmls  = content.count('</html>')

print(f'Scripts: {opens} opens, {closes} closes')
print(f'</body>: {bodies}')
print(f'</html>: {htmls}')
print(f'Tamanho: {len(content)} chars')

# Encontra posição do </body> falso (dentro do romaneio)
body_positions = [m.start() for m in re.finditer(r'</body>', content)]
html_positions = [m.start() for m in re.finditer(r'</html>', content)]
print(f'\n</body> posições: {body_positions}')
print(f'</html> posições: {html_positions}')

# Mostra contexto de cada </body>
for pos in body_positions:
    print(f'\n  Pos {pos}: {repr(content[max(0,pos-80):pos+15])}')
