path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica se tem meta charset
if '<meta charset="UTF-8">' in content:
    print('Meta charset OK')
else:
    print('Meta charset ausente!')

# Verifica primeiros bytes do arquivo
with open(path, 'rb') as f:
    first = f.read(10)
print(f'Primeiros bytes: {first}')

# Conta tags abertas vs fechadas
import re
opens  = len(re.findall(r'<script[^/]', content))
closes = len(re.findall(r'</script>', content))
print(f'<script> abertos: {opens}, </script> fechados: {closes}')

divs_open  = len(re.findall(r'<div', content))
divs_close = len(re.findall(r'</div>', content))
print(f'<div> abertos: {divs_open}, </div> fechados: {divs_close}')

# Verifica se tem algum </script> dentro de string JS (falso fechamento)
# Isso pode fazer o browser interpretar o script como encerrado prematuramente
idx = 0
falsos = []
while True:
    idx = content.find('</script>', idx)
    if idx == -1: break
    ln = content[:idx].count('\n')+1
    falsos.append(ln)
    idx += 1
print(f'</script> encontrados nas linhas: {falsos}')
