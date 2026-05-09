path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total: {len(lines)}')

# Encontra linha do modal CSV (deve estar por volta de 3399-3401)
modal_line = None
for i, line in enumerate(lines):
    if '<!-- MODAL IMPORTA' in line:
        modal_line = i
        print(f'Modal CSV na linha {i+1}: {repr(line[:60])}')
        break

# Verifica se há </script> imediatamente antes
if modal_line:
    for j in range(modal_line-1, max(0,modal_line-5), -1):
        print(f'Linha {j+1}: {repr(lines[j][:60])}')

# A linha antes do modal deve ser </script>
# Se não for, insere
if modal_line and '</script>' not in lines[modal_line-1]:
    print(f'\nInserindo </script> antes da linha {modal_line+1}')
    lines.insert(modal_line, '</script>\n')
    modal_line += 1  # ajusta
    print('Inserido!')
else:
    print('\n</script> já está antes do modal')

# Agora verifica o segundo script (funções de clientes + funções novas)
# Deve abrir depois dos modais
import re
content = ''.join(lines)
opens  = len(re.findall(r'<script[^>]*>', content))
closes = len(re.findall(r'</script>', content))
print(f'\nScripts: {opens} opens / {closes} closes')

# Mostra estrutura completa dos scripts
for m in re.finditer(r'<script[^>]*>|</script>', content):
    line_num = content[:m.start()].count('\n') + 1
    print(f'  {m.group()} na linha {line_num}')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('\nSalvo!')
