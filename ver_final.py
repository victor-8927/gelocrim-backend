path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total: {len(lines)}')
print('\n=== LINHAS 3668-3683 ===')
for i in range(3667, min(3683, len(lines))):
    print(f'{i+1}: {repr(lines[i][:100])}')

import re
content = ''.join(lines)
opens  = len(re.findall(r'<script[^>]*>', content))
closes = len(re.findall(r'</script>', content))
print(f'\nScripts: {opens} opens / {closes} closes')
