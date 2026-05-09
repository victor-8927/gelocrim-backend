import re

path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra o </body> que está DENTRO do gerarRomaneio (falso)
# É o primeiro </body> que aparece DENTRO de uma string JS
body_positions = [m.start() for m in re.finditer(r'</body>', content)]
script_opens   = [m.start() for m in re.finditer(r'<script[^>]*>', content)]
script_closes  = [m.start() for m in re.finditer(r'</script>', content)]

print(f'</body> em: {body_positions}')
print(f'<script> em: {script_opens}')
print(f'</script> em: {script_closes}')

# O script principal abre em ~149673
# Tudo que está ENTRE o primeiro <script> e o primeiro </body>
# faz parte do JS — o </body> dentro é falso

# Estratégia: remover o </body></html> que está dentro do romaneio JS
# Busca por </body>\n\n\n  <!-- MODAL que é o padrão do arquivo corrompido
falso = content.find('</body>\n  <!-- MODAL')
if falso == -1:
    falso = content.find('</body>\n\n  <!-- MODAL')
if falso == -1:
    # Tenta encontrar dentro de string JS (entre aspas backtick)
    # O romaneio usa template literal que acaba com </body></html>
    # Depois vem os modais HTML
    for pos in body_positions[:-1]:  # ignora o último (real)
        ctx = content[max(0,pos-50):pos+20]
        print(f'\nFalso </body> em {pos}: {repr(ctx)}')
        # Remove esse </body>
        content = content[:pos] + content[pos+7:]
        print('Removido!')
        # Refaz a busca
        body_positions = [m.start() for m in re.finditer(r'</body>', content)]
        break

# Remove </html> falso também
html_positions = [m.start() for m in re.finditer(r'</html>', content)]
print(f'\n</html> em: {html_positions}')
for pos in html_positions[:-1]:
    ctx = content[max(0,pos-50):pos+20]
    print(f'Falso </html> em {pos}: {repr(ctx)}')
    content = content[:pos] + content[pos+7:]
    html_positions = [m.start() for m in re.finditer(r'</html>', content)]
    break

# Verifica scripts
opens  = len(re.findall(r'<script[^>]*>', content))
closes = len(re.findall(r'</script>', content))
print(f'\nScripts: {opens} opens, {closes} closes')

# Fecha scripts desbalanceados
if opens > closes:
    last_body = content.rfind('</body>')
    content = content[:last_body] + '\n</script>'*(opens-closes) + '\n</body>\n</html>'
    print(f'Adicionados {opens-closes} </script>')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nTotal: {len(content)} chars')
print('Pronto! Ctrl+Shift+R.')
