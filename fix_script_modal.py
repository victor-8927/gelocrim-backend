path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# O script abre em 149673 e vai até 197227 (onde começa outro script)
# O problema é que tem HTML do modal DENTRO do script
# Solução: inserir </script> antes do HTML do modal, e reabrir depois

# Encontra onde o JS termina e o HTML do modal começa
# Procura pelo primeiro </div> que fecha o modal dentro do script
import re

script_content = content[149673:197227]

# Encontra o último } de função JS antes do HTML
# O HTML começa com \n\n  <!-- MODAL
modal_start = script_content.find('\n\n\n  <!-- MODAL')
if modal_start == -1:
    modal_start = script_content.find('\n  <!-- MODAL')
if modal_start == -1:
    modal_start = script_content.find('<div id="modal-')

print(f'HTML dentro do script começa em offset: {modal_start}')
print(f'Contexto: {repr(script_content[max(0,modal_start-50):modal_start+100])}')

if modal_start > 0:
    # Posição absoluta
    abs_pos = 149673 + modal_start
    print(f'\nPosição absoluta: {abs_pos}')
    
    # Insere </script> antes do HTML e <script> depois do HTML do modal
    # O modal HTML termina em 197227 (início do próximo script)
    
    new_content = (
        content[:abs_pos] +
        '\n</script>\n' +
        content[abs_pos:197227] +
        content[197227:]
    )
    
    # Verifica
    opens  = len(re.findall(r'<script[^>]*>', new_content))
    closes = len(re.findall(r'</script>', new_content))
    print(f'Após correção: {opens} opens, {closes} closes')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Salvo! Ctrl+Shift+R.')
else:
    print('Modal não encontrado no script!')
    print('Primeiros 500 chars do script:')
    print(script_content[:500])
