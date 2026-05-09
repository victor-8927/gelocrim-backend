path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

import re
content = ''.join(lines)
opens  = len(re.findall(r'<script[^>]*>', content))
closes = len(re.findall(r'</script>', content))
print(f'Opens: {opens} / Closes: {closes} / Falta: {opens-closes}')

# Adiciona </script> antes do ultimo </body>
last_body = len(lines) - 1
for i in range(len(lines)-1, 0, -1):
    if '</body>' in lines[i]:
        last_body = i
        break

print(f'</body> na linha {last_body+1}')
lines.insert(last_body, '</script>\n')

content2 = ''.join(lines)
opens2  = len(re.findall(r'<script[^>]*>', content2))
closes2 = len(re.findall(r'</script>', content2))
print(f'Após: Opens: {opens2} / Closes: {closes2}')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Pronto! Ctrl+Shift+R.')
