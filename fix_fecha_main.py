path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# O script abre em 149673 e o próximo script abre em 196730
# Precisamos inserir </script> antes da posição 196730

pos_insert = 196730

# Verifica o que tem antes de 196730
print('Contexto antes de 196730:')
print(repr(content[196680:196740]))

# Insere </script>\n antes do segundo <script>
content = content[:pos_insert] + '</script>\n' + content[pos_insert:]

# Verifica
import re
opens  = len(re.findall(r'<script[^>]*>', content))
closes = len(re.findall(r'</script>', content))
print(f'\nApós: Opens={opens} Closes={closes}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Ctrl+Shift+R.')
