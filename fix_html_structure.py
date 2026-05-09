path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Mostra contexto dos 3 </body>
body_matches = list(re.finditer(r'</body>', content))
print(f'Total </body>: {len(body_matches)}')
for m in body_matches:
    print(f'  Pos {m.start()}: {content[max(0,m.start()-80):m.start()+20]}')

print('\n---')

# A estratégia: pegar tudo antes do primeiro </body>
# + pegar todo o JS dos scripts extras que vieram depois
# + montar um </body></html> correto no final

primeiro_body = body_matches[0].start()

# Conteúdo principal (antes do primeiro </body>)
parte_html = content[:primeiro_body]

# Extrai todos os <script> que estão DEPOIS do primeiro </body>
scripts_extras = re.findall(r'<script[^>]*>(.*?)</script>', content[primeiro_body:], re.DOTALL)
print(f'Scripts extras após primeiro </body>: {len(scripts_extras)}')

# Extrai modais que estão depois do primeiro </body>
modais_extras = re.findall(r'(<!--.*?-->)?\s*(<div[^>]*id="modal-[^"]*".*?</div>\s*</div>\s*</div>)', 
                           content[primeiro_body:], re.DOTALL)
print(f'Modais extras: {len(modais_extras)}')

# Monta o arquivo correto
novo_conteudo = parte_html

# Adiciona modais antes do </body>
for _, modal in modais_extras:
    if modal.strip() and modal not in parte_html:
        novo_conteudo += '\n' + modal

# Adiciona scripts extras em um bloco
js_unificado = '\n'.join(scripts_extras)
if js_unificado.strip():
    novo_conteudo += '\n<script>\n' + js_unificado + '\n</script>'

# Fecha corretamente
novo_conteudo += '\n</body>\n</html>'

with open(path, 'w', encoding='utf-8') as f:
    f.write(novo_conteudo)

# Verifica resultado
body_count = novo_conteudo.count('</body>')
html_count = novo_conteudo.count('</html>')
print(f'\nResultado: {body_count} </body>, {html_count} </html>')
print(f'Tamanho: {len(novo_conteudo)} chars')
print('Pronto! Ctrl+Shift+R.')
