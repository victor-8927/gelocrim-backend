path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontra linha com </script> atual (deve estar por volta de 3396)
script_close = None
modal_csv = None

for i, line in enumerate(lines):
    if '</script>' in line and script_close is None and i > 3000:
        script_close = i
        print(f'</script> na linha {i+1}: {repr(line[:60])}')
    if '<!-- MODAL IMPORTA' in line and modal_csv is None:
        modal_csv = i
        print(f'Modal CSV na linha {i+1}: {repr(line[:60])}')

print(f'\nscript_close={script_close}, modal_csv={modal_csv}')

if script_close and modal_csv:
    if script_close > modal_csv:
        # </script> está depois do modal — problema!
        print('PROBLEMA: </script> está depois dos modais!')
    elif script_close < modal_csv - 2:
        print('</script> está antes dos modais — OK')
    else:
        print('</script> está na posição correta')
        
    # Solução: garante que </script> está na linha IMEDIATAMENTE antes dos modais
    # Remove o </script> atual
    del lines[script_close]
    print(f'Removido </script> da linha {script_close+1}')
    
    # Recalcula posição do modal após remoção
    new_modal = modal_csv - 1  # ajusta por causa da remoção
    
    # Insere </script> uma linha antes do modal
    lines.insert(new_modal, '</script>\n')
    print(f'Inserido </script> antes da linha {new_modal+1}')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

import re
content = ''.join(lines)
opens  = len(re.findall(r'<script[^>]*>', content))
closes = len(re.findall(r'</script>', content))
print(f'\nScripts: {opens} opens / {closes} closes')
print(f'Total: {len(lines)} linhas')
print('Pronto! Ctrl+Shift+R.')
