path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
import re
opens  = len(re.findall(r'<script[^>]*>', content))
closes = len(re.findall(r'</script>', content))
print(f'Opens:{opens} Closes:{closes} Falta:{opens-closes}')
# Adiciona fechamentos faltando
last_body = content.rfind('</body>')
content = content[:last_body] + '\n</script>'*(opens-closes) + '\n</body>\n</html>'
with open(path,'w',encoding='utf-8') as f:
    f.write(content)
print('Pronto!')
